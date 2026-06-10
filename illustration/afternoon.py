"""
Hessentials — an afternoon with one object.

One real object. One page. The whole thing drawn a few times — large, small,
cropped, unfinished — and then the one part that won't resolve drawn over and
over, with the other parts studied between. The page should reveal the problem,
not the object: the handle, the leg-to-seat joint, the depth of a window frame,
the lamp's shade, the bowl's rim. Line only. No grid. No composition. Attention.
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


# ============================================================= MUG (handle)
def _mug(lp, elev, hand=1, inner=True, base=True, R=44, H=74, thick=4):
    ry = max(1.0, abs(elev) * R * 0.6); top = -H; Rb = R * 0.94
    lp.l([(-R, top), (-Rb, 0)]); lp.l([(R, top), (Rb, 0)]); lp.p(ell(0, top, R, ry))
    if elev > 0.18 and inner:
        lp.p(ell(0, top + thick * 0.7, R - thick, ry * 0.9))
    if base:
        if elev >= 0:
            lp.p(ell(0, 0, Rb, max(0.8, ry * 0.8), a0=0.06, a1=np.pi - 0.06))
        else:
            lp.p(ell(0, 0, Rb, ry)); lp.p(ell(0, 0, Rb * 0.7, ry * 0.7))
    hx = hand * R; hw = 30
    lp.l([(hx, top + H * 0.2), (hx + hand * hw, top + H * 0.28), (hx + hand * hw * 1.04, top + H * 0.6), (hx, top + H * 0.72)], smooth=True)
    lp.l([(hx, top + H * 0.3), (hx + hand * hw * 0.6, top + H * 0.36), (hx + hand * hw * 0.62, top + H * 0.56), (hx, top + H * 0.62)], smooth=True)


def m_side(lp): _mug(lp, 0.12, inner=False)
def m_3q(lp): _mug(lp, 0.42)
def m_above(lp): _mug(lp, 0.85)
def m_below(lp): _mug(lp, -0.45)
def m_rim(lp): lp.p(ell(0, 0, 44, 16)); lp.p(ell(0, 3, 40, 14))
def m_base(lp): lp.p(ell(0, 0, 41, 12))
def m_profile(lp): lp.l([(-44, -74), (-41, 0), (41, 0), (44, -74)]); lp.p(ell(0, -74, 44, 9))
def m_attach(lp):                                        # the join, isolated
    lp.l([(-16, -44), (0, -46), (0, 46), (-16, 44)], smooth=True)
    lp.l([(0, -30), (22, -26), (22, -8)], smooth=True)
    lp.l([(0, 30), (22, 26), (22, 8)], smooth=True)
def m_handle(lp, rot=0.0):                               # THE PROBLEM
    h = 34; W = 28 * (1 - 0.8 * rot)
    lp.l([(0, -h), (W, -h * 0.78), (W * 1.06, h * 0.5), (0, h)], smooth=True)
    lp.l([(0, -h * 0.72), (W * 0.56, -h * 0.5), (W * 0.58, h * 0.3), (0, h * 0.7)], smooth=True)
    lp.l([(0, -h - 8), (0, h + 8)])
MUG = dict(big=m_3q, center=(545, 1080), bigscale=9.5, thumb=m_side,
           problem=m_handle, palt=m_attach, pfeat=(62, -34),
           samp=lambda r: dict(rot=float(r.choice([0, 0.2, 0.4, 0.6, 0.8]))),
           feats=[(m_rim, (0, -74), 3), (m_base, (0, -2), 2)])


# =========================================================== CHAIR (joint)
def ch_side(lp):
    lp.l([(-24, 0), (-24, -44), (24, -44), (24, 0)]); lp.l([(24, -44), (24, 0)])
    lp.l([(-24, -44), (-26, -98)]); lp.l([(-26, -98), (-12, -98)]); lp.l([(-25, -74), (-13, -74)])
def ch_3q(lp):
    lp.l([(-28, -44), (20, -48), (34, -30), (-14, -26)], closed=True)
    lp.l([(-28, -44), (-32, 0)]); lp.l([(20, -48), (22, 0)]); lp.l([(-14, -26), (-16, 4)])
    lp.l([(-14, -26), (-12, -92)]); lp.l([(34, -30), (36, -96)]); lp.l([(-12, -92), (36, -96)])
def ch_leg(lp): lp.l([(-3, -50), (-1, 0)]); lp.l([(4, -50), (2, 0)]); lp.l([(-4, -44), (5, -44)])
def ch_joint(lp, k=0):                                   # THE PROBLEM: leg meets seat
    lp.l([(-32, -44), (10, -47)])                        # seat front edge
    lp.l([(-32, -44), (-48, -36)])                       # seat side edge, receding
    lp.l([(-32, -44), (-31, -12), (-32, 0)])             # front leg from the corner
    lp.l([(-30, -30), (-10, -32)])                       # apron
    lp.l([(-48, -36), (-48, -8)])                        # side leg
    lp.l([(-32, -16), (-46, -18)])                       # side stretcher
CHAIR = dict(big=ch_3q, center=(560, 1120), bigscale=7.4, thumb=ch_side,
             problem=ch_joint, palt=ch_leg, pfeat=(-28, -44),
             samp=lambda r: dict(k=0), feats=[(ch_leg, (22, -24), 2)])


# ========================================================== WINDOW (depth)
def wi_front(lp):
    lp.l([(-60, -90), (60, -90), (60, 90), (-60, 90)], closed=True)
    lp.l([(0, -90), (0, 90)]); lp.l([(-60, 0), (60, 0)])
    lp.l([(-74, 90), (74, 96)])
def wi_sill(lp): lp.l([(-60, 0), (60, 4)]); lp.l([(-74, 0), (74, 6)]); lp.l([(-74, 0), (-74, 14), (60, 18)])
def wi_depth(lp, k=0):                                   # THE PROBLEM: frame depth
    d = 22
    lp.l([(-50, -50), (44, -52)]); lp.l([(-50, -50), (-52, 44)])          # outer corner
    lp.l([(-50 + d, -50 + d * 0.7), (44, -52 + d * 0.6)]); lp.l([(-50 + d, -50 + d * 0.7), (-52 + d * 0.8, 44)])  # inner
    lp.l([(-50, -50), (-50 + d, -50 + d * 0.7)])                          # reveal
    lp.l([(44, -52), (44, -52 + d * 0.6)]); lp.l([(-52, 44), (-52 + d * 0.8, 44)])
WINDOW = dict(big=wi_front, center=(560, 1080), bigscale=4.1, thumb=wi_front,
              problem=wi_depth, palt=wi_sill, pfeat=(-60, -90),
              samp=lambda r: dict(k=0), feats=[(wi_sill, (0, 90), 2)])


# ============================================================ LAMP (shade)
def la_whole(lp):
    lp.l([(0, 0), (0, -90)]); lp.l([(-24, 0), (24, 0)])
    lp.l([(-32, -90), (32, -90), (20, -150), (-20, -150)], closed=True)
    lp.p(ell(0, -150, 20, 6)); lp.p(ell(0, -90, 32, 9))
def la_base(lp): lp.l([(-26, 0), (26, 2)]); lp.p(ell(0, -3, 24, 7))
def la_shade(lp, elev=0.4):                              # THE PROBLEM
    rt, rb, H = 20, 34, 60
    lp.l([(-rb, 0), (rb, 0), (rt, -H), (-rt, -H)], closed=True)
    lp.p(ell(0, -H, rt, max(1.4, elev * rt * 0.6)))
    lp.p(ell(0, 0, rb, max(1.4, elev * rb * 0.4), a0=0.06, a1=np.pi - 0.06))
LAMP = dict(big=la_whole, center=(560, 1240), bigscale=5.0, thumb=la_whole,
            problem=la_shade, palt=la_base, pfeat=(0, -120),
            samp=lambda r: dict(elev=float(r.choice([0.15, 0.35, 0.55, 0.8]))),
            feats=[(la_base, (0, 0), 2)])


# ============================================================= BOWL (rim)
def _bowl(lp, elev, R=52, depth=30):
    ry = max(1.0, abs(elev) * R * 0.7)
    lp.p(ell(0, -depth, R, ry)); lp.p(ell(0, -depth + 4, R - 5, ry * 0.85))
    lp.l([(-R, -depth), (-R * 0.4, 0), (R * 0.4, 0), (R, -depth)], smooth=True)
    lp.p(ell(0, 0, R * 0.34, max(0.8, ry * 0.34), a0=0.1, a1=np.pi - 0.1))
def bo_side(lp): _bowl(lp, 0.1)
def bo_3q(lp): _bowl(lp, 0.45)
def bo_above(lp): _bowl(lp, 0.9)
def bo_profile(lp): lp.l([(-52, -30), (-22, 0), (22, 0), (52, -30)], smooth=True)
def bo_foot(lp): lp.p(ell(0, 0, 18, 7)); lp.l([(-18, 0), (-22, 8)]); lp.l([(18, 0), (22, 8)])
def bo_rim(lp, elev=0.5):                                # THE PROBLEM
    R = 52; ry = max(1.4, elev * R * 0.72)
    lp.p(ell(0, 0, R, ry)); lp.p(ell(0, ry * 0.18 + 2, R - 5, ry * 0.88))
BOWL = dict(big=bo_3q, center=(540, 1060), bigscale=6.4, thumb=bo_side,
            problem=bo_rim, palt=bo_profile, pfeat=(0, -30),
            samp=lambda r: dict(elev=float(r.choice([0.12, 0.3, 0.5, 0.7, 0.9]))),
            feats=[(bo_profile, (0, -15), 2), (bo_foot, (0, 0), 2)])


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


def page(obj, seed, out):
    global RNG
    RNG = np.random.default_rng(seed)
    rng = RNG
    dark, faint = [], []
    placed = []

    def spot(scale, near=None):
        for _ in range(200):
            if near is not None and rng.random() < 0.6:
                cx = near[0] + rng.uniform(-90, 90); cy = near[1] + rng.uniform(-70, 70)
            else:
                cx = rng.uniform(150, SW - 150); cy = rng.uniform(190, SH - 160)
            if cx < 120 or cx > SW - 120 or cy < 150 or cy > SH - 130:
                continue
            if all(((cx - px) ** 2 + (cy - py) ** 2) > (scale * 26) ** 2 for px, py in placed) or rng.random() < 0.18:
                placed.append((cx, cy)); return cx, cy
        placed.append((cx, cy)); return cx, cy

    def draw(fn, kw, scale, into, frac=1.0, near=None):
        cx, cy = spot(scale, near)
        ang = rng.uniform(-0.06, 0.06)
        lp = LP(); fn(lp, **kw)
        place(lp, cx, cy, scale, ang, frac, into)
        return cx, cy

    # a few whole studies — one large, some small, one cropped/unfinished
    for j in range(4):
        fn = obj["wholes"][rng.integers(0, len(obj["wholes"]))]
        sc = [2.7, 1.6, 1.4, 2.0][j] * rng.uniform(0.9, 1.1)
        draw(fn, {}, sc, faint if rng.random() < 0.25 else dark, frac=(rng.uniform(0.4, 0.7) if rng.random() < 0.3 else 1.0))
    # the parts, studied between
    for _ in range(5):
        fn = obj["parts"][rng.integers(0, len(obj["parts"]))]
        draw(fn, {}, rng.uniform(1.1, 1.7), dark, frac=(rng.uniform(0.5, 0.8) if rng.random() < 0.25 else 1.0))
    # THE PROBLEM — drawn over and over, half of them clustered, with first tries
    cluster = None
    for _ in range(12):
        kw = obj["samp"](rng)
        sc = rng.uniform(1.2, 1.9)
        near = cluster if (cluster and rng.random() < 0.55) else None
        if rng.random() < 0.4:                               # a faint first try under it
            lp0 = LP(); obj["problem"](lp0, **kw)
            cx0, cy0 = spot(sc, near)
            place(lp0, cx0 + rng.uniform(-6, 6), cy0 + rng.uniform(-5, 5), sc * rng.uniform(0.96, 1.05), rng.uniform(-0.05, 0.05), 1.0, faint)
            place(LP() or lp0, cx0, cy0, sc, rng.uniform(-0.05, 0.05), (rng.uniform(0.45, 0.8) if rng.random() < 0.35 else 1.0), dark)
            pos = (cx0, cy0)
        else:
            pos = draw(obj["problem"], kw, sc, dark, frac=(rng.uniform(0.45, 0.8) if rng.random() < 0.35 else 1.0), near=near)
        if cluster is None and rng.random() < 0.5:
            cluster = pos

    img = np.ones((SH, SW, 3)) * CREAM
    af = stroke_alpha(SW, SH, faint, width=1.6, jitterblur=0.6, supersample=3) * 0.4
    img = img * (1 - af[..., None]) + INK * af[..., None]
    ad = stroke_alpha(SW, SH, dark, width=1.9, jitterblur=0.55, supersample=3)
    img = img * (1 - ad[..., None]) + INK * ad[..., None]
    img += (np.asarray(Image.fromarray((rng.normal(0, 1, (SH, SW)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 5.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35)).save(os.path.join(OUT, out), quality=92)
    print("saved", out)


def page(obj, seed, out):   # gravity well — accumulates around one dominant drawing
    global RNG
    RNG = np.random.default_rng(seed); rng = RNG
    dark, faint = [], []
    ax, ay = obj["center"]; BS = obj["bigscale"]

    def put(fn, kw, cx, cy, sc, into, frac=1.0):
        lp = LP(); fn(lp, **kw)
        place(lp, cx, cy, sc, rng.uniform(-0.06, 0.06), frac, into)

    def feat(xy):
        return (ax + xy[0] * BS, ay + xy[1] * BS)

    put(obj["big"], {}, ax + rng.uniform(-10, 10), ay + rng.uniform(-8, 8), BS * 1.015, faint)  # first try, faint
    put(obj["big"], {}, ax, ay, BS, dark)                                                       # the dominant drawing

    pf = feat(obj["pfeat"])                       # the problem, accumulated at its feature
    for _ in range(11):
        kw = obj["samp"](rng)
        sc = float(rng.choice([2.4, 1.5, 1.1, 0.85, 0.6, 0.45], p=[.06, .16, .22, .24, .18, .14]))
        cx = pf[0] + rng.normal(0, 92); cy = pf[1] + rng.normal(0, 80)
        if rng.random() < 0.45:                   # a correction over a faint first attempt
            put(obj["problem"], kw, cx + rng.uniform(-5, 5), cy + rng.uniform(-4, 4), sc * rng.uniform(0.95, 1.05), faint)
        put(obj["problem"], kw, cx, cy, sc, dark, frac=(rng.uniform(0.45, 0.8) if rng.random() < 0.35 else 1.0))
    if obj.get("palt"):
        for _ in range(2):
            put(obj["palt"], {}, pf[0] + rng.normal(0, 80), pf[1] + rng.normal(0, 66), rng.uniform(0.8, 1.4), dark, frac=rng.uniform(0.6, 1.0))

    for fn, xy, cnt in obj["feats"]:              # secondary features near their own anchors
        fa = feat(xy)
        for _ in range(cnt):
            put(fn, {}, fa[0] + rng.normal(0, 60), fa[1] + rng.normal(0, 52), rng.uniform(0.7, 1.4), dark, frac=(rng.uniform(0.5, 0.85) if rng.random() < 0.3 else 1.0))

    for _ in range(4):                            # tiny whole thumbnails out in the surround
        put(obj["thumb"], {}, ax + rng.uniform(120, 760), ay + rng.uniform(-660, 240), rng.uniform(0.5, 0.9), dark, frac=(rng.uniform(0.4, 0.7) if rng.random() < 0.4 else 1.0))
    anchors = [obj["pfeat"]] + [xy for _, xy, _ in obj["feats"]]
    for _ in range(5):                            # microscopic fragments at features
        xy = anchors[rng.integers(0, len(anchors))]; fa = feat(xy)
        put(obj["problem"], obj["samp"](rng), fa[0] + rng.normal(0, 44), fa[1] + rng.normal(0, 40), rng.uniform(0.34, 0.5), dark, frac=rng.uniform(0.3, 0.6))

    img = np.ones((SH, SW, 3)) * CREAM
    af = stroke_alpha(SW, SH, faint, width=1.6, jitterblur=0.6, supersample=3) * 0.4
    img = img * (1 - af[..., None]) + INK * af[..., None]
    ad = stroke_alpha(SW, SH, dark, width=1.9, jitterblur=0.55, supersample=3)
    img = img * (1 - ad[..., None]) + INK * ad[..., None]
    img += (np.asarray(Image.fromarray((rng.normal(0, 1, (SH, SW)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 5.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35)).save(os.path.join(OUT, out), quality=92)
    print("saved", out)


if __name__ == "__main__":
    page(MUG, 3, "afternoon-mug.jpg")
    page(CHAIR, 6, "afternoon-chair.jpg")
    page(WINDOW, 9, "afternoon-window.jpg")
    page(LAMP, 13, "afternoon-lamp.jpg")
    page(BOWL, 18, "afternoon-bowl.jpg")
