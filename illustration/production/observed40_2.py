"""
501-P — OBSERVED PEOPLE, installment 2. The consequence rule applied:
"What else would this change?" The observation must spread through
the entire body.

OB5v2 — THE STRAP STUDENT, redrawn as a chain: strap drops the right
        shoulder → neck tilts LEFT to keep the head level (bodies
        hide their adaptations) → ribcage drifts off the load → pelvis
        hikes right → weight settles on the left leg → right foot
        turns out, half off duty. One cause, six consequences.

OB6  — PROTECTING WARMTH (the young woman, arms crossed): cold →
        arms cross → shoulders rise and roll forward → chest hollows →
        chin tucks → knees press, feet together. Every hinge folded
        inward.

OB7  — SAVING ENERGY (the man at the shelter post): the post takes a
        third of him → near leg goes slack and crosses → hip juts to
        the post → far shoulder drops → hands find pockets. The body
        pays out the savings everywhere.
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


def ob5v2_strap_chain():
    S = []
    DROP = 30          # strap shoulder, right
    NECK = -12         # neck tilts LEFT to level the head
    RIB = -16          # ribcage drifts left, off the load
    PELV = 14          # pelvis hikes right
    # head LEVEL — the whole point: the chain exists to keep it level
    S.append(st([(-54 + NECK, 168), (-60 + NECK, 114), (-38 + NECK, 70),
                 (6 + NECK, 56), (46 + NECK, 72), (58 + NECK, 116),
                 (50 + NECK, 166)], 2.2, swell=0.14))
    S.append(st([(-46 + NECK, 150), (2 + NECK, 160), (46 + NECK, 148)], 1.5,
                swell=0.09))
    S.append(st([(-22 + NECK, 78), (-28 + NECK, 124)], 0.8, swell=0.06))
    # the neck — visibly oblique: head center left of the neck base
    S.append(st([(-16 + NECK, 174), (-10, 212)], 1.4))
    S.append(st([(24 + NECK, 176), (32, 214)], 1.4))
    # shoulders — right carried down by the strap
    S.append(st([(-10, 212), (-80 + RIB * .4, 236), (-124 + RIB * .4, 258)],
                2.2, swell=0.14))
    S.append(st([(32, 214), (94, 242 + DROP * .6), (132, 264 + DROP)], 2.2,
                swell=0.14))
    # the strap and its bag
    S.append(st([(118, 270 + DROP), (10 + RIB * .5, 424), (-94 + RIB, 564)],
                1.6, swell=0.09))
    S.append(st([(128, 288 + DROP), (20 + RIB * .5, 440), (-86 + RIB, 580)],
                1.0, swell=0.06))
    S.append(st([(-158 + RIB, 584), (-90 + RIB, 576), (-84 + RIB, 704),
                 (-154 + RIB, 712), (-158 + RIB, 584)], 1.7, swell=0.1))
    # torso — ribcage left, pelvis right: the S made of compensations
    S.append(st([(-124 + RIB * .4, 258), (-116 + RIB, 420), (-104 + PELV * .4, 600),
                 (-98 + PELV, 700)], 2.2, swell=0.15))
    S.append(st([(132, 264 + DROP), (124 + RIB, 430), (114 + PELV * .6, 608),
                 (110 + PELV, 706)], 2.2, swell=0.15))
    # hem tips twice: with the shoulders AND with the hiked pelvis
    S.append(st([(-98 + PELV, 702 - PELV * .4), (4 + PELV, 716),
                 (110 + PELV, 704 + PELV * .4)], 1.4, swell=0.09))
    # arms: strap hand at the chest; free arm hangs PAST the low shoulder
    S.append(st([(-124 + RIB * .4, 258), (-136 + RIB, 340), (-118 + RIB, 422),
                 (-94 + RIB, 470)], 1.9, swell=0.14))
    S.append(st([(-94 + RIB, 470), (-78 + RIB, 488), (-86 + RIB, 504)], 1.3,
                swell=0.09))
    S.append(st([(132, 264 + DROP), (144 + RIB * .5, 430), (134 + PELV * .5, 570),
                 (126 + PELV, 656)], 1.9, swell=0.14))
    S.append(st([(126 + PELV, 658), (134 + PELV, 684), (120 + PELV, 696)], 1.3,
                swell=0.09))
    # legs — weight LEFT (under the leveled head), right foot turned out
    S.append(st([(-98 + PELV, 704), (-86, 900), (-66, 1090), (-58, 1210)],
                2.3, swell=0.16))                                         # weight leg, plumb-ish
    S.append(st([(110 + PELV, 708), (112, 900), (118, 1090), (122, 1204)],
                2.1, swell=0.14))                                         # free leg, eased
    S.append(st([(6 + PELV, 718), (16, 940), (24, 1206)], 1.7, lead=0.2,
                swell=0.12))
    S.append(st([(-58, 1210), (-80, 1236), (-18, 1244), (-14, 1214)], 1.6,
                swell=0.1))                                               # weight foot, square
    S.append(st([(122, 1204), (148, 1224), (174, 1238), (118, 1244), (112, 1208)],
                1.6, swell=0.1))                                          # free foot, turned out
    return S


def ob6_warmth():
    S = []
    RISE = 22   # shoulders up
    # head — chin tucked: head low and forward, hair past the cheeks
    S.append(st([(-50, 208), (-56, 156), (-34, 112), (8, 98), (46, 114),
                 (58, 158), (50, 206)], 2.2, swell=0.14))
    S.append(st([(-42, 192), (4, 202), (46, 190)], 1.4, swell=0.08))
    S.append(st([(-54, 140), (-66, 230), (-58, 300)], 1.2, swell=0.08))    # hair, falling closed
    S.append(st([(54, 138), (66, 228), (58, 298)], 1.2, swell=0.08))
    # almost no neck — the shoulders have risen to meet the head
    S.append(st([(-22, 214), (-24, 234 - RISE * .4)], 1.3))
    S.append(st([(26, 216), (30, 236 - RISE * .4)], 1.3))
    S.append(st([(-24, 234 - RISE * .4), (-88, 244 - RISE), (-122, 262 - RISE * .6)],
                2.2, swell=0.14))
    S.append(st([(30, 236 - RISE * .4), (92, 246 - RISE), (124, 264 - RISE * .6)],
                2.2, swell=0.14))
    # the crossed arms — one bar of folded warmth across the hollowed chest
    S.append(st([(-122, 262 - RISE * .6), (-130, 340), (-112, 400)], 2.0, swell=0.14))
    S.append(st([(124, 264 - RISE * .6), (132, 342), (114, 402)], 2.0, swell=0.14))
    S.append(st([(-112, 402), (-40, 430), (40, 432), (114, 404)], 2.1, swell=0.14))
    S.append(st([(-104, 446), (-30, 470), (44, 468), (108, 444)], 1.7, swell=0.12))
    S.append(st([(96, 420), (76, 446), (84, 466)], 1.2, swell=0.08))       # tucked hand
    # hollowed torso — the body curls around its own warmth
    S.append(st([(-110, 420), (-96, 540), (-86, 660), (-84, 740)], 2.2, swell=0.15))
    S.append(st([(112, 422), (98, 542), (88, 662), (86, 742)], 2.2, swell=0.15))
    S.append(st([(-84, 742), (2, 754), (86, 742)], 1.4, swell=0.09))
    # legs pressed together, feet touching
    S.append(st([(-58, 756), (-48, 940), (-36, 1120), (-32, 1212)], 2.2, swell=0.15))
    S.append(st([(60, 754), (50, 938), (38, 1118), (34, 1210)], 2.2, swell=0.15))
    S.append(st([(0, 760), (2, 980), (2, 1208)], 1.5, lead=0.22, swell=0.11))
    S.append(st([(-32, 1212), (-50, 1238), (0, 1244), (2, 1216)], 1.5, swell=0.1))
    S.append(st([(34, 1210), (52, 1236), (4, 1242)], 1.5, swell=0.1))
    return S


def ob7_post_leaner():
    S = []
    # the post — it does a third of the standing
    S.append(st([(150, 80), (152, 1240)], 2.4, swell=0.05, cs=True, ce=True))
    LEAN = 54   # whole upper body toward the post
    # head, easy, tipped a degree toward the post
    S.append(st([(-50 + LEAN, 170), (-56 + LEAN, 116), (-34 + LEAN, 72),
                 (8 + LEAN, 58), (46 + LEAN, 74), (58 + LEAN, 118),
                 (50 + LEAN, 168)], 2.2, swell=0.14))
    S.append(st([(-42 + LEAN, 152), (4 + LEAN, 162), (46 + LEAN, 150)], 1.4,
                swell=0.08))
    S.append(st([(-20 + LEAN, 80), (-26 + LEAN, 126)], 0.8, swell=0.06))
    S.append(st([(-14 + LEAN, 176), (-12 + LEAN * .8, 212)], 1.4))
    S.append(st([(26 + LEAN, 178), (28 + LEAN * .8, 214)], 1.4))
    # the post-side shoulder wedges INTO the post; the far one drops
    S.append(st([(28 + LEAN * .8, 214), (88 + LEAN * .7, 238), (124 + LEAN * .55, 262)],
                2.2, swell=0.14))                                          # meets the post
    S.append(st([(-12 + LEAN * .8, 212), (-78 + LEAN * .6, 248), (-118 + LEAN * .5, 284)],
                2.2, swell=0.14))                                          # far shoulder, low
    # torso — hip juts toward the post; the body hangs off the contact
    S.append(st([(-118 + LEAN * .5, 284), (-112 + LEAN * .35, 450),
                 (-96 + LEAN * .2, 620), (-88 + LEAN * .15, 730)], 2.2, swell=0.15))
    S.append(st([(124 + LEAN * .55, 262), (126 + LEAN * .4, 430),
                 (120 + LEAN * .3, 600), (114 + LEAN * .2, 724)], 2.2, swell=0.15))
    S.append(st([(-88 + LEAN * .15, 732), (12 + LEAN * .15, 744),
                 (114 + LEAN * .2, 726)], 1.4, swell=0.09))
    # hands in pockets — both; the saving is total
    S.append(st([(-118 + LEAN * .5, 284), (-128 + LEAN * .4, 420),
                 (-108 + LEAN * .3, 540), (-86 + LEAN * .25, 590)], 1.9, swell=0.14))
    S.append(st([(-106 + LEAN * .3, 596), (-72 + LEAN * .25, 588)], 1.0,
                cs=True, ce=True))                                         # pocket seam
    S.append(st([(124 + LEAN * .55, 262), (136 + LEAN * .4, 400),
                 (122 + LEAN * .3, 520), (104 + LEAN * .25, 576)], 1.9, swell=0.14))
    S.append(st([(122 + LEAN * .3, 582), (88 + LEAN * .25, 574)], 1.0,
                cs=True, ce=True))
    # legs — the standing leg plumb under the post contact; the near
    # leg slack, crossed over, toe down
    S.append(st([(96 + LEAN * .2, 728), (96, 920), (92, 1110), (90, 1212)],
                2.3, swell=0.16))                                          # standing leg
    S.append(st([(-66 + LEAN * .15, 736), (-20, 900), (40, 1060), (66, 1180)],
                2.1, swell=0.15))                                          # slack leg, crossing
    S.append(st([(90, 1212), (68, 1238), (130, 1246), (134, 1216)], 1.6, swell=0.1))
    S.append(st([(66, 1180), (58, 1226), (76, 1248), (88, 1238)], 1.5, swell=0.1))  # toe down
    return S


PEOPLE = [
    (ob5v2_strap_chain, "The strap drops one shoulder; the neck tilts to "
                        "level the head; the ribs drift, the pelvis hikes, "
                        "the right foot half retires. One bag, six "
                        "consequences."),
    (ob6_warmth, "Cold: the arms cross, the shoulders rise, the chest "
                 "hollows, the chin tucks, the knees press. Every hinge "
                 "folded inward."),
    (ob7_post_leaner, "The post does a third of the standing; the near leg "
                      "goes slack and crosses, the hip juts, the hands "
                      "retire to the pockets. The body pays out the "
                      "savings everywhere."),
]

if __name__ == "__main__":
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    gap = 12
    cap_h = 110
    sheet = Image.new("RGB", (PW * 3 + gap * 4, PH + cap_h + gap * 2),
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
        for line in textwrap.wrap(sentence, width=44):
            d.text((x0 + 6, y), line, font=font, fill=(31, 29, 27))
            y += 19
    sheet.save(os.path.join(HERE, "observed40_sheet2.png"))
    print("done")
