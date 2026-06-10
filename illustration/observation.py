"""
Hessentials — observation pages. One ordinary object, studied an afternoon.

Not twenty-five variations: the SAME object, looked at repeatedly — different
viewpoints (above, below, side, cropped), isolated parts (the handle, the rim,
the base, the profile), the hard views attempted again and again, studies left
half-finished or abandoned to a faint contour. Scattered organically, varied in
scale, no grid. Evidence of looking, not generation. Line only, no meaning.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "about")
CREAM = np.array([246, 241, 232], float)
INK = np.array([52, 47, 42], float)
SW, SH = 1700, 2150
RNG = np.random.default_rng(7)


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


def ell(cx, cy, rx, ry, a0=0.0, a1=2 * np.pi, n=40):
    t = np.linspace(a0, a1, n)
    return list(zip(cx + rx * np.cos(t), cy + ry * np.sin(t)))


class LP:
    def __init__(self):
        self.s = []
    def l(self, nodes, w=2.0, smooth=False, closed=False, n=14):
        if smooth:
            pts = _cmr(nodes, closed=closed)
        else:
            nn = [np.array(p, float) for p in nodes]
            if closed:
                nn = nn + [nn[0]]
            pts = np.vstack([np.linspace(nn[i], nn[i + 1], n) for i in range(len(nn) - 1)])
        self.s.append((np.array(pts, float), w))
    def p(self, pts, w=1.8):
        self.s.append((np.array(pts, float), w))


# ================================================================ MUG views
def mug_body(lp, R=44, H=74, elev=0.4, hand=1, thick=4, base=True, inner=True):
    ry = max(1.0, abs(elev) * R * 0.6)
    top = -H
    Rb = R * 0.94
    lp.l([(-R, top), (-Rb, 0)]); lp.l([(R, top), (Rb, 0)])
    lp.p(ell(0, top, R, ry))
    if elev > 0.18 and inner:
        lp.p(ell(0, top + thick * 0.7, R - thick, ry * 0.9))
    if base:
        if elev >= 0:
            lp.p(ell(0, 0, Rb, max(0.8, ry * 0.8), a0=0.06, a1=np.pi - 0.06))
        else:
            lp.p(ell(0, 0, Rb, ry, n=40))                    # seen from below: whole base
            lp.p(ell(0, 0, Rb * 0.7, ry * 0.7, n=30))        # foot ring
    hx = hand * R
    hw = 30
    lp.l([(hx, top + H * 0.20), (hx + hand * hw, top + H * 0.28), (hx + hand * hw * 1.04, top + H * 0.60), (hx, top + H * 0.72)], smooth=True)
    lp.l([(hx, top + H * 0.30), (hx + hand * hw * 0.6, top + H * 0.36), (hx + hand * hw * 0.62, top + H * 0.56), (hx, top + H * 0.62)], smooth=True)


def mug_side(lp): mug_body(lp, elev=0.12, inner=False)
def mug_3q(lp): mug_body(lp, elev=0.42)
def mug_above(lp): mug_body(lp, elev=0.85)
def mug_below(lp): mug_body(lp, elev=-0.45)
def mug_3q_l(lp): mug_body(lp, elev=0.42, hand=-1)
def mug_handle(lp):                                          # the handle, alone
    lp.l([(0, -54), (30, -44), (33, -8), (0, 2)], smooth=True)
    lp.l([(0, -44), (18, -38), (20, -14), (0, -6)], smooth=True)
def mug_rim(lp):                                             # the rim, alone
    lp.p(ell(0, 0, 44, 16)); lp.p(ell(0, 3, 40, 14))
def mug_base(lp): lp.p(ell(0, 0, 41, 12))
def mug_profile(lp):                                         # silhouette only
    lp.l([(-44, -74), (-41, 0), (41, 0), (44, -74)]); lp.p(ell(0, -74, 44, 9))

MUG = [(3, mug_side), (3, mug_3q), (2, mug_3q_l), (2, mug_above), (2, mug_below),
       (2, mug_handle), (2, mug_rim), (1, mug_base), (2, mug_profile)]


# ================================================================ BOWL views
def bowl_body(lp, R=52, depth=30, elev=0.4):
    ry = max(1.0, abs(elev) * R * 0.7)
    lp.p(ell(0, -depth, R, ry))                              # rim
    lp.p(ell(0, -depth + 4, R - 5, ry * 0.85))               # wall thickness
    lp.l([(-R, -depth), (-R * 0.4, 0), (R * 0.4, 0), (R, -depth)], smooth=True)  # bowl profile
    lp.p(ell(0, 0, R * 0.34, ry * 0.34, a0=0.1, a1=np.pi - 0.1))  # foot
def bowl_side(lp): bowl_body(lp, elev=0.1)
def bowl_3q(lp): bowl_body(lp, elev=0.45)
def bowl_above(lp): bowl_body(lp, elev=0.9)
def bowl_rim(lp): lp.p(ell(0, 0, 52, 20)); lp.p(ell(0, 4, 47, 18))
def bowl_profile(lp): lp.l([(-52, -30), (-22, 0), (22, 0), (52, -30)], smooth=True)
BOWL = [(3, bowl_side), (3, bowl_3q), (3, bowl_above), (2, bowl_rim), (3, bowl_profile)]


# ================================================================ POT views
def pot_body(lp, Rt=40, Rb=28, H=58, elev=0.4, lip=6):
    ry = max(1.0, abs(elev) * Rt * 0.6)
    lp.l([(-Rt, -H), (-Rb, 0)]); lp.l([(Rt, -H), (Rb, 0)])   # tapered sides
    lp.p(ell(0, -H, Rt, ry))                                 # rim
    lp.l([(-Rt - lip, -H), (-Rt - lip, -H + lip), (-Rt + 2, -H + lip)])  # lip
    lp.l([(Rt + lip, -H), (Rt + lip, -H + lip), (Rt - 2, -H + lip)])
    lp.p(ell(0, 0, Rb, max(0.8, ry * 0.7), a0=0.06, a1=np.pi - 0.06))
def pot_side(lp): pot_body(lp, elev=0.12)
def pot_3q(lp): pot_body(lp, elev=0.45)
def pot_above(lp): pot_body(lp, elev=0.85)
def pot_lip(lp): lp.p(ell(0, 0, 40, 14)); lp.p(ell(0, 4, 36, 12)); lp.l([(-46, 0), (-46, 8), (-36, 9)])
def pot_profile(lp): lp.l([(-40, -58), (-28, 0), (28, 0), (40, -58)])
POT = [(3, pot_side), (3, pot_3q), (2, pot_above), (2, pot_lip), (3, pot_profile)]


# ================================================================ WATERING CAN
def can_body(lp, elev=0.4):
    R, H = 36, 50
    ry = abs(elev) * R * 0.55
    lp.l([(-R, -H), (-R + 4, 0)]); lp.l([(R, -H), (R - 4, 0)])
    lp.p(ell(0, -H, R, max(1.0, ry)))
    lp.p(ell(0, 0, R - 4, max(0.8, ry * 0.8), a0=0.06, a1=np.pi - 0.06))
    lp.l([(R, -H + 10), (R + 34, -H - 2), (R + 60, -H + 18), (R + 70, -H + 30)], smooth=True)  # spout
    lp.l([(R, -H + 24), (R + 30, -H + 16), (R + 56, -H + 30)], smooth=True)
    lp.l([(R + 64, -H + 20), (R + 80, -H + 26), (R + 72, -H + 40)], smooth=True)              # rose
    lp.l([(-R + 6, -H), (-R - 6, -H - 26), (6, -H - 30), (8, -H - 6)], smooth=True)           # handle
def can_side(lp): can_body(lp, elev=0.1)
def can_3q(lp): can_body(lp, elev=0.4)
def can_spout(lp):
    lp.l([(0, 0), (34, -16), (60, 2), (70, 14)], smooth=True)
    lp.l([(0, 12), (30, 0), (56, 14)], smooth=True)
    lp.l([(64, 4), (80, 10), (72, 24)], smooth=True)
def can_handle(lp): lp.l([(0, 0), (-12, -34), (38, -38), (40, -4)], smooth=True)
CAN = [(3, can_side), (3, can_3q), (3, can_spout), (2, can_handle)]


# ================================================================ SHOE views
def shoe_side(lp):
    lp.l([(-58, 0), (-60, -16), (-30, -22), (10, -20), (40, -10), (58, -2), (58, 4), (-58, 4)], smooth=True, closed=True)
    lp.l([(-30, -22), (-20, -4)]); lp.l([(-10, -21), (-2, -4)]); lp.l([(2, -20), (8, -5)])    # laces
    lp.l([(-58, -2), (58, 0)])                               # sole line
    lp.l([(36, -10), (40, 2)])                               # heel break
def shoe_3q(lp):
    lp.l([(-58, 4), (-62, -14), (-34, -26), (6, -26), (40, -14), (60, 0), (58, 8)], smooth=True)
    lp.p(ell(-30, -18, 26, 12, a0=np.pi, a1=2 * np.pi))      # the opening
    lp.l([(-58, 6), (60, 4)])
def shoe_top(lp):
    lp.l([(-20, -54), (-30, 0), (-22, 50), (10, 56), (28, 30), (26, -20), (10, -52), (-20, -54)], smooth=True, closed=True)
    lp.p(ell(-6, -34, 18, 22))                               # the opening from above
def shoe_sole(lp):
    lp.l([(-58, 0), (-30, -10), (20, -10), (58, 2), (50, 14), (-50, 14), (-58, 0)], smooth=True, closed=True)
SHOE = [(3, shoe_side), (3, shoe_side), (2, shoe_3q), (2, shoe_top), (2, shoe_sole)]


# ----------------------------------------------------------------- the page
def place(lp, cx, cy, s, ang, frac, into, wob=0.9):
    ca, sa = np.cos(ang), np.sin(ang)
    strokes = lp.s[: max(1, int(len(lp.s) * frac))]
    for pts, w in strokes:
        q = pts * s
        x = q[:, 0] * ca - q[:, 1] * sa + cx
        y = q[:, 0] * sa + q[:, 1] * ca + cy
        m = len(x)
        def sm(k):
            k = max(1, min(k, m))
            return np.convolve(RNG.normal(0, 1, m), np.ones(k) / k, mode="same")
        x = x + sm(6) * wob + sm(2) * wob * 0.4
        y = y + sm(6) * wob + sm(2) * wob * 0.4
        into.append((list(zip(x, y)), w))


def page(repertoire, seed, out):
    rng = np.random.default_rng(seed)
    global RNG
    RNG = rng
    fns = [f for _, f in repertoire]
    wts = np.array([wt for wt, _ in repertoire], float); wts /= wts.sum()
    dark, faint = [], []
    placed = []
    n, tries = 0, 0
    while n < 25 and tries < 1600:
        tries += 1
        cx = rng.uniform(150, SW - 150)
        cy = rng.uniform(170, SH - 150)
        s = rng.choice([1.3, 1.5, 1.7, 1.9, 2.4, 3.1], p=[.30, .24, .16, .12, .12, .06])
        rr = s * 42
        if not all(((cx - px) ** 2 + (cy - py) ** 2) > (rr * 0.55) ** 2 for px, py in placed):
            if rng.random() > 0.16:          # mostly avoid heavy overlap, allow a little
                continue
        placed.append((cx, cy))
        fn = rng.choice(fns, p=wts)
        ang = rng.uniform(-0.07, 0.07)
        roll = rng.random()
        frac = 1.0 if roll > 0.32 else rng.uniform(0.35, 0.7)   # ~1/3 unfinished
        is_faint = rng.random() < 0.22                          # ~1/5 abandoned/faint
        lp = LP(); fn(lp)
        place(lp, cx, cy, s, ang, frac, faint if is_faint else dark)
        # repeated attempt: sometimes draw the same view again right beside it
        if rng.random() < 0.22:
            lp2 = LP(); fn(lp2)
            place(lp2, cx + s * rng.uniform(-26, 26), cy + s * rng.uniform(-10, 14),
                  s * rng.uniform(0.9, 1.05), ang + rng.uniform(-0.05, 0.05),
                  rng.uniform(0.5, 1.0), dark)
        n += 1
    img = np.ones((SH, SW, 3)) * CREAM
    af = stroke_alpha(SW, SH, faint, width=1.7, jitterblur=0.6, supersample=3) * 0.42
    img = img * (1 - af[..., None]) + INK * af[..., None]
    ad = stroke_alpha(SW, SH, dark, width=1.9, jitterblur=0.55, supersample=3)
    img = img * (1 - ad[..., None]) + INK * ad[..., None]
    img += (np.asarray(Image.fromarray((rng.normal(0, 1, (SH, SW)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 5.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35)).save(os.path.join(OUT, out), quality=92)
    print("saved", out)


if __name__ == "__main__":
    page(MUG, 3, "obs-mug.jpg")
    page(BOWL, 5, "obs-bowl.jpg")
    page(POT, 8, "obs-pot.jpg")
    page(CAN, 12, "obs-can.jpg")
    page(SHOE, 17, "obs-shoe.jpg")
