"""
Hessentials — About page, Study 08: one evidence.

Study 07's room, untouched, plus the single piece of evidence that makes the
kitchen belong to Jordan: the wine is open, the cork is out, and there is
exactly one wine glass — yours. Variant B adds the permitted second piece:
the cook's own glass of water standing alone by the stove. Nothing explains.
A stranger who counts glasses learns it second.

  A — bottle + one glass only          (about-room-one-evidence.png)
  B — plus the cook's water, by the pan (about-room-one-evidence-b.png)
"""
import numpy as np
from about_two_horizons import Cam, Scene, circle3, ell, render

W, H = 1500, 1900
WZ = 3.1
CZ = 2.5
CT = 0.92


def build(variant="a"):
    cam = Cam(W, H, eye_level=0.42, f=1250, cam_h=1.45, vpx=0.46)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    # ---------------- room anatomy
    S.poly([(-1.9, CT, WZ), (2.6, CT, WZ)], w=1.8)
    S.poly([(-1.9, CT, CZ), (2.6, CT, CZ)], w=2.2)
    S.poly([(-0.02, 0.10, CZ), (2.6, 0.10, CZ)], w=1.6)
    for vx in (0.30, 1.22):
        S.poly([(vx, 0.88, CZ), (vx, 0.12, CZ)], w=1.4, layer="faint")

    x0, x1, y0, y1 = -0.95, 0.05, 1.18, 2.05
    for seg in ([(x0, y0), (x1, y0)], [(x1, y0), (x1, y1)],
                [(x1, y1), (x0, y1)], [(x0, y1), (x0, y0)],
                [(-0.45, y0), (-0.45, y1)]):
        S.poly([(a, b, WZ) for a, b in seg], w=2.0)
    S.poly([(x0 - 0.06, y0 - 0.025, WZ - 0.04),
            (x1 + 0.06, y0 - 0.025, WZ - 0.04)], w=1.8)

    sx, sy, s, zc = S.anchor((-0.62, CT, WZ - 0.12))
    S.glyph([(0, 0), (0, -0.34), (0.025, -0.39), (0.12, -0.405), (0.20, -0.385),
             (0.205, -0.33)], sx, sy, s, w=2.2)

    # ---------------- stove: cooktop, pan, steam, oven, towel
    S.poly(circle3(0.46, CT + 0.004, 2.82, 0.105), w=1.5, layer="faint")
    S.poly(circle3(0.90, CT + 0.004, 2.80, 0.125), w=1.5, layer="faint")
    S.poly(circle3(0.90, CT + 0.010, 2.80, 0.150), w=1.8)
    S.poly(circle3(0.90, CT + 0.052, 2.80, 0.157), w=2.0)
    S.poly([(1.055, CT + 0.050, 2.78), (1.30, CT + 0.058, 2.71)], w=1.9)
    sx, sy, s, zc = S.anchor((0.90, CT + 0.06, 2.80))
    for cx0, drift in ((-0.03, 0.05), (0.045, -0.04)):
        pts = [(cx0 + drift * np.sin(t * 3.1), -0.02 - 0.22 * t)
               for t in np.linspace(0, 1, 12)]
        S.glyph(pts, sx, sy, s, w=1.3, layer="faint")

    S.poly([(0.38, 0.76, CZ), (1.16, 0.76, CZ), (1.16, 0.30, CZ),
            (0.38, 0.30, CZ), (0.38, 0.76, CZ)], w=1.8)
    S.poly([(0.50, 0.665, CZ), (1.04, 0.665, CZ), (1.04, 0.44, CZ),
            (0.50, 0.44, CZ), (0.50, 0.665, CZ)], w=1.3, layer="faint")
    S.poly([(0.42, 0.795, CZ - 0.02), (1.12, 0.795, CZ - 0.02)], w=2.0)
    S.poly([(0.50, 0.795, CZ - 0.02), (0.50, 0.84, CZ)], w=1.5)
    S.poly([(1.04, 0.795, CZ - 0.02), (1.04, 0.84, CZ)], w=1.5)
    # the towel: hung over the bar in deliberate thirds — the same fold every
    # time, even mid-cook. The habit is in the manner, not the object.
    tz = CZ - 0.035
    tl, tr, ttop, tbot = 0.59, 0.89, 0.82, 0.44
    S.poly([(tl, ttop, tz), (tr, ttop, tz), (tr, tbot, tz),
            (tl, tbot + 0.02, tz), (tl, ttop, tz)], w=1.9)            # outline
    for tx in (tl + (tr - tl) / 3, tl + 2 * (tr - tl) / 3):           # two crease lines
        S.poly([(tx, ttop - 0.01, tz - 0.004), (tx + 0.004, tbot + 0.015, tz - 0.004)],
               w=1.5)
    S.poly([(tl + 0.012, ttop - 0.04, tz - 0.006),                    # the bar-fold lip
            (tr - 0.012, ttop - 0.04, tz - 0.006)], w=1.3)

    # ---------------- island
    A, B = (-0.05, CT, 0.62), (-0.05, CT, 1.12)
    S.poly([(-2.2, CT, 0.62), A], w=2.4)
    S.poly([(-2.2, CT - 0.035, 0.625), (-0.55, CT - 0.035, 0.62)], w=1.6)
    S.poly([A, B], w=2.4)
    S.poly([B, (-2.2, CT, 1.12)], w=2.2)
    S.poly([A, (-0.05, 0.40, 0.62)], w=2.2)
    S.poly([B, (-0.05, 0.28, 1.12)], w=2.2)

    # the board, mid-task (shifted left to make room at the corner)
    S.poly([(-0.62, CT + 0.008, 0.77), (-0.26, CT + 0.008, 0.74),
            (-0.22, CT + 0.008, 1.02), (-0.58, CT + 0.008, 1.05),
            (-0.62, CT + 0.008, 0.77)], w=2.0)
    sx, sy, s, zc = S.anchor((-0.38, CT + 0.012, 0.93))
    S.glyph(ell(0, 0, 0.046, 0.040, a0=np.pi, a1=2 * np.pi), sx, sy, s, w=1.8)
    S.glyph([(-0.046, 0), (0.046, 0)], sx, sy, s, w=1.6)
    S.glyph(ell(0, 0, 0.030, 0.026, a0=np.pi * 1.1, a1=np.pi * 1.9),
            sx, sy, s, w=1.2)
    S.glyph([(0.012, -0.040), (0.02, -0.062), (0.032, -0.055)], sx, sy, s, w=1.3)
    rng = np.random.default_rng(5)
    sx, sy, s, zc = S.anchor((-0.52, CT + 0.012, 0.88))
    for _ in range(11):
        px, py = rng.uniform(-0.05, 0.05), rng.uniform(-0.018, 0.012)
        a = rng.uniform(0, np.pi)
        d = 0.0065
        S.glyph([(px - d * np.cos(a), py - d * np.sin(a)),
                 (px + d * np.cos(a), py + d * np.sin(a))], sx, sy, s, w=1.4)
    k0, k1 = (-0.315, CT + 0.014, 0.81), (-0.235, CT + 0.014, 0.99)
    kv = np.array(k1) - np.array(k0)
    kn = np.array([-kv[2], 0, kv[0]])
    kn = kn / np.linalg.norm(kn) * 0.012
    S.poly([k0, k1, tuple(np.array(k1) * 0.2 + np.array(k0) * 0.8 + kn),
            tuple(np.array(k0) + kn * 0.6), k0], w=1.7)
    S.poly([k0, tuple(np.array(k0) - kv * 0.42)], w=2.6)

    # THE HABIT lives in the towel above — not a new object, but the manner of
    # one already here: it hangs in deliberate thirds even tossed. (See towel.)

    # ---------------- the stool, untouched: it carries the absence
    scx, scz, syaw = 0.12, 1.46, 0.62
    ca, sa = np.cos(syaw), np.sin(syaw)

    def L(x, z, y):
        return (scx + x * ca + z * sa, y, scz - x * sa + z * ca)

    S.poly([L(0.15 * np.cos(a), 0.15 * np.sin(a), 0.655)
            for a in np.linspace(0, 2 * np.pi, 36)], w=2.2)
    S.poly([L(0.15 * np.cos(a), 0.15 * np.sin(a), 0.625)
            for a in np.linspace(np.pi * 1.02, np.pi * 1.98, 18)], w=1.8)
    for a in (0.35, 1.25, 3.45, 4.35):
        lx, lz = 0.115 * np.cos(a), 0.115 * np.sin(a)
        S.poly([L(lx, lz, 0.625), L(lx * 1.75, lz * 1.75, 0.0)], w=2.0)
    S.poly([L(0.17 * np.cos(a), 0.17 * np.sin(a), 0.22)
            for a in np.linspace(np.pi * 1.02, np.pi * 1.98, 20)], w=1.7)

    # ---------------- the water bowl, filled to the rim
    mat = [(0.98, 0.004, 2.24), (1.40, 0.004, 2.24), (1.40, 0.004, 2.54),
           (0.98, 0.004, 2.54), (0.98, 0.004, 2.24)]
    S.poly(mat, w=1.8)
    bx = 1.19
    S.poly(circle3(bx, 0.078, 2.39, 0.082), w=1.8)
    S.poly(circle3(bx, 0.072, 2.39, 0.072), w=1.3)
    S.poly(circle3(bx, 0.008, 2.39, 0.062, a0=np.pi * 1.02,
                   a1=np.pi * 1.98), w=1.6)
    for sgn in (-1, 1):
        S.poly([(bx + sgn * 0.081, 0.072, 2.385),
                (bx + sgn * 0.062, 0.010, 2.385)], w=1.5)

    # ---------------- evening light
    S.poly([(0.55, 0, 1.95), (1.78, 0, 2.25), (1.50, 0, 2.92), (0.44, 0, 2.50),
            (0.55, 0, 1.95)], w=1.8, layer="faint")
    S.poly([(0.57, 0, 1.98), (1.77, 0, 2.27)], w=1.8, layer="faint")
    S.poly([(1.48, 0, 2.90), (0.46, 0, 2.49)], w=1.8, layer="faint")
    S.poly([(-0.30, CT + 0.003, 1.115), (-0.05, CT + 0.003, 1.00)],
           w=1.5, layer="faint")

    return S


if __name__ == "__main__":
    render(build("a"), W, H, "about-room-habit.png", seed=41)