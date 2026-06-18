"""
501-P EMOTIONAL MOMENTS — tranche 1. One figure, minimal environment,
emotion carried by face + posture + situation together.

The two emotions that LOST as isolated faces return here with bodies —
the professor's correction under test: humans don't read emotion from
faces alone; the answer may be a larger human being.

M1 — THE WARM MUG (contentment, retested): the woman — her third
     appearance — leaning back against the counter, ankles crossed,
     both hands wrapped around the mug at her chest, head bowed to
     it, eyes closed. No steam; the warmth is in the wrap of the
     hands and the curl of the shoulders. First front-view body.

M2 — WORK FINISHED (relief, retested): the painter, done. Head
     dropped, eyes closed, one hand on the back of his own neck,
     the roller hanging loose in the other hand, almost touching
     the floor. The day is over; the body knows it first.
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


def m1_warm_mug():
    S = []
    cx = 450
    # the counter behind her — one plane, two lines, passing behind
    S.append(st([(70, 756), (300, 752)], 1.8, swell=0.08))
    S.append(st([(600, 752), (830, 756)], 1.8, swell=0.08))
    S.append(st([(78, 776), (300, 772)], 1.2, swell=0.06))
    S.append(st([(600, 772), (822, 776)], 1.2, swell=0.06))
    S.append(st([(110, 778), (112, 1240)], 1.4, swell=0.06, cs=True))      # one leg of it
    S.append(st([(792, 778), (790, 1240)], 1.4, swell=0.06, cs=True))

    # head — bowed toward the mug; front view, eyes closed soft
    S.append(st([(382, 282), (372, 212), (396, 148), (452, 126), (506, 150),
                 (528, 214), (516, 286), (484, 330), (450, 342), (414, 328)],
                2.3, swell=0.14))
    S.append(st([(388, 180), (450, 142), (512, 184)], 1.6, swell=0.1))      # hairline
    S.append(st([(376, 226), (366, 250), (376, 274)], 1.2, swell=0.08))     # ear
    S.append(st([(522, 224), (532, 248), (522, 272)], 1.2, swell=0.08))
    S.append(st([(370, 200), (358, 280), (366, 340)], 1.3, swell=0.08))     # hair fall, left
    S.append(st([(528, 198), (542, 278), (534, 338)], 1.3, swell=0.08))     # hair fall, right
    # face, bowed: brows soft, eyes closed downward, the small true smile
    S.append(st([(404, 240), (424, 232), (442, 238)], 1.3, swell=0.08))
    S.append(st([(462, 238), (480, 230), (498, 238)], 1.3, swell=0.08))
    S.append(st([(408, 262), (424, 270), (440, 264)], 1.4, swell=0.1))      # closed, down
    S.append(st([(464, 264), (480, 270), (494, 262)], 1.4, swell=0.1))
    S.append(st([(452, 268), (448, 296), (456, 304)], 1.0, swell=0.07))
    S.append(st([(424, 322), (452, 330), (482, 320)], 1.4, swell=0.1))      # the smile, small
    # neck into sloped, curled shoulders
    S.append(st([(424, 344), (420, 386)], 1.5))
    S.append(st([(478, 344), (484, 388)], 1.5))
    S.append(st([(420, 386), (348, 412), (296, 446)], 2.2, swell=0.14))
    S.append(st([(484, 388), (556, 414), (606, 448)], 2.2, swell=0.14))
    # arms folding in to the mug at her chest
    S.append(st([(296, 446), (288, 530), (330, 586), (390, 608)], 2.1, swell=0.16))
    S.append(st([(606, 448), (614, 532), (572, 588), (512, 608)], 2.1, swell=0.16))
    # the mug, and her hands wrapped — fingers as two quiet lines
    S.append(st([(404, 568), (402, 636)], 1.7, swell=0.1, cs=True))
    S.append(st([(498, 566), (500, 634)], 1.7, swell=0.1, cs=True))
    S.append(st([(404, 568), (450, 560), (498, 566)], 1.4, swell=0.08))
    S.append(st([(402, 636), (452, 644), (500, 634)], 1.5, swell=0.1))
    S.append(st([(404, 590), (450, 598), (498, 588)], 1.0, swell=0.06))     # her fingers
    S.append(st([(410, 612), (452, 620), (494, 610)], 1.0, swell=0.06))
    # the dress — front view, falling past the counter she leans on
    S.append(st([(330, 470), (318, 600), (330, 740), (350, 920), (358, 1056)],
                2.3, swell=0.16))
    S.append(st([(572, 472), (586, 602), (574, 742), (556, 922), (548, 1058)],
                2.3, swell=0.16))
    S.append(st([(358, 1056), (452, 1072), (548, 1058)], 1.7, swell=0.1))   # hem
    S.append(st([(420, 660), (414, 850), (410, 1010)], 0.8, lead=0.3,
                tail=0.32, swell=0.05))                                     # one fold
    # legs — leaning; ankles crossed, one toe pointed down
    S.append(st([(404, 1062), (398, 1170), (390, 1296)], 1.9, swell=0.12))
    S.append(st([(448, 1064), (446, 1168), (442, 1294)], 1.6, swell=0.1))
    S.append(st([(496, 1062), (470, 1180), (428, 1300), (414, 1368)], 1.9,
                swell=0.12))                                                # crossing leg
    S.append(st([(534, 1060), (506, 1180), (462, 1300), (448, 1364)], 1.6,
                swell=0.1))
    S.append(st([(388, 1298), (366, 1318), (424, 1326), (430, 1300)], 1.6,
                swell=0.1))                                                 # planted flat
    S.append(st([(414, 1368), (408, 1396), (442, 1402), (450, 1370)], 1.5,
                swell=0.1))                                                 # pointed toe
    # floor
    S.append(st([(70, 1408), (430, 1402), (830, 1406)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


def m2_work_finished():
    S = []
    cx = 430
    # head dropped forward — crown toward us, face foreshortened low
    S.append(st([(356, 250), (350, 180), (378, 120), (434, 100), (490, 122),
                 (514, 184), (506, 254), (476, 296), (438, 308), (398, 296)],
                2.3, swell=0.14))
    S.append(st([(362, 200), (434, 162), (504, 204)], 1.6, swell=0.1))      # hairline, high
    S.append(st([(398, 152), (404, 196)], 0.8, swell=0.06))                 # hair direction
    S.append(st([(462, 150), (468, 194)], 0.8, swell=0.06))
    # the face, low on the dropped head: closed eyes, exhale mouth
    S.append(st([(396, 252), (414, 246), (430, 250)], 1.2, swell=0.08))
    S.append(st([(448, 250), (464, 244), (480, 250)], 1.2, swell=0.08))
    S.append(st([(400, 268), (414, 274), (428, 268)], 1.3, swell=0.09))     # closed
    S.append(st([(450, 268), (464, 274), (476, 266)], 1.3, swell=0.09))
    S.append(st([(440, 272), (436, 292), (444, 298)], 1.0, swell=0.07))
    S.append(st([(414, 310), (440, 316), (466, 308)], 1.2, swell=0.08))     # slack exhale
    # neck; right arm UP — hand on the back of his own neck, elbow out
    S.append(st([(408, 310), (404, 352)], 1.5))
    S.append(st([(468, 310), (474, 350)], 1.5))
    S.append(st([(474, 350), (560, 380), (628, 366)], 2.3, swell=0.16))     # to the elbow, high
    S.append(st([(628, 366), (596, 300), (532, 270)], 2.1, swell=0.16))     # forearm folding back
    S.append(st([(532, 270), (508, 282), (502, 304)], 1.5, swell=0.1))      # hand at the nape
    S.append(st([(404, 352), (330, 384), (286, 410)], 2.3, swell=0.16))     # left shoulder
    # left arm slack, the roller loose in the hand, nearly at the floor
    S.append(st([(286, 410), (270, 540), (262, 700), (258, 826)], 2.2, swell=0.16))
    S.append(st([(310, 444), (296, 580), (288, 720), (286, 808)], 1.5,
                lead=0.22, swell=0.12))
    S.append(st([(258, 828), (252, 856), (268, 868), (282, 852)], 1.5, swell=0.1))
    # the roller hanging from his hand — pole down, head near the floor
    S.append(st([(268, 866), (264, 1080), (260, 1300)], 1.4, swell=0.06, cs=True))
    S.append(st([(228, 1318), (262, 1312), (296, 1316)], 1.6, swell=0.1))
    S.append(st([(226, 1334), (260, 1328), (294, 1332)], 1.6, swell=0.1))
    S.append(st([(228, 1318), (226, 1334)], 1.0, cs=True, ce=True))
    S.append(st([(296, 1316), (294, 1332)], 1.0, cs=True, ce=True))
    # torso — emptied; the shirt hangs
    S.append(st([(330, 430), (320, 560), (330, 700), (328, 776)], 2.2, swell=0.16))
    S.append(st([(560, 408), (552, 540), (540, 690), (538, 772)], 2.2, swell=0.16))
    S.append(st([(328, 780), (434, 788), (538, 774)], 1.5, swell=0.1))
    # legs — weight uneven, one knee soft; just standing
    S.append(st([(334, 784), (340, 1010), (332, 1240), (338, 1378)], 2.4, swell=0.18))
    S.append(st([(534, 778), (524, 1000), (538, 1120), (528, 1260), (518, 1372)],
                2.4, swell=0.2))                                            # soft knee
    S.append(st([(434, 800), (438, 1080), (434, 1372)], 1.9, lead=0.2, swell=0.16))
    S.append(st([(338, 1378), (316, 1402), (374, 1410), (380, 1382)], 1.7, swell=0.1))
    S.append(st([(518, 1372), (498, 1398), (554, 1404), (560, 1376)], 1.7, swell=0.1))
    # floor
    S.append(st([(60, 1414), (420, 1408), (840, 1412)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


if __name__ == "__main__":
    for name, build in (("m1_warm_mug", m1_warm_mug),
                        ("m2_work_finished", m2_work_finished)):
        fa = render_strokes(build(), W, H)
        out = np.ones((H, W, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
            os.path.join(HERE, f"{name}.png"))
        print(name, "done")
