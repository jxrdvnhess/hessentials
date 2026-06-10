"""
Hessentials — sketchbook. Observation, not interpretation.

Twenty-five graphite studies of ordinary things, drawn from imagination. No
covers, no essays, no symbols, no meanings. The only question is whether each
one feels like something a human actually drew: confident living line, honest
proportion, restraint, a little air. Meaning, if it comes, comes after.

Output: a handful of sketchbook sheets, several studies each.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "about")
CREAM = np.array([245, 240, 231], float)
INK = np.array([66, 60, 54], float)
SHEET_W, SHEET_H = 1480, 1960          # a portrait sheet
COLS, ROWS = 2, 3                       # 6 studies per sheet


class Pen:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.polys = []
        self.shadows = []

    def _wob(self, pts, amp, k=7, overshoot=0.0):
        m = len(pts)
        def sm(kk):
            kk = max(1, min(kk, m))
            return np.convolve(self.rng.normal(0, 1, m), np.ones(kk) / kk, mode="same")
        pts = pts.copy()
        pts[:, 0] += sm(k) * amp + sm(2) * amp * 0.4
        pts[:, 1] += sm(k) * amp + sm(2) * amp * 0.4
        if overshoot:
            d = pts[-1] - pts[-2]
            pts = np.vstack([pts, pts[-1] + d * overshoot])
        return pts

    def L(self, nodes, w=2.0, amp=1.2, closed=False, smooth=False, overshoot=0.0, n=16):
        if smooth:
            pts = _cmr(nodes, closed=closed)
        else:
            nn = [np.array(p, float) for p in nodes]
            if closed:
                nn = nn + [nn[0]]
            pts = np.vstack([np.linspace(nn[i], nn[i + 1], n) for i in range(len(nn) - 1)])
        self.polys.append(([tuple(q) for q in self._wob(pts, amp, overshoot=overshoot)], w))

    def shadow(self, cx, by, hw):
        self.shadows.append((cx, by, hw))


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


# ---------------------------------------------------------------- the subjects
def s_window(p, cx, by, s=1.0):
    w, h = 220 * s, 250 * s
    x0, y0 = cx - w / 2, by - h - 60 * s
    p.L([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], w=2.4, amp=1.2, closed=True)
    p.L([(x0 + w / 2, y0), (x0 + w / 2, y0 + h)], w=1.6, amp=1.0)
    p.L([(x0, y0 + h / 2), (x0 + w, y0 + h / 2)], w=1.6, amp=1.0)
    p.L([(x0 - 18 * s, y0 + h), (x0 + w + 18 * s, y0 + h + 6)], w=2.4, amp=1.2)   # sill
    p.L([(x0 - 6, y0 - 6), (x0 + w + 6, y0 - 6)], w=1.4, amp=1.0)                 # head


def s_door(p, cx, by, s=1.0):
    w, h = 150 * s, 320 * s
    x0, y0 = cx - w / 2, by - h
    p.L([(x0, by), (x0, y0), (x0 + w, y0), (x0 + w, by)], w=2.4, amp=1.2)        # frame
    p.L([(x0 + 14 * s, by), (x0 + 14 * s, y0 + 14 * s), (x0 - 70 * s, y0 + 6 * s), (x0 - 70 * s, by + 6 * s)], w=2.0, amp=1.3)  # door ajar
    p.L([(x0 - 60 * s, by - 150 * s), (x0 - 52 * s, by - 158 * s)], w=1.6, amp=0.8)  # handle
    p.shadow(cx - 30 * s, by, 120 * s)


def s_chairA(p, cx, by, s=1.0):
    sw = 120 * s
    sf = by - 150 * s
    p.L([(cx - sw / 2, sf), (cx + sw / 2, sf - 8 * s), (cx + sw / 2 + 24 * s, sf + 36 * s), (cx - sw / 2 + 24 * s, sf + 46 * s)], w=2.2, amp=1.2, closed=True)
    p.L([(cx - sw / 2, sf), (cx - sw / 2 + 6 * s, sf - 130 * s)], w=2.2, amp=1.1)
    p.L([(cx + sw / 2, sf - 8 * s), (cx + sw / 2 + 4 * s, sf - 138 * s)], w=2.2, amp=1.1)
    p.L([(cx - sw / 2 + 6 * s, sf - 130 * s), (cx + sw / 2 + 4 * s, sf - 138 * s)], w=2.2, amp=1.0, smooth=True)
    p.L([(cx - sw / 2 + 4 * s, sf - 70 * s), (cx + sw / 2 + 2 * s, sf - 76 * s)], w=1.6, amp=1.0)
    p.L([(cx - sw / 2, sf), (cx - sw / 2 + 4 * s, by)], w=2.0, amp=1.0)
    p.L([(cx + sw / 2, sf - 8 * s), (cx + sw / 2 + 4 * s, by - 6 * s)], w=2.0, amp=1.0)
    p.L([(cx - sw / 2 + 24 * s, sf + 46 * s), (cx - sw / 2 + 28 * s, by)], w=2.0, amp=1.0)
    p.shadow(cx, by, 110 * s)


def s_stool(p, cx, by, s=1.0):
    sw = 90 * s
    sf = by - 150 * s
    p.L([(cx - sw / 2, sf), (cx + sw / 2, sf - 6 * s), (cx + sw / 2 + 20 * s, sf + 28 * s), (cx - sw / 2 + 20 * s, sf + 36 * s)], w=2.2, amp=1.1, closed=True)
    for lx, lo in [(-sw / 2, 0), (sw / 2, -6), (-sw / 2 + 20, 36), (sw / 2 + 20, 28)]:
        p.L([(cx + lx * s, sf + lo * s), (cx + lx * s + 4 * s, by)], w=2.0, amp=1.0)
    p.shadow(cx, by, 80 * s)


def s_armchair(p, cx, by, s=1.0):
    p.L([(cx - 130 * s, by - 110 * s), (cx - 90 * s, by - 124 * s), (cx + 90 * s, by - 120 * s), (cx + 130 * s, by - 106 * s)], w=2.4, amp=1.3, smooth=True)
    p.L([(cx - 130 * s, by - 110 * s), (cx - 150 * s, by - 200 * s), (cx - 110 * s, by - 246 * s), (cx - 84 * s, by - 224 * s), (cx - 92 * s, by - 150 * s)], w=2.4, amp=1.4, smooth=True)
    p.L([(cx + 130 * s, by - 106 * s), (cx + 150 * s, by - 198 * s), (cx + 110 * s, by - 244 * s), (cx + 86 * s, by - 222 * s), (cx + 94 * s, by - 150 * s)], w=2.4, amp=1.4, smooth=True)
    p.L([(cx - 92 * s, by - 224 * s), (cx - 60 * s, by - 312 * s), (cx, by - 330 * s), (cx + 62 * s, by - 312 * s), (cx + 94 * s, by - 222 * s)], w=2.4, amp=1.4, smooth=True)
    p.L([(cx - 100 * s, by - 150 * s), (cx, by - 162 * s), (cx + 96 * s, by - 150 * s)], w=1.5, amp=1.0, smooth=True)
    p.L([(cx - 104 * s, by - 104 * s), (cx - 128 * s, by)], w=2.0, amp=1.0)
    p.L([(cx + 104 * s, by - 102 * s), (cx + 128 * s, by)], w=2.0, amp=1.0)
    p.shadow(cx, by, 150 * s)


def s_table_lamp(p, cx, by, s=1.0):
    p.L([(cx, by), (cx, by - 130 * s)], w=2.0, amp=1.1)
    p.L([(cx - 40 * s, by - 130 * s), (cx + 40 * s, by - 130 * s), (cx + 26 * s, by - 188 * s), (cx - 26 * s, by - 188 * s)], w=1.9, amp=1.1, closed=True)
    p.L([(cx - 30 * s, by), (cx + 30 * s, by + 2 * s)], w=1.9, amp=1.0)
    p.shadow(cx, by, 46 * s)


def s_floor_lamp(p, cx, by, s=1.0):
    p.L([(cx, by), (cx + 4 * s, by - 320 * s)], w=2.0, amp=1.1)
    p.L([(cx - 46 * s, by - 320 * s), (cx + 54 * s, by - 320 * s), (cx + 34 * s, by - 392 * s), (cx - 26 * s, by - 392 * s)], w=1.9, amp=1.1, closed=True)
    p.L([(cx - 36 * s, by), (cx + 36 * s, by)], w=1.9, amp=1.0)
    p.L([(cx - 26 * s, by - 4 * s), (cx + 26 * s, by - 4 * s)], w=1.4, amp=0.8)
    p.shadow(cx, by, 60 * s)


def s_table(p, cx, by, s=1.0):
    w, t = 240 * s, by - 150 * s
    p.L([(cx - w / 2, t), (cx + w / 2, t - 8 * s), (cx + w / 2 + 40 * s, t + 30 * s), (cx - w / 2 + 40 * s, t + 38 * s)], w=2.3, amp=1.2, closed=True)
    p.L([(cx - w / 2, t), (cx - w / 2 + 4 * s, by)], w=2.1, amp=1.0)
    p.L([(cx + w / 2, t - 8 * s), (cx + w / 2 + 4 * s, by - 8 * s)], w=2.1, amp=1.0)
    p.L([(cx - w / 2 + 40 * s, t + 38 * s), (cx - w / 2 + 44 * s, by + 30 * s)], w=2.1, amp=1.0)
    p.L([(cx + w / 2 + 40 * s, t + 30 * s), (cx + w / 2 + 44 * s, by + 22 * s)], w=2.1, amp=1.0)
    p.shadow(cx + 10 * s, by + 14 * s, 150 * s)


def s_side_table(p, cx, by, s=1.0):
    p.L([(cx - 70 * s, by - 150 * s), (cx + 70 * s, by - 156 * s), (cx + 80 * s, by - 134 * s), (cx - 80 * s, by - 128 * s)], w=2.2, amp=1.1, closed=True)
    p.L([(cx - 60 * s, by - 130 * s), (cx - 58 * s, by)], w=2.0, amp=1.0)
    p.L([(cx + 60 * s, by - 134 * s), (cx + 62 * s, by - 6 * s)], w=2.0, amp=1.0)
    p.L([(cx - 20 * s, by - 132 * s), (cx - 18 * s, by - 2 * s)], w=1.8, amp=1.0)
    p.shadow(cx, by, 90 * s)


def s_plant_leafy(p, cx, by, s=1.0):
    p.L([(cx - 34 * s, by - 70 * s), (cx - 28 * s, by), (cx + 28 * s, by), (cx + 34 * s, by - 70 * s)], w=2.0, amp=1.1)
    p.L([(cx - 34 * s, by - 70 * s), (cx + 34 * s, by - 70 * s)], w=1.6, amp=0.9)
    for a in np.linspace(-1.3, 1.3, 7):
        L = (120 + p.rng.uniform(0, 50)) * s
        tx, ty = cx + np.sin(a) * L * 0.8, by - 70 * s - np.cos(a) * L
        p.L([(cx, by - 64 * s), (cx + np.sin(a) * L * 0.4, by - 70 * s - np.cos(a) * L * 0.55), (tx, ty)], w=1.5, amp=1.4, smooth=True)
        p.L([(cx + np.sin(a) * L * 0.55, by - 70 * s - np.cos(a) * L * 0.7), (tx, ty), (cx + np.sin(a) * L * 0.62, by - 70 * s - np.cos(a) * L * 0.82)], w=1.2, amp=1.2, smooth=True)
    p.shadow(cx, by, 60 * s)


def s_plant_stems(p, cx, by, s=1.0):
    p.L([(cx - 26 * s, by - 64 * s), (cx - 30 * s, by), (cx + 30 * s, by), (cx + 26 * s, by - 64 * s)], w=2.0, amp=1.1)  # jug
    p.L([(cx + 26 * s, by - 64 * s), (cx + 42 * s, by - 58 * s), (cx + 40 * s, by - 40 * s)], w=1.6, amp=1.0, smooth=True)  # spout
    for a in np.linspace(-0.5, 0.6, 5):
        L = (150 + p.rng.uniform(0, 70)) * s
        tx, ty = cx + np.sin(a) * L * 0.5, by - 64 * s - np.cos(a) * L
        p.L([(cx, by - 60 * s), (tx, ty)], w=1.4, amp=1.6, smooth=True)
        for k in range(3):
            f = 0.4 + k * 0.2
            bx, byy = cx + np.sin(a) * L * 0.5 * f, by - 64 * s - np.cos(a) * L * f
            p.L([(bx, byy), (bx + p.rng.uniform(-10, 10) * s, byy - 10 * s)], w=1.0, amp=0.8)
    p.shadow(cx, by, 50 * s)


def s_shelf(p, cx, by, s=1.0):
    w, h = 220 * s, 300 * s
    x0, y0 = cx - w / 2, by - h
    p.L([(x0, by), (x0, y0), (x0 + w, y0), (x0 + w, by)], w=2.3, amp=1.1)
    for yy in (y0 + 90 * s, y0 + 180 * s, y0 + 270 * s):
        p.L([(x0, yy), (x0 + w, yy)], w=2.0, amp=1.0)
        bx = x0 + 12 * s
        while bx < x0 + w - 20 * s:
            bw = (12 + p.rng.uniform(0, 8)) * s
            bh = (60 + p.rng.uniform(-12, 6)) * s
            lean = p.rng.normal(0, 2.5)
            p.L([(bx, yy), (bx + lean, yy - bh), (bx + bw + lean, yy - bh), (bx + bw, yy)], w=1.5, amp=0.9)
            bx += bw + 4 * s
    p.shadow(cx, by, 130 * s)


def s_books(p, cx, by, s=1.0):
    x = cx - 80 * s
    yy = by
    for i in range(5):
        w = (150 + p.rng.uniform(-30, 30)) * s
        off = p.rng.normal(0, 8) * s
        tilt = p.rng.normal(0, 3) * s
        p.L([(x + off, yy), (x + w + off, yy + tilt), (x + w + off, yy + tilt - 18 * s), (x + off, yy - 18 * s)], w=1.8, amp=0.9, closed=True)
        yy -= 18 * s
    p.shadow(cx, by, 100 * s)


def s_stairs(p, cx, by, s=1.0):
    x, y = cx - 130 * s, by
    for i in range(6):
        p.L([(x, y), (x + 70 * s, y)], w=2.1, amp=1.0)            # tread
        p.L([(x + 70 * s, y), (x + 70 * s, y - 44 * s)], w=2.1, amp=1.0)  # riser
        x += 44 * s
        y -= 44 * s
    p.L([(cx - 130 * s, by), (cx - 130 * s, by - 60 * s)], w=1.8, amp=1.0)
    p.shadow(cx - 60 * s, by, 130 * s)


def s_hallway(p, cx, by, s=1.0):
    vx, vy = cx + 20 * s, by - 200 * s
    p.L([(cx - 200 * s, by), (vx, vy)], w=2.0, amp=1.0)
    p.L([(cx + 200 * s, by), (vx, vy)], w=2.0, amp=1.0)
    p.L([(cx - 200 * s, by - 360 * s), (vx, vy)], w=1.8, amp=1.0)
    p.L([(cx + 200 * s, by - 360 * s), (vx, vy)], w=1.8, amp=1.0)
    p.L([(vx - 36 * s, vy + 70 * s), (vx - 36 * s, vy - 30 * s), (vx + 36 * s, vy - 30 * s), (vx + 36 * s, vy + 70 * s)], w=1.8, amp=1.0)  # door at end


def s_counter(p, cx, by, s=1.0):
    p.L([(cx - 200 * s, by - 150 * s), (cx + 200 * s, by - 150 * s)], w=2.3, amp=1.1)  # counter top
    p.L([(cx - 200 * s, by - 150 * s), (cx - 200 * s, by)], w=2.0, amp=1.0)
    p.L([(cx + 200 * s, by - 150 * s), (cx + 200 * s, by)], w=2.0, amp=1.0)
    p.L([(cx - 60 * s, by - 150 * s), (cx - 60 * s, by)], w=1.6, amp=1.0)
    # a tap
    p.L([(cx + 120 * s, by - 150 * s), (cx + 120 * s, by - 210 * s), (cx + 90 * s, by - 214 * s)], w=2.0, amp=1.1, smooth=True)
    # a bowl + a bottle
    p.L([(cx - 130 * s, by - 150 * s), (cx - 150 * s, by - 178 * s), (cx - 110 * s, by - 178 * s)], w=1.7, amp=1.0, smooth=True)
    p.L([(cx + 20 * s, by - 150 * s), (cx + 20 * s, by - 220 * s), (cx + 44 * s, by - 220 * s), (cx + 44 * s, by - 150 * s)], w=1.7, amp=1.0)


def s_gate(p, cx, by, s=1.0):
    p.L([(cx - 130 * s, by), (cx - 130 * s, by - 250 * s)], w=2.4, amp=1.1)   # posts
    p.L([(cx + 130 * s, by), (cx + 130 * s, by - 250 * s)], w=2.4, amp=1.1)
    p.L([(cx - 110 * s, by - 30 * s), (cx + 110 * s, by - 30 * s)], w=2.0, amp=1.0)  # gate frame
    p.L([(cx - 110 * s, by - 200 * s), (cx + 110 * s, by - 200 * s)], w=2.0, amp=1.0)
    p.L([(cx - 110 * s, by - 30 * s), (cx - 110 * s, by - 200 * s)], w=2.0, amp=1.0)
    p.L([(cx + 110 * s, by - 30 * s), (cx + 110 * s, by - 200 * s)], w=2.0, amp=1.0)
    for bx in np.linspace(cx - 90 * s, cx + 90 * s, 6):
        p.L([(bx, by - 36 * s), (bx, by - 196 * s)], w=1.4, amp=1.0)
    p.L([(cx - 110 * s, by - 196 * s), (cx + 110 * s, by - 40 * s)], w=1.5, amp=1.1)  # brace
    p.shadow(cx, by, 150 * s)


def s_vase(p, cx, by, s=1.0):
    p.L([(cx - 40 * s, by - 6 * s), (cx - 52 * s, by - 80 * s), (cx - 30 * s, by - 150 * s), (cx - 36 * s, by - 178 * s), (cx + 36 * s, by - 178 * s), (cx + 30 * s, by - 150 * s), (cx + 52 * s, by - 80 * s), (cx + 40 * s, by - 6 * s)], w=2.2, amp=1.1, smooth=True, closed=True)
    p.shadow(cx, by, 56 * s)


def s_mug(p, cx, by, s=1.0):
    p.L([(cx - 34 * s, by), (cx - 34 * s, by - 78 * s), (cx + 34 * s, by - 78 * s), (cx + 34 * s, by)], w=2.2, amp=1.0, smooth=True)
    p.L([(cx - 34 * s, by), (cx + 34 * s, by)], w=2.0, amp=1.0, smooth=True)
    p.L([(cx + 34 * s, by - 60 * s), (cx + 64 * s, by - 54 * s), (cx + 52 * s, by - 20 * s), (cx + 34 * s, by - 24 * s)], w=1.8, amp=1.0, smooth=True)
    p.shadow(cx, by, 50 * s)


def s_pegs(p, cx, by, s=1.0):
    rail = by - 240 * s
    p.L([(cx - 160 * s, rail), (cx + 160 * s, rail)], w=2.4, amp=1.1)
    for hx in np.linspace(cx - 120 * s, cx + 120 * s, 5):
        p.L([(hx, rail), (hx, rail + 22 * s), (hx + 12 * s, rail + 26 * s)], w=2.0, amp=1.0, smooth=True)
    # a cloth hanging from one peg
    p.L([(cx - 60 * s, rail + 24 * s), (cx - 96 * s, rail + 150 * s), (cx - 60 * s, rail + 230 * s), (cx - 20 * s, rail + 150 * s), (cx - 50 * s, rail + 30 * s)], w=1.6, amp=1.5, smooth=True)


def s_bench(p, cx, by, s=1.0):
    p.L([(cx - 150 * s, by - 110 * s), (cx + 150 * s, by - 114 * s), (cx + 160 * s, by - 96 * s), (cx - 160 * s, by - 92 * s)], w=2.3, amp=1.1, closed=True)
    for lx in (-130, 130, -130 + 30, 130 + 30):
        oo = 0 if abs(lx) == 130 else 4
        p.L([(cx + lx * s, by - 100 * s), (cx + (lx + oo) * s, by)], w=2.0, amp=1.0)
    p.shadow(cx, by, 160 * s)


def s_sill_plant(p, cx, by, s=1.0):
    s_window(p, cx, by, s * 0.92)
    # a small pot on the sill
    sx = cx - 70 * s
    p.L([(sx - 22 * s, by - 60 * s), (sx - 18 * s, by - 110 * s), (sx + 18 * s, by - 110 * s), (sx + 22 * s, by - 60 * s)], w=1.8, amp=1.0)
    for a in np.linspace(-0.8, 0.8, 4):
        p.L([(sx, by - 108 * s), (sx + np.sin(a) * 60 * s, by - 110 * s - np.cos(a) * 70 * s)], w=1.3, amp=1.3, smooth=True)


def s_reading_corner(p, cx, by, s=1.0):
    s_armchair(p, cx - 20 * s, by, s * 0.8)
    s_floor_lamp(p, cx + 150 * s, by, s * 0.62)
    s_books(p, cx - 150 * s, by, s * 0.5)


def s_candlestick(p, cx, by, s=1.0):
    p.L([(cx - 30 * s, by), (cx - 14 * s, by - 10 * s), (cx + 14 * s, by - 10 * s), (cx + 30 * s, by)], w=2.0, amp=1.0, smooth=True)  # base
    p.L([(cx - 10 * s, by - 10 * s), (cx - 6 * s, by - 150 * s), (cx + 6 * s, by - 150 * s), (cx + 10 * s, by - 10 * s)], w=2.0, amp=1.0)  # stem
    p.L([(cx - 16 * s, by - 150 * s), (cx + 16 * s, by - 150 * s)], w=1.8, amp=0.9)
    p.L([(cx, by - 150 * s), (cx, by - 178 * s)], w=1.6, amp=0.9)   # candle
    p.L([(cx, by - 178 * s), (cx + 4 * s, by - 196 * s), (cx, by - 206 * s), (cx - 3 * s, by - 192 * s)], w=1.2, amp=1.0, smooth=True)  # flame
    p.shadow(cx, by, 50 * s)


def s_bowl(p, cx, by, s=1.0):
    p.L([(cx - 80 * s, by - 50 * s), (cx - 60 * s, by - 6 * s), (cx + 60 * s, by - 6 * s), (cx + 80 * s, by - 50 * s)], w=2.2, amp=1.1, smooth=True)
    p.L([(cx - 80 * s, by - 50 * s), (cx, by - 38 * s), (cx + 80 * s, by - 50 * s)], w=1.5, amp=1.0, smooth=True)  # rim ellipse front
    p.shadow(cx, by, 86 * s)


SUBJECTS = [
    s_window, s_door, s_chairA, s_armchair, s_stool, s_table_lamp,
    s_floor_lamp, s_table, s_side_table, s_plant_leafy, s_plant_stems, s_shelf,
    s_books, s_stairs, s_hallway, s_counter, s_gate, s_vase,
    s_mug, s_pegs, s_bench, s_sill_plant, s_reading_corner, s_candlestick, s_bowl,
]


def render_sheet(subjects_with_pos, seed):
    p = Pen(seed)
    for fn, (cx, by, s) in subjects_with_pos:
        fn(p, cx, by, s)
    img = np.ones((SHEET_H, SHEET_W, 3)) * CREAM
    yy, xx = np.mgrid[0:SHEET_H, 0:SHEET_W].astype(float)
    for (cx, by, hw) in p.shadows:
        d = ((xx - cx) / (hw)) ** 2 + ((yy - by - 10) / (hw * 0.28)) ** 2
        img -= np.clip(1 - d, 0, 1)[..., None] * np.array([8.0, 9.0, 10.0])
    a = stroke_alpha(SHEET_W, SHEET_H, p.polys, width=2.0, jitterblur=0.6, supersample=3)
    img = img * (1 - a[..., None]) + INK * a[..., None]
    img += (np.asarray(Image.fromarray((p.rng.normal(0, 1, (SHEET_H, SHEET_W)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 6.0
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))


if __name__ == "__main__":
    cellw, cellh = SHEET_W / COLS, SHEET_H / ROWS
    per = COLS * ROWS
    sheets = []
    for i, fn in enumerate(SUBJECTS):
        sheets.append((i // per, fn))
    n_sheets = (len(SUBJECTS) + per - 1) // per
    for sh in range(n_sheets):
        items = []
        for fn in [f for (s, f) in sheets if s == sh]:
            idx = SUBJECTS.index(fn) % per
            r, c = idx // COLS, idx % COLS
            cx = c * cellw + cellw / 2
            by = r * cellh + cellh * 0.74
            sc = 1.0
            items.append((fn, (cx, by, sc)))
        render_sheet(items, seed=sh + 3).save(os.path.join(OUT, f"sketchbook-{sh + 1}.jpg"), quality=92)
        print("saved sheet", sh + 1, "with", len(items), "studies")
