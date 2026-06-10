"""
Hessentials — ABOUT panel. A wall where something important used to hang.

Concept locked. This pass is for emotional specificity and truth, not interest.

  - The light has an hour: low, warm, late afternoon, raking ACROSS the wall, so
    the real surface of the plaster catches it — the grazing light that makes a
    wall feel old and lived-with rather than rendered.
  - The fade is no longer a crisp rectangle but a soft, slightly irregular patch
    the sun spared; part of it slips into the warm shadow on the right, so the
    eye discovers it rather than reads it.
  - No floor line. It behaves like a wall, not a composition. The bottom falls
    into warm shadow.
  - One absence only: the patch and a single nail. The wall's other marks are
    not traces of meaning — just the small truths raking light finds in old
    plaster: a hairline, an uneven hand-troweled surface, a breath of soot.

Programmatic synthesis only. No letters, no branding.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "about", "about-room.jpg")

W, H = 1200, 1600
# warm plaster cream, late light
CREAM = np.array([243, 237, 226], float)


def _blur(a, r):
    return np.asarray(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), float)


def lowfreq(rng, cell):
    z = rng.normal(0, 1, (H // cell + 2, W // cell + 2))
    return np.asarray(Image.fromarray(((z - z.min()) / (np.ptp(z) + 1e-6) * 255).astype(np.uint8))
                      .resize((W, H), Image.BICUBIC), float) / 255.0


def graphite_field(value, rng, n, angle, strength):
    D = np.clip(0.9 - value / 255.0, 0, 1)
    flat = (D ** 1.3).ravel()
    s = flat.sum()
    if s <= 0:
        return np.zeros((H, W))
    idx = rng.choice(flat.size, size=n, p=flat / s)
    iy, ix = np.divmod(idx, W)
    dens = D[iy, ix]
    ang = angle + rng.normal(0, 0.18, n)
    L = 5 + dens * 14
    t = np.linspace(-0.5, 0.5, 8)
    xs = ix + rng.uniform(-1.2, 1.2, n)
    ys = iy + rng.uniform(-1.2, 1.2, n)
    px = np.clip((xs[:, None] + np.cos(ang)[:, None] * L[:, None] * t[None, :]).ravel().astype(int), 0, W - 1)
    py = np.clip((ys[:, None] + np.sin(ang)[:, None] * L[:, None] * t[None, :]).ravel().astype(int), 0, H - 1)
    canvas = np.zeros((H, W))
    np.add.at(canvas, (py, px), 1.0)
    return 1 - np.exp(-strength * canvas)


def hand(d, pts, rng, width=2, jitter=1.5, fill=(112, 104, 92), n=60, breaks=0.0):
    pts = np.array(pts, float)
    p = np.vstack([np.linspace(pts[i], pts[i + 1], n) for i in range(len(pts) - 1)])
    m = len(p)

    def sm(k):
        return np.convolve(rng.normal(0, 1, m), np.ones(k) / k, mode="same")

    p[:, 0] += sm(9) * jitter
    p[:, 1] += sm(9) * jitter
    skip = rng.uniform(0, 1, m) < breaks
    for i in range(m - 1):
        if skip[i]:
            continue
        d.line([tuple(p[i]), tuple(p[i + 1])], fill=fill, width=width)


def compose(seed=9):
    rng = np.random.default_rng(seed)
    img = np.ones((H, W, 3)) * CREAM
    yy, xx = np.mgrid[0:H, 0:W].astype(float)

    # --- late-afternoon raking light: low, warm, from the upper-left ---
    lit = (1 - xx / W) * 0.58 + (1 - yy / H) * 0.42
    lit = _blur(lit * 255, 80) / 255.0
    img += (lit[..., None] - 0.5) * 9.0                        # even, quiet light — low contrast
    img += lit[..., None] * np.array([6.0, 3.0, -2.0])         # a little warmth where the light sits
    img += (1 - lit[..., None]) * np.array([3.0, 1.0, -4.0])   # the shadow stays warm, never cold
    pool = np.exp(-(((xx - 250) / 560) ** 2 + ((yy - 430) / 620) ** 2))
    img += pool[..., None] * np.array([5.0, 3.0, -1.0])        # the faintest sense of a light source

    # --- real plaster: a hand-troweled surface, lit raking so its relief shows ---
    height = lowfreq(rng, 7) * 0.55 + lowfreq(rng, 22) * 0.45
    gy, gx = np.gradient(_blur(height * 255, 1.1) / 255.0)
    relief = (gx * -0.7 + gy * -0.7)                            # facing the light = brighter
    relief = relief / (np.abs(relief).max() + 1e-6)
    img += relief[..., None] * 8.0 * (0.5 + 0.5 * lit[..., None])    # a calm, true surface — the wall is the subject, not a texture show
    img += (lowfreq(rng, 60) - 0.5)[..., None] * np.array([7.0, 6.0, 4.0])  # broad uneven aging

    # --- the bottom falls into warm shadow — no floor line, just a wall ---
    drop = np.clip((yy - 1180) / 420, 0, 1) ** 1.4
    img += drop[..., None] * np.array([-14.0, -16.0, -19.0])

    # --- a light graphite tooth so the surface reads drawn, not photographed ---
    a = graphite_field(img.mean(2), rng, n=42000, angle=1.3, strength=0.3)
    img -= a[..., None] * np.array([15.0, 15.0, 17.0])
    img += (_blur(rng.normal(0, 1, (H, W)) * 255, 0.6) / 255.0 - 0.5)[..., None] * 6.0

    # --- the one piece of evidence: a crack that was filled and painted over.
    #     Real, observable, unresolved. The wall settled once; someone repaired it.
    #     Off to one side — the eye finds the line, follows it, and notices the
    #     patched stretch, and is left with a question rather than an answer. ---
    cr = [(1060, 286), (1022, 392), (1046, 486), (1006, 582), (1030, 668),
          (988, 760), (1008, 854), (966, 958), (994, 1068)]
    cr = np.vstack([np.linspace(cr[i], cr[i + 1], 44) for i in range(len(cr) - 1)])
    m = len(cr)

    def jag(k):
        return np.convolve(rng.normal(0, 1, m), np.ones(k) / k, mode="same")

    cr[:, 0] += jag(6) * 3.2 + jag(2) * 1.5    # meander + fine jaggedness
    cr[:, 1] += jag(6) * 1.4

    # the repaired stretch: a soft band, smoother and a hair lighter where it was
    # filled and painted, with a faint putty-knife smear dragged across it
    inband = (cr[:, 1] > 560) & (cr[:, 1] < 858)
    bandL = Image.new("L", (W, H), 0)
    ImageDraw.Draw(bandL).line([tuple(q) for q in cr[inband]], fill=255, width=36)
    band = _blur(np.asarray(bandL, float), 17) / 255.0
    img += band[..., None] * np.array([5.0, 4.5, 3.5])
    smear = Image.new("L", (W, H), 0)
    ImageDraw.Draw(smear).line([(946, 712), (1086, 695)], fill=255, width=20)
    img += (_blur(np.asarray(smear, float), 16) / 255.0)[..., None] * 3.5

    # the crack itself — thin, dark, a little broken, faded where it was filled
    crackL = Image.new("L", (W, H), 0)
    dc = ImageDraw.Draw(crackL)
    for i in range(m - 1):
        if rng.uniform() < 0.05:
            continue
        dc.line([tuple(cr[i]), tuple(cr[i + 1])], fill=255, width=(2 if rng.uniform() < 0.4 else 1))
    crack_a = np.clip(np.asarray(crackL, float) / 255.0 * (1 - 0.82 * band), 0, 1)
    img -= crack_a[..., None] * np.array([58.0, 60.0, 66.0])

    out = img
    # warm vignette so the room feels lit from one side, not evenly exposed
    r = np.sqrt(((xx - W * 0.34) / (W * 0.78)) ** 2 + ((yy - H * 0.42) / (H * 0.8)) ** 2)
    out -= (np.clip(r - 0.55, 0, 1) ** 1.7 * 18)[..., None] * np.array([1.0, 1.05, 1.15])

    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))


if __name__ == "__main__":
    compose().save(OUT, quality=92)
    print("saved", OUT)
