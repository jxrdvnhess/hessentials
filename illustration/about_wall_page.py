"""
ABOUT — the painted wall, composed FOR the page (2026-06-11).

Page contact. The portrait study survived as an image; this is the
landscape composition the essay actually lives in. Faculty framing:
the page examines coexistence, not the illustration — the question is
what the reader is looking at after thirty seconds.

Composition decisions, from the coexistence reference study:
  - Rooms being made are dense LOW and open HIGH. Evidence pools at
    the floor; the wall above stays calm. So: tray + can at his feet
    (the queue, the time dimension), nothing on the painted side
    where the essay sits.
  - The wall is cooperative, not quiet: the strip seams continue
    under the reading column but soften there (texture that defers,
    not texture that disappears).
  - The settled field (left ~45%) is the essay's living area. The
    working evidence — figure, pole, roller, current strip, lift
    mark — stays right, at body height.

Outputs:
  samples/about_wall_page_proof.png    — full landscape proof
  ../public/about/about-wall-wide.jpg  — desktop backdrop, q88
  (mobile keeps the portrait the-man-scene-d.png)
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from about_figure import figure_strokes, render_strokes, PAPER, INK, SAMPLES, WEB
from about_scenes import s, scaled

W, H = 1920, 1280
FLOOR_Y = 1150          # wall meets floor
BASE_Y = 1122           # baseboard top
K, DX, DY = 0.353, 1310, 619   # feet land exactly on FLOOR_Y

CLAY = np.array([216, 179, 160], float)
FIELD_ALPHA, ROLLER_ALPHA = 0.85, 1.0

# current strip / roller geometry. The current strip must CONTAIN the
# roller and read as solid fresh paint from the ceiling down to it, so the
# roller sits at the wet frontier (paint left and above, cream right and
# below) instead of floating in the unpainted field.
STRIP3_L, STRIP3_R = 1096, 1208
ROLLER_X0, ROLLER_X1 = 1106, 1198
ROLLER_Y0, ROLLER_Y1 = 362, 380


def ink_strokes():
    S = scaled(figure_strokes(0, left_arm="raised"), K, DX, DY)
    # pole — leaning from the strip he's working back to his grip
    S.append(s([(1152, 386), (1212, 527), (1272, 668), (1281, 700)], 1.5,
               swell=0.06, cs=True))
    # roller, mid-pull near the top of the current strip
    S.append(s([(1105, 366), (1152, 362), (1200, 365)], 1.7, swell=0.1))
    S.append(s([(1103, 382), (1150, 378), (1198, 381)], 1.7, swell=0.1))
    S.append(s([(1105, 366), (1103, 382)], 1.1, cs=True, ce=True))
    S.append(s([(1200, 365), (1198, 381)], 1.1, cs=True, ce=True))
    # the room — baseboard, then the floor line
    S.append(s([(40, BASE_Y + 4), (700, BASE_Y), (1340, BASE_Y + 3),
                (1880, BASE_Y)], 0.9, lead=0.1, tail=0.1, swell=0.04))
    S.append(s([(28, FLOOR_Y + 2), (660, FLOOR_Y - 2), (1300, FLOOR_Y + 1),
                (1892, FLOOR_Y - 2)], 1.4, lead=0.06, tail=0.06, swell=0.06))
    # floor evidence, right of him — the tray and the can: the queue,
    # past and future at floor level, where it doesn't compete
    S.append(s([(1390, 1128), (1440, 1125), (1490, 1126)], 1.5, swell=0.1))   # tray, top edge
    S.append(s([(1390, 1128), (1397, 1148)], 1.1, cs=True))                    # tray, left end
    S.append(s([(1490, 1126), (1484, 1146)], 1.1, cs=True))                    # tray, right end
    S.append(s([(1397, 1148), (1442, 1150), (1484, 1146)], 1.2, swell=0.08))   # tray, bottom
    S.append(s([(1520, 1090), (1523, 1146)], 1.5, swell=0.1))                  # can, left
    S.append(s([(1564, 1088), (1566, 1144)], 1.5, swell=0.1))                  # can, right
    S.append(s([(1520, 1090), (1542, 1084), (1564, 1088)], 1.2, swell=0.08))   # can, top
    S.append(s([(1522, 1098), (1563, 1096)], 0.8, swell=0.05))                 # can, rim
    S.append(s([(1525, 1147), (1561, 1145)], 1.0, swell=0.06))                 # can, bottom
    return S


def _wavy(yy, base, amp, period, phase):
    return base + amp * np.sin(2 * np.pi * yy / period + phase)


def paint_mask():
    yy = np.arange(H, dtype=float)[:, None]
    xx = np.arange(W, dtype=float)[None, :]
    below = yy >= BASE_Y
    m = np.zeros((H, W))

    # settled field — the essay's living area
    e0 = _wavy(yy, 870, 4, 320, 0.8)
    m = np.maximum(m, np.where((xx < e0) & ~below, FIELD_ALPHA, 0))

    # strip 1 — full height, one coat. Value kept close to the settled
    # field: a matte wall, not light-and-shadow folds.
    l1, r1 = _wavy(yy, 850, 4, 260, 2.1), _wavy(yy, 1000, 5, 290, 4.0)
    m = np.maximum(m, np.where((xx >= l1) & (xx < r1) & ~below, 0.82, 0))

    # strip 2 — bottom unfinished, tight rounded lift
    l2, r2 = _wavy(yy, 985, 4, 270, 1.2), _wavy(yy, 1120, 6, 300, 5.3)
    end2 = 950 + 55 * np.sin(np.pi * np.clip((xx - 985) / 135, 0, 1))
    in2 = (xx >= l2) & (xx < r2) & ~below
    a2 = np.where(yy < end2 - 24, 0.80,
                  np.where(yy < end2, 0.80 * (end2 - yy) / 24, 0.0))
    m = np.maximum(m, np.where(in2, a2, 0))

    # strip 3 — the CURRENT strip: solid fresh paint, ceiling down to the
    # bottom of the roller (the wet frontier he's just laid). Full field
    # weight so it reads as wall, not a faint tongue; spans past the roller
    # on both sides so the roller sits inside its own fresh strip.
    l3, r3 = _wavy(yy, STRIP3_L, 4, 250, 3.3), _wavy(yy, STRIP3_R, 5, 330, 0.4)
    m = np.maximum(m, np.where((xx >= l3) & (xx < r3) & (yy < ROLLER_Y1 + 2),
                               FIELD_ALPHA, 0))

    # pass seams — now a whisper: just enough to say two pulls met here,
    # never a fold crease. Thin and shallow.
    for sx, ph in ((240, 5.1), (440, 0.7), (640, 2.2), (855, 4.1), (992, 3.0)):
        c = _wavy(yy, sx, 2.5, 230, ph)
        depth = 0.022 if sx < 700 else 0.035
        band = np.abs(xx - c) < 5
        m = np.where(band & (m > 0.2) & ~below, np.minimum(m + depth, 0.97), m)

    # roller-pass texture — much quieter vertical streak; the field should
    # read matte, with only the faintest directional memory of the roller.
    rng = np.random.default_rng(19)
    streak = rng.normal(0, 1, W)
    k = np.ones(31) / 31
    for _ in range(3):
        streak = np.convolve(streak, k, mode="same")
    streak /= np.abs(streak).max() + 1e-9
    amp = np.where(np.arange(W) < 700, 0.016, 0.03)
    m *= 1 + amp[None, :] * streak[None, :]

    # low-frequency, NON-directional mottle — limewash applied by hand.
    # This is what replaces the curtain read: gentle 2-D unevenness that
    # carries no vertical grain, so the field says "painted", not "cloth".
    g = rng.normal(0, 1, (H, W))
    g = np.asarray(
        Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-9) * 255).astype(np.uint8))
        .filter(ImageFilter.GaussianBlur(26)), float) / 255.0
    g = (g - g.mean()) / (g.std() + 1e-9)
    m = m * (1 + 0.013 * np.clip(g, -2.2, 2.2))

    # the wet places — loaded roller, paint in the tray, open can
    m[ROLLER_Y0:ROLLER_Y1, ROLLER_X0:ROLLER_X1] = ROLLER_ALPHA
    m[1132:1146, 1402:1480] = ROLLER_ALPHA          # tray pool
    m[1086:1096, 1524:1562] = ROLLER_ALPHA          # open can, top
    return np.clip(m, 0, 1)


if __name__ == "__main__":
    ink = render_strokes(ink_strokes(), W, H)
    mask = paint_mask()
    out = np.ones((H, W, 3)) * PAPER
    out = out * (1 - mask[..., None]) + CLAY * mask[..., None]
    out = out * (1 - ink[..., None]) + INK * ink[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    img.save(os.path.join(SAMPLES, "about_wall_page_proof.png"))
    img.save(os.path.join(WEB, "about-wall-wide.jpg"), quality=88)
    print("done")
