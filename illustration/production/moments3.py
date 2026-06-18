"""
501-P HUMAN MOMENTS — tranche 3. Moments, not actions.

H3 — DECIDING NOT TO KNOCK: the sequel the moment invited. Same
     door, same man, same flowers — but the body has already turned
     away while the head still hasn't. The feet point left; the face
     lingers toward the door; the flowers have dropped from "held"
     to "carried," low against the leg. The bell is untouched. The
     gap won. (Symbol watch: the flowers earn their new meaning by
     their changed posture — from offering to baggage.)

H4 — NOTICING THE ROOM IS EMPTY: a figure stopped in the doorway,
     one hand still on the jamb — the stop drawn as contact. Beyond:
     one chair against the far wall and nothing else. The subject is
     the space; the negative space must be active (401's lesson
     cashed). Back view, small in the frame; the room large.
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


def door(S, x0=640):
    S.append(st([(x0, 140), (x0 + 3, 1280)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(x0 + 170, 138), (x0 + 172, 1280)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(x0 - 4, 142), (x0 + 84, 138), (x0 + 174, 142)], 2.0, swell=0.08))
    S.append(st([(x0 + 36, 220), (x0 + 38, 760)], 1.1, swell=0.05))
    S.append(st([(x0 + 130, 222), (x0 + 132, 762)], 1.1, swell=0.05))
    S.append(st([(x0 + 36, 222), (x0 + 84, 218), (x0 + 130, 222)], 1.1, swell=0.05))
    S.append(st([(x0 + 148, 690), (x0 + 158, 702)], 1.6, swell=0.1))
    # the bell, untouched
    S.append(st([(x0 - 20, 552), (x0 - 4, 550), (x0 - 2, 566), (x0 - 18, 568),
                 (x0 - 20, 552)], 1.3, swell=0.08))


def h3_not_knocking():
    S = []
    door(S)
    # ---- THE MAN — body turned away (facing left), head lingering
    # back toward the door: a sliver of profile past the shoulder ----
    # skull from this side — back of head toward us now
    S.append(st([(386, 318), (372, 252), (392, 192), (444, 170), (494, 192),
                 (510, 248), (504, 300)], 2.3, swell=0.14))
    S.append(st([(398, 204), (444, 184), (488, 206)], 1.4, swell=0.08))
    # the lingering face — brow and nose just past the right shoulder line
    S.append(st([(504, 300), (516, 314), (510, 326), (518, 342), (506, 354)],
                1.7, swell=0.12))                                           # brow→nose→lip, back
    S.append(st([(398, 270), (388, 292), (398, 314)], 1.2, swell=0.08))     # ear, now left
    # neck; shoulders rotating away — left shoulder leads
    S.append(st([(414, 330), (408, 372)], 1.5))
    S.append(st([(470, 344), (468, 380)], 1.5))
    S.append(st([(408, 372), (348, 404), (310, 442)], 2.3, swell=0.16))     # leading shoulder
    S.append(st([(468, 380), (520, 406), (548, 440)], 2.2, swell=0.14))     # trailing shoulder
    # the bell arm, dropped — hangs on the door side, empty hand
    S.append(st([(548, 440), (560, 560), (556, 690), (548, 776)], 2.1, swell=0.16))
    S.append(st([(548, 778), (542, 806), (558, 816), (570, 800)], 1.5, swell=0.1))
    # torso, leaving
    S.append(st([(310, 442), (296, 560), (300, 700), (308, 800)], 2.3, swell=0.16))
    S.append(st([(498, 452), (492, 580), (486, 700), (482, 790)], 1.8, swell=0.12))
    # the flower arm — far side, low; blooms now pointing DOWN the leg
    S.append(st([(330, 460), (322, 580), (326, 700), (332, 788)], 2.0, swell=0.16))
    S.append(st([(332, 788), (326, 818), (342, 828), (354, 812)], 1.5, swell=0.1))
    S.append(st([(344, 822), (352, 900), (356, 960)], 1.2, swell=0.08))     # stems, down
    S.append(st([(348, 824), (362, 902), (370, 952)], 1.1, swell=0.07))
    S.append(st([(348, 968), (340, 986), (356, 996), (368, 982), (362, 964)],
                1.3, swell=0.09))                                           # bloom, hanging
    S.append(st([(364, 956), (358, 974), (372, 982), (382, 968)], 1.2, swell=0.08))
    # legs — first step taken, away
    S.append(st([(308, 802), (296, 1000), (272, 1190), (256, 1330)], 2.4, swell=0.18))
    S.append(st([(394, 806), (398, 1010), (408, 1200), (412, 1342)], 2.2, swell=0.16))
    S.append(st([(482, 792), (470, 980), (452, 1160), (446, 1300)], 2.0, swell=0.14))
    S.append(st([(256, 1330), (224, 1352), (282, 1362), (292, 1336)], 1.7, swell=0.1))
    S.append(st([(412, 1342), (396, 1368), (452, 1374), (460, 1348)], 1.6, swell=0.1))
    S.append(st([(446, 1300), (452, 1318)], 0.9, cs=True, ce=True))         # trailing heel, up
    # floor
    S.append(st([(70, 1386), (430, 1380), (840, 1384)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


def h4_empty_room():
    S = []
    # ---- THE DOORWAY, left — the figure stopped in it ----
    S.append(st([(150, 130), (153, 1270)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(348, 128), (350, 1270)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(146, 132), (248, 128), (354, 132)], 2.0, swell=0.08))
    # ---- THE FIGURE — back view, in the frame, stopped ----
    S.append(st([(212, 388), (206, 338), (224, 294), (262, 280), (298, 296),
                 (312, 340), (306, 386)], 2.2, swell=0.14))                 # head
    S.append(st([(218, 372), (262, 382), (302, 370)], 1.6, swell=0.09))     # nape
    S.append(st([(230, 300), (236, 336)], 0.8, swell=0.06))
    S.append(st([(236, 392), (234, 424)], 1.4))
    S.append(st([(284, 394), (288, 426)], 1.4))
    # the stopping hand — ON the jamb, mid-height
    S.append(st([(288, 426), (330, 452), (348, 490)], 2.0, swell=0.14))     # arm to the jamb
    S.append(st([(348, 490), (352, 516), (344, 530)], 1.5, swell=0.1))      # the hand, holding
    S.append(st([(234, 424), (192, 452), (176, 484)], 2.0, swell=0.14))     # other shoulder
    S.append(st([(176, 484), (170, 580), (174, 680), (180, 752)], 1.9, swell=0.14))
    S.append(st([(180, 754), (174, 780), (190, 790), (200, 774)], 1.4, swell=0.1))
    # torso and legs — weight stopped mid-stride, front foot inside
    S.append(st([(196, 470), (192, 580), (200, 690), (206, 760)], 2.0, swell=0.14))
    S.append(st([(310, 480), (314, 590), (308, 700), (304, 762)], 2.0, swell=0.14))
    S.append(st([(206, 764), (256, 772), (304, 762)], 1.4, swell=0.09))
    S.append(st([(208, 766), (214, 940), (224, 1110), (230, 1232)], 2.2, swell=0.16))
    S.append(st([(300, 764), (296, 930), (288, 1100), (284, 1218)], 2.2, swell=0.16))
    S.append(st([(254, 780), (256, 1000), (256, 1224)], 1.7, lead=0.2, swell=0.14))
    S.append(st([(230, 1234), (214, 1258), (268, 1264), (274, 1238)], 1.6, swell=0.1))
    S.append(st([(284, 1220), (296, 1244), (338, 1240), (330, 1216)], 1.6, swell=0.1))
    # ---- THE ROOM — large, and almost nothing in it ----
    S.append(st([(352, 1146), (600, 1136), (862, 1142)], 1.5, swell=0.07))  # far floor line
    S.append(st([(354, 1268), (610, 1258), (866, 1264)], 1.4, lead=0.06,
                tail=0.06, swell=0.06))                                     # near floor line
    # one chair against the far wall — nobody in it
    S.append(st([(700, 980), (702, 1130)], 1.7, swell=0.08, cs=True))
    S.append(st([(764, 978), (766, 1128)], 1.7, swell=0.08, cs=True))
    S.append(st([(696, 1038), (734, 1034), (770, 1038)], 1.7, swell=0.09))  # seat
    S.append(st([(700, 982), (734, 978), (764, 982)], 1.3, swell=0.07))     # back rail
    S.append(st([(704, 1130), (702, 1144)], 1.2, cs=True))
    S.append(st([(762, 1128), (764, 1142)], 1.2, cs=True))
    # the wall's only mark — a nail where something hung
    S.append(st([(728, 640), (732, 644)], 1.6, cs=True, ce=True))
    return S


if __name__ == "__main__":
    for name, build in (("h3_not_knocking", h3_not_knocking),
                        ("h4_empty_room", h4_empty_room)):
        fa = render_strokes(build(), W, H)
        out = np.ones((H, W, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
            os.path.join(HERE, f"{name}.png"))
        print(name, "done")
