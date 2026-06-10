"""
Hessentials — observation studies. One object, twenty-five times, line only.

Not icons. Constructed from the geometry that actually governs the thing:
  mug    — the rim and base are ELLIPSES whose openness is the viewpoint; the
           wall has thickness (inner rim); the handle attaches somewhere real.
  chair  — seat depth, back angle, leg relationships, silhouette.
  window — proportion, muntins, sill, casing, openings, asymmetry.

Each sheet is a matrix: viewpoint across, proportion down — so the variation is
legible and you can feel the looking sharpen. Black line, no shading, no rooms,
small on abundant paper.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "about")
CREAM = np.array([246, 241, 232], float)
INK = np.array([54, 49, 44], float)
SW, SH = 1600, 2000
N = 5  # 5 x 5 grid


class Pen:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.polys = []

    def _wob(self, pts, amp):
        m = len(pts)
        if m < 3:
            return pts
        def sm(k):
            k = max(1, min(k, m))
            return np.convolve(self.rng.normal(0, 1, m), np.ones(k) / k, mode="same")
        pts = np.array(pts, float)
        pts[:, 0] += sm(6) * amp + sm(2) * amp * 0.4
        pts[:, 1] += sm(6) * amp + sm(2) * amp * 0.4
        return pts

    def line(self, nodes, w=1.7, amp=0.7, smooth=False, closed=False, n=18):
        if smooth:
            pts = _cmr(nodes, closed=closed)
        else:
            nn = [np.array(p, float) for p in nodes]
            if closed:
                nn = nn + [nn[0]]
            pts = np.vstack([np.linspace(nn[i], nn[i + 1], n) for i in range(len(nn) - 1)])
        self.polys.append(([tuple(q) for q in self._wob(pts, amp)], w))

    def poly(self, pts, w=1.6, amp=0.6):
        self.polys.append(([tuple(q) for q in self._wob(pts, amp)], w))


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


# ----------------------------------------------------------------------- MUG
def mug(p, cx, by, R=46, H=78, elev=0.4, hand=1, hsize=1.0, taper=0.06, thick=4.0):
    """elev 0 = dead side-on (rim a line), 1 = looking straight down (rim round)."""
    ry = max(1.2, R * elev * 0.62)
    top = by - H
    Rb = R * (1 - taper)
    ryb = max(1.0, Rb * elev * 0.5)
    p.line([(cx - R, top), (cx - Rb, by)], w=1.8, amp=0.5)            # body sides
    p.line([(cx + R, top), (cx + Rb, by)], w=1.8, amp=0.5)
    p.poly(ell(cx, top, R, ry), w=1.8, amp=0.5)                        # rim
    if elev > 0.16:                                                   # wall thickness, seen into
        p.poly(ell(cx, top + thick * 0.7, R - thick, ry * 0.9), w=1.2, amp=0.4)
    p.poly(ell(cx, by, Rb, ryb, a0=0.05, a1=np.pi - 0.05), w=1.7, amp=0.5)  # base, front arc only
    hx = cx + hand * R
    hw = (24 + 20 * hsize)
    p.line([(hx, top + H * 0.20), (hx + hand * hw, top + H * 0.28), (hx + hand * hw * 1.04, top + H * 0.60), (hx, top + H * 0.72)], w=1.7, amp=0.6, smooth=True)
    p.line([(hx, top + H * 0.30), (hx + hand * hw * 0.62, top + H * 0.36), (hx + hand * hw * 0.64, top + H * 0.56), (hx, top + H * 0.62)], w=1.2, amp=0.5, smooth=True)


def mug_params(i):
    col, row = i % N, i // N
    elev = [0.10, 0.26, 0.44, 0.64, 0.82][col]                       # viewpoint across
    R, H, taper, thick = [(50, 70, 0.04, 4), (40, 92, 0.02, 3), (58, 60, 0.12, 6),
                          (44, 80, 0.0, 4.5), (46, 78, 0.08, 5)][row]  # proportion down
    return dict(R=R, H=H, elev=elev, taper=taper, thick=thick,
                hand=(1 if (i % 2 == 0) else -1), hsize=[0.7, 1.0, 1.4][i % 3])


# --------------------------------------------------------------------- CHAIR
def chair(p, cx, by, sw=120, sd=60, backh=150, backang=0.10, splay=10, view=0.5):
    """view 0 = near side-on, 1 = more frontal (seat opens up)."""
    so = sd * (0.3 + 0.6 * view)                                     # seat foreshortening
    sf = by - 150
    fl = (cx - sw / 2, sf); fr = (cx + sw / 2, sf - 4)
    br = (cx + sw / 2 - sw * 0.16, sf - so); bl = (cx - sw / 2 - sw * 0.16, sf - so)
    p.line([fl, fr, br, bl], closed=True, w=1.9, amp=0.6)            # seat
    bt = sf - so - backh
    p.line([bl, (bl[0] - backang * backh, bt)], w=1.9, amp=0.6)      # back posts
    p.line([br, (br[0] - backang * backh, bt + 4)], w=1.9, amp=0.6)
    p.line([(bl[0] - backang * backh, bt), (br[0] - backang * backh, bt + 4)], w=1.9, amp=0.5)
    p.line([(bl[0] - backang * backh * 0.5, bt + backh * 0.45), (br[0] - backang * backh * 0.5, bt + backh * 0.45 + 4)], w=1.4, amp=0.5)
    p.line([fl, (fl[0] - splay, by)], w=1.7, amp=0.5)                # legs
    p.line([fr, (fr[0] + splay, by - 4)], w=1.7, amp=0.5)
    p.line([br, (br[0] + splay * 0.4, by - so * 0.2)], w=1.6, amp=0.5)
    p.line([bl, (bl[0] - splay * 0.4, by - so * 0.2)], w=1.4, amp=0.5)


def chair_params(i):
    col, row = i % N, i // N
    view = [0.1, 0.32, 0.55, 0.78, 0.95][col]
    sw, sd, backh, backang = [(120, 64, 150, 0.06), (96, 50, 188, 0.16),
                              (140, 70, 120, 0.0), (110, 58, 160, 0.10),
                              (104, 60, 200, 0.20)][row]
    return dict(sw=sw, sd=sd, backh=backh, backang=backang, splay=[4, 10, 16][i % 3], view=view)


# -------------------------------------------------------------------- WINDOW
def window(p, cx, cy, w=150, h=190, vlites=2, hlites=2, sill=1.0, casing=1.0, ajar=0.0, asym=0.5):
    x0, y0 = cx - w / 2, cy - h / 2
    if casing > 0:                                                  # casing
        c = 8 * casing
        p.line([(x0 - c, y0 - c), (x0 + w + c, y0 - c), (x0 + w + c, y0 + h + c), (x0 - c, y0 + h + c)], closed=True, w=1.5, amp=0.5)
    p.line([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], closed=True, w=1.9, amp=0.6)  # frame
    for k in range(1, vlites):                                     # vertical muntins (asymmetric)
        fx = x0 + w * (k / vlites) + (asym - 0.5) * 18
        p.line([(fx, y0), (fx, y0 + h)], w=1.3, amp=0.5)
    for k in range(1, hlites):                                     # horizontal muntins
        fy = y0 + h * (k / hlites)
        p.line([(x0, fy), (x0 + w, fy)], w=1.3, amp=0.5)
    if sill > 0:                                                   # sill
        s = 14 * sill
        p.line([(x0 - s, y0 + h), (x0 + w + s, y0 + h + 4)], w=1.9, amp=0.6)
        p.line([(x0 - s, y0 + h + 8 * sill), (x0 + w + s, y0 + h + 8 * sill + 4)], w=1.4, amp=0.5)
    if ajar > 0:                                                   # a casement cracked open
        ox = x0 + w * 0.5
        p.line([(ox, y0 + 6), (ox - ajar * 40, y0 + h * 0.18), (ox - ajar * 46, y0 + h * 0.82), (ox, y0 + h - 6)], w=1.4, amp=0.6, smooth=True)


def window_params(i):
    col, row = i % N, i // N
    vl, hl = [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3)][col]          # opening / muntins across
    w, h, sill, casing = [(150, 190, 1.0, 1.0), (110, 220, 0.7, 0.5),
                          (200, 150, 1.2, 1.4), (130, 180, 1.0, 0.0),
                          (160, 200, 0.5, 1.0)][row]                # proportion down
    return dict(w=w, h=h, vlites=vl, hlites=hl, sill=sill, casing=casing,
                ajar=(0.8 if i % 7 == 3 else 0.0), asym=[0.5, 0.5, 0.32, 0.68, 0.5][i % 5])


def sheet(draw_one, params, seed):
    p = Pen(seed)
    cw, ch = SW / N, SH / N
    for i in range(N * N):
        col, row = i % N, i // N
        cx = col * cw + cw / 2
        cyb = row * ch + ch * 0.66        # baseline-ish anchor, small in a big cell
        draw_one(p, cx, cyb, params(i))
    img = np.ones((SH, SW, 3)) * CREAM
    a = stroke_alpha(SW, SH, p.polys, width=1.7, jitterblur=0.5, supersample=3)
    img = img * (1 - a[..., None]) + INK * a[..., None]
    img += (np.asarray(Image.fromarray((p.rng.normal(0, 1, (SH, SW)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 5.0
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35))


if __name__ == "__main__":
    sheet(lambda p, cx, cy, kw: mug(p, cx, cy, **kw), mug_params, 3).save(os.path.join(OUT, "study-mugs.jpg"), quality=92)
    sheet(lambda p, cx, cy, kw: chair(p, cx, cy, **kw), chair_params, 4).save(os.path.join(OUT, "study-chairs.jpg"), quality=92)
    sheet(lambda p, cx, cy, kw: window(p, cx, cy, **kw), window_params, 5).save(os.path.join(OUT, "study-windows.jpg"), quality=92)
    print("saved study-mugs / study-chairs / study-windows")
