"""
501-P — OBSERVED PEOPLE, installment 1 of the forty. Five real
individuals, seen at two bus stops (street photography study,
2026-06-11), reconstructed never traced. The sentence came first;
the drawing serves the sentence.

OB1 — woman, heavyset, middle-aged: "Hands in pockets push the whole
      jacket forward; she has stopped expecting the bus."
OB2 — woman, older, narrow: "Stands perfectly vertical inside the
      coat, as if taking up less space keeps her warmer."
OB3 — man, tall: "His neck cranes past the shelter edge; the whole
      back leans into the looking."
OB4 — man, stocky: "The parka erases his waist; only the feet say
      where the body divides."
OB5 — student: "The bag's strap has lowered one shoulder so long the
      body has built itself around it."
"""
import os
import sys
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from about_figure import render_strokes, PAPER, INK

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PH = 430, 760
K, DY = 0.42, 30


def st(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


def sc(S):
    out = []
    for t in S:
        t2 = dict(t)
        t2["ctrl"] = [(x * K + PW / 2, y * K + DY) for (x, y) in t["ctrl"]]
        t2["w"] = max(0.7, t["w"] * K * 1.6)
        out.append(t2)
    return out


def ob1_pocket_woman():
    S = []
    # head small over the mass, chin slightly down
    S.append(st([(-56, 184), (-62, 130), (-40, 84), (6, 68), (48, 86),
                 (62, 132), (54, 182)], 2.2, swell=0.14))
    S.append(st([(-46, 168), (4, 178), (50, 166)], 1.5, swell=0.09))
    S.append(st([(-30, 92), (-36, 140)], 0.8, swell=0.06))
    S.append(st([(-18, 192), (-20, 224)], 1.4))
    S.append(st([(22, 194), (26, 226)], 1.4))
    # the jacket — pushed forward by the pocketed fists: the silhouette
    # widens BELOW the shoulders and bumps at the fists
    S.append(st([(-20, 224), (-96, 252), (-148, 286)], 2.3, swell=0.15))
    S.append(st([(26, 226), (100, 254), (150, 288)], 2.3, swell=0.15))
    S.append(st([(-148, 286), (-176, 420), (-182, 540), (-168, 660), (-150, 706)],
                2.4, swell=0.16))                                          # left fall + fist bump
    S.append(st([(150, 288), (180, 424), (186, 544), (170, 662), (152, 708)],
                2.4, swell=0.16))
    S.append(st([(-150, 708), (-40, 722), (70, 720), (152, 708)], 1.7, swell=0.1))
    # the pocketed fists — two pushes from inside
    S.append(st([(-130, 540), (-108, 560), (-112, 588)], 1.1, swell=0.07))
    S.append(st([(132, 542), (112, 562), (116, 590)], 1.1, swell=0.07))
    S.append(st([(-60, 300), (-58, 480)], 0.9, lead=0.3, tail=0.3, swell=0.05))  # zip
    # the bag from the right wrist
    S.append(st([(160, 660), (158, 720)], 1.0, swell=0.06))
    S.append(st([(140, 720), (186, 718), (192, 790), (138, 792), (140, 720)],
                1.4, swell=0.09))
    # sturdy legs, feet apart, flat
    S.append(st([(-96, 724), (-92, 920), (-86, 1100)], 2.3, swell=0.15))
    S.append(st([(-30, 726), (-32, 920), (-34, 1098)], 1.8, swell=0.12))
    S.append(st([(96, 722), (94, 918), (90, 1096)], 2.3, swell=0.15))
    S.append(st([(34, 726), (36, 918), (38, 1096)], 1.8, swell=0.12))
    S.append(st([(-88, 1100), (-110, 1128), (-26, 1134), (-22, 1104)], 1.7, swell=0.1))
    S.append(st([(90, 1098), (114, 1126), (32, 1132), (28, 1102)], 1.7, swell=0.1))
    return S


def ob2_vertical_woman():
    S = []
    # erect head, short hair, high collar; everything vertical
    S.append(st([(-50, 170), (-56, 116), (-34, 72), (8, 58), (46, 74),
                 (58, 118), (50, 168)], 2.2, swell=0.14))
    S.append(st([(-42, 152), (4, 162), (46, 150)], 1.4, swell=0.08))
    S.append(st([(-44, 100), (-52, 150), (-44, 188)], 1.1, swell=0.07))    # short hair edge
    # scarf — two close lines at the neck
    S.append(st([(-28, 188), (-30, 218), (30, 220), (32, 190)], 1.5, swell=0.09))
    S.append(st([(-26, 232), (28, 234)], 1.1, swell=0.06))
    # the coat — narrow, straight, long; collar points up
    S.append(st([(-30, 218), (-72, 238), (-94, 262)], 2.0, swell=0.13))
    S.append(st([(32, 220), (72, 240), (96, 264)], 2.0, swell=0.13))
    S.append(st([(-94, 262), (-98, 540), (-96, 840), (-92, 1120)], 2.2, swell=0.14))
    S.append(st([(96, 264), (100, 542), (98, 842), (94, 1118)], 2.2, swell=0.14))
    S.append(st([(-92, 1120), (0, 1132), (94, 1118)], 1.5, swell=0.09))
    S.append(st([(-4, 250), (-2, 700), (0, 1100)], 0.8, lead=0.25, tail=0.25,
                swell=0.05))                                               # the button line
    # arms inside the verticality — only the cuffs and hands show
    S.append(st([(-86, 600), (-80, 660), (-72, 700)], 1.3, swell=0.08))
    S.append(st([(88, 602), (82, 662), (74, 702)], 1.3, swell=0.08))
    S.append(st([(-72, 702), (-64, 726), (-74, 740)], 1.2, swell=0.08))
    S.append(st([(74, 704), (66, 728), (76, 742)], 1.2, swell=0.08))
    # heels together — the small V
    S.append(st([(-24, 1122), (-40, 1182), (-46, 1196), (-8, 1200), (-10, 1130)],
                1.6, swell=0.1))
    S.append(st([(24, 1120), (38, 1180), (44, 1194), (8, 1198), (10, 1128)],
                1.6, swell=0.1))
    return S


def ob3_craning_man():
    S = []
    sh = 36   # the lean, at the top
    # tall: small head, tipped back and turned — chin line up
    S.append(st([(-46 + sh, 150), (-50 + sh, 100), (-28 + sh, 60), (12 + sh, 48),
                 (50 + sh, 66), (60 + sh, 110), (50 + sh, 148)], 2.1, swell=0.13))
    S.append(st([(50 + sh, 148), (66 + sh, 138), (74 + sh, 124)], 1.4, swell=0.09))  # chin, up
    S.append(st([(-38 + sh, 136), (6 + sh, 146), (46 + sh, 134)], 1.3, swell=0.08))
    # the extended neck — longer than comfortable
    S.append(st([(-14 + sh, 158), (-18 + sh * .8, 212)], 1.5))
    S.append(st([(26 + sh, 160), (28 + sh * .8, 214)], 1.5))
    # high shoulders leaning into the look
    S.append(st([(-18 + sh * .8, 212), (-86 + sh * .7, 238), (-128 + sh * .7, 268)],
                2.2, swell=0.14))
    S.append(st([(28 + sh * .8, 214), (92 + sh * .7, 240), (132 + sh * .7, 270)],
                2.2, swell=0.14))
    # long coat, the lean running out of it toward the street
    S.append(st([(-128 + sh * .7, 268), (-122 + sh * .4, 520), (-108, 800),
                 (-100, 980)], 2.2, swell=0.15))
    S.append(st([(132 + sh * .7, 270), (128 + sh * .4, 524), (116, 804),
                 (110, 982)], 2.2, swell=0.15))
    S.append(st([(-100, 982), (6, 994), (110, 982)], 1.5, swell=0.09))
    # arms back, hands clasped behind? no — one hand holds the shelter post line
    S.append(st([(-118 + sh * .6, 300), (-130 + sh * .3, 480), (-126, 640),
                 (-118, 700)], 1.8, swell=0.13))
    S.append(st([(118 + sh * .6, 302), (130 + sh * .3, 482), (124, 644),
                 (118, 702)], 1.8, swell=0.13))
    # long legs, one foot ahead (toward the looking)
    S.append(st([(-58, 994), (-66, 1180), (-78, 1330), (-84, 1420)], 2.2, swell=0.15))
    S.append(st([(58, 992), (52, 1170), (40, 1320), (36, 1408)], 2.2, swell=0.15))
    S.append(st([(-2, 1000), (-8, 1200), (-14, 1416)], 1.7, lead=0.2, swell=0.12))
    S.append(st([(-84, 1420), (-108, 1444), (-46, 1452), (-42, 1424)], 1.6, swell=0.1))
    S.append(st([(36, 1408), (18, 1434), (74, 1440), (78, 1412)], 1.6, swell=0.1))
    return S


def ob4_parka_man():
    S = []
    # head half-sunk into the parka collar; hood bump behind
    S.append(st([(-52, 200), (-56, 150), (-34, 108), (8, 94), (48, 110),
                 (58, 152), (50, 198)], 2.2, swell=0.14))
    S.append(st([(-44, 184), (2, 194), (46, 182)], 1.4, swell=0.08))
    S.append(st([(50, 150), (84, 168), (92, 216), (76, 252)], 1.6, swell=0.1))  # hood, behind
    # the parka — one mass, no waist: shoulder to hem in single falls
    S.append(st([(-26, 214), (-104, 248), (-150, 296), (-160, 440), (-156, 600),
                 (-146, 780), (-138, 838)], 2.5, swell=0.16))
    S.append(st([(30, 216), (106, 250), (152, 298), (162, 442), (158, 602),
                 (148, 782), (140, 840)], 2.5, swell=0.16))
    S.append(st([(-138, 840), (-20, 854), (84, 852), (140, 840)], 1.7, swell=0.1))
    S.append(st([(-58, 320), (-56, 560), (-52, 800)], 0.9, lead=0.28, tail=0.3,
                swell=0.05))                                               # zip line
    # pocket slits — where the hands are
    S.append(st([(-118, 560), (-92, 590)], 1.2, cs=True, ce=True))
    S.append(st([(120, 562), (94, 592)], 1.2, cs=True, ce=True))
    # short sturdy legs — the body divides only here
    S.append(st([(-78, 856), (-74, 1020), (-70, 1180)], 2.3, swell=0.15))
    S.append(st([(-16, 858), (-18, 1020), (-20, 1178)], 1.8, swell=0.12))
    S.append(st([(80, 854), (76, 1018), (72, 1176)], 2.3, swell=0.15))
    S.append(st([(22, 858), (24, 1018), (26, 1176)], 1.8, swell=0.12))
    S.append(st([(-72, 1182), (-94, 1210), (-12, 1216), (-8, 1186)], 1.7, swell=0.1))
    S.append(st([(74, 1178), (96, 1206), (16, 1212), (12, 1182)], 1.7, swell=0.1))
    return S


def ob5_strap_student():
    S = []
    DROP = 26  # the strap shoulder, lowered for years
    # back view; head tilted a touch toward the low shoulder
    S.append(st([(-54, 168), (-60, 114), (-38, 70), (6, 56), (46, 72),
                 (58, 116), (50, 166)], 2.2, swell=0.14))
    S.append(st([(-46, 150), (2, 160), (46, 148)], 1.5, swell=0.09))
    S.append(st([(-22, 78), (-28, 124)], 0.8, swell=0.06))
    S.append(st([(-16, 174), (-18, 210)], 1.4))
    S.append(st([(24, 176), (28, 212)], 1.4))
    # shoulders — right carries the strap, lowered; left rides normal
    S.append(st([(-18, 210), (-84, 234), (-128, 258)], 2.2, swell=0.14))
    S.append(st([(28, 212), (92, 240 + DROP * .6), (130, 262 + DROP)], 2.2,
                swell=0.14))
    # the strap — diagonal across the back, the cause made visible
    S.append(st([(116, 268 + DROP), (10, 420), (-96, 560)], 1.6, swell=0.09))
    S.append(st([(126, 286 + DROP), (20, 436), (-88, 576)], 1.0, swell=0.06))
    # torso — built around the asymmetry; hem tips with the shoulders
    S.append(st([(-128, 258), (-118, 420), (-108, 600), (-104, 700)], 2.2, swell=0.15))
    S.append(st([(130, 262 + DROP), (122, 426), (112, 606), (108, 706)], 2.2,
                swell=0.15))
    S.append(st([(-104, 702), (2, 714), (108, 706)], 1.4, swell=0.09))
    # the bag at the left hip
    S.append(st([(-160, 580), (-92, 572), (-86, 700), (-156, 708), (-160, 580)],
                1.7, swell=0.1))
    S.append(st([(-152, 612), (-94, 606)], 1.0, swell=0.06))               # flap line
    # arms: strap-side hand holds the strap at the chest; other hangs
    S.append(st([(130, 262 + DROP), (140, 420), (132, 560), (124, 640)], 1.9,
                swell=0.14))
    S.append(st([(124, 642), (132, 668), (118, 680)], 1.3, swell=0.09))
    S.append(st([(-128, 258), (-138, 340), (-120, 420), (-96, 470)], 1.9, swell=0.14))
    S.append(st([(-96, 470), (-80, 488), (-88, 504)], 1.3, swell=0.09))    # hand on strap
    # legs — weight on the right (under the load), left easy
    S.append(st([(-104, 704), (-96, 900), (-84, 1090), (-80, 1212)], 2.2, swell=0.15))
    S.append(st([(108, 708), (102, 900), (94, 1086), (92, 1206)], 2.2, swell=0.15))
    S.append(st([(2, 716), (8, 940), (10, 1208)], 1.7, lead=0.2, swell=0.12))
    S.append(st([(-80, 1212), (-102, 1238), (-40, 1246), (-36, 1216)], 1.6, swell=0.1))
    S.append(st([(92, 1206), (112, 1232), (52, 1240), (48, 1210)], 1.6, swell=0.1))
    return S


PEOPLE = [
    (ob1_pocket_woman, "Hands in pockets push the whole jacket forward; "
                       "she has stopped expecting the bus."),
    (ob2_vertical_woman, "Stands perfectly vertical inside the coat, as if "
                         "taking up less space keeps her warmer."),
    (ob3_craning_man, "His neck cranes past the shelter edge; the whole "
                      "back leans into the looking."),
    (ob4_parka_man, "The parka erases his waist; only the feet say where "
                    "the body divides."),
    (ob5_strap_student, "The bag's strap has lowered one shoulder so long "
                        "the body has built itself around it."),
]

if __name__ == "__main__":
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    gap = 12
    cap_h = 84
    sheet = Image.new("RGB", (PW * 5 + gap * 6, PH + cap_h + gap * 2),
                      tuple(int(v) for v in PAPER))
    d = ImageDraw.Draw(sheet)
    for i, (build, sentence) in enumerate(PEOPLE):
        fa = render_strokes(sc(build()), PW, PH)
        out = np.ones((PH, PW, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        p = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
        x0 = gap + i * (PW + gap)
        sheet.paste(p, (x0, gap))
        y = PH + gap + 6
        for line in textwrap.wrap(sentence, width=42):
            d.text((x0 + 6, y), line, font=font, fill=(31, 29, 27))
            y += 19
    sheet.save(os.path.join(HERE, "observed40_sheet1.png"))
    print("done")
