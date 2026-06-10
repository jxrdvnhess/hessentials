"""
Hessentials — chair specimens. Not variations of one chair: different chairs.

Twenty-odd distinct chairs a person might draw across a few afternoons trying to
understand the species — each with a reason to exist (the spindles of a Windsor,
the rockers, the X of a folding frame, the cantilever's missing back legs). Loose
and exploratory: different scales, a few half-finished, one tipped over, the
occasional overlap. Line only. Evidence of looking, not generation.

Local coords per chair: floor at y=0, the chair built upward in -y, centred on x.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "about")
CREAM = np.array([246, 241, 232], float)
INK = np.array([54, 49, 44], float)
SW, SH = 1700, 2100
POLYS = []
RNG = np.random.default_rng(11)


def _cmr(nodes, n=14, closed=False):
    P = [np.array(p, float) for p in nodes]
    P = ([P[-1]] + P + [P[0], P[1]]) if closed else ([P[0]] + P + [P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2 = t * t; t3 = t2 * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(P[-2])
    return np.array(out)


class LP:
    def __init__(self):
        self.strokes = []
    def l(self, nodes, w=2.0, smooth=False, closed=False, n=14):
        if smooth:
            pts = _cmr(nodes, closed=closed)
        else:
            nn = [np.array(p, float) for p in nodes]
            if closed:
                nn = nn + [nn[0]]
            pts = np.vstack([np.linspace(nn[i], nn[i + 1], n) for i in range(len(nn) - 1)])
        self.strokes.append((np.array(pts, float), w))


def place(lp, cx, cy, s=1.0, ang=0.0, wob=0.7):
    ca, sa = np.cos(ang), np.sin(ang)
    for pts, w in lp.strokes:
        q = pts * s
        x = q[:, 0] * ca - q[:, 1] * sa + cx
        y = q[:, 0] * sa + q[:, 1] * ca + cy
        m = len(x)
        def sm(k):
            k = max(1, min(k, m))
            return np.convolve(RNG.normal(0, 1, m), np.ones(k) / k, mode="same")
        x = x + sm(6) * wob + sm(2) * wob * 0.4
        y = y + sm(6) * wob + sm(2) * wob * 0.4
        POLYS.append((list(zip(x, y)), w))


# ------------------------------------------------------------------- specimens
def c_side(lp):                       # plain dining side chair
    lp.l([(-24, 0), (-24, -44), (24, -44), (24, 0)])           # legs + seat span (side)
    lp.l([(24, -44), (24, 0)]); lp.l([(-24, -44), (-26, -98)])  # back post
    lp.l([(-26, -98), (-12, -98)]); lp.l([(-25, -74), (-13, -74)])


def c_ladder(lp):
    lp.l([(-24, 0), (-24, -44), (24, -44), (24, 0)])
    lp.l([(-24, -44), (-26, -100)]); lp.l([(-12, -44), (-13, -100)])
    lp.l([(-26, -100), (-11, -100)])
    for yy in (-62, -78, -94):
        lp.l([(-25, yy), (-12, yy)])


def c_windsor(lp):
    lp.l([(-30, -44), (30, -42)], smooth=True)                 # saddle seat front
    lp.l([(-30, -44), (-30, -36), (30, -34), (30, -42)], smooth=True)
    for lx, ll in [(-26, (-46, 8)), (24, (44, 6)), (-10, (-30, 4))]:
        lp.l([(lx, -42), (lx + ll[0] * 0.3, 0)])               # splayed turned legs
    for i, sx in enumerate(np.linspace(-22, 6, 7)):
        lp.l([(sx, -44), (sx - 6 + i, -104)])                  # spindle fan
    lp.l([(-30, -104), (8, -106)], smooth=True)                # bow top


def c_wing(lp):                       # wingback, 3/4 front
    lp.l([(-34, -28), (-24, -33), (24, -32), (34, -27)], smooth=True)
    lp.l([(-34, -28), (-40, -56), (-28, -68), (-22, -58), (-25, -38)], smooth=True)
    lp.l([(34, -27), (40, -55), (28, -67), (22, -57), (25, -38)], smooth=True)
    lp.l([(-25, -62), (-18, -90), (0, -96), (18, -90), (25, -60)], smooth=True)
    lp.l([(-27, -26), (-33, 0)]); lp.l([(27, -25), (33, 0)])


def c_stool(lp):
    lp.l([(-22, -44), (22, -44)])
    for lx in (-20, 20, -8): lp.l([(lx, -44), (lx + lx * 0.18, 0)])
    lp.l([(-18, -30), (18, -30)])     # stretcher


def c_barstool(lp):
    lp.l([(-18, -74), (18, -74)])
    for lx in (-16, 16): lp.l([(lx, -74), (lx + lx * 0.1, 0)])
    lp.l([(-15, -22), (15, -22)]); lp.l([(-15, -40), (15, -40)])
    lp.l([(-18, -74), (-19, -92)]); lp.l([(18, -74), (19, -92)])  # low back


def c_folding(lp):
    lp.l([(-24, 0), (22, -50)]); lp.l([(22, 0), (-24, -50)])  # X frame
    lp.l([(-24, -50), (22, -50)])                              # seat
    lp.l([(22, -50), (26, -100)]); lp.l([(-2, -50), (2, -100)])
    lp.l([(2, -100), (26, -100)])


def c_director(lp):
    lp.l([(-24, 0), (-20, -50), (20, -50), (24, 0)])
    lp.l([(-24, 0), (20, -50)]); lp.l([(24, 0), (-20, -50)])
    lp.l([(-20, -50), (-22, -96), (22, -96), (20, -50)])       # sling back
    lp.l([(-22, -88), (22, -88)], smooth=True)


def c_bench(lp):
    lp.l([(-54, -42), (54, -42)])
    for lx in (-50, 50, -10, 14): lp.l([(lx, -42), (lx, 0)])
    lp.l([(-54, -42), (-56, -78)]); lp.l([(54, -42), (56, -78)]); lp.l([(-56, -78), (56, -78)])


def c_rocker(lp):
    lp.l([(-24, -40), (24, -40)])
    lp.l([(-24, -40), (-28, -98)]); lp.l([(-12, -40), (-13, -98)])
    lp.l([(-28, -98), (-11, -98)])
    for yy in (-58, -76): lp.l([(-26, yy), (-12, yy)])
    lp.l([(24, -40), (26, -6)]); lp.l([(-24, -40), (-22, -6)])
    lp.l([(-40, -2), (-22, -10), (28, -10), (44, -4)], smooth=True)  # rocker
    lp.l([(-38, 4), (44, 2)], smooth=True)


def c_adirondack(lp):
    lp.l([(-30, -34), (10, -46)])                              # slanted seat
    lp.l([(10, -46), (28, -110)])                              # slanted back
    lp.l([(-30, -34), (-32, 0)]); lp.l([(10, -46), (12, 0)])
    for sx in (16, 22, 28): lp.l([(sx - 4, -52), (sx + 8, -110)])
    lp.l([(-34, -50), (-30, -34)]); lp.l([(-34, -50), (-36, -20)])  # flat arm
    lp.l([(-36, -50), (-10, -52)])


def c_shell(lp):                      # molded shell on dowel legs (3/4)
    lp.l([(-26, -44), (-22, -56), (22, -56), (26, -44), (18, -40), (-18, -40)], smooth=True, closed=True)
    lp.l([(-26, -50), (-20, -92), (20, -92), (26, -50)], smooth=True)
    for lx in (-22, 22, -12, 14): lp.l([(lx, -42), (lx + lx * 0.5, 0)])


def c_cantilever(lp):                 # tubular, no back legs
    lp.l([(-26, 0), (-30, -20), (-10, -44), (26, -44)], smooth=True)  # base->seat
    lp.l([(26, 0), (24, -44)])
    lp.l([(-10, -44), (-16, -100), (8, -104)], smooth=True)   # cantilever back
    lp.l([(-13, -72), (4, -74)])


def c_tulip(lp):                      # pedestal (front)
    lp.l([(-28, -44), (-22, -56), (22, -56), (28, -44), (16, -40), (-16, -40)], smooth=True, closed=True)
    lp.l([(-26, -50), (-20, -94), (20, -94), (26, -50)], smooth=True)  # back
    lp.l([(-8, -40), (-12, -6)]); lp.l([(8, -40), (12, -6)])
    lp.l([(-22, -2), (22, -4)], smooth=True)                  # round foot


def c_tall(lp):
    lp.l([(-22, 0), (-22, -44), (22, -44), (22, 0)])
    lp.l([(22, -44), (22, 0)]); lp.l([(-22, -44), (-24, -130)]); lp.l([(-8, -44), (-9, -130)])
    lp.l([(-24, -130), (-7, -130)])
    for sx in np.linspace(-21, -10, 4): lp.l([(sx, -52), (sx, -128)])


def c_armcushion(lp):
    lp.l([(-30, -40), (30, -40)])                             # seat line
    lp.l([(-30, -36), (-26, -44), (26, -44), (30, -38)], smooth=True)  # cushion
    lp.l([(-30, -40), (-32, 0)]); lp.l([(30, -40), (32, 0)]); lp.l([(-8, -40), (-8, 0)])
    lp.l([(-30, -40), (-32, -64), (-22, -64), (-22, -42)], smooth=True)  # arm
    lp.l([(-22, -44), (-20, -100), (24, -98), (26, -42)], smooth=True)   # back


def c_partial(lp):                    # an abandoned study — back + one leg only
    lp.l([(-22, -44), (-24, -100)]); lp.l([(-24, -100), (-10, -100)])
    lp.l([(-10, -100), (-9, -50)])
    lp.l([(-22, -44), (16, -44)])     # seat trailing off
    lp.l([(-22, -44), (-23, -10)])


def c_behind(lp):                     # a chair from behind
    lp.l([(-24, -44), (-26, -100), (26, -100), (24, -44)])
    lp.l([(-25, -72), (25, -72)])
    lp.l([(-24, -44), (-30, 0)]); lp.l([(24, -44), (30, 0)])


SPECIMENS = [c_side, c_ladder, c_windsor, c_wing, c_stool, c_barstool, c_folding,
             c_director, c_bench, c_rocker, c_adirondack, c_shell, c_cantilever,
             c_tulip, c_tall, c_armcushion, c_behind]


if __name__ == "__main__":
    # a loose layout: a rough 5x5 grid, jittered position / scale / rotation, a few
    # repeats (second attempts), one tipped over, one abandoned, occasional overlap.
    plan = list(SPECIMENS)
    plan += [c_side, c_stool, c_windsor, c_rocker]    # second attempts
    plan += [c_partial, c_partial]                    # abandoned studies
    plan += ["TIP", "BIG"]                            # special handling
    RNG.shuffle(plan)
    cols, rows = 5, 5
    cw, ch = SW / cols, SH / rows
    for i, fn in enumerate(plan[: cols * rows]):
        col, row = i % cols, i // cols
        cx = col * cw + cw / 2 + RNG.uniform(-48, 48)
        cy = row * ch + ch * 0.66 + RNG.uniform(-40, 40)
        s = RNG.uniform(1.35, 1.7)
        ang = RNG.uniform(-0.08, 0.08)
        if fn == "TIP":
            fn = c_side; ang = 1.5; s = 1.5
        elif fn == "BIG":
            fn = c_windsor; s = 2.5                    # a larger, focused attempt
        lp = LP()
        fn(lp)
        place(lp, cx, cy, s=s, ang=ang, wob=0.8)
    img = np.ones((SH, SW, 3)) * CREAM
    a = stroke_alpha(SW, SH, POLYS, width=2.0, jitterblur=0.55, supersample=3)
    img = img * (1 - a[..., None]) + INK * a[..., None]
    img += (np.asarray(Image.fromarray((RNG.normal(0, 1, (SH, SW)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 5.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35)).save(os.path.join(OUT, "specimens-chairs.jpg"), quality=92)
    print("saved specimens-chairs.jpg —", len(POLYS), "strokes")
