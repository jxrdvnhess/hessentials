"""
ABOUT — VERSION A, THE TRACE (2026-06-12).

The faculty's decision phase: build the strongest case for an About page
that generates Jordan WITHOUT showing him. The investigation's selected
carrier is the steady-present, stakes-free gesture — "this is how someone
lives here": a made bed with exactly ONE corner of the cover turned down,
where someone sat.

No figure. No symbolic objects. No clock, no jeopardy. The whole image is
order maintained everywhere and one local deviation shaped to a single body:
the turned-down corner + a shallow sat-dip in the near edge. Fit to one body.

Drawn in the brand's established register so it stands as a true sibling to
Version B (the painter), not a downgrade: confident MADE line on warm paper
(the line_figure engine), the first admitted color (clay) carried as a flat
limewash field on the coverlet, generous negative space on the left for the
essay column. Magazine-page composition, not a product shot.

Outputs:
  samples/about_bed_trace_paper.png      — for judging
  ../public/about/about-bed-trace.png    — opaque web asset (clay is part
                                           of the artwork, like scene D)
"""
import os
import numpy as np
from PIL import Image, ImageDraw
from line_figure import stroke, catmull, SS

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(HERE, "samples")
WEB = os.path.normpath(os.path.join(HERE, "..", "public", "about"))
os.makedirs(SAMPLES, exist_ok=True)

W, H = 2000, 1180
PAPER = np.array([241, 237, 229], float)   # plaster cream
INK = np.array([31, 29, 27], float)        # #1f1d1b
CLAY = np.array([216, 179, 160], float)    # the first admitted color
CLAY_ALPHA = 0.80                          # flat field, limewash-held
UNDER = np.array([233, 224, 212], float)   # the turned-back underside, paler


# ---- the bed, as a low volume seen from slightly above and to the right ----
# Top surface (coverlet plane), clockwise:
A = (640, 506)    # head, far
B = (1432, 560)   # foot, far
C = (1500, 742)   # foot, near   (the turndown lives at this corner)
D = (560, 688)    # head, near
# Front drop (coverlet falling toward the floor) from the near edge D->C:
Dd = (566, 980)
Cc = (1496, 1012)


def bed_strokes():
    S = []
    def a(ctrl, w, lead=0.14, tail=0.2, swell=0.2, sm=0.55, cs=False, ce=False,
          ph=0.0):
        S.append(dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                      smoothing=sm, cap_start=cs, cap_end=ce, phase=ph))

    # ---- HEADBOARD — low, wide, plain; a calm panel behind the pillows ----
    a([(556, 470), (560, 560), (560, 648)], 2.2, swell=0.1)             # left post
    a([(556, 470), (740, 442), (930, 458)], 2.4, swell=0.12)            # top rail
    a([(930, 458), (934, 532), (928, 580)], 2.0, swell=0.1, ce=True)    # right post (into surface)

    # ---- TOP SURFACE edges (selective — not a closed box) ----
    a([A, (1040, 524), B], 2.4, swell=0.14)                             # far edge, head->foot
    a([B, (1470, 650), C], 2.2, swell=0.12)                             # foot end
    # near edge, head->foot, carrying the SAT-DIP around x~1000-1180
    a([D, (760, 706), (940, 716), (1010, 742), (1110, 744), (1190, 726),
       (1320, 730), C], 2.6, swell=0.16)

    # ---- FRONT DROP — coverlet falls to near the floor, soft folds ----
    a([D, (560, 800), Dd], 2.2, swell=0.12)                             # head-side drop
    a([C, (1502, 880), Cc], 2.2, swell=0.12)                            # foot-side drop
    a([Dd, (760, 996), (1000, 1004), (1240, 1006), Cc], 2.0, swell=0.1) # hem, uneven
    # a few quiet vertical folds in the drop (economical)
    a([(820, 720), (812, 856), (818, 980)], 1.1, lead=0.24, tail=0.3, swell=0.08)
    a([(1080, 742), (1072, 870), (1078, 996)], 1.0, lead=0.26, tail=0.3, swell=0.08)
    a([(1330, 736), (1338, 868), (1330, 1000)], 1.0, lead=0.26, tail=0.3, swell=0.08)

    # ---- PILLOWS — two, calm, at the head; soft slabs, front occludes back.
    #      Wider than tall (pillow proportion), short off-centre creases so
    #      they read as linen, not rings. ----
    # back pillow (higher, peeking) — OPEN arc: top + sides only, so the
    # front pillow occludes its lower edge instead of a second ring showing
    a([(632, 582), (626, 548), (704, 506), (852, 506), (904, 542),
       (898, 578)], 1.8, swell=0.12)
    a([(742, 522), (760, 548)], 0.9, cs=True, ce=True, swell=0.06)       # short crease
    # front pillow (lower, in front — its top edge crosses the back one)
    a([(636, 600), (724, 560), (876, 566), (922, 606), (902, 652),
       (818, 668), (704, 664), (646, 640), (636, 600)], 1.9, swell=0.12)
    a([(792, 588), (808, 618)], 0.9, cs=True, ce=True, swell=0.06)       # short crease

    # ---- SAT-DIP — the one body's print: compression contours on the top
    #      surface just inside the near edge, mid-bed ----
    a([(960, 712), (1030, 728), (1110, 730), (1180, 716)], 1.2,
      lead=0.22, tail=0.26, swell=0.1)                                   # dip rim
    a([(1000, 700), (1060, 712), (1130, 706)], 0.8, lead=0.3, tail=0.32,
      swell=0.06)                                                        # inner compression
    a([(1024, 690), (1078, 698)], 0.7, lead=0.34, tail=0.34, swell=0.05) # faint second

    # ---- THE TURNED-DOWN CORNER — the foot-near corner folded back
    #      toward the head, a triangle of the paler underside revealed ----
    # the fold crease (hinge), running back into the bed
    a([(1318, 728), (1392, 690), (1452, 636)], 1.8, lead=0.18, swell=0.12)
    # the flipped triangle's outer edges (the turned-back flap)
    a([(1318, 728), (1366, 676), (1430, 648)], 1.6, swell=0.1)           # near fold edge
    a([(1430, 648), (1452, 636)], 1.2, cs=True, ce=True)                 # tip
    a([(1452, 636), (1470, 650)], 1.0, cs=True, ce=True)                 # tie to foot edge
    # a small soft fold inside the flap
    a([(1360, 690), (1396, 668), (1432, 652)], 0.8, lead=0.3, tail=0.3, swell=0.06)

    return S


def render_strokes(S):
    im = Image.new("L", (W * SS, H * SS), 0)
    d = ImageDraw.Draw(im)
    for s in S:
        stroke(d, **s)
    return np.asarray(im.resize((W, H), Image.LANCZOS), float) / 255.0


def _poly(draw, pts, fill):
    draw.polygon([(x * SS, y * SS) for (x, y) in pts], fill=fill)


def _smooth_poly(pts, n=60):
    """A closed soft polygon via catmull through the points (for the field)."""
    closed = list(pts) + [pts[0], pts[1]]
    P = catmull(closed, n=n)
    return [tuple(p) for p in P]


def clay_field():
    """Flat clay over the coverlet (top surface + front drop), minus the
    pillows and minus the turned-back underside. A whisper of per-column
    variation so it reads as limewash, not a vector fill."""
    im = Image.new("L", (W * SS, H * SS), 0)
    d = ImageDraw.Draw(im)
    # top surface
    _poly(d, [A, B, C, D], 255)
    # front drop
    _poly(d, [D, C, Cc, Dd], 255)
    field = np.asarray(im.resize((W, H), Image.LANCZOS), float) / 255.0

    # carve the pillows back out (they sit ON the coverlet but read as linen)
    im2 = Image.new("L", (W * SS, H * SS), 0)
    d2 = ImageDraw.Draw(im2)
    d2.polygon([(x * SS, y * SS) for (x, y) in _smooth_poly(
        [(620, 544), (704, 500), (856, 500), (910, 540), (892, 586),
         (700, 598), (624, 578)])], fill=255)
    d2.polygon([(x * SS, y * SS) for (x, y) in _smooth_poly(
        [(630, 598), (724, 554), (880, 560), (928, 604), (906, 656),
         (700, 668), (640, 642)])], fill=255)
    pill = np.asarray(im2.resize((W, H), Image.LANCZOS), float) / 255.0
    field = np.clip(field - pill, 0, 1)

    # the turned-back flap — paler underside, so it reads as the one event
    imf = Image.new("L", (W * SS, H * SS), 0)
    df = ImageDraw.Draw(imf)
    _poly(df, [(1318, 728), (1452, 636), (1470, 650)], 255)
    flap = np.asarray(imf.resize((W, H), Image.LANCZOS), float) / 255.0
    field = np.clip(field - flap, 0, 1)

    # limewash variation
    rng = np.random.default_rng(7)
    streak = rng.normal(0, 1, W)
    k = np.ones(41) / 41
    for _ in range(3):
        streak = np.convolve(streak, k, mode="same")
    streak /= np.abs(streak).max() + 1e-9
    field = field * (1 + 0.05 * streak[None, :])
    return np.clip(field, 0, 1), flap


def main():
    ink = render_strokes(bed_strokes())
    field, flap = clay_field()

    out = np.ones((H, W, 3)) * PAPER
    # clay coverlet
    out = out * (1 - (field * CLAY_ALPHA)[..., None]) + CLAY * (field * CLAY_ALPHA)[..., None]
    # the paler turned-back underside
    fa = flap * 0.9
    out = out * (1 - fa[..., None]) + UNDER * fa[..., None]
    # ink line on top
    out = out * (1 - ink[..., None]) + INK * ink[..., None]

    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    img.save(os.path.join(SAMPLES, "about_bed_trace_paper.png"))
    img.save(os.path.join(WEB, "about-bed-trace.png"))
    print("done")


if __name__ == "__main__":
    main()
