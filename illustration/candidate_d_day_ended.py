"""
501-13 Candidate D — THE DAY ENDED. INSTRUMENT, NOT ASSET.

Why is the wall unfinished? Because daylight ran out. Work has a
daily shape, and this day's is over.

No figure. The tools are cleaned and lined at the baseboard, far
right — the pole leaning, the tray standing on edge against the wall,
the can closed (no wet clay anywhere; the care is in the cleanup).
A band of late light crosses the wall from a tall window off-frame
right — drawn in scene-B grammar: edges, not rays. Where the band
crosses the painted field, the clay lifts a shade (pigment in light);
on the bare wall the band exists only as its drawn edges.

Emotional thesis: the day ended before the work did, and the light
came back to look. Honest limits. Houston register: long light, late
dusk, sealed house.
"""
import os
import numpy as np
from PIL import Image
from about_figure import PAPER, INK, SAMPLES, render_strokes
from about_wall_ablations import build, with_text, _wavy, W, H, BASE_Y, FLOOR_Y
from about_scenes import s

# light band, leaning with the late sun: x at top, x at baseboard.
# It must land ON the work — across the settled field and the working
# edge — or the light has nothing to look at.
BAND_TOP = (760, 1290)
BAND_BASE = (470, 1000)


def band_lr(yy):
    t = yy / BASE_Y
    l = BAND_TOP[0] + (BAND_BASE[0] - BAND_TOP[0]) * t
    r = BAND_TOP[1] + (BAND_BASE[1] - BAND_TOP[1]) * t
    return l, r


def light_edges():
    S = []
    S.append(s([(BAND_TOP[0], 40), ((BAND_TOP[0] + BAND_BASE[0]) / 2, BASE_Y / 2),
                (BAND_BASE[0], BASE_Y - 6)], 0.7, lead=0.3, tail=0.3, swell=0.04))
    S.append(s([(BAND_TOP[1], 40), ((BAND_TOP[1] + BAND_BASE[1]) / 2, BASE_Y / 2),
                (BAND_BASE[1], BASE_Y - 6)], 0.7, lead=0.3, tail=0.3, swell=0.04))
    return S


def lined_tools():
    """Cleaned and lined at the baseboard, far right. Order = care.
    The pole lies flat along the floor — laid down, not leaned: the
    day is over, nothing is waiting to be picked back up tonight."""
    S = []
    # the pole, lying along the floor, roller at its left end
    S.append(s([(1512, 1136), (1690, 1139), (1862, 1137)], 1.5, swell=0.06,
               cs=True, ce=True))
    S.append(s([(1452, 1124), (1482, 1122), (1512, 1125)], 1.6, swell=0.1))  # roller, top
    S.append(s([(1450, 1142), (1480, 1140), (1510, 1143)], 1.6, swell=0.1))  # roller, bottom
    S.append(s([(1452, 1124), (1450, 1142)], 1.0, cs=True, ce=True))
    S.append(s([(1512, 1125), (1510, 1143)], 1.0, cs=True, ce=True))
    # the tray, washed, standing on edge against the wall
    S.append(s([(1740, 1042), (1742, 1146)], 1.4, swell=0.08, cs=True))
    S.append(s([(1798, 1040), (1799, 1144)], 1.4, swell=0.08, cs=True))
    S.append(s([(1740, 1042), (1770, 1038), (1798, 1040)], 1.3, swell=0.08))
    S.append(s([(1742, 1146), (1772, 1148), (1799, 1144)], 1.1, swell=0.06))
    # the can, closed — lid seam, no color showing
    S.append(s([(1836, 1090), (1839, 1146)], 1.5, swell=0.1))
    S.append(s([(1880, 1088), (1882, 1144)], 1.5, swell=0.1))
    S.append(s([(1836, 1090), (1858, 1084), (1880, 1088)], 1.2, swell=0.08))
    S.append(s([(1838, 1094), (1879, 1092)], 0.8, swell=0.05))             # lid seam
    S.append(s([(1841, 1147), (1877, 1145)], 1.0, swell=0.06))
    return S


if __name__ == "__main__":
    base = build(figure=False, action=False, roller=False, floor_ev=False)
    out = np.asarray(base, float)

    # the light lifting the painted field inside the band
    yy = np.arange(H, dtype=float)[:, None]
    xx = np.arange(W, dtype=float)[None, :]
    l, r = band_lr(yy)
    band = (xx >= l) & (xx < r) & (yy < BASE_Y)
    # lift anything pigmented toward the light (clay lightens; paper
    # barely moves — light is invisible on what is already light)
    lift = np.where(band, 0.16, 0.0)[..., None]
    out = out + (np.array([255, 251, 242]) - out) * lift

    ink = render_strokes(light_edges() + lined_tools(), W, H)
    out = out * (1 - ink[..., None]) + np.array([31, 29, 27]) * ink[..., None]

    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    img.save(os.path.join(SAMPLES, "candidate_d_day_ended_proof.png"))
    with_text(img.copy()).save(os.path.join(SAMPLES, "candidate_d_day_ended_page.png"))
    print("done")
