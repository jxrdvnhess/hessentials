"""
501-P BATCH 2 — someone carrying groceries. Two entrants, one scene.

New production doctrine applied: begin with a scene, draw first,
judge second, extract third. Toolbox used: 101 for the load-bearing
anatomy (a carried weight redraws the whole body), croquis
observation for how the body actually compensates.

P3 — SYMMETRIC: a bag in each hand, even stance. The polite version.
P4 — ASYMMETRIC: one heavy bag hanging from the right hand (shoulder
     dropped, spine leaning away to counterweight), one bag cradled
     against the chest in the left arm, greens standing out of it.
     Mid-step, back foot heel just off the ground.

Prediction to be tested by the verdict: asymmetry wins, because life
is asymmetric and a body under load is a drawing of physics.
"""
import os
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from about_figure import render_strokes, PAPER, INK

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 900, 1500


def st(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


def head(S, cx, hy=130, lean=0):
    """Canonical head, optionally shifted by the body's lean."""
    c = cx + lean
    S.append(st([(c - 64, hy + 70), (c - 72, hy + 12), (c - 48, hy - 50),
                 (c + 4, hy - 70), (c + 54, hy - 52), (c + 74, hy + 14),
                 (c + 65, hy + 68)], 2.4, swell=0.18))
    S.append(st([(c - 52, hy + 54), (c - 20, hy + 62), (c + 16, hy + 62),
                 (c + 54, hy + 52)], 1.9, swell=0.1))
    S.append(st([(c - 22, hy - 42), (c - 30, hy - 2), (c - 32, hy + 38)],
                0.9, swell=0.08))
    S.append(st([(c + 16, hy - 46), (c + 22, hy - 4), (c + 20, hy + 36)],
                0.9, swell=0.08))


def paper_bag(S, x, y, w_, h_, tilt=0):
    """A paper grocery bag, slightly out of square — carried, not drawn."""
    S.append(st([(x, y), (x + w_ * .5 + tilt, y - 4), (x + w_, y)], 1.7, swell=0.1))
    S.append(st([(x, y), (x - 4 + tilt * .4, y + h_ * .55), (x + 2, y + h_)],
                1.8, swell=0.12))
    S.append(st([(x + w_, y), (x + w_ + 5 + tilt * .4, y + h_ * .5),
                 (x + w_ - 2, y + h_)], 1.8, swell=0.12))
    S.append(st([(x + 2, y + h_), (x + w_ * .5, y + h_ + 4), (x + w_ - 2, y + h_)],
                1.6, swell=0.1))
    S.append(st([(x + w_ * .3, y + 6), (x + w_ * .32, y + h_ * .4)], 0.7,
                lead=0.3, tail=0.34, swell=0.04))                       # one crease


def p3_symmetric():
    S = []
    cx = 430
    head(S, cx)
    S.append(st([(cx - 26, 202), (cx - 29, 246)], 1.8))
    S.append(st([(cx + 27, 202), (cx + 31, 248)], 1.8))
    S.append(st([(cx - 29, 246), (cx - 96, 282), (cx - 152, 308)], 2.6, swell=0.16))
    S.append(st([(cx + 31, 248), (cx + 98, 284), (cx + 154, 310)], 2.6, swell=0.16))
    # both arms straight down to the bags, evenly loaded
    S.append(st([(cx - 152, 308), (cx - 168, 460), (cx - 170, 620), (cx - 166, 740)],
                2.4, swell=0.18))
    S.append(st([(cx + 154, 310), (cx + 170, 462), (cx + 172, 622), (cx + 168, 742)],
                2.4, swell=0.18))
    S.append(st([(cx - 124, 372), (cx - 140, 520), (cx - 146, 680)], 1.6,
                lead=0.22, swell=0.12))
    S.append(st([(cx + 126, 374), (cx + 142, 522), (cx + 148, 682)], 1.6,
                lead=0.22, swell=0.12))
    # torso, even; hem level
    S.append(st([(cx - 118, 380), (cx - 102, 520), (cx - 108, 700), (cx - 104, 758)],
                2.2, swell=0.16))
    S.append(st([(cx + 120, 382), (cx + 104, 522), (cx + 110, 702), (cx + 106, 758)],
                2.2, swell=0.16))
    S.append(st([(cx - 104, 760), (cx + 2, 766), (cx + 106, 760)], 1.5, swell=0.1))
    # even legs
    S.append(st([(cx - 104, 762), (cx - 96, 1010), (cx - 86, 1260), (cx - 82, 1416)],
                2.4, swell=0.18))
    S.append(st([(cx + 106, 762), (cx + 98, 1012), (cx + 88, 1262), (cx + 84, 1418)],
                2.4, swell=0.18))
    S.append(st([(cx + 2, 778), (cx + 6, 1080), (cx + 8, 1414)], 1.9,
                lead=0.2, swell=0.16))
    S.append(st([(cx - 82, 1416), (cx - 104, 1442), (cx - 50, 1450), (cx - 44, 1422)],
                1.7, swell=0.1))
    S.append(st([(cx + 84, 1418), (cx + 106, 1444), (cx + 52, 1452), (cx + 46, 1424)],
                1.7, swell=0.1))
    # the two bags, hung level
    paper_bag(S, cx - 238, 742, 140, 180)
    paper_bag(S, cx + 100, 744, 140, 180)
    # floor
    S.append(st([(60, 1462), (420, 1456), (840, 1460)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


def p4_asymmetric():
    S = []
    cx = 430
    LEAN = -26          # spine leans LEFT, away from the heavy right bag
    head(S, cx, lean=LEAN)
    S.append(st([(cx - 26 + LEAN, 202), (cx - 28 + LEAN * .7, 246)], 1.8))
    S.append(st([(cx + 27 + LEAN, 202), (cx + 30 + LEAN * .7, 248)], 1.8))
    # shoulders: right dropped hard by the load, left riding up
    S.append(st([(cx - 28 + LEAN * .7, 246), (cx - 96 + LEAN * .6, 274),
                 (cx - 150 + LEAN * .5, 296)], 2.6, swell=0.16))
    S.append(st([(cx + 30 + LEAN * .7, 248), (cx + 96 + LEAN * .4, 296),
                 (cx + 150 + LEAN * .3, 330)], 2.6, swell=0.16))
    # right arm: straight, elongated by the weight, to the hanging bag
    S.append(st([(cx + 150 + LEAN * .3, 330), (cx + 166, 480), (cx + 172, 640),
                 (cx + 170, 768)], 2.4, swell=0.18))
    S.append(st([(cx + 124, 392), (cx + 144, 540), (cx + 152, 700),
                 (cx + 154, 756)], 1.6, lead=0.22, swell=0.12))
    # left arm: forearm horizontal, cradling the second bag to the chest
    S.append(st([(cx - 150 + LEAN * .5, 296), (cx - 176 + LEAN * .4, 380),
                 (cx - 160 + LEAN * .4, 450)], 2.3, swell=0.18))          # upper
    S.append(st([(cx - 160 + LEAN * .4, 450), (cx - 92 + LEAN * .4, 472),
                 (cx - 20 + LEAN * .4, 470)], 2.1, swell=0.16))           # forearm across
    # torso: load side stretched, free side compressed
    S.append(st([(cx - 116 + LEAN * .6, 372), (cx - 100 + LEAN * .8, 520),
                 (cx - 102 + LEAN, 700), (cx - 98 + LEAN, 756)], 2.2, swell=0.16))
    S.append(st([(cx + 122 + LEAN * .4, 386), (cx + 110 + LEAN * .2, 540),
                 (cx + 112, 706), (cx + 108, 760)], 2.2, swell=0.16))
    # hem tips with the carry
    S.append(st([(cx - 98 + LEAN, 762), (cx + 4 + LEAN * .4, 772), (cx + 108, 756)],
                1.5, swell=0.1))
    # legs: mid-step — left forward planted, right heel just lifting
    S.append(st([(cx - 98 + LEAN, 764), (cx - 110 + LEAN * .5, 1000),
                 (cx - 124, 1250), (cx - 128, 1408)], 2.4, swell=0.18))
    S.append(st([(cx + 108, 762), (cx + 96, 1010), (cx + 66, 1260), (cx + 50, 1394)],
                2.4, swell=0.18))
    S.append(st([(cx + 4 + LEAN * .4, 780), (cx - 10, 1080), (cx - 22, 1404)],
                1.9, lead=0.2, swell=0.16))
    # forward foot flat; back heel off the ground, toe down
    S.append(st([(cx - 128, 1408), (cx - 152, 1434), (cx - 96, 1442), (cx - 90, 1414)],
                1.7, swell=0.1))
    S.append(st([(cx + 50, 1394), (cx + 40, 1428), (cx + 88, 1446), (cx + 92, 1420)],
                1.7, swell=0.1))
    # the hanging bag — heavy, pulling the right arm taut
    paper_bag(S, cx + 102, 770, 142, 184, tilt=4)
    # the cradled bag — against the chest, above the forearm
    paper_bag(S, cx - 134 + LEAN * .4, 330, 124, 142, tilt=-3)
    # greens standing out of the cradled bag — two made strokes, no scribble
    S.append(st([(cx - 92 + LEAN * .4, 332), (cx - 84 + LEAN * .4, 286),
                 (cx - 70 + LEAN * .4, 252)], 1.1, swell=0.1))
    S.append(st([(cx - 76 + LEAN * .4, 330), (cx - 62 + LEAN * .4, 290),
                 (cx - 60 + LEAN * .4, 262)], 1.0, swell=0.08))
    # floor
    S.append(st([(60, 1462), (420, 1456), (840, 1460)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


if __name__ == "__main__":
    for name, build in (("p3_groceries_symmetric", p3_symmetric),
                        ("p4_groceries_asymmetric", p4_asymmetric)):
        fa = render_strokes(build(), W, H)
        out = np.ones((H, W, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
            os.path.join(HERE, f"{name}.png"))
        print(name, "done")
