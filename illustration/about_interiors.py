"""
Hessentials — ABOUT, three rooms (original authored drawings, no source photo).

Not a symbol. A condition: a room where years of keeping-and-removing have become
visible. Built from imagination in the brand's graphite language on warm ivory —
FLW only as atmosphere (long horizontals, a low built-in, light handled honestly),
never recreated. Fresh flowers alive in each.

  A  edited        — the right things, large calm space; selection made visible
  B  mid-decision  — discernment in progress; samples up, two things compared
  C  lived-into    — inevitable, beloved, nothing auditioning anymore

Three theses to choose between — composition over polish. Programmatic synthesis.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from linen import stroke_alpha

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "about")

W, H = 1500, 1050
CREAM = np.array([245, 239, 229], float)
INK = np.array([70, 64, 57], float)
FLOOR_Y = 712


def cmr(nodes, n=18, closed=False):
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


class Pen:
    def __init__(self, rng):
        self.rng = rng
        self.polys = []

    def _wob(self, pts, amp, k=7, overshoot=0.0):
        m = len(pts)
        def sm(kk):
            kk = max(1, min(kk, m))
            return np.convolve(self.rng.normal(0, 1, m), np.ones(kk) / kk, mode="same")
        pts = pts.copy()
        pts[:, 0] += sm(k) * amp + sm(2) * amp * 0.4
        pts[:, 1] += sm(k) * amp + sm(2) * amp * 0.4
        if overshoot:
            d = pts[-1] - pts[-2]; pts = np.vstack([pts, pts[-1] + d * overshoot])
        return pts

    def line(self, nodes, w=2.2, amp=1.4, smooth=False, closed=False, overshoot=0.0, n=20):
        if smooth:
            pts = cmr(nodes, n=14, closed=closed)
        else:
            nn = [np.array(p, float) for p in nodes]
            if closed:
                nn = nn + [nn[0]]
            pts = np.vstack([np.linspace(nn[i], nn[i + 1], n) for i in range(len(nn) - 1)])
        pts = self._wob(pts, amp, overshoot=overshoot)
        self.polys.append(([tuple(p) for p in pts], w))

    def bloom(self, c, r):
        # a small loose flower head: a few short petal strokes around a centre
        cx, cy = c
        for a in np.linspace(0, 2 * np.pi, self.rng.integers(5, 7), endpoint=False):
            a += self.rng.normal(0, 0.2)
            self.line([(cx, cy), (cx + np.cos(a) * r, cy + np.sin(a) * r * 0.9)], w=1.6, amp=0.8, n=8)


def blurmask(poly, blur):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(blur)), float) / 255.0


def base_room(p, rng, warmth=1.0, quiet=False):
    """Tonal light + the room's bones: floor, a wall edge, a window that is mostly
    light, a low shelf beneath it. When quiet, the architecture recedes so the
    life is what remains."""
    img = np.ones((H, W, 3)) * CREAM
    yy, xx = np.mgrid[0:H, 0:W].astype(float)

    leftwall = np.clip((250 - xx) / 250, 0, 1)
    img -= leftwall[..., None] * np.array([7.0, 8.0, 9.0])
    img += blurmask([(384, 206), (1186, 206), (1186, 470), (384, 470)], 28)[..., None] * np.array([8.0, 7.0, 4.0]) * warmth
    pool = blurmask([(440, FLOOR_Y), (1140, FLOOR_Y), (1320, 1040), (300, 1040)], 72)
    img += pool[..., None] * np.array([9.0, 8.0, 5.0]) * warmth
    floor = blurmask([(0, FLOOR_Y), (W, FLOOR_Y), (W, H), (0, H)], 2)
    img += floor[..., None] * np.array([-7.0, -8.0, -10.0])

    p.line([(0, FLOOR_Y - 6), (W, FLOOR_Y + 8)], w=2.2, amp=1.8)
    p.line([(250, 150), (250, FLOOR_Y)], w=1.8, amp=1.8)
    if quiet:
        # the window is mostly light now — a soft frame, a single mullion, no grid
        p.line([(384, 210), (1186, 204), (1186, 470), (384, 474)], w=1.4, amp=1.6, closed=True)
        p.line([(742, 214), (738, 464)], w=1.2, amp=1.3)
        # the shelf, drawn quietly
        p.line([(430, 560), (1086, 556), (1086, 690), (430, 694)], w=1.7, amp=1.5, closed=True)
        p.line([(430, 588), (1086, 584)], w=1.1, amp=1.1)
    else:
        p.line([(384, 206), (1186, 206), (1186, 470), (384, 470)], w=2.2, amp=1.3, closed=True)
        for mx in (584, 784, 984):
            p.line([(mx, 208), (mx, 468)], w=1.6, amp=1.0)
        p.line([(384, 340), (1186, 344)], w=1.4, amp=1.0)
        p.line([(430, 560), (1086, 556), (1086, 690), (430, 694)], w=2.2, amp=1.2, closed=True)
        p.line([(430, 588), (1086, 584)], w=1.4, amp=1.0)
    return img, yy, xx


def messy_stack(p, x, y, n, lean=1.0):
    """Books that accumulated rather than were composed — varied, nudged, some
    pulled half-out, never a tidy tower."""
    yy = y
    for i in range(n):
        wdt = 110 + p.rng.uniform(-30, 40)
        off = p.rng.normal(0, 9 * lean) + i * p.rng.normal(0, 3)
        tilt = p.rng.normal(0, 3.0 * lean)
        p.line([(x + off, yy), (x + wdt + off, yy + tilt)], w=2.0, amp=1.1)
        p.line([(x + off, yy), (x + off + p.rng.normal(0, 2), yy - 14 - p.rng.uniform(0, 8))], w=1.3, amp=0.8)
        p.line([(x + wdt + off, yy + tilt), (x + wdt + off, yy + tilt - 14 - p.rng.uniform(0, 8))], w=1.3, amp=0.8)
        p.line([(x + off, yy - 16), (x + wdt + off, yy + tilt - 16)], w=1.7, amp=1.0)
        yy -= 17 + p.rng.uniform(0, 5)


def vase_flowers(p, cx, base_y, scale=1.0, fullness=5, loose=0.0):
    s = scale
    p.line([(cx - 26 * s, base_y - 60 * s), (cx - 20 * s, base_y), (cx + 20 * s, base_y), (cx + 26 * s, base_y - 60 * s)], w=2.0, amp=1.0)
    p.line([(cx - 26 * s, base_y - 60 * s), (cx + 26 * s, base_y - 60 * s)], w=1.6, amp=0.9)  # rim
    for i in range(fullness):
        a = -np.pi / 2 + (i - fullness / 2) * 0.34 + p.rng.normal(0, 0.06 + loose)
        L = (90 + p.rng.uniform(0, 60)) * s
        tipx = cx + np.cos(a) * L * 0.5
        tipy = base_y - 60 * s + np.sin(a) * L
        p.line([(cx, base_y - 55 * s), (cx + np.cos(a) * L * 0.25, base_y - 60 * s + np.sin(a) * L * 0.55), (tipx, tipy)], w=1.5, amp=1.2 + loose * 4, smooth=True)
        p.bloom((tipx, tipy), (9 + p.rng.uniform(0, 5)) * s)


def chair(p, cx, cy, s=1.0, soft=False):
    """A simple midcentury side chair in loose 3/4 view. cy = floor contact."""
    fw = 130 * s
    sf, sb = cy - 150 * s, cy - 178 * s          # seat front / back heights
    fl = (cx - fw / 2, sf); fr = (cx + fw / 2, sf)
    br = (cx + fw / 2 - 26 * s, sb); bl = (cx - fw / 2 - 26 * s, sb)
    p.line([fl, fr, br, bl], closed=True, w=2.2, amp=1.1 if not soft else 1.9, smooth=soft)   # seat
    p.line([fl, (fl[0] + 3 * s, cy)], w=2.0, amp=1.0)                     # legs
    p.line([fr, (fr[0] + 4 * s, cy - 6 * s)], w=2.0, amp=1.0)
    p.line([br, (br[0] + 2 * s, cy - 34 * s)], w=1.8, amp=1.0)
    btop = sb - 152 * s
    p.line([bl, (bl[0] - 4 * s, btop)], w=2.2, amp=1.1)                   # back posts
    p.line([br, (br[0] - 4 * s, btop + 4 * s)], w=2.2, amp=1.1)
    p.line([(bl[0] - 4 * s, btop), (br[0] - 4 * s, btop + 4 * s)], w=2.2, amp=1.0, smooth=soft)  # top rail
    if not soft:
        p.line([(bl[0] - 2 * s, btop + 70 * s), (br[0] - 2 * s, btop + 74 * s)], w=1.6, amp=1.0)  # a mid rail
    if soft:  # a throw thrown over the seat back
        p.line([(bl[0], sb), (cx - 20 * s, sb - 40 * s), (cx + 30 * s, sb - 10 * s), (fr[0] - 10 * s, sf + 8 * s)], w=1.7, amp=2.2, smooth=True)


def book_stack(p, x, y, n, jog=0.0):
    yy = y
    for i in range(n):
        wdt = 120 + p.rng.uniform(-14, 14)
        off = p.rng.normal(0, jog)
        p.line([(x + off, yy), (x + wdt + off, yy - 4)], w=2.0, amp=1.0)
        p.line([(x + off, yy), (x + off, yy - 16)], w=1.4, amp=0.8)
        p.line([(x + wdt + off, yy - 4), (x + wdt + off, yy - 20)], w=1.4, amp=0.8)
        p.line([(x + off, yy - 16), (x + wdt + off, yy - 20)], w=1.8, amp=1.0)
        yy -= 18


def lamp(p, x, y, h=300):
    p.line([(x, y), (x, y - h)], w=2.0, amp=1.2)              # stem
    p.line([(x - 46, y - h), (x + 46, y - h), (x + 30, y - h - 60), (x - 30, y - h - 60)], w=1.8, amp=1.1, closed=True)  # shade
    p.line([(x - 34, y), (x + 34, y)], w=1.8, amp=1.0)        # base


def lounge_chair(p, cx, by, s=1.0):
    """THE chair — worn into over years. Seat sagged where a body settles, back
    leaned a little to one side, a throw fallen rumpled over the near arm."""
    p.line([(cx - 150 * s, by - 108 * s), (cx - 86 * s, by - 118 * s), (cx - 8 * s, by - 110 * s), (cx + 72 * s, by - 120 * s), (cx + 150 * s, by - 104 * s)], w=2.4, amp=1.4, smooth=True)  # seat front, sagged in the middle
    p.line([(cx - 150 * s, by - 108 * s), (cx - 164 * s, by - 200 * s), (cx - 150 * s, by - 240 * s), (cx - 110 * s, by - 252 * s), (cx - 92 * s, by - 232 * s), (cx - 100 * s, by - 150 * s)], w=2.4, amp=1.4, smooth=True)  # near arm
    p.line([(cx + 150 * s, by - 104 * s), (cx + 164 * s, by - 198 * s), (cx + 150 * s, by - 238 * s), (cx + 112 * s, by - 250 * s), (cx + 96 * s, by - 230 * s), (cx + 104 * s, by - 150 * s)], w=2.4, amp=1.4, smooth=True)  # far arm
    p.line([(cx - 96 * s, by - 232 * s), (cx - 82 * s, by - 330 * s), (cx - 14 * s, by - 352 * s), (cx + 64 * s, by - 324 * s), (cx + 98 * s, by - 228 * s)], w=2.4, amp=1.5, smooth=True)  # back cushion, slumped to one side
    p.line([(cx - 104 * s, by - 150 * s), (cx - 22 * s, by - 166 * s), (cx + 96 * s, by - 150 * s)], w=1.5, amp=1.2, smooth=True)  # seat crease
    p.line([(cx - 44 * s, by - 126 * s), (cx + 28 * s, by - 132 * s)], w=1.1, amp=1.4, smooth=True)  # a soft cushion dent
    p.line([(cx - 122 * s, by - 102 * s), (cx - 150 * s, by)], w=2.0, amp=1.0)  # splayed legs
    p.line([(cx + 122 * s, by - 100 * s), (cx + 150 * s, by + 2 * s)], w=2.0, amp=1.0)
    # the throw, fallen rumpled over the near arm and onto the seat — not arranged
    p.line([(cx - 150 * s, by - 236 * s), (cx - 182 * s, by - 186 * s), (cx - 148 * s, by - 148 * s), (cx - 116 * s, by - 178 * s), (cx - 92 * s, by - 122 * s), (cx - 36 * s, by - 150 * s)], w=1.6, amp=2.6, smooth=True)


def side_table(p, cx, by, s=1.0):
    """A low side table beside the chair, with a mug and a book set down."""
    p.line([(cx - 72 * s, by - 70 * s), (cx + 72 * s, by - 74 * s), (cx + 80 * s, by - 56 * s), (cx - 80 * s, by - 52 * s)], w=2.0, amp=1.0, closed=True)
    p.line([(cx - 60 * s, by - 56 * s), (cx - 58 * s, by)], w=1.8, amp=1.0)
    p.line([(cx + 58 * s, by - 56 * s), (cx + 60 * s, by - 4 * s)], w=1.8, amp=1.0)
    # a mug, half-finished
    p.line([(cx - 36 * s, by - 78 * s), (cx - 36 * s, by - 106 * s), (cx - 4 * s, by - 106 * s), (cx - 4 * s, by - 78 * s)], w=1.6, amp=0.9, smooth=True)
    p.line([(cx - 4 * s, by - 100 * s), (cx + 12 * s, by - 96 * s), (cx + 6 * s, by - 84 * s), (cx - 4 * s, by - 86 * s)], w=1.4, amp=0.9, smooth=True)
    # a book set face-down, mid-read
    p.line([(cx + 16 * s, by - 80 * s), (cx + 70 * s, by - 86 * s), (cx + 66 * s, by - 70 * s), (cx + 12 * s, by - 64 * s)], w=1.5, amp=1.0, closed=True)
    p.line([(cx + 41 * s, by - 83 * s), (cx + 39 * s, by - 67 * s)], w=1.0, amp=0.6)


def render(p, img, seed):
    rng = np.random.default_rng(seed)
    a = stroke_alpha(W, H, p.polys, width=2.2, jitterblur=0.6, supersample=3)
    img = img * (1 - a[..., None]) + INK * a[..., None]
    img += (np.asarray(Image.fromarray((rng.normal(0, 1, (H, W)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 6.0
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))


def compose(variant, seed=7):
    rng = np.random.default_rng(seed)
    p = Pen(rng)
    img, yy, xx = base_room(p, rng, warmth=1.4 if variant == "C" else 1.0, quiet=(variant == "C"))

    # shared: the chair, a low table, the credenza's flowers
    if variant == "A":
        chair(p, 1250, 930, s=1.05)
        vase_flowers(p, 900, 556, scale=1.0, fullness=5)         # cut this week
        book_stack(p, 470, 556, 3)
        lamp(p, 560, 556, h=210)                                  # a table lamp on the credenza
        # otherwise large areas of calm, empty floor

    elif variant == "B":
        chair(p, 1250, 930, s=1.05)
        # paint samples taped to the wall beside the window
        for i, sx in enumerate((300, 318, 336)):
            p.line([(sx, 250 + i * 2), (sx + 14, 248 + i * 2), (sx + 14, 320), (sx, 322)], w=1.4, amp=0.8, closed=True)
        # two near-identical vessels being compared on the credenza
        vase_flowers(p, 700, 556, scale=0.8, fullness=4)
        vase_flowers(p, 840, 556, scale=0.82, fullness=4)
        book_stack(p, 470, 556, 3, jog=10)                        # mid re-stack
        book_stack(p, 560, FLOOR_Y + 170, 5, jog=12)             # a pile on the floor, being re-sorted

    else:  # C — lived into (V2: edited by time, arranged by habit not design)
        # a soft rug, settled a little off-square under the chair
        p.line([(1010, 982), (1244, 1002), (1432, 978), (1398, 1036), (1238, 1052), (1036, 1034)], w=1.4, amp=2.2, smooth=True, closed=True)
        lounge_chair(p, 1235, 962, s=1.02)                        # THE chair
        side_table(p, 1012, 942, s=1.0)                           # mug actually set down, book at an angle
        # the shelf, arranged by use: books accumulated at the left, the lamp
        # belongs beside them, flowers loose and off to the right, a dish left out of true
        messy_stack(p, 452, 556, 4, lean=1.1)
        lamp(p, 622, 556, h=205)
        vase_flowers(p, 952, 556, scale=1.05, fullness=6, loose=0.13)
        p.line([(846, 549), (892, 545), (900, 558), (852, 562)], w=1.5, amp=1.1, smooth=True, closed=True)  # a small dish, nudged out of line

    # soft contact shadows under the big pieces, so they sit on the floor
    for (sx0, sx1, sy) in [(1150, 1360, 952), (430, 1086, 700)]:
        sh = blurmask([(sx0, sy), (sx1, sy), (sx1 + 30, sy + 26), (sx0 - 30, sy + 26)], 18)
        img -= sh[..., None] * np.array([10.0, 11.0, 13.0])

    if variant == "C":  # the familiar, golden warmth of a room arrived-into
        img += np.array([6.0, 3.0, -3.0])

    return render(p, img, seed)


def vessel(p, x, base, w=30, h=36):
    """A small cup-ish thing on the console — anonymous enough to be a candidate."""
    p.line([(x, base), (x - 3, base - h), (x + w + 3, base - h), (x + w, base)], w=1.8, amp=1.0, closed=True, smooth=True)


def chair_back(p, cx, by, s=1.0):
    """THE chair, seen from behind, turned to the light. Use, not display."""
    p.line([(cx - 120 * s, by - 150 * s), (cx - 150 * s, by - 300 * s), (cx - 110 * s, by - 362 * s), (cx, by - 376 * s), (cx + 110 * s, by - 362 * s), (cx + 150 * s, by - 300 * s), (cx + 120 * s, by - 150 * s)], w=2.4, amp=1.5, smooth=True)  # back shell, leaned-into
    p.line([(cx - 120 * s, by - 150 * s), (cx - 170 * s, by - 178 * s), (cx - 178 * s, by - 118 * s), (cx - 150 * s, by - 100 * s), (cx - 116 * s, by - 126 * s)], w=2.2, amp=1.4, smooth=True)  # near arm
    p.line([(cx + 120 * s, by - 150 * s), (cx + 170 * s, by - 178 * s), (cx + 178 * s, by - 118 * s), (cx + 150 * s, by - 100 * s), (cx + 116 * s, by - 126 * s)], w=2.2, amp=1.4, smooth=True)  # far arm
    p.line([(cx - 112 * s, by - 108 * s), (cx - 140 * s, by)], w=2.0, amp=1.0)
    p.line([(cx + 112 * s, by - 108 * s), (cx + 140 * s, by)], w=2.0, amp=1.0)
    # a throw fallen over the top of the back and down one side, not arranged
    p.line([(cx - 78 * s, by - 360 * s), (cx - 34 * s, by - 330 * s), (cx + 8 * s, by - 360 * s), (cx + 52 * s, by - 326 * s), (cx + 86 * s, by - 352 * s)], w=1.6, amp=2.4, smooth=True)
    p.line([(cx - 70 * s, by - 352 * s), (cx - 98 * s, by - 250 * s), (cx - 80 * s, by - 186 * s)], w=1.5, amp=2.2, smooth=True)  # falls over the left shoulder, not the centre


def compose_C(seed=7):
    """The earned room. Turned to the light, arranged for use, stripped to only
    what survived. A portrait of a standard, not an owner."""
    rng = np.random.default_rng(seed)
    p = Pen(rng)
    img = np.ones((H, W, 3)) * CREAM
    yy, xx = np.mgrid[0:H, 0:W].astype(float)

    img -= np.clip((230 - xx) / 230, 0, 1)[..., None] * np.array([6.0, 7.0, 8.0])
    img += blurmask([(540, 200), (980, 196), (980, 470), (540, 474)], 30)[..., None] * np.array([9.0, 8.0, 5.0]) * 1.4  # the window, mostly light
    img += blurmask([(560, FLOOR_Y), (960, FLOOR_Y), (1120, 1040), (360, 1040)], 74)[..., None] * np.array([10.0, 9.0, 6.0]) * 1.4  # light pooled on the floor it faces
    img += blurmask([(0, FLOOR_Y), (W, FLOOR_Y), (W, H), (0, H)], 2)[..., None] * np.array([-7.0, -8.0, -10.0])

    p.line([(0, FLOOR_Y - 6), (W, FLOOR_Y + 8)], w=2.2, amp=1.9)
    p.line([(230, 150), (230, FLOOR_Y)], w=1.7, amp=1.9)
    p.line([(540, 202), (980, 198), (980, 470), (540, 474)], w=1.4, amp=1.7, closed=True)  # window — quiet, light
    p.line([(760, 206), (757, 466)], w=1.1, amp=1.4)

    # the console — a room still quietly being edited. What earned its place sits
    # settled and spaced; two near-twins still sit together at the end, one nudged
    # forward, not yet resolved; and a clear gap where something was just removed.
    p.line([(130, 560), (560, 556), (560, 690), (130, 694)], w=1.6, amp=1.5, closed=True)
    p.line([(130, 586), (560, 582)], w=1.0, amp=1.1)
    vase_flowers(p, 196, 556, scale=0.92, fullness=5, loose=0.12)   # alive, casually kept
    messy_stack(p, 268, 556, 3, lean=0.7)                           # a few books that earned it
    # (a gap here, ~x395–448 — something was just taken down)
    vessel(p, 454, 556, w=30, h=36)                                 # two near-twins, still being weighed
    vessel(p, 488, 552, w=30, h=41)                                 # one nudged forward, unresolved

    chair_back(p, 840, 950, s=1.05)                             # THE chair, turned to the light
    side_table(p, 1130, 932, s=0.95)                            # the coffee, set down within reach

    img -= blurmask([(700, 948), (980, 948), (1014, 976), (666, 976)], 18)[..., None] * np.array([10.0, 11.0, 13.0])
    img += np.array([6.0, 3.0, -3.0])                           # the familiar warmth
    return render(p, img, seed)


if __name__ == "__main__":
    for v in ("A", "B"):
        compose(v).save(os.path.join(OUT, f"about-interior-{v}.jpg"), quality=92)
    compose_C().save(os.path.join(OUT, "about-interior-C.jpg"), quality=92)
    print("saved A B C")
