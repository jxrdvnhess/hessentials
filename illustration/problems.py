"""
Hessentials — observation 002: one page, one problem.

Not a page of objects. A page of attention. The same small difficulty worked
over and over — the handle, the rim, the bowl's section, the spout, the pot's
lip — from angle after angle, with first tries left faint underneath corrected
lines, attempts repeated, some abandoned. Obsessive, repetitive, almost boring,
because that is what learning one thing looks like. Line only, no meaning.
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


def _cmr(nodes, n=16, closed=False):
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


# ------------------------------------------------------------------ problems
def handle(lp, rot=0.0, attach=True):
    """A mug handle, foreshortening as it rotates toward the viewer (rot 0 = full
    loop, rot 1 = nearly edge-on). The problem is the attachment and the inner
    curve."""
    h = 36
    W = 30 * (1 - 0.80 * rot)
    lp.l([(0, -h), (W, -h * 0.78), (W * 1.06, h * 0.5), (0, h)], smooth=True)        # outer
    lp.l([(0, -h * 0.72), (W * 0.56, -h * 0.5), (W * 0.58, h * 0.30), (0, h * 0.70)], smooth=True)  # inner
    if attach:
        lp.l([(0, -h - 8), (0, h + 8)])                                             # wall edge
        lp.l([(-10, -h - 8), (0, -h - 8)]); lp.l([(-10, h + 8), (0, h + 8)])


def rim(lp, elev=0.4):
    R = 46
    ry = max(1.2, elev * R * 0.62)
    lp.p(ell(0, 0, R, ry))
    if elev > 0.15:
        lp.p(ell(0, ry * 0.16 + 2, R - 4, ry * 0.9))


def bowl_profile(lp, depth=40, flareW=52):
    lp.l([(-flareW, -depth), (-flareW * 0.5, -depth * 0.4), (-flareW * 0.16, 0),
          (flareW * 0.16, 0), (flareW * 0.5, -depth * 0.4), (flareW, -depth)], smooth=True)
    lp.p(ell(0, -depth, flareW, max(2.0, flareW * 0.16)))


def spout(lp, ang=0.4, length=84):
    rise = -34 * ang
    lp.l([(0, 0), (length * 0.4, rise * 0.5), (length * 0.82, rise), (length, rise + 6)], smooth=True)   # top
    lp.l([(0, 16), (length * 0.4, 16 + rise * 0.5), (length * 0.8, 18 + rise)], smooth=True)             # underside taper
    lp.l([(length * 0.9, rise - 8), (length + 14, rise + 2), (length + 4, rise + 22)], smooth=True)      # rose
    lp.l([(0, 0), (-6, 8), (0, 16)], smooth=True)                                                        # where it leaves the body


def pot_lip(lp, elev=0.5):
    R = 40
    ry = max(1.4, elev * R * 0.6)
    lp.p(ell(0, 0, R, ry))
    lp.p(ell(0, ry * 0.2 + 2, R - 4, ry * 0.9))
    lp.l([(-R - 6, 0), (-R - 6, 9), (-R + 2, 10)])
    lp.l([(R + 6, 0), (R + 6, 9), (R - 2, 10)])


# ----------------------------------------------------------------- the page
def place(lp, cx, cy, s, ang, frac, into):
    ca, sa = np.cos(ang), np.sin(ang)
    for pts, w in lp.s[: max(1, int(len(lp.s) * frac))]:
        q = pts * s
        x = q[:, 0] * ca - q[:, 1] * sa + cx
        y = q[:, 0] * sa + q[:, 1] * ca + cy
        m = len(x)
        def sm(k):
            k = max(1, min(k, m))
            return np.convolve(RNG.normal(0, 1, m), np.ones(k) / k, mode="same")
        x = x + sm(6) * 0.9 + sm(2) * 0.4
        y = y + sm(6) * 0.9 + sm(2) * 0.4
        into.append((list(zip(x, y)), w))


def page(problem, sampler, seed, out, count=27):
    global RNG
    RNG = np.random.default_rng(seed)
    rng = RNG
    dark, faint = [], []
    placed = []
    tries = 0
    while len(placed) < count and tries < 2400:
        tries += 1
        cx = rng.uniform(150, SW - 150)
        cy = rng.uniform(180, SH - 160)
        s = rng.choice([1.1, 1.3, 1.5, 1.8, 2.4], p=[.34, .28, .18, .12, .08])
        if not all(((cx - px) ** 2 + (cy - py) ** 2) > (s * 30) ** 2 for px, py in placed):
            if rng.random() > 0.2:
                continue
        placed.append((cx, cy))
        t = sampler(rng)
        ang = rng.uniform(-0.06, 0.06)
        # a faint first try, then the corrected line over it
        if rng.random() < 0.38:
            lp0 = LP(); problem(lp0, **t)
            place(lp0, cx + rng.uniform(-6, 6), cy + rng.uniform(-5, 5), s * rng.uniform(0.96, 1.05), ang + rng.uniform(-0.04, 0.04), 1.0, faint)
        frac = 1.0 if rng.random() > 0.30 else rng.uniform(0.4, 0.75)   # some abandoned mid-stroke
        lp = LP(); problem(lp, **t)
        place(lp, cx, cy, s, ang, frac, dark)
        # the same attempt again, right beside it (still cannot get it)
        if rng.random() < 0.30:
            lp2 = LP(); problem(lp2, **t)
            place(lp2, cx + s * rng.uniform(18, 34) * rng.choice([-1, 1]), cy + s * rng.uniform(-8, 8), s * rng.uniform(0.9, 1.05), ang + rng.uniform(-0.05, 0.05), rng.uniform(0.6, 1.0), dark)
            placed.append((cx, cy))
    img = np.ones((SH, SW, 3)) * CREAM
    af = stroke_alpha(SW, SH, faint, width=1.6, jitterblur=0.6, supersample=3) * 0.4
    img = img * (1 - af[..., None]) + INK * af[..., None]
    ad = stroke_alpha(SW, SH, dark, width=1.9, jitterblur=0.55, supersample=3)
    img = img * (1 - ad[..., None]) + INK * ad[..., None]
    img += (np.asarray(Image.fromarray((rng.normal(0, 1, (SH, SW)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 5.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35)).save(os.path.join(OUT, out), quality=92)
    print("saved", out)


if __name__ == "__main__":
    page(handle, lambda r: dict(rot=float(r.choice([0, 0.2, 0.4, 0.6, 0.8])), attach=bool(r.random() < 0.7)), 3, "prob-handles.jpg")
    page(rim, lambda r: dict(elev=float(r.choice([0.12, 0.3, 0.5, 0.7, 0.9]))), 5, "prob-rims.jpg")
    page(bowl_profile, lambda r: dict(depth=float(r.uniform(28, 56)), flareW=float(r.uniform(42, 60))), 8, "prob-bowl-profiles.jpg")
    page(spout, lambda r: dict(ang=float(r.choice([0.1, 0.35, 0.6, 0.85])), length=float(r.uniform(70, 95))), 12, "prob-spouts.jpg")
    page(pot_lip, lambda r: dict(elev=float(r.choice([0.15, 0.35, 0.55, 0.75, 0.95]))), 17, "prob-pot-lips.jpg")
