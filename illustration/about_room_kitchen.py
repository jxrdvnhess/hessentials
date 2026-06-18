"""
Hessentials — About page, Study 06: the room as conjunction.

One room, one sightline: the kitchen seen from the island, where a guest
leans. No hero object. Every element can disappear without collapsing the
image: the worn-narrow knife beside its wide sibling, two pans on a rail and
one on the cooktop, three broken-in cookbooks on a shelf left mostly bare,
the glass-front cabinet holding its full set, the dog's water station squared
to the counter's end inside the late light, a glass already poured at the
viewer's hand.

Evaluation: what does a stranger learn second?
"""
import numpy as np
from about_two_horizons import Cam, Scene, circle3, ell, render

W, H = 1500, 1900
WZ = 3.1          # back wall depth
CZ = 2.5          # counter front edge depth
CT = 0.92         # counter height


def sketch_room():
    cam = Cam(W, H, eye_level=0.42, f=1250, cam_h=1.45, vpx=0.46)
    S = Scene(cam, yaw=0.0, dx=0.0, dz=0.0)

    # ---------------- the counter run (full width)
    S.poly([(-1.9, CT, WZ), (2.6, CT, WZ)], w=1.8)           # wall junction
    S.poly([(-1.9, CT, CZ), (2.6, CT, CZ)], w=2.2)           # counter front edge
    S.poly([(-0.02, 0.10, CZ), (2.6, 0.10, CZ)], w=1.6)      # toe kick (island hides the rest)
    for vx in (0.52, 1.42):                                  # cabinet divisions
        S.poly([(vx, 0.88, CZ), (vx, 0.12, CZ)], w=1.4, layer="faint")

    # ---------------- window (closed; the light is its argument)
    x0, x1, y0, y1 = -0.95, 0.05, 1.18, 2.05
    for seg in ([(x0, y0), (x1, y0)], [(x1, y0), (x1, y1)],
                [(x1, y1), (x0, y1)], [(x0, y1), (x0, y0)],
                [(-0.45, y0), (-0.45, y1)]):                 # one mullion
        S.poly([(a, b, WZ) for a, b in seg], w=2.0)
    S.poly([(x0 - 0.06, y0 - 0.025, WZ - 0.04),
            (x1 + 0.06, y0 - 0.025, WZ - 0.04)], w=1.8)      # sill

    # herb pot on the sill
    sx, sy, s, zc = S.anchor((-0.16, y0 - 0.02, WZ - 0.05))
    S.glyph([(-0.045, 0), (-0.035, -0.085), (0.035, -0.085), (0.045, 0)],
            sx, sy, s, w=1.6)
    for dx, dy in ((-0.02, -0.10), (0.012, -0.115), (0.038, -0.095)):
        S.glyph([(0, -0.085), (dx, dy - 0.04), (dx * 1.6, dy - 0.07)],
                sx, sy, s, w=1.3)

    # faucet, in front of the window
    sx, sy, s, zc = S.anchor((-0.62, CT, WZ - 0.12))
    S.glyph([(0, 0), (0, -0.34), (0.025, -0.39), (0.12, -0.405), (0.20, -0.385),
             (0.205, -0.33)], sx, sy, s, w=2.2)

    # ---------------- open shelf, left — mostly bare
    S.poly([(-1.66, 1.62, WZ), (-1.02, 1.62, WZ)], w=2.0)
    for bx in (-1.58, -1.515, -1.455):                       # three upright spines
        S.poly([(bx, 1.62, WZ), (bx, 1.855, WZ)], w=1.9)
    S.poly([(-1.43, 1.62, WZ), (-1.325, 1.835, WZ)], w=1.9)  # one leaning
    S.poly([(-1.58, 1.855, WZ), (-1.455, 1.855, WZ)], w=1.6) # tops
    for r, ry in ((0.100, 1.665), (0.080, 1.698), (0.058, 1.725)):
        S.poly([(-1.17 - r, ry, WZ), (-1.17 - r * 0.6, 1.625, WZ),
                (-1.17 + r * 0.6, 1.625, WZ), (-1.17 + r, ry, WZ)],
               w=1.5)                                        # nested bowls

    # ---------------- knife rail: the wide one and the worn-narrow one
    S.poly([(-1.54, 1.345, WZ), (-1.12, 1.345, WZ)], w=1.9)
    sx, sy, s, zc = S.anchor((-1.42, 1.345, WZ))
    S.glyph([(0, -0.035), (0, 0)], sx, sy, s, w=1.7)                  # handle
    S.glyph([(-0.019, 0), (0.019, 0), (0.004, 0.205), (-0.013, 0.21),
             (-0.019, 0)], sx, sy, s, w=1.6)                          # wide blade
    sx, sy, s, zc = S.anchor((-1.25, 1.345, WZ))
    S.glyph([(0, -0.035), (0, 0)], sx, sy, s, w=1.7)
    S.glyph([(-0.010, 0), (0.010, 0), (0.002, 0.185), (-0.007, 0.19),
             (-0.010, 0)], sx, sy, s, w=1.6)                          # the narrow one

    # ---------------- cooktop + one resting pan
    S.poly(circle3(0.42, CT + 0.004, 2.82, 0.105), w=1.5, layer="faint")
    S.poly(circle3(0.88, CT + 0.004, 2.80, 0.125), w=1.5, layer="faint")
    S.poly(circle3(0.88, CT + 0.010, 2.80, 0.150), w=1.8)             # the pan
    S.poly(circle3(0.88, CT + 0.052, 2.80, 0.157), w=2.0)             # its rim
    S.poly([(1.035, CT + 0.050, 2.78), (1.28, CT + 0.058, 2.71)], w=1.9)

    # ---------------- glass-front cabinet, right (faint interior: the set)
    cx0, cx1, cy0, cy1 = 0.62, 1.62, 1.42, 2.12
    for seg in ([(cx0, cy0), (cx1, cy0)], [(cx1, cy0), (cx1, cy1)],
                [(cx1, cy1), (cx0, cy1)], [(cx0, cy1), (cx0, cy0)],
                [(1.12, cy0), (1.12, cy1)]):
        S.poly([(a, b, WZ) for a, b in seg], w=2.0)
    S.poly([(cx0, 1.76, WZ), (cx1, 1.76, WZ)], w=1.4, layer="faint")  # inner shelf
    for gx in (0.87, 1.37):                                           # pane verticals
        S.poly([(gx, cy0, WZ), (gx, cy1, WZ)], w=1.3, layer="faint")
    for row_y in (1.475, 1.815):                                      # the glasses
        for gx in np.linspace(0.72, 1.52, 6):
            sx, sy, s, zc = S.anchor((gx, row_y, WZ))
            S.glyph([(-0.028, -0.135), (-0.024, 0), (0.024, 0), (0.028, -0.135)],
                    sx, sy, s, w=1.2, layer="faint")

    # ---------------- pan rail under the cabinet: two hanging
    S.poly([(0.72, 1.31, WZ), (1.50, 1.31, WZ)], w=1.9)
    for px, pr in ((0.92, 0.13), (1.27, 0.105)):
        S.poly([(px + pr * np.cos(a), 1.10 + pr * np.sin(a), WZ)
                for a in np.linspace(0, 2 * np.pi, 40)], w=1.9)
        S.poly([(px, 1.10 + pr, WZ), (px, 1.31, WZ)], w=1.6)

    # ---------------- board + salt box on the counter, right of the window
    S.poly([(0.07, CT, 2.96), (0.28, CT, 3.0), (0.31, 1.26, WZ),
            (0.10, 1.26, WZ), (0.07, CT, 2.96)], w=1.9)
    S.poly([(0.38, CT, 2.88), (0.52, CT, 2.88), (0.52, 1.035, 2.92),
            (0.38, 1.035, 2.92), (0.38, CT, 2.88)], w=1.6)

    # ---------------- the island (the viewer leans here)
    A, B = (-0.05, CT, 0.62), (-0.05, CT, 1.12)
    S.poly([(-2.2, CT, 0.62), A], w=2.4)                     # near edge
    S.poly([(-2.2, CT - 0.035, 0.625), (-0.55, CT - 0.035, 0.62)], w=1.6)
    S.poly([A, B], w=2.4)                                    # right end, top
    S.poly([B, (-2.2, CT, 1.12)], w=2.2)                     # far edge
    S.poly([A, (-0.05, 0.40, 0.62)], w=2.2)                  # right end, face
    S.poly([B, (-0.05, 0.28, 1.12)], w=2.2)

    # the glass already poured, at the viewer's hand
    sx, sy, s, zc = S.anchor((-0.30, CT, 0.80))
    sq = S.squash(CT + 0.105, zc)
    S.glyph([(-0.036, 0), (-0.033, -0.105)], sx, sy, s, w=1.8)
    S.glyph([(0.036, 0), (0.033, -0.105)], sx, sy, s, w=1.8)
    S.glyph(ell(0, -0.105, 0.033, 0.033 * sq), sx, sy, s, w=1.6)
    S.glyph(ell(0, 0, 0.036, 0.036 * sq * 0.8, a0=0.15, a1=np.pi - 0.15),
            sx, sy, s, w=1.5)

    # citrus bowl, island left, cropped by the frame at body distance
    S.poly(circle3(-0.58, CT + 0.065, 0.98, 0.155), w=2.0)            # rim
    sx, sy, s, zc = S.anchor((-0.58, CT, 0.98))
    S.glyph([(-0.145, -0.062), (-0.10, -0.012), (0.10, -0.012), (0.145, -0.062)],
            sx, sy, s, w=1.8)                                          # belly
    for fx, fz, fr in ((-0.64, 0.95, 0.052), (-0.535, 0.96, 0.05),
                       (-0.585, 1.02, 0.048)):
        S.poly(circle3(fx, CT + 0.085, fz, fr), w=1.5)                 # fruit

    # ---------------- the dog's station, in the light past the island's end
    mat = [(0.80, 0.004, 2.24), (1.24, 0.004, 2.24), (1.24, 0.004, 2.54),
           (0.80, 0.004, 2.54), (0.80, 0.004, 2.24)]
    S.poly(mat, w=1.8)
    for bx in (0.94, 1.13):
        S.poly(circle3(bx, 0.078, 2.39, 0.082), w=1.8)                 # rims
        S.poly(circle3(bx, 0.008, 2.39, 0.062, a0=np.pi * 1.02,
                       a1=np.pi * 1.98), w=1.6)                        # bases
        for sgn in (-1, 1):                                            # side walls
            S.poly([(bx + sgn * 0.081, 0.072, 2.385),
                    (bx + sgn * 0.062, 0.010, 2.385)], w=1.5)

    # ---------------- late light on the floor, reaching the station
    S.poly([(0.55, 0, 1.95), (1.70, 0, 2.25), (1.42, 0, 2.92), (0.44, 0, 2.50),
            (0.55, 0, 1.95)], w=1.8, layer="faint")
    # double-stroke the long edges so the light holds at page scale
    S.poly([(0.57, 0, 1.98), (1.69, 0, 2.27)], w=1.8, layer="faint")
    S.poly([(1.40, 0, 2.90), (0.46, 0, 2.49)], w=1.8, layer="faint")

    render(S, W, H, "about-room-kitchen.png", seed=31)


if __name__ == "__main__":
    sketch_room()
