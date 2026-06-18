"""
HUMAN STUDIES VOL. 1 — Batch 12 (h086–h105): THE FINAL TWENTY.
Sources: MEHR agency anthem-row photograph (ten strangers, hands on
hearts, 3/4-to-profile, anthem gravity) and the applause photograph
(arms raised, heads tipped, open emotion) — observed this session;
five repeats from different photographs already in the corpus.
Head 100 is the severe-profile silver-templed man, drawn with
everything the volume learned. Architecture notes per head: ledger.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def head_34(skull_w, face_len, brow_w, brow_y, eye_open, beard,
            hair, mouth, extras=None, roll=0.0, jaw="normal"):
    """Three-quarter-left head builder. Parameters are OBSERVED per
    subject; nothing defaults silently — every call states its bones."""
    S = []
    cx = 350
    hw = skull_w // 2
    # skull
    S += [s([(cx-hw, 300), (cx-hw+12, 212), (cx-44, 156), (cx+24, 146),
             (cx+hw-18, 178), (cx+hw, 258), (cx+hw+2, 312)], 3.1)]
    # hair variants
    if hair == "silver_back":
        S += [s([(cx-hw+22, 296), (cx-22, 258), (cx+34, 252), (cx+hw-14, 282)], 1.9)]
        S += [s([(cx-30, 256), (cx-10, 210)], 1.3)]
    elif hair == "flat_dark":
        S += [s([(cx-hw+18, 292), (cx-30, 262), (cx+30, 256), (cx+hw-16, 284)], 2.1)]
        S += [s([(cx-40, 260), (cx+20, 250)], 1.3)]
    elif hair == "buzz":
        S += [s([(cx-hw+16, 290), (cx-26, 260), (cx+28, 254), (cx+hw-14, 282)], 1.5)]
    elif hair == "curly":
        S += [s([(cx-hw+8, 280), (cx-44, 240), (cx-12, 252), (cx+20, 236),
                 (cx+52, 252), (cx+hw-10, 276)], 2.2)]
    elif hair == "quiff":
        S += [s([(cx-40, 240), (cx-20, 186), (cx+24, 158)], 2.1)]
        S += [s([(cx-hw+20, 298), (cx-26, 262), (cx+30, 270), (cx+hw-14, 296)], 1.9)]
    # face sides: jaw variants
    fl = face_len
    if jaw == "heavy":
        side_l = [(cx-hw+6, 318), (cx-hw, 388), (cx-hw+12, 450),
                  (cx-hw+30, fl-60), (cx-hw+62, fl-18), (cx-2, fl)]
        side_r = [(cx+hw+2, 322), (cx+hw+6, 392), (cx+hw-6, 452),
                  (cx+hw-24, fl-58), (cx+hw-56, fl-16), (cx+4, fl+2)]
    else:
        side_l = [(cx-hw+8, 318), (cx-hw+2, 390), (cx-hw+14, 452),
                  (cx-hw+32, fl-56), (cx-hw+62, fl-14), (cx-2, fl)]
        side_r = [(cx+hw, 322), (cx+hw+4, 392), (cx+hw-8, 452),
                  (cx+hw-26, fl-54), (cx+hw-56, fl-12), (cx+4, fl+2)]
    S += [s(side_l, 2.8)]
    S += [s(side_r, 3.3)]
    # brows
    S += [s([(cx-66, brow_y), (cx-34, brow_y-6), (cx-6, brow_y-2)], brow_w)]
    S += [s([(cx+28, brow_y-3), (cx+60, brow_y-9), (cx+88, brow_y-3)], brow_w)]
    # eyes
    ey = brow_y + 30
    if eye_open == "closed":
        S += [s([(cx-60, ey), (cx-36, ey+4), (cx-14, ey)], 2.4)]
        S += [s([(cx+34, ey-2), (cx+56, ey+2), (cx+78, ey-2)], 2.4)]
    elif eye_open == "slit":
        S += [s([(cx-60, ey), (cx-36, ey-5), (cx-14, ey)], 2.5)]
        S += [s([(cx-40, ey-2), (cx-31, ey+5)], 1.9)]
        S += [s([(cx+34, ey-2), (cx+56, ey-7), (cx+78, ey-2)], 2.5)]
        S += [s([(cx+52, ey-4), (cx+61, ey+3)], 1.9)]
    else:  # open
        S += [s([(cx-62, ey), (cx-36, ey-7), (cx-12, ey-1)], 2.5)]
        S += [s([(cx-42, ey-3), (cx-34, ey+5), (cx-43, ey+7)], 2.3)]
        S += [s([(cx-58, ey+9), (cx-36, ey+12), (cx-16, ey+7)], 1.4)]
        S += [s([(cx+32, ey-2), (cx+58, ey-9), (cx+82, ey-3)], 2.5)]
        S += [s([(cx+52, ey-5), (cx+60, ey+3), (cx+51, ey+5)], 2.3)]
        S += [s([(cx+36, ey+7), (cx+58, ey+10), (cx+78, ey+5)], 1.4)]
    # nose (3/4: slightly left of center)
    S += [s([(cx+4, brow_y+8), (cx, brow_y+78)], 1.9)]
    S += [s([(cx-24, brow_y+90), (cx-2, brow_y+100), (cx+24, brow_y+88)], 2.3)]
    # mouth variants
    my = fl - 86
    if mouth == "set":
        S += [s([(cx-36, my), (cx-10, my-5), (cx+6, my-3), (cx+22, my-6), (cx+44, my)], 2.6)]
        S += [s([(cx-28, my+13), (cx+4, my+18), (cx+36, my+11)], 1.9)]
    elif mouth == "down":
        S += [s([(cx-36, my-4), (cx-8, my-7), (cx+20, my-6), (cx+44, my+2)], 2.6)]
        S += [s([(cx-26, my+11), (cx+6, my+15), (cx+34, my+11)], 1.8)]
    elif mouth == "open_shout":
        S += [s([(cx-32, my-12), (cx-4, my-18), (cx+26, my-14)], 2.7)]
        S += [s([(cx-26, my+16), (cx-2, my+26), (cx+24, my+14)], 2.8)]
        S += [s([(cx-22, my-6), (cx+18, my-8)], 1.4)]
    elif mouth == "grin":
        S += [s([(cx-44, my-8), (cx-12, my+2), (cx+12, my+4), (cx+38, my-4), (cx+58, my-14)], 2.9)]
        S += [s([(cx-32, my), (cx, my+1), (cx+34, my-3)], 1.4)]
        S += [s([(cx-30, my+8), (cx+2, my+18), (cx+36, my+4)], 2.6)]
    # beard
    if beard == "full":
        S += [s([(cx-hw+16, 452), (cx-hw+18, fl-30), (cx-30, fl+34),
                 (cx+24, fl+38), (cx+hw-40, fl-24), (cx+hw-10, 452)], 3.6)]
        S += [s([(cx-30, fl-40), (cx-22, fl)], 1.3)]
        S += [s([(cx+30, fl-44), (cx+38, fl-6)], 1.3)]
    elif beard == "stubble":
        S += [s([(cx-hw+34, fl-44), (cx-hw+44, fl-26)], 1.0)]
        S += [s([(cx+hw-52, fl-46), (cx+hw-60, fl-28)], 1.0)]
    # chin shelf when beardless
    if beard == "none" or beard == "stubble":
        S += [s([(cx-44, fl-12), (cx-16, fl+2), (cx+18, fl+2), (cx+42, fl-12)], 2.2)]
    # neck + dark coat (anthem row uniform)
    S += [s([(cx-40, fl+8), (cx-46, fl+62)], 2.5)]
    S += [s([(cx+44, fl+6), (cx+50, fl+58)], 2.5)]
    S += [s([(cx-110, fl+118), (cx-44, fl+74), (cx+2, fl+68)], 3.0)]
    S += [s([(cx+112, fl+114), (cx+52, fl+72), (cx+8, fl+68)], 3.0)]
    if extras:
        S += extras
    return tilt(S, roll), [s([(cx-hw, brow_y+30), (cx+hw, brow_y+30)], 1.0)]


def hand_on_heart(cx=350, y=760):
    return [s([(cx-90, y), (cx-50, y-26), (cx-4, y-22)], 2.4),
            s([(cx-70, y+14), (cx-32, y-8)], 1.8)]


# ---- the anthem row (h086–h095, h100) -------------------------------
def h086(): return head_34(252, 614, 3.4, 364, "slit", "none", "silver_back", "down",
                           extras=hand_on_heart(), roll=-2.0, jaw="heavy")
def h087(): return head_34(262, 596, 2.9, 372, "slit", "none", "flat_dark", "set",
                           extras=hand_on_heart(), roll=1.5)
def h088(): return head_34(240, 604, 2.2, 366, "open", "none", "silver_back", "set",
                           extras=[s([(296, 388), (332, 380), (366, 386), (370, 410), (358, 422), (326, 424), (298, 414), (294, 396), (296, 388)], 2.2),
                                   s([(370, 396), (392, 392)], 1.8)], roll=-1.0)
def h089(): return head_34(246, 610, 3.6, 358, "open", "full", "curly", "set",
                           extras=[s([(294, 384), (330, 376), (362, 382), (366, 408), (354, 420), (322, 422), (296, 412), (292, 392), (294, 384)], 2.4)], roll=2.0)
def h090(): return head_34(250, 600, 3.0, 368, "closed", "stubble", "buzz", "set",
                           extras=hand_on_heart(), roll=-1.5)
def h091(): return head_34(244, 622, 3.2, 352, "slit", "full", "flat_dark", "set",
                           extras=hand_on_heart(), roll=-6.0)   # chin up
def h093(): return head_34(270, 588, 3.1, 370, "open", "full", "curly", "set",
                           extras=hand_on_heart(), roll=1.0, jaw="heavy")
def h094(): return head_34(268, 592, 2.6, 374, "slit", "stubble", "buzz", "set",
                           extras=hand_on_heart(), roll=-1.0, jaw="heavy")
def h095():
    """Far-right elder, lean, TRUE PROFILE right — drawn freehand."""
    S = []
    S += [s([(216, 384), (212, 292), (246, 206), (322, 158), (404, 148), (462, 184)], 3.4)]
    S += [s([(462, 184), (478, 246), (472, 304)], 2.9)]
    S += [s([(246, 290), (282, 252), (332, 238)], 1.7)]            # silver back-sweep
    S += [s([(472, 304), (488, 322), (484, 338)], 2.7)]            # brow ridge
    S += [s([(484, 338), (506, 380), (502, 394)], 2.7)]            # lean nose
    S += [s([(502, 394), (486, 404), (478, 408)], 1.9)]
    S += [s([(484, 420), (500, 427)], 2.2)]
    S += [s([(482, 438), (496, 444)], 1.8)]
    S += [s([(478, 454), (488, 478), (472, 508)], 2.5)]            # firm old chin
    S += [s([(472, 508), (420, 542), (350, 560)], 3.1)]
    S += [s([(432, 330), (462, 322), (478, 328)], 2.8)]
    S += [s([(440, 348), (462, 342), (476, 347)], 2.1)]
    S += [s([(444, 356), (462, 360), (474, 354)], 1.2)]
    S += [s([(428, 372), (452, 404), (450, 432)], 1.5)]            # cheek age, one line
    S += [s([(330, 334), (360, 322), (376, 356), (364, 400), (334, 406)], 2.6)]
    S += [s([(350, 562), (346, 622)], 2.6)]
    S += [s([(254, 668), (348, 636), (420, 640)], 3.0)]
    S += [s([(488, 600), (430, 636)], 3.0)]
    return tilt(S, 1.0), [s([(216, 348), (484, 348)], 1.0)]
def h100():
    """HEAD ONE HUNDRED. The silver-templed man, severe profile at
    anthem. Everything the volume learned, spent at once: profile
    room (l.11), age in relationships (s5), marks as weather (l.5),
    occlusion edge (l.27), the climate carried by one deep-set eye
    under a heavy brow step."""
    S = []
    S += [s([(212, 392), (208, 296), (244, 208), (324, 158), (408, 150), (466, 190)], 3.5)]
    S += [s([(466, 190), (484, 252), (478, 312)], 3.0)]
    S += [s([(250, 286), (296, 248), (348, 236)], 1.8)]            # silver temple sweep
    S += [s([(274, 258), (308, 240)], 1.2)]
    S += [s([(478, 312), (496, 332), (492, 348)], 2.9)]            # the brow step
    S += [s([(492, 348), (514, 394), (510, 408)], 2.8)]            # strong nose
    S += [s([(510, 408), (492, 418), (484, 422)], 2.0)]
    S += [s([(490, 436), (508, 443)], 2.4)]                        # set lips
    S += [s([(488, 456), (502, 462)], 1.9)]
    S += [s([(484, 474), (494, 500), (476, 532)], 2.6)]            # chin, held up
    S += [s([(476, 532), (418, 562), (348, 578)], 3.2)]            # jaw home
    # the one visible eye: deep under the step — the climate, alone
    S += [s([(434, 340), (466, 330), (486, 338)], 3.2)]
    S += [s([(442, 360), (466, 353), (482, 359)], 2.3)]
    S += [s([(458, 356), (468, 364)], 1.9)]
    S += [s([(446, 369), (466, 373), (480, 366)], 1.3)]
    # age as relationships: ONE nasolabial, ONE cheek line
    S += [s([(486, 428), (468, 452), (462, 470)], 1.7)]
    S += [s([(430, 380), (452, 416), (450, 448)], 1.4)]
    # ear, collar, the hand on the heart cropping the chest (l.27:
    # the hand owns its edge; the coat never shares it)
    S += [s([(332, 342), (362, 330), (378, 364), (366, 408), (336, 414)], 2.6)]
    S += [s([(348, 580), (344, 636)], 2.6)]
    S += [s([(250, 682), (346, 648), (418, 652)], 3.0)]
    S += [s([(490, 618), (432, 650)], 3.0)]
    S += [s([(260, 730), (320, 700), (382, 696)], 2.6)]
    S += [s([(282, 748), (330, 722)], 2.0)]
    return tilt(S, 0.5), [s([(212, 352), (492, 352)], 1.0)]


# ---- difficult heads from the applause photograph --------------------
def h092(): return head_34(248, 590, 3.2, 396, "slit", "full", "flat_dark", "open_shout",
                           extras=[s([(180, 250), (230, 180), (286, 140)], 2.8),
                                   s([(520, 246), (470, 178), (416, 140)], 2.8)], roll=-8.0)  # arms up, head UP
def h096(): return head_34(244, 596, 2.8, 388, "slit", "stubble", "curly", "grin",
                           extras=[s([(176, 240), (228, 172), (284, 134)], 2.8),
                                   s([(524, 238), (472, 170), (420, 134)], 2.8)], roll=-7.0)
def h097(): return head_34(258, 588, 3.0, 380, "slit", "full", "curly", "grin",
                           extras=[s([(190, 262), (240, 190), (294, 148)], 2.8)], roll=6.0)
def h098(): return head_34(246, 604, 2.7, 348, "closed", "stubble", "flat_dark", "set",
                           roll=9.0, jaw="normal")                 # head DOWN, clapping
def h099(): return head_34(252, 598, 2.9, 344, "closed", "none", "buzz", "down",
                           extras=hand_on_heart(), roll=11.0)      # bowed, anthem


# ---- repeats from different photographs ------------------------------
def h101():
    """Greg — BEACH photo this time (vs couch/firepit): open grin with
    teeth, wet cropped hair, sun squint. Different weather, same
    architecture: redundant — folds OR squint each carry him."""
    S = []
    S += [s([(238, 302), (248, 214), (312, 168), (384, 164), (448, 200), (470, 278), (474, 316)], 3.2)]
    S += [s([(264, 300), (296, 264), (350, 252), (406, 266), (442, 304)], 2.1)]
    S += [s([(244, 318), (238, 388), (248, 448), (266, 506), (298, 548), (344, 568)], 3.0)]
    S += [s([(472, 322), (476, 392), (466, 452), (450, 508), (418, 550), (354, 570)], 3.6)]
    S += [s([(302, 552), (332, 566), (376, 566), (414, 550)], 2.8)]
    S += [s([(280, 360), (312, 352), (342, 358)], 2.7)]
    S += [s([(378, 356), (410, 348), (440, 356)], 2.7)]
    S += [s([(288, 388), (312, 382), (336, 387)], 2.5)]            # sun squint
    S += [s([(292, 395), (314, 391), (334, 394)], 1.5)]
    S += [s([(380, 386), (404, 380), (428, 385)], 2.5)]
    S += [s([(384, 393), (406, 389), (426, 392)], 1.5)]
    S += [s([(356, 364), (352, 434)], 1.9)]
    S += [s([(330, 446), (354, 457), (380, 445)], 2.4)]
    S += [s([(296, 490), (330, 479), (358, 484), (388, 478), (420, 488)], 3.1)]
    S += [s([(308, 499), (342, 496), (376, 495), (408, 494)], 1.6)]
    S += [s([(306, 508), (340, 524), (376, 525), (412, 504)], 2.9)]
    S += [s([(318, 532), (356, 542), (394, 529)], 2.0)]
    S += [s([(328, 452), (304, 486)], 2.2)]
    S += [s([(388, 450), (414, 482)], 2.2)]
    S += [s([(304, 570), (298, 634)], 2.8)]
    S += [s([(404, 568), (412, 632)], 2.8)]
    S += [s([(252, 690), (320, 650), (358, 644)], 3.0)]            # bare shoulders
    S += [s([(456, 686), (400, 648), (362, 644)], 3.0)]
    return tilt(S, 3.0), [s([(244, 386), (472, 386)], 1.0)]
def h102():
    """Jake — the family-table cover photo (vs the selfie): no
    glasses visible at distance, beard fuller, big open laugh."""
    S = []
    S += [s([(240, 302), (252, 210), (316, 160), (386, 156), (448, 194), (470, 272), (474, 314)], 3.2)]
    S += [s([(268, 296), (306, 260), (354, 248), (404, 262), (438, 298)], 2.0)]
    S += [s([(246, 318), (240, 388), (252, 448)], 2.8)]
    S += [s([(472, 324), (476, 394), (464, 452)], 3.2)]
    S += [s([(252, 448), (262, 524), (292, 580), (334, 606), (380, 606), (416, 580), (444, 524), (464, 452)], 3.8)]
    S += [s([(278, 358), (310, 350), (340, 356)], 2.9)]
    S += [s([(378, 354), (410, 346), (440, 354)], 2.9)]
    S += [s([(286, 390), (312, 382), (336, 388)], 2.6)]
    S += [s([(290, 397), (314, 392), (334, 396)], 1.6)]
    S += [s([(378, 386), (404, 378), (428, 385)], 2.6)]
    S += [s([(382, 393), (406, 388), (426, 392)], 1.6)]
    S += [s([(356, 366), (352, 436)], 1.8)]
    S += [s([(334, 448), (354, 458), (378, 447)], 2.2)]
    S += [s([(310, 496), (338, 486), (360, 490), (384, 484), (410, 494)], 2.9)]   # open laugh in beard
    S += [s([(320, 504), (350, 502), (380, 500), (402, 498)], 1.5)]
    S += [s([(318, 512), (346, 526), (380, 526), (404, 508)], 2.7)]
    S += [s([(318, 606), (312, 654)], 2.4)]
    S += [s([(390, 606), (396, 652)], 2.4)]
    S += [s([(296, 660), (354, 678), (410, 656)], 2.6)]
    return tilt(S, -5.0), [s([(246, 388), (472, 388)], 1.0)]
def h103():
    """Nicolas — frame A this time (arms crossed, 3/4 against the
    wall): the heavy LOW brows hold; mouth closed here, jaw set."""
    S = []
    S += [s([(240, 298), (246, 208), (298, 152), (372, 132), (442, 156), (472, 218), (476, 302)], 3.4)]
    S += [s([(298, 168), (332, 138), (374, 130)], 1.8)]
    S += [s([(262, 292), (300, 258), (352, 246), (406, 260), (442, 294)], 2.0)]
    S += [s([(252, 314), (246, 386), (256, 450), (274, 512), (306, 556), (350, 576)], 2.8)]
    S += [s([(474, 320), (478, 392), (466, 454), (444, 516), (408, 560), (354, 578)], 3.2)]
    S += [s([(310, 560), (336, 574), (372, 574), (398, 560)], 2.2)]
    S += [s([(278, 376), (314, 372), (346, 376)], 3.8)]
    S += [s([(378, 375), (412, 370), (444, 375)], 3.8)]
    S += [s([(288, 394), (314, 388), (340, 394)], 2.4)]
    S += [s([(306, 391), (315, 401), (304, 401)], 2.4)]
    S += [s([(382, 392), (408, 386), (432, 392)], 2.4)]
    S += [s([(400, 389), (409, 399), (398, 399)], 2.4)]
    S += [s([(358, 382), (354, 454)], 2.0)]
    S += [s([(334, 464), (356, 474), (382, 463)], 2.3)]
    S += [s([(320, 510), (346, 504), (362, 507), (378, 502), (400, 509)], 2.7)]
    S += [s([(328, 522), (360, 529), (392, 519)], 2.2)]
    # crossed arms entering low
    S += [s([(240, 690), (310, 650), (392, 648), (462, 686)], 3.4)]
    S += [s([(300, 668), (360, 690), (420, 666)], 2.8)]
    return tilt(S, -2.0), [s([(252, 392), (474, 392)], 1.0)]
def h104():
    """Simona — the brick-wall frame (full sun, hair tucked behind
    one ear this time): deep-set shadow eyes hold; jaw corner holds."""
    S = []
    S += [s([(338, 122), (272, 142), (232, 200), (218, 298), (222, 416), (234, 536), (248, 636)], 3.4)]
    S += [s([(338, 122), (402, 140), (440, 198), (452, 296), (446, 414), (438, 534), (430, 632)], 3.4)]
    S += [s([(338, 126), (336, 168)], 1.6)]
    S += [s([(254, 296), (240, 416), (252, 528)], 1.3)]
    # tucked side: ear shows
    S += [s([(436, 360), (452, 374), (446, 408), (430, 416)], 2.0)]
    S += [s([(272, 330), (266, 398), (276, 458), (286, 506), (308, 548), (348, 566)], 2.8)]
    S += [s([(436, 334), (442, 402), (432, 462), (422, 510), (398, 552), (354, 568)], 3.2)]
    S += [s([(312, 552), (336, 564), (372, 564), (394, 552)], 2.0)]
    S += [s([(286, 372), (316, 366), (344, 372), (350, 378)], 2.9)]
    S += [s([(358, 378), (364, 371), (392, 365), (420, 371)], 2.9)]
    S += [s([(292, 396), (318, 388), (342, 395)], 2.5)]
    S += [s([(308, 391), (318, 402), (306, 402)], 2.8)]
    S += [s([(296, 406), (320, 410), (340, 403)], 1.3)]
    S += [s([(300, 418), (320, 421), (336, 415)], 0.9)]
    S += [s([(366, 394), (392, 386), (416, 393)], 2.5)]
    S += [s([(382, 389), (392, 400), (380, 400)], 2.8)]
    S += [s([(370, 404), (394, 408), (414, 401)], 1.3)]
    S += [s([(374, 416), (394, 419), (410, 413)], 0.9)]
    S += [s([(356, 378), (352, 444)], 1.8)]
    S += [s([(332, 454), (354, 464), (378, 453)], 2.2)]
    S += [s([(314, 500), (340, 494), (356, 497), (372, 492), (396, 499)], 3.2)]
    S += [s([(322, 512), (355, 520), (388, 510)], 2.4)]
    S += [s([(316, 568), (312, 628)], 2.3)]
    S += [s([(390, 568), (394, 626)], 2.3)]
    S += [s([(258, 672), (316, 640), (356, 636)], 2.6)]
    S += [s([(444, 668), (398, 638), (360, 636)], 2.6)]
    return tilt(S, 1.5), [s([(272, 392), (436, 394)], 1.0)]
def h105():
    """Jim — the golf-course wave (vs beret/patio/court): distance
    head under a sun hat, the grin readable at twenty yards. The
    architecture survives scale: redundancy needs no close-up."""
    S = []
    # distance figure: hat + grin + lean frame, knee-up wave
    S += [s([(310, 256), (322, 230), (354, 218), (386, 228), (398, 254)], 2.6)]
    S += [s([(296, 264), (350, 252), (404, 260)], 2.6)]            # brim
    S += [s([(312, 268), (308, 300), (316, 330), (336, 348), (366, 350), (388, 332), (394, 298), (392, 266)], 2.4)]
    S += [s([(330, 296), (342, 292), (352, 295)], 1.5)]            # squint dash L
    S += [s([(362, 294), (374, 290), (384, 294)], 1.5)]
    S += [s([(336, 322), (352, 330), (372, 320)], 2.0)]            # the grin, tiny
    S += [s([(340, 350), (336, 380)], 1.9)]
    S += [s([(366, 350), (372, 378)], 1.9)]
    # polo + raised wave arm
    S += [s([(312, 386), (296, 420), (290, 470)], 2.4)]
    S += [s([(376, 384), (398, 360), (424, 312), (440, 270)], 2.6)]
    S += [s([(440, 270), (456, 252), (470, 258)], 2.2)]            # the wave hand
    S += [s([(290, 470), (302, 478), (368, 478), (380, 470), (376, 384)], 2.4)]
    S += [s([(304, 478), (300, 540), (308, 600)], 2.2)]
    S += [s([(364, 478), (370, 540), (362, 600)], 2.2)]
    S += [s([(296, 606), (316, 610)], 1.9)]
    S += [s([(354, 604), (374, 608)], 1.9)]
    # green horizon
    S += [s([(120, 640), (360, 630), (600, 638)], 1.6)]
    return tilt(S, -1.0), [s([(120, 640), (600, 638)], 0.8)]


HEADS = [("h086", h086), ("h087", h087), ("h088", h088), ("h089", h089),
         ("h090", h090), ("h091", h091), ("h092", h092), ("h093", h093),
         ("h094", h094), ("h095", h095), ("h096", h096), ("h097", h097),
         ("h098", h098), ("h099", h099), ("h100", h100), ("h101", h101),
         ("h102", h102), ("h103", h103), ("h104", h104), ("h105", h105)]

if __name__ == "__main__":
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for name, fn in HEADS:
        if only and name not in only:
            continue
        S, G = fn()
        img = render(S, G, W, H, seed=hash(name) % 999)
        img.save(os.path.join(OUT, f"{name}.png"))
        print("wrote", name)
