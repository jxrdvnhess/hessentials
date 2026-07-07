"""
Hessentials — July cover: "What grew."

Two conditions from the finalized essay, drawn in the house engine
(about_two_horizons: one camera, one ground plane, wandering living line
on cream, a faint layer for light). Evidence only. No figure. No moral.
Generous negative space — the wall/ground sit low, the plant rises into
the empty cream, magazine-page composition.

  corner    — the plant pushed into a hard corner and forgotten, holding
              through the heat. Leans toward the low light; one long dusk
              shadow. "What thrived on neglect."
  volunteer — the thing you never planted, come up on its own in open,
              cracked ground. Off-centre, alone in a wide dry field.
              "What you didn't plant."

Made line, not scribble (the banned ditch): the plant is a handful of
confident tapered strokes, a stem and a few leaf marks — not a texture.
Render outputs land in samples/ (gitignored) for judgment; the winner is
copied to /public only after Jordan picks.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from about_two_horizons import (Cam, Scene, render, CREAM, OUT, circle3,
                                resample, split_runs, inside, add_noise)
from linen import stroke_alpha

W, H = 1400, 2100


# ------------------------------------------------------------------ plant
def leaf(a, L, wdt, droop=0.0):
    """A made leaf mark in local screen coords (negative y = up): a smooth
    lens outline from base to tip and back, widest at the middle. `a` is the
    leaf's direction (radians), `droop` bends the tip downward under heat.
    Returns the closed outline; the midrib is drawn separately."""
    ca, sa = np.cos(a), np.sin(a)
    n = 8

    def rib(t):                                  # midrib point, with droop
        mx, my = L * t * ca, L * t * sa
        my += droop * (t ** 2) * L               # sag toward the ground (+y)
        return mx, my

    def side(t, s):
        mx, my = rib(t)
        wprof = (np.sin(np.pi * t) ** 0.65) * wdt * s
        return (mx - sa * wprof, my + ca * wprof)

    left = [side(t, +1) for t in np.linspace(0, 1, n)]
    right = [side(t, -1) for t in np.linspace(1, 0, n)]
    return left + right, [rib(0), rib(0.5), rib(1.0)]


def plant(S, x, z, h=0.52, lean=0.0, seed_leaves=(), w_stem=2.5, w_leaf=1.8,
          midrib=True):
    """A plant anchored at its base on the ground (y=0). `lean` tips the whole
    thing (radians, + = toward camera-right / the light). `seed_leaves` =
    list of (node_height_frac, angle, length, width, droop). `midrib=False`
    keeps small leaves as clean single outlines (no internal vein cross)."""
    sx, sy, s, zc = S.anchor((x, 0.0, z))
    cl, sl = np.cos(lean), np.sin(lean)

    def rot(px, py):                       # apply lean about the base
        return (px * cl - py * sl, px * sl + py * cl)

    # stem: a slight S, base to top, leaning
    raw = [(0, 0), (0.012, -h * 0.34), (-0.010, -h * 0.66),
           (0.018, -h * 0.90), (0.006, -h)]
    stem = [rot(px, py) for px, py in raw]
    S.glyph(stem, sx, sy, s, w=w_stem)

    # leaves hung at nodes up the stem
    for frac, ang, L, wdt, droop in seed_leaves:
        ny = -h * frac
        nx = 0.014 * np.sin(frac * 3.0)
        nx, ny = rot(nx, ny)
        outline, rib = leaf(ang, L, wdt, droop)
        S.glyph([(nx + px, ny + py) for px, py in outline], sx, sy, s, w=w_leaf)
        if midrib:
            S.glyph([(nx + px, ny + py) for px, py in rib], sx, sy, s,
                    w=w_leaf * 0.7)


def ground_shadow(S, x, z, dx, dz, spread=0.10, w=1.4):
    """A long faint cast shadow on the ground: a thin lozenge from the base
    stretching toward (x+dx, z+dz). Dusk evidence — the long light."""
    bx, bz = x, z
    tx, tz = x + dx, z + dz
    nx, nz = -(tz - bz), (tx - bx)
    n = np.hypot(nx, nz) + 1e-9
    nx, nz = nx / n * spread, nz / n * spread
    S.poly([(bx - nx * 0.4, 0.001, bz - nz * 0.4),
            (tx, 0.001, tz),
            (bx + nx * 0.4, 0.001, bz + nz * 0.4)], w=w, layer="faint")


# ------------------------------------------------------------------ corner
def build_corner():
    cam = Cam(W, H, eye_level=0.54, f=1350, cam_h=1.30, vpx=0.44)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    cxz, cz = 0.60, 2.86            # the corner point (x, z), pushed right
    hw = 0.66                       # a medium garden wall — reads as a corner
    lx = -1.8                       # back wall runs left to here
    sz = 1.70                       # side wall runs toward camera to here

    # back wall: base, top, left end
    S.poly([(lx, 0, cz), (cxz, 0, cz)], w=1.9)
    S.poly([(lx, hw, cz), (cxz, hw, cz)], w=2.1)
    S.poly([(lx, 0, cz), (lx, hw, cz)], w=1.5, layer="faint")
    # side wall: base, top
    S.poly([(cxz, 0, cz), (cxz, 0, sz)], w=1.7)
    S.poly([(cxz, hw, cz), (cxz, hw, sz)], w=1.9)
    # the corner itself — the hard join
    S.poly([(cxz, 0, cz), (cxz, hw, cz)], w=2.3)

    # the plant — the hero. Nestled INTO the crook (just left of the corner,
    # just in front of the back wall), leaning left out of the corner into the
    # open, overtopping the wall into cream. Leaves spread so none stack.
    px, pz = 0.24, 2.70
    # (no cast-shadow here — the wall grounds the plant; a lone faint diagonal
    #  read as a stray mark. The dusk stays implied by the leaning reach.)
    plant(S, px, pz, h=1.06, lean=-0.17, w_stem=2.7, seed_leaves=[
        (0.30, -np.pi * 0.16, 0.32, 0.080, 0.11),   # low broad, out of corner
        (0.46,  np.pi * 0.10, 0.24, 0.058, 0.07),   # short, back toward wall
        (0.62, -np.pi * 0.30, 0.30, 0.072, 0.05),   # long, reaching out
        (0.80,  np.pi * 0.22, 0.19, 0.046, 0.02),
        (0.93, -np.pi * 0.46, 0.14, 0.032, 0.0),    # young top
    ])

    return S


# ------------------------------------------------------------------ volunteer
def build_volunteer():
    cam = Cam(W, H, eye_level=0.50, f=1350, cam_h=1.24, vpx=0.55)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    # open ground: one faint far line, nothing built. The field is cream.
    S.poly([(-2.4, 0, 3.5), (2.4, 0, 3.5)], w=1.5, layer="faint")

    # a few cracks in the dry ground near the plant — restraint, not texture
    cracks = [
        [(-0.60, 0, 2.34), (-0.18, 0, 2.16), (0.12, 0, 2.24)],
        [(-0.18, 0, 2.16), (-0.06, 0, 1.84)],
        [(0.12, 0, 2.24), (0.52, 0, 2.12), (0.78, 0, 2.30)],
        [(-0.06, 0, 1.84), (0.26, 0, 1.70)],
    ]
    for c in cracks:
        S.poly(c, w=1.2, layer="faint")

    # the volunteer, off-centre — younger than the corner plant, but a real
    # made plant, not a sprig.
    px, pz = -0.10, 2.16
    ground_shadow(S, px, pz, dx=-0.88, dz=-0.55, spread=0.072)
    plant(S, px, pz, h=0.66, lean=-0.06, w_stem=2.3, seed_leaves=[
        (0.30,  np.pi * 0.16, 0.26, 0.064, 0.05),
        (0.46, -np.pi * 0.20, 0.28, 0.070, 0.04),
        (0.62,  np.pi * 0.30, 0.22, 0.052, 0.02),
        (0.80, -np.pi * 0.40, 0.16, 0.038, 0.0),
        (0.93,  np.pi * 0.50, 0.11, 0.026, 0.0),
    ])

    return S


# ------------------------------------------------------------------ the ground
# Fourth pass (Jordan's direction): the subject is the GROUND / the condition,
# not the plant. The plant is evidence — small, unheroic, "the world
# accidentally admitted it." The crack does the storytelling. Draw the
# condition the essay is about ("what the ground would keep"), not the metaphor.

def crack(S, pts_xz, y=0.0, w=1.5, layer="solid"):
    """A meandering line on the ground plane (y=0): a seam where two surfaces
    meet, or a fine fracture."""
    S.poly([(x, y, z) for x, z in pts_xz], w=w, layer=layer)


def build_seam():
    """A single small plant emerging from the crack where two surfaces meet.
    No wall, no bed. The seam crosses low; the plant merely exists on it."""
    cam = Cam(W, H, eye_level=0.47, f=1350, cam_h=1.22, vpx=0.52)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    # the seam — two surfaces meeting, crossing the lower frame, meandering
    seam = [(-2.0, 2.06), (-1.15, 2.0), (-0.55, 2.13), (-0.06, 1.99),
            (0.42, 2.09), (1.05, 1.98), (2.0, 2.07)]
    crack(S, seam, w=1.6)
    # hairline fractures spidering toward the viewer from one point on the
    # seam (faint) — the ground has a history, all incident kept to the left
    crack(S, [(-0.06, 1.99), (0.02, 1.74), (0.07, 1.55)], w=1.1, layer="faint")
    crack(S, [(-0.06, 1.99), (-0.20, 1.82), (-0.28, 1.66)], w=1.0, layer="faint")

    # the plant — small, off-centre, growing right out of the seam
    px, pz = -0.44, 2.115
    plant(S, px, pz, h=0.21, lean=0.05, w_stem=2.1, seed_leaves=[
        (0.40,  np.pi * 0.18, 0.105, 0.028, 0.03),
        (0.64, -np.pi * 0.24, 0.090, 0.023, 0.02),
        (0.90,  np.pi * 0.42, 0.052, 0.014, 0.0),
    ])
    return S


def build_ground():
    """Center the ground. The crack is the subject: a branching fracture that
    recedes to the left and runs forward to the bottom-right, with the plant
    at its junction. A high faint horizon, a large empty cream field, and the
    plant found last. The image asks 'why is this one here?'"""
    cam = Cam(W, H, eye_level=0.31, f=1350, cam_h=1.12, vpx=0.5)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    # a high, very faint horizon — a distant edge, most of the frame is cream
    S.poly([(-4.0, 0, 8.0), (4.0, 0, 8.0)], w=1.0, layer="faint")

    # THE CRACK — the subject. It WANDERS (undulating up and down, not a clean
    # arrow), passes near the plant without aiming at it, and carries on to the
    # bottom-right. The reader discovers the plant grew from it; it isn't
    # announced.
    main = [(-1.95, 2.10), (-1.42, 2.20), (-1.02, 2.04), (-0.66, 2.14),
            (-0.40, 2.03), (-0.20, 1.93), (0.02, 1.96), (0.24, 1.78),
            (0.44, 1.68), (0.66, 1.52), (0.74, 1.40), (1.02, 1.30),
            (1.24, 1.14), (1.58, 0.98)]
    crack(S, main, w=1.3)
    # a fork wandering off mid-right — the ground's own branching, not a guide
    crack(S, [(0.44, 1.68), (0.66, 1.74), (0.86, 1.60), (1.12, 1.66),
              (1.34, 1.72)], w=1.05)
    # two hairline sub-branches, off to the sides (faint)
    crack(S, [(-0.66, 2.14), (-0.82, 2.22), (-1.0, 2.20)], w=0.9, layer="faint")
    crack(S, [(0.24, 1.78), (0.30, 1.56), (0.26, 1.38)], w=0.9, layer="faint")

    # THE PLANT — observed, not symbolic. It sits just off the crack's wander
    # (not on a bullseye junction) and reads as SETTLED: broad lower leaves at
    # rest, alternate phyllotaxy, varied sizes, tips relaxing — a plant that
    # found the conditions it wanted, not one straining to survive. Inevitable,
    # not resilient. A subtle midrib now reads as a leaf vein (observation),
    # since the leaves are broad enough not to facet.
    px, pz = -0.33, 1.985
    plant(S, px, pz, h=0.168, lean=-0.06, w_stem=2.0, midrib=False, seed_leaves=[
        (0.34,  np.pi * 0.16, 0.092, 0.030, 0.05),   # lowest leaf, at ease
        (0.52, -np.pi * 0.20, 0.100, 0.032, 0.04),   # opposite, slightly larger
        (0.70,  np.pi * 0.28, 0.068, 0.022, 0.02),   # smaller, more upright
        (0.86, -np.pi * 0.36, 0.048, 0.016, 0.01),   # newer
        (0.96,  np.pi * 0.44, 0.030, 0.011, 0.0),    # youngest at the tip
    ])
    return S


# ------------------------------------------------------------------ atmosphere
# Jordan's direction (fourth-and-a-half pass): the evolution isn't a single
# living "element" but ATMOSPHERE — the conditions themselves made felt, so the
# world reads as inhabited. Graphite line, cream, and restraint all stay. What
# changes is the air: the cream takes on late-afternoon July warmth, warmer
# toward the ground where the light rakes, a soft pool of light where the plant
# exists. Felt, not seen — the reader notices the page feels alive, not "green."

def warm_field(cx, cy, strength):
    """A restrained late-July light field over the frame: warmer toward the
    ground (a raking low sun) and pooled softly around the plant. Returns the
    blend weight and the light-pool mask."""
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    vgrad = np.clip((yy / H - 0.26) / 0.74, 0, 1) ** 1.25       # ground is warmer
    r = np.hypot(xx - cx, yy - cy)
    pool = np.exp(-(r / (0.58 * W)) ** 2)                       # light gathers here
    w = np.clip(strength * (0.40 * vgrad + 0.66 * pool), 0, 1.0)
    return w, pool


def render_cover(S, fname, seed=29, glow_world=(-0.30, 0.0, 1.95), warm=0.85,
                 gold=(243, 228, 201)):
    """The graphite engine's stroke pipeline, but the cream base carries the
    warm July atmosphere and a faint luminous lift where the light pools."""
    rng = np.random.default_rng(seed)
    sil = S.table_silhouette()
    solid, faint = [], []
    for pts2, wdt, layer, occl in S.strokes:
        q = resample(pts2)
        if len(q) < 2:
            continue
        runs = split_runs(q, inside(q, sil)) if occl else [q]
        for run in runs:
            run = add_noise(run, rng, amp=1.5 if layer == "solid" else 2.0)
            (solid if layer == "solid" else faint).append(
                (list(map(tuple, run)), wdt))

    cx, cy = S.cam.project(S.T(glow_world))
    wf, pool = warm_field(cx, cy, strength=warm)
    img = np.ones((H, W, 3)) * CREAM
    img = img * (1 - wf[..., None]) + np.array(gold, float) * wf[..., None]
    img += pool[..., None] * np.array([6.0, 5.0, 3.0]) * warm   # light, not colour

    af = stroke_alpha(W, H, faint, width=2.0, jitterblur=0.7, supersample=3) * 0.23
    a = stroke_alpha(W, H, solid, width=2.0, jitterblur=0.55, supersample=3)
    a = np.clip(np.maximum(a, af), 0, 1)
    ink = np.array([52, 47, 42], float)                         # a hair warmer ink
    img = img * (1 - a[..., None]) + ink * a[..., None]

    g = rng.normal(0, 1, (H, W))
    g = np.asarray(Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-6) * 255)
                   .astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float)
    img += (g / 255.0 - 0.5)[..., None] * 5.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)) \
        .filter(ImageFilter.GaussianBlur(0.3)).save(os.path.join(OUT, fname),
                                                    quality=94)
    print("saved", fname)


# ------------------------------------------------------------------ the yard
# Sixth pass (Jordan's breakthrough): the earlier single plant on the slope
# read as a FIGURE hiking uphill with a load — agency, effort, intention. The
# essay is the opposite: no one made anything happen; the yard answered. So:
# no protagonist, no action, no before/after pair, nothing centered or heroic.
# A discovered Sonoran yard in late July. Quiet pieces of evidence scattered at
# different depths that only become meaningful after the essay. Reads first as
# "a quiet July yard," then "every object was evidence." Rewards a second look.

def bush(S, x, z, rx=0.20, ry=0.26, seed=0, w=1.3, fill=6, stems=2):
    """A LIVING desert shrub, drawn as a confident rounded silhouette: a lumpy
    low canopy contour (made line, organic) on a short stem or two, with a few
    interior leaf-ticks for life. Reads instantly as a full, thriving mound
    without tipping into scribble density."""
    rng = np.random.default_rng(seed)
    sx, sy, s, zc = S.anchor((x, 0.0, z))
    ccy = -ry * 0.60                                    # low centre = a mound
    lobes = int(rng.integers(5, 8))
    ph = rng.uniform(0, 2 * np.pi)
    m = 30
    outline = []
    for i in range(m + 1):
        a = 2 * np.pi * i / m
        rad = 1.0 + 0.10 * np.sin(a * lobes + ph) + rng.uniform(-0.035, 0.035)
        outline.append((np.cos(a) * rx * rad, ccy - np.sin(a) * ry * 0.60 * rad))
    S.glyph(outline, sx, sy, s, w=w)
    for _ in range(stems):                              # a short stem, mostly hidden
        a = rng.uniform(-0.10, 0.10)
        S.glyph([(0, 0), (a * rx * 0.3, ccy * 0.5)], sx, sy, s, w=w * 1.05)
    for _ in range(fill):                               # a few interior ticks
        t = rng.uniform(0, 2 * np.pi)
        rr = np.sqrt(rng.uniform(0, 0.60))
        px = np.cos(t) * rx * rr * 0.85
        py = ccy - np.sin(t) * ry * 0.42 * rr
        S.glyph([(px, py + ry * 0.07), (px + rng.uniform(-0.015, 0.015),
                 py - ry * 0.09)], sx, sy, s, w=w * 0.7)


def stake(S, x, z, height=0.24, lean=0.06, w=1.5):
    """A weathered nursery stake standing over nothing — intention, not action.
    A plain thin post with a small label-tag to ONE side (never a crossbar, so
    it can't read as a grave cross)."""
    sx, sy, s, zc = S.anchor((x, 0.0, z))
    tx = lean * height
    S.glyph([(0, 0), (tx * 0.5, -height * 0.5), (tx, -height)], sx, sy, s, w=w)
    S.glyph([(tx, -height * 0.9), (tx + 0.05, -height * 0.87),
             (tx + 0.05, -height * 0.77), (tx, -height * 0.80)],
            sx, sy, s, w=w * 0.7)


def basin(S, x, z, r=0.20, w=1.3):
    """A faint circular watering basin, almost nothing left inside — a shallow
    ring on the ground with one dead twig."""
    S.poly(circle3(x, 0.0, z, r, n=44), w=w, layer="faint")
    S.poly(circle3(x, 0.0, z, r * 0.58, n=36), w=w * 0.85, layer="faint")
    S.poly([(x - r * 0.2, 0.0, z + r * 0.1), (x + r * 0.15, 0.0, z - r * 0.2)],
           w=w * 0.9, layer="faint")


def build_yard():
    cam = Cam(W, H, eye_level=0.43, f=1300, cam_h=1.30, vpx=0.5)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    # a high faint horizon and one gentle ground swell — no climbable ridge
    S.poly([(-4.0, 0, 7.5), (4.0, 0, 7.5)], w=1.0, layer="faint")
    S.poly([(-2.6, 0, 2.30), (-0.6, 0, 2.40), (1.1, 0, 2.34), (2.6, 0, 2.44)],
           w=1.0, layer="faint")

    # subtle irrigation scars / dry cracks wandering across the ground (faint)
    crack(S, [(-2.2, 2.7), (-1.3, 2.55), (-0.4, 2.66), (0.6, 2.5), (1.7, 2.62)],
          w=1.0, layer="faint")
    crack(S, [(0.6, 2.5), (0.9, 2.2), (1.05, 1.95)], w=0.9, layer="faint")

    # the evidence, scattered — none centered, none heroic, varied depths.
    # The plants present read ALIVE (what grew); the failures show as absence.
    # a healthy volunteer that chose its own place (near-left, low mound)
    bush(S, -0.80, 2.52, rx=0.28, ry=0.22, seed=3, fill=8, stems=1)
    # an established plant thriving farther off (right, distant, full mound)
    bush(S, 1.18, 4.1, rx=0.24, ry=0.19, seed=7, fill=7, stems=1)
    # an empty nursery stake where something once stood (mid) — absence
    stake(S, 0.36, 3.05, height=0.23)
    # a nearly-empty watering basin (left-of-centre, far, faint) — absence
    basin(S, -0.42, 3.8, r=0.19)
    # quiet desert weeds, foreground, sparse (small living tufts)
    bush(S, 0.14, 1.98, rx=0.055, ry=0.10, seed=11, w=1.15, fill=2, stems=1)
    bush(S, -0.24, 2.12, rx=0.05, ry=0.085, seed=17, w=1.15, fill=2, stems=1)

    # scattered gravel — a few faint ticks, not a texture
    rng = np.random.default_rng(5)
    for _ in range(9):
        gx = rng.uniform(-1.4, 1.6)
        gz = rng.uniform(2.0, 3.2)
        d = 0.012
        S.poly([(gx - d, 0.0, gz), (gx + d, 0.0, gz + d * 0.5)],
               w=0.9, layer="faint")

    return S


if __name__ == "__main__":
    render(build_ground(), W, H, "july-ground.png", seed=29)          # graphite
    render_cover(build_ground(), "july-ground-warm.png", seed=29)     # atmosphere
    render_cover(build_yard(), "july-yard.png", seed=14,
                 glow_world=(0.1, 0.0, 2.6), warm=1.02)               # the yard
