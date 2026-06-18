"""
501-P BATCH 1 — first production sitting. Two entrants, two new
problems. Winner/loser protocol: generate, review, select, reject.

P1 — THE READER BY THE WINDOW (seated; the corpus has never sat down;
     profile view — the corpus has never left the back view)
P2 — THE WOMAN WATERING (standing back view; the corpus is all one
     man; a dress — fabric that drapes instead of fitting)

Anatomy is observation: the reader's spine settles into the chair the
way weight actually settles; the dress falls from the shoulders and
breaks at the body's two contact points, not along a rig.
"""
import os
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from about_figure import render_strokes, PAPER, INK
from about_scenes import scaled

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1040, 1500


def st(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


def reader_by_window():
    """Seated profile, facing the window. The light comes to the book."""
    S = []
    cx, cy = 430, 0  # loose origin

    # ---- THE CHAIR — side view, honest and plain ----
    S.append(st([(248, 640), (242, 880), (246, 1108)], 2.2, swell=0.1))     # back post
    S.append(st([(248, 640), (262, 700), (286, 760)], 1.8, swell=0.1))      # back, top curl
    S.append(st([(258, 720), (270, 880), (276, 1000)], 1.6, swell=0.1))     # back cushion
    S.append(st([(276, 1000), (420, 1006), (560, 1000)], 2.0, swell=0.1))   # seat
    S.append(st([(560, 1000), (584, 1040), (588, 1108)], 1.8, swell=0.1))   # front rail
    S.append(st([(584, 1108), (588, 1230)], 1.8, cs=True))                  # front leg
    S.append(st([(252, 1108), (250, 1230)], 1.8, cs=True))                  # back leg
    S.append(st([(246, 1106), (420, 1110), (590, 1106)], 1.4, swell=0.08))  # rail

    # ---- THE READER — settled, head bowed to the book ----
    # head, profile right: skull, brow, nose hint, jaw — one line
    S.append(st([(404, 480), (380, 420), (392, 352), (444, 322), (496, 344),
                 (510, 392), (502, 414), (512, 432), (500, 446), (478, 470)],
                2.4, swell=0.16))
    S.append(st([(398, 360), (430, 338), (466, 342)], 0.9, swell=0.08))     # hair sweep
    S.append(st([(452, 452), (470, 464)], 1.0, swell=0.06))                 # jaw → ear hint
    # nape into the curved back — the settle line, one breath
    S.append(st([(404, 478), (366, 560), (330, 680), (318, 800), (326, 920),
                 (340, 1000)], 2.6, swell=0.2))
    # chest line under the bowed head
    S.append(st([(474, 488), (452, 560), (430, 640)], 1.8, swell=0.14))
    # thigh, horizontal to the knee; shin drops; foot on the floor
    S.append(st([(348, 1004), (470, 990), (586, 974)], 2.4, swell=0.16))    # thigh, top
    S.append(st([(586, 974), (606, 1040), (598, 1108)], 2.2, swell=0.14))   # knee
    S.append(st([(598, 1108), (592, 1180), (588, 1238)], 2.0, swell=0.12))  # shin
    S.append(st([(588, 1238), (650, 1244), (664, 1232)], 1.7, swell=0.1))   # foot
    S.append(st([(420, 1004), (470, 1014), (540, 1010)], 1.5, swell=0.1))   # lap fold
    # arms to the book — forearms converge on it
    S.append(st([(438, 640), (470, 720), (520, 780)], 1.9, swell=0.14))     # near arm
    S.append(st([(352, 700), (420, 760), (492, 792)], 1.6, lead=0.2,
                swell=0.12))                                                # far arm
    # the book — held open, two planes
    S.append(st([(508, 770), (552, 752), (594, 760)], 1.8, swell=0.1))
    S.append(st([(508, 774), (548, 788), (590, 778)], 1.8, swell=0.1))
    S.append(st([(550, 752), (549, 788)], 1.0, swell=0.06))                 # spine

    # ---- THE WINDOW — tall, plain; the light comes to the reader ----
    S.append(st([(760, 180), (762, 920)], 2.2, swell=0.08, cs=True, ce=True))
    S.append(st([(948, 184), (949, 916)], 2.2, swell=0.08, cs=True, ce=True))
    S.append(st([(760, 182), (854, 178), (948, 184)], 2.2, swell=0.08))
    S.append(st([(748, 926), (856, 922), (960, 926)], 2.4, swell=0.1))      # sill
    S.append(st([(854, 186), (855, 920)], 1.4, swell=0.06))                 # mullion
    S.append(st([(764, 540), (946, 542)], 1.4, swell=0.06))                 # transom
    # thrown light — edges only, reaching the chair's feet
    S.append(st([(768, 936), (700, 1120), (618, 1252)], 0.7, swell=0.04,
                lead=0.3, tail=0.32))
    S.append(st([(940, 932), (900, 1140), (852, 1264)], 0.7, swell=0.04,
                lead=0.3, tail=0.32))
    S.append(st([(622, 1248), (740, 1262), (848, 1262)], 0.6, swell=0.03,
                lead=0.34, tail=0.36))

    # floor line
    S.append(st([(60, 1268), (420, 1262), (760, 1266), (1000, 1262)], 1.4,
                lead=0.08, tail=0.08, swell=0.06))
    return S


def woman_watering():
    """Standing back view, weight settled left, the can reaching the
    plant. The dress drapes — falls from the shoulders, touches at the
    hips, breaks into folds below."""
    S = []
    cx = 560

    # ---- HEAD — low bun; the neck shows ----
    S.append(st([(cx - 56, 196), (cx - 64, 138), (cx - 40, 84), (cx + 8, 66),
                 (cx + 52, 86), (cx + 66, 142), (cx + 58, 192)], 2.3, swell=0.16))
    S.append(st([(cx - 10, 168), (cx + 14, 186), (cx + 38, 206), (cx + 20, 226),
                 (cx - 2, 212), (cx - 4, 188)], 1.6, swell=0.1))             # bun
    S.append(st([(cx - 38, 110), (cx - 20, 160), (cx - 12, 192)], 0.8, swell=0.06))
    # neck — longer, lighter
    S.append(st([(cx - 18, 208), (cx - 20, 258)], 1.5))
    S.append(st([(cx + 22, 210), (cx + 26, 260)], 1.5))

    # ---- SHOULDERS — narrower; the working arm lifts the can left ----
    S.append(st([(cx - 20, 258), (cx - 74, 286), (cx - 122, 304)], 2.2, swell=0.14))
    S.append(st([(cx + 26, 260), (cx + 82, 292), (cx + 126, 312)], 2.2, swell=0.14))
    # raised left arm to the can — bare arm, real taper
    S.append(st([(cx - 122, 304), (cx - 178, 280), (cx - 224, 246)], 2.0, swell=0.18))
    S.append(st([(cx - 104, 330), (cx - 162, 308), (cx - 204, 280)], 1.4,
                lead=0.22, swell=0.12))
    S.append(st([(cx - 228, 250), (cx - 244, 240), (cx - 242, 220), (cx - 224, 218),
                 (cx - 218, 236)], 1.5, swell=0.1))                          # hand
    # hanging right arm
    S.append(st([(cx + 126, 312), (cx + 142, 420), (cx + 134, 540), (cx + 120, 620)],
                1.9, swell=0.16))
    S.append(st([(cx + 120, 622), (cx + 130, 648), (cx + 118, 662), (cx + 106, 648)],
                1.4, swell=0.1))

    # ---- THE DRESS — falls from the shoulders, touches at the hips,
    # breaks below; the hem swings slightly toward the reach ----
    S.append(st([(cx - 96, 322), (cx - 88, 470), (cx - 102, 600), (cx - 132, 800),
                 (cx - 148, 1014)], 2.3, swell=0.18))                        # left fall
    S.append(st([(cx + 104, 334), (cx + 96, 480), (cx + 108, 610), (cx + 134, 810),
                 (cx + 146, 1020)], 2.3, swell=0.18))                        # right fall
    S.append(st([(cx - 148, 1014), (cx - 60, 1030), (cx + 40, 1032),
                 (cx + 146, 1020)], 1.7, swell=0.1))                         # hem
    S.append(st([(cx - 44, 560), (cx - 52, 760), (cx - 58, 940)], 0.8,
                lead=0.3, tail=0.32, swell=0.05))                            # one fold
    S.append(st([(cx + 52, 620), (cx + 58, 820), (cx + 62, 980)], 0.8,
                lead=0.3, tail=0.32, swell=0.05))                            # one fold

    # ---- LEGS below the hem — calves, settled weight left ----
    S.append(st([(cx - 96, 1032), (cx - 92, 1130), (cx - 84, 1238)], 1.9, swell=0.12))
    S.append(st([(cx - 44, 1034), (cx - 46, 1130), (cx - 50, 1236)], 1.6, swell=0.1))
    S.append(st([(cx + 58, 1034), (cx + 66, 1140), (cx + 60, 1230)], 1.9, swell=0.12))
    S.append(st([(cx + 102, 1032), (cx + 104, 1136), (cx + 96, 1226)], 1.6, swell=0.1))
    # flats
    S.append(st([(cx - 88, 1240), (cx - 110, 1258), (cx - 44, 1264), (cx - 40, 1242)],
                1.6, swell=0.1))
    S.append(st([(cx + 62, 1232), (cx + 44, 1252), (cx + 104, 1256), (cx + 100, 1234)],
                1.6, swell=0.1))

    # ---- THE CAN — body, handle, spout reaching the plant ----
    S.append(st([(cx - 320, 196), (cx - 318, 252)], 1.8, swell=0.1))
    S.append(st([(cx - 252, 192), (cx - 252, 248)], 1.8, swell=0.1))
    S.append(st([(cx - 320, 196), (cx - 286, 188), (cx - 252, 192)], 1.5, swell=0.08))
    S.append(st([(cx - 318, 252), (cx - 284, 258), (cx - 252, 248)], 1.5, swell=0.08))
    S.append(st([(cx - 256, 210), (cx - 240, 200), (cx - 228, 222)], 1.3, swell=0.08))  # handle to hand
    S.append(st([(cx - 318, 210), (cx - 360, 240), (cx - 384, 268)], 1.4, swell=0.08))  # spout, tipped

    # ---- THE PLANT on its stand — receiving ----
    S.append(st([(cx - 470, 330), (cx - 438, 296), (cx - 414, 318)], 1.2, swell=0.1))   # leaf
    S.append(st([(cx - 452, 332), (cx - 470, 290), (cx - 488, 318)], 1.2, swell=0.1))   # leaf
    S.append(st([(cx - 432, 334), (cx - 408, 306)], 1.0, swell=0.08))                   # leaf
    S.append(st([(cx - 488, 340), (cx - 484, 392), (cx - 416, 394), (cx - 412, 340)],
                1.7, swell=0.1))                                                        # pot
    S.append(st([(cx - 496, 340), (cx - 450, 336), (cx - 404, 340)], 1.4, swell=0.08))  # rim
    S.append(st([(cx - 504, 400), (cx - 450, 396), (cx - 396, 400)], 1.7, swell=0.1))   # stand top
    S.append(st([(cx - 482, 402), (cx - 478, 1248)], 1.6, swell=0.08, cs=True))         # stand leg
    S.append(st([(cx - 420, 402), (cx - 416, 1248)], 1.6, swell=0.08, cs=True))         # stand leg

    # floor line
    S.append(st([(40, 1262), (400, 1256), (760, 1260), (1000, 1256)], 1.4,
                lead=0.08, tail=0.08, swell=0.06))
    return S


if __name__ == "__main__":
    for name, build in (("p1_reader_by_window", reader_by_window),
                        ("p2_woman_watering", woman_watering)):
        fa = render_strokes(build(), W, H)
        out = np.ones((H, W, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
            os.path.join(HERE, f"{name}.png"))
        print(name, "done")
