"""
ABOUT — three environments for the still figure. Jordan's art direction,
2026-06-10: the environment reveals choices, not preferences. Evidence,
not possessions. Enough environment to establish a question; never
enough to establish a story.

  A — THE SHELF      a wall shelf, three objects, one gap where a
                     fourth was. A faint dust ring is the evidence.
  B — THE WINDOW     a window, light falling across the wall. Nothing
                     else. The least symbolic.
  C — THE COMPARISON a narrow console, two nearly identical vessels,
                     one slightly forward. No indication which is
                     correct. The viewer starts discerning.

Same figure in all three (about_figure.figure_strokes). Economical
line. No objects of taste, no visual resume.

Outputs per scene X in {a, b, c}:
  samples/about_scene_X_paper.png   — proof on plaster cream
  ../public/about/the-man-scene-X.png — RGBA transparent for web
"""
import os
import numpy as np
from about_figure import (figure_strokes, render_strokes, save_paper,
                          save_web, SAMPLES, WEB)

W, H = 1040, 1560
FCX = 680   # the figure stands right of center; the question hangs to his left


def s(ctrl, w, lead=0.14, tail=0.2, swell=0.18, sm=0.6, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


# ---------------------------------------------------------------- A — SHELF
def scene_a():
    S = figure_strokes(FCX)
    # the shelf — one board on the wall, just above his shoulder line
    S.append(s([(96, 332), (270, 327), (446, 330)], 2.2, swell=0.1))      # board, front edge
    S.append(s([(102, 344), (272, 339), (440, 342)], 1.2, swell=0.08))    # board, thickness
    S.append(s([(132, 344), (134, 372)], 1.0, cs=True))                   # bracket
    S.append(s([(404, 344), (406, 372)], 1.0, cs=True))                   # bracket
    # three objects, plain silhouettes — a bowl, a vase, a small box
    S.append(s([(136, 326), (146, 302), (172, 294), (198, 300),
                (208, 326)], 1.8, swell=0.12))                            # bowl
    S.append(s([(238, 326), (234, 286), (244, 252), (242, 226)], 1.8,
               swell=0.14))                                               # vase, left profile
    S.append(s([(278, 326), (282, 288), (272, 252), (274, 226)], 1.8,
               swell=0.14))                                               # vase, right profile
    S.append(s([(242, 224), (258, 220), (274, 224)], 1.2, swell=0.08))    # vase mouth
    S.append(s([(310, 326), (312, 282), (352, 280), (354, 326)], 1.6,
               swell=0.1))                                                # small box
    # the gap — where the fourth thing stood. In flat elevation any mark
    # on the board reads as another object, so the gap carries it alone:
    # three things close together, then bare board where the fourth was.
    return S


# --------------------------------------------------------------- B — WINDOW
def scene_b():
    S = figure_strokes(FCX)
    # the window — frame, one mullion, sill. Tall, plain.
    S.append(s([(120, 200), (122, 880)], 2.2, swell=0.08, cs=True, ce=True))   # left jamb
    S.append(s([(330, 204), (331, 876)], 2.2, swell=0.08, cs=True, ce=True))   # right jamb
    S.append(s([(120, 202), (228, 198), (330, 204)], 2.2, swell=0.08))         # head
    S.append(s([(104, 884), (226, 880), (348, 884)], 2.4, swell=0.1))          # sill
    S.append(s([(112, 898), (340, 897)], 1.2, swell=0.06))                     # sill underside
    S.append(s([(226, 206), (227, 878)], 1.4, swell=0.06))                     # mullion
    S.append(s([(124, 540), (328, 542)], 1.4, swell=0.06))                     # transom
    # the light — not rays, edges. The thrown patch of late sun on the
    # floor: two faint boundaries leaving the window's base, and a far
    # edge. It reaches toward him and stops short.
    S.append(s([(126, 906), (260, 1180), (420, 1452)], 0.7, swell=0.04,
               lead=0.3, tail=0.32))
    S.append(s([(342, 902), (480, 1130), (640, 1372)], 0.7, swell=0.04,
               lead=0.3, tail=0.32))
    S.append(s([(414, 1448), (530, 1414), (632, 1376)], 0.6, swell=0.03,
               lead=0.34, tail=0.36))
    return S


# ----------------------------------------------------------- C — COMPARISON
def scene_c():
    S = figure_strokes(FCX)
    # the console — narrow, plain: top, apron, two legs
    S.append(s([(130, 906), (290, 901), (452, 905)], 2.2, swell=0.1))     # top, front edge
    S.append(s([(136, 920), (290, 915), (446, 919)], 1.2, swell=0.08))    # apron line
    S.append(s([(190, 920), (193, 1190), (194, 1452)], 1.9, swell=0.1))   # left leg
    S.append(s([(410, 919), (413, 1190), (414, 1450)], 1.9, swell=0.1))   # right leg
    # two nearly identical vessels, overlapping: the left sits back, the
    # right has been brought forward — lower on the page, a shade larger,
    # its shoulder crossing in front of the other. Nothing says which
    # placement is right.
    # back vessel — its right profile stops where the forward one occludes it
    S.append(s([(240, 898), (234, 858), (244, 826), (242, 802)], 1.7, swell=0.12))
    S.append(s([(282, 802), (288, 822), (291, 844)], 1.5, swell=0.1))
    S.append(s([(242, 800), (262, 796), (282, 800)], 1.1, swell=0.08))    # mouth
    # forward vessel
    S.append(s([(296, 908), (288, 866), (300, 830), (298, 804)], 1.8, swell=0.12))
    S.append(s([(340, 908), (347, 868), (336, 830), (338, 804)], 1.8, swell=0.12))
    S.append(s([(298, 802), (318, 798), (338, 802)], 1.2, swell=0.08))    # mouth
    return S


# ------------------------------------------------------------ D — THE PAINTER
def scene_d():
    """Jordan's direction, 2026-06-11: the man mid-paint. The painted
    side of the wall is the text's living area — the cream wash the
    page already uses to lift the essay becomes diegetic. He is the
    reason the words have somewhere to sit.

    Evidence kept minimal: the raised arm, the roller at the wet edge,
    the edge itself running the height of the wall. No tray, no drips,
    no drop cloth — enough to establish the act, never the story."""
    S = figure_strokes(FCX, left_arm="raised")
    # the roller — frame from the fist, then a full-width cylinder
    # against the wall (a 9-inch roller is near half his shoulder span)
    S.append(s([(394, 180), (380, 158)], 1.4, cs=True))                   # frame/handle
    S.append(s([(316, 138), (372, 132), (428, 136)], 2.0, swell=0.1))     # cylinder, top
    S.append(s([(314, 158), (370, 152), (426, 156)], 2.0, swell=0.1))     # cylinder, bottom
    S.append(s([(316, 138), (314, 158)], 1.3, cs=True, ce=True))          # end cap
    S.append(s([(428, 136), (426, 156)], 1.3, cs=True, ce=True))          # end cap
    # the wet edge — the boundary of what he has painted, full height,
    # alive, slightly wandering. Everything left of it is done; the
    # essay lives there.
    S.append(s([(374, 60), (377, 280), (371, 560), (376, 840),
                (372, 1080), (374, 1230)], 1.3, lead=0.04, tail=0.3,
               swell=0.06, cs=True))
    # one recent pass, not yet cut in — fades both ends
    S.append(s([(350, 184), (354, 446)], 0.6, lead=0.3, tail=0.35,
               swell=0.03))
    return S


if __name__ == "__main__":
    for name, build in (("a", scene_a), ("b", scene_b), ("c", scene_c),
                        ("d", scene_d)):
        fa = render_strokes(build(), W, H)
        save_paper(fa, os.path.join(SAMPLES, f"about_scene_{name}_paper.png"))
        save_web(fa, os.path.join(WEB, f"the-man-scene-{name}.png"))
        print(name, "done")
