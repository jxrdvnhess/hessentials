"""
501-P HUMAN MOMENTS — tranche 2. Life carrying emotion; no labels.

H1 — FLOWERS, BEFORE THE BELL: profile, at the door. One hand holds
     the flowers; the other is raised, finger extended toward the
     bell and NOT touching it. The emotion is the gap. (Viewpoint
     lesson applied: profile, so the hover can be seen.)

H2 — SITTING AFTER DIFFICULT WORK: the seated figure returns, bones
     first this time — pelvis on the seat plane, thigh cylinders,
     shin drops, THEN contour. Profile. Slumped forward, forearms on
     thighs, hands hanging between the knees, head dropped. The
     spent sit. No props; the body says it.
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


def h1_flowers_bell():
    S = []
    # ---- THE DOOR — frame, panel, the bell on the casing ----
    S.append(st([(640, 140), (643, 1280)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(810, 138), (812, 1280)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(636, 142), (724, 138), (814, 142)], 2.0, swell=0.08))
    S.append(st([(676, 220), (678, 760)], 1.1, swell=0.05))                 # panel line
    S.append(st([(770, 222), (772, 762)], 1.1, swell=0.05))
    S.append(st([(676, 222), (724, 218), (770, 222)], 1.1, swell=0.05))
    S.append(st([(788, 690), (798, 702)], 1.6, swell=0.1))                  # knob
    # the bell — small, on the casing, at the height bells live
    S.append(st([(620, 552), (636, 550), (638, 566), (622, 568), (620, 552)],
                1.3, swell=0.08))
    # ---- THE FIGURE — profile, facing the door ----
    # head: brow, nose, lips, chin — looking at the bell
    S.append(st([(404, 318), (390, 256), (408, 196), (458, 172), (506, 192),
                 (524, 244), (520, 282)], 2.3, swell=0.14))                 # skull
    S.append(st([(520, 282), (534, 300), (528, 312), (538, 330), (526, 344),
                 (510, 362), (480, 374)], 1.9, swell=0.12))                 # brow→nose→lips→chin
    S.append(st([(412, 208), (452, 186), (496, 204)], 1.4, swell=0.08))     # hairline
    S.append(st([(414, 268), (404, 290), (414, 312)], 1.2, swell=0.08))     # ear
    S.append(st([(508, 286), (520, 290)], 1.2, swell=0.08))                 # the eye, on the bell
    # neck, chest — a slight forward lean, weight on the toes
    S.append(st([(478, 376), (470, 416)], 1.5))
    S.append(st([(432, 350), (428, 400)], 1.5))
    S.append(st([(428, 400), (392, 448), (380, 520)], 2.2, swell=0.14))     # back of shoulder
    # raised arm — to the bell, finger extended, NOT touching
    S.append(st([(470, 418), (530, 450), (560, 492)], 2.2, swell=0.16))     # upper arm
    S.append(st([(560, 492), (588, 530), (600, 556)], 1.9, swell=0.14))     # forearm rising
    S.append(st([(600, 556), (612, 560)], 1.2, swell=0.08))                 # the finger
    S.append(st([(596, 566), (604, 574), (596, 582)], 1.1, swell=0.08))     # curled others
    # the back line down; the flower arm hangs
    S.append(st([(380, 520), (376, 640), (386, 760), (392, 830)], 2.3, swell=0.16))
    S.append(st([(440, 430), (442, 540), (448, 660), (452, 760), (450, 808)],
                2.0, swell=0.16))                                           # hanging arm, front line
    S.append(st([(450, 808), (446, 836), (462, 846), (474, 830)], 1.5, swell=0.1))
    # the flowers in the hanging hand — stems down-forward, three blooms up
    S.append(st([(462, 838), (492, 776), (516, 724)], 1.2, swell=0.08))     # stem
    S.append(st([(464, 842), (502, 790), (532, 748)], 1.1, swell=0.07))     # stem
    S.append(st([(514, 712), (506, 694), (522, 684), (534, 698), (526, 714)],
                1.3, swell=0.09))                                           # bloom
    S.append(st([(534, 740), (528, 722), (544, 714), (556, 728), (546, 744)],
                1.3, swell=0.09))
    S.append(st([(496, 738), (490, 722), (504, 714), (514, 726)], 1.2, swell=0.08))
    # trousers — profile; the lean shows in the line of the front leg
    S.append(st([(392, 832), (398, 1000), (412, 1180), (424, 1330)], 2.4, swell=0.18))
    S.append(st([(478, 840), (476, 1000), (470, 1180), (468, 1326)], 2.2, swell=0.16))
    S.append(st([(424, 1330), (418, 1372), (480, 1380), (492, 1352), (470, 1330)],
                1.7, swell=0.1))                                            # foot toward the door
    S.append(st([(430, 1356), (446, 1350)], 0.9, cs=True, ce=True))         # back heel, lifting
    # floor
    S.append(st([(70, 1392), (430, 1386), (840, 1390)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


def h2_after_work():
    S = []
    # ---- THE CHAIR — plain, profile; seat plane first (the bones) ----
    S.append(st([(338, 952), (450, 946), (562, 950)], 2.0, swell=0.1))      # seat plane
    S.append(st([(352, 954), (348, 1240)], 1.8, swell=0.08, cs=True))       # front leg
    S.append(st([(548, 952), (552, 1238)], 1.8, swell=0.08, cs=True))       # back leg
    S.append(st([(556, 948), (566, 800), (570, 690)], 1.8, swell=0.1))      # back post
    # ---- THE FIGURE — pelvis ON the seat, thighs forward, slumped ----
    # head, dropped — profile facing left, chin near the chest
    S.append(st([(330, 700), (318, 646), (340, 594), (392, 574), (438, 594),
                 (454, 644), (448, 686)], 2.3, swell=0.14))                 # skull
    S.append(st([(330, 700), (342, 716), (336, 726), (344, 742), (334, 754),
                 (322, 766)], 1.7, swell=0.12))                             # brow→nose→mouth, down
    S.append(st([(344, 606), (388, 588), (430, 604)], 1.4, swell=0.08))     # hairline
    S.append(st([(432, 668), (442, 690), (432, 710)], 1.2, swell=0.08))     # ear
    # nape into the slumped back — the long spent curve to the pelvis
    S.append(st([(448, 688), (504, 760), (536, 840), (544, 910)], 2.6, swell=0.18))
    # chest line under the dropped head
    S.append(st([(340, 762), (366, 810), (398, 850)], 1.8, swell=0.12))
    # pelvis sits; thigh runs forward; shin drops; heel under the knee
    S.append(st([(544, 912), (540, 948)], 1.8, swell=0.1))                  # seat contact
    S.append(st([(420, 856), (340, 868), (252, 878)], 2.4, swell=0.16))     # thigh, top line
    S.append(st([(252, 878), (240, 906), (244, 940)], 2.0, swell=0.12))     # knee
    S.append(st([(244, 940), (236, 1090), (232, 1238)], 2.2, swell=0.14))   # shin
    S.append(st([(296, 952), (290, 1090), (286, 1236)], 1.6, lead=0.2,
                swell=0.12))                                                # calf line
    S.append(st([(232, 1240), (182, 1248), (176, 1262), (288, 1262), (288, 1240)],
                1.7, swell=0.1))                                            # foot, flat, done
    # second leg behind, slightly back
    S.append(st([(430, 880), (372, 950), (346, 1090), (338, 1232)], 2.0,
                swell=0.14))
    S.append(st([(338, 1234), (300, 1244), (296, 1258), (380, 1258), (378, 1238)],
                1.5, swell=0.1))
    # arms — upper arm drops from the shoulder; forearm RESTS on the
    # thigh; the hand hangs off the knee, slack
    S.append(st([(444, 740), (452, 810), (444, 862)], 2.2, swell=0.16))     # upper arm
    S.append(st([(444, 862), (370, 872), (300, 876)], 2.0, swell=0.14))     # forearm on thigh
    S.append(st([(300, 876), (292, 912), (296, 938)], 1.5, swell=0.1))      # the hand, hanging
    S.append(st([(306, 914), (302, 936)], 0.9, swell=0.06))                 # one slack finger
    # shirt hem bunched at the seat
    S.append(st([(456, 900), (508, 906), (542, 898)], 1.2, swell=0.08))
    # floor
    S.append(st([(70, 1270), (430, 1264), (840, 1268)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


if __name__ == "__main__":
    for name, build in (("h1_flowers_bell", h1_flowers_bell),
                        ("h2_after_work", h2_after_work)):
        fa = render_strokes(build(), W, H)
        out = np.ones((H, W, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
            os.path.join(HERE, f"{name}.png"))
        print(name, "done")
