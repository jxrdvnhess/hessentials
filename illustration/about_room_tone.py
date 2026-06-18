"""
Hessentials — About page, Study 10: the tone pass.

Line carried the composition as far as it can. This adds value, light, shadow,
edge, material, mood to the strongest room (Study 07/09, the interrupted
kitchen). Doctrine from ILLUSTRATION.md: mass the lights together and the
shadows together; limit the value set; control edges — hard where planes meet,
soft where form turns, lost where a thing melts into the ground.

Two light sources, massed: the window (back wall) and the evening patch it
throws across the floor. Everything else falls away warm. Upper room stays
near-empty cream — restraint is the frame for the intensity below.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from about_room_habit import build, W, H, CT, WZ, CZ
from about_two_horizons import resample, add_noise

CREAM = np.array([245, 240, 231], float)
INK = np.array([52, 47, 43], float)
WARMSH = np.array([171, 156, 136], float)     # warm taupe shadow
DEEPSH = np.array([132, 118, 101], float)     # deeper warm shadow
GLOW = np.array([253, 250, 244], float)       # window / lit warmth


def mask(proj, pts3, blur, ss=2):
    im = Image.new("L", (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    d.polygon([(proj(p)[0] * ss, proj(p)[1] * ss) for p in pts3], fill=255)
    im = im.filter(ImageFilter.GaussianBlur(blur * ss))
    return np.asarray(im.resize((W, H), Image.LANCZOS), float) / 255.0


def vgrad(top, bot):
    """vertical 0..1 ramp top->bot of frame."""
    return np.linspace(top, bot, H)[:, None] * np.ones((1, W))


def hgrad(left, right):
    return (np.linspace(left, right, W)[None, :] * np.ones((H, 1)))


def render_tone(fname, seed=41):
    S = build("a")
    P = S.cam.project
    img = np.ones((H, W, 3)) * CREAM

    def lay(m, color, strength):
        nonlocal img
        m = np.clip(m * strength, 0, 1)[..., None]
        img = img * (1 - m) + color * m

    # ---- big soft atmosphere: cooler-darker left, warm light pooling right
    g = hgrad(1.0, 0.0) * vgrad(0.55, 0.25)
    lay(g, WARMSH, 0.16)
    g = hgrad(0.0, 1.0) * vgrad(0.20, 0.55)
    lay(g, GLOW, 0.12)

    # ---- window glow (the source), heavily soft
    win = [(-0.95, 2.05, WZ), (0.05, 2.05, WZ), (0.05, 1.18, WZ), (-0.95, 1.18, WZ)]
    lay(mask(P, win, blur=16), GLOW, 0.55)
    lay(mask(P, [(-0.99, 2.10, WZ), (0.09, 2.10, WZ), (0.09, 1.14, WZ),
                 (-0.99, 1.14, WZ)], blur=34), GLOW, 0.28)   # bloom past the frame

    # ---- evening patch thrown across the floor (second light mass)
    patch = [(0.55, 0, 1.95), (1.78, 0, 2.25), (1.50, 0, 2.92), (0.44, 0, 2.50)]
    lay(mask(P, patch, blur=20), GLOW, 0.34)
    lay(mask(P, patch, blur=46), GLOW, 0.16)

    # ---- under-counter cabinetry: a long warm shadow band (massed dark),
    # darker low and feathered so it reads as recess, not a panel
    band = [(-1.9, CT, CZ), (2.6, CT, CZ), (2.6, 0, CZ), (-1.9, 0, CZ)]
    lay(mask(P, band, blur=22), WARMSH, 0.20)
    low = [(-1.9, 0.55, CZ), (2.6, 0.55, CZ), (2.6, 0, CZ), (-1.9, 0, CZ)]
    lay(mask(P, low, blur=18), WARMSH, 0.16)
    oven = [(0.40, 0.74, CZ), (1.14, 0.74, CZ), (1.14, 0.32, CZ), (0.40, 0.32, CZ)]
    lay(mask(P, oven, blur=15), DEEPSH, 0.16)

    # ---- back wall: faint shadow upper-left, away from the window's reach
    wall = [(-1.9, 2.6, WZ), (-0.6, 2.6, WZ), (-0.6, CT, WZ), (-1.9, CT, WZ)]
    lay(mask(P, wall, blur=40), WARMSH, 0.10)

    # ---- the island front: the foreground dark mass (anchor). Harder edge.
    isl = [(-2.2, CT, 0.62), (-0.05, CT, 0.62), (-0.05, -0.8, 0.62),
           (-2.2, -0.8, 0.62)]
    lay(mask(P, isl, blur=9), WARMSH, 0.42)
    lay(mask(P, [(-2.2, 0.50, 0.62), (-0.05, 0.50, 0.62), (-0.05, -0.8, 0.62),
                 (-2.2, -0.8, 0.62)], blur=6), DEEPSH, 0.30)   # deeper toward floor

    # ---- cast shadows on the floor (light from upper right → fall left/forward)
    # stool: soft pool to its left
    lay(mask(P, [(-0.35, 0, 1.55), (0.30, 0, 1.62), (0.20, 0, 2.05),
                 (-0.45, 0, 1.95)], blur=11), WARMSH, 0.22)
    # water bowl + mat: small soft shadow trailing left
    lay(mask(P, [(0.78, 0, 2.34), (1.0, 0, 2.30), (0.96, 0, 2.60),
                 (0.74, 0, 2.60)], blur=9), WARMSH, 0.18)

    # ---- core shadows: small crescents where round forms turn from the light
    # the pan, far rim
    lay(mask(P, [(0.78, CT + 0.05, 2.86), (0.90, CT + 0.05, 2.90),
                 (1.00, CT + 0.05, 2.84), (0.90, CT + 0.05, 2.80)], blur=4),
        DEEPSH, 0.20)

    # ================= LINE LAYER on top (the drawing, intact) =============
    rng = np.random.default_rng(seed)
    solid, faint = [], []
    for pts2, w, layer, occl in S.strokes:
        q = resample(pts2)
        if len(q) < 2:
            continue
        q = add_noise(q, rng, amp=1.5 if layer == "solid" else 2.0)
        (solid if layer == "solid" else faint).append((list(map(tuple, q)), w))

    from linen import stroke_alpha
    af = stroke_alpha(W, H, faint, width=2.0, jitterblur=0.7, supersample=3) * 0.20
    a = stroke_alpha(W, H, solid, width=2.0, jitterblur=0.55, supersample=3)
    a = np.clip(np.maximum(a, af), 0, 1)
    # ink softened slightly where it crosses deep shadow (lost edges)
    img = img * (1 - a[..., None]) + INK * a[..., None]

    # ---- material grain + a unifying soft focus
    grain = rng.normal(0, 1, (H, W))
    grain = np.asarray(Image.fromarray(((grain - grain.min()) / (np.ptp(grain) + 1e-6)
                                        * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.7)), float)
    img += (grain / 255.0 - 0.5)[..., None] * 7.0
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)) \
        .filter(ImageFilter.GaussianBlur(0.35))
    out.save(f"samples/{fname}", quality=94)
    print("saved", fname)


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    render_tone("about-room-tone.png")
