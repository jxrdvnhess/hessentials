"""
501-P BATCH 3 — two situations where the world acts on the body.

P5 — FOLDING LAUNDRY (the sheet-fold moment): the woman from P2 —
     same bun, same flats, her second appearance; inhabitants
     accumulate. Arms wide holding the sheet's corners; the sheet is
     the force — a hanging plane that sways, sags between the hands,
     and falls where gravity says. Basket at her feet.

P6 — REACHING FOR A BOOK: the man, high shelf. The shelf decides
     everything: both heels off the floor, the body elongated, the
     free arm drifting out for balance, the hem riding up on the
     reaching side, one finger tipping the spine out.

Doctrine: the situations are teaching the anatomy.
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


def p5_folding():
    S = []
    cx = 450
    # head — her head: contour + the bun from P2
    S.append(st([(cx - 56, 256), (cx - 64, 198), (cx - 40, 144), (cx + 8, 126),
                 (cx + 52, 146), (cx + 66, 202), (cx + 58, 252)], 2.3, swell=0.16))
    S.append(st([(cx - 10, 228), (cx + 14, 246), (cx + 38, 266), (cx + 20, 286),
                 (cx - 2, 272), (cx - 4, 248)], 1.6, swell=0.1))
    S.append(st([(cx - 38, 170), (cx - 20, 220), (cx - 12, 252)], 0.8, swell=0.06))
    S.append(st([(cx - 18, 268), (cx - 20, 312)], 1.5))
    S.append(st([(cx + 22, 270), (cx + 26, 314)], 1.5))
    # both arms up and wide to the sheet's corners — the work is overhead
    S.append(st([(cx - 20, 312), (cx - 86, 330), (cx - 150, 322)], 2.2, swell=0.14))
    S.append(st([(cx + 26, 314), (cx + 90, 334), (cx + 152, 326)], 2.2, swell=0.14))
    S.append(st([(cx - 150, 322), (cx - 196, 300), (cx - 226, 296)], 2.0, swell=0.16))
    S.append(st([(cx + 152, 326), (cx + 198, 304), (cx + 228, 298)], 2.0, swell=0.16))
    S.append(st([(cx - 226, 298), (cx - 240, 288), (cx - 236, 272), (cx - 220, 274)],
                1.5, swell=0.1))                                          # left hand
    S.append(st([(cx + 228, 300), (cx + 242, 290), (cx + 238, 274), (cx + 222, 276)],
                1.5, swell=0.1))                                          # right hand
    # her back and dress under the raised arms — lifted hem, alive
    S.append(st([(cx - 96, 352), (cx - 86, 470), (cx - 100, 600), (cx - 128, 800),
                 (cx - 142, 996)], 2.3, swell=0.18))
    S.append(st([(cx + 100, 356), (cx + 92, 474), (cx + 104, 604), (cx + 130, 804),
                 (cx + 142, 1000)], 2.3, swell=0.18))
    S.append(st([(cx - 142, 996), (cx - 50, 1012), (cx + 50, 1014), (cx + 142, 1000)],
                1.7, swell=0.1))
    S.append(st([(cx - 40, 540), (cx - 48, 740), (cx - 54, 920)], 0.8,
                lead=0.3, tail=0.32, swell=0.05))
    # legs + her flats
    S.append(st([(cx - 92, 1012), (cx - 88, 1120), (cx - 80, 1232)], 1.9, swell=0.12))
    S.append(st([(cx - 42, 1014), (cx - 44, 1122), (cx - 48, 1230)], 1.6, swell=0.1))
    S.append(st([(cx + 56, 1016), (cx + 62, 1126), (cx + 56, 1226)], 1.9, swell=0.12))
    S.append(st([(cx + 98, 1014), (cx + 100, 1122), (cx + 92, 1222)], 1.6, swell=0.1))
    S.append(st([(cx - 84, 1234), (cx - 106, 1252), (cx - 42, 1258), (cx - 38, 1236)],
                1.6, swell=0.1))
    S.append(st([(cx + 58, 1228), (cx + 40, 1248), (cx + 100, 1252), (cx + 96, 1230)],
                1.6, swell=0.1))
    # THE SHEET — hanging from her hands, in front of her; it sags
    # between the grips, falls in two panels past her body, and sways
    # at the bottom. Drawn in segments where her body occludes it.
    S.append(st([(cx - 222, 286), (cx - 150, 306), (cx - 102, 318)], 1.4, swell=0.08))
    S.append(st([(cx + 106, 320), (cx + 154, 308), (cx + 224, 288)], 1.4, swell=0.08))
    S.append(st([(cx - 232, 300), (cx - 262, 560), (cx - 268, 880), (cx - 250, 1148)],
                2.0, swell=0.16))                                         # left fall
    S.append(st([(cx + 234, 302), (cx + 262, 562), (cx + 266, 884), (cx + 246, 1150)],
                2.0, swell=0.16))                                         # right fall
    S.append(st([(cx - 250, 1148), (cx - 190, 1162), (cx - 152, 1154)], 1.5,
                swell=0.1))                                               # bottom, left of her
    S.append(st([(cx + 150, 1156), (cx + 192, 1164), (cx + 246, 1150)], 1.5,
                swell=0.1))                                               # bottom, right of her
    S.append(st([(cx - 196, 330), (cx - 206, 600), (cx - 198, 900), (cx - 188, 1120)],
                0.8, lead=0.25, tail=0.28, swell=0.05))                   # one fold, left
    S.append(st([(cx + 198, 334), (cx + 208, 604), (cx + 200, 904), (cx + 190, 1124)],
                0.8, lead=0.25, tail=0.28, swell=0.05))                   # one fold, right
    # the basket at her feet, one cloth lump over the rim
    S.append(st([(cx + 196, 1180), (cx + 200, 1252), (cx + 332, 1250), (cx + 334, 1178)],
                1.8, swell=0.12))
    S.append(st([(cx + 188, 1180), (cx + 266, 1172), (cx + 342, 1178)], 1.6, swell=0.1))
    S.append(st([(cx + 222, 1176), (cx + 244, 1156), (cx + 274, 1162), (cx + 284, 1176)],
                1.2, swell=0.08))                                         # cloth over rim
    # floor
    S.append(st([(60, 1268), (420, 1262), (840, 1266)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


def p6_reaching():
    S = []
    cx = 360
    STRETCH = -36   # everything rises; the shelf is doing this to him
    # head — his, tilted up toward the book
    hy = 150 + STRETCH
    S.append(st([(cx - 60, hy + 64), (cx - 68, hy + 8), (cx - 44, hy - 50),
                 (cx + 8, hy - 68), (cx + 56, hy - 48), (cx + 72, hy + 10),
                 (cx + 62, hy + 60)], 2.4, swell=0.16))
    S.append(st([(cx - 48, hy + 40), (cx - 16, hy + 48), (cx + 18, hy + 46),
                 (cx + 52, hy + 36)], 1.8, swell=0.1))
    S.append(st([(cx - 20, hy - 40), (cx - 28, hy), (cx - 30, hy + 32)], 0.9,
                swell=0.08))
    # neck stretched
    S.append(st([(cx - 24, hy + 70), (cx - 26, hy + 120)], 1.6))
    S.append(st([(cx + 26, hy + 72), (cx + 30, hy + 122)], 1.6))
    # right arm — straight up the shelf, shoulder pulled high with it
    S.append(st([(cx + 30, hy + 122), (cx + 92, hy + 150), (cx + 134, hy + 128)],
                2.4, swell=0.16))
    S.append(st([(cx + 134, hy + 128), (cx + 158, hy + 20), (cx + 172, hy - 110)],
                2.3, swell=0.18))
    S.append(st([(cx + 110, hy + 168), (cx + 134, hy + 60), (cx + 146, hy - 60)],
                1.5, lead=0.22, swell=0.12))
    S.append(st([(cx + 170, hy - 114), (cx + 178, hy - 138), (cx + 190, hy - 142)],
                1.4, swell=0.1))                                          # finger to the spine
    # left arm — drifting out and down, counterbalance
    S.append(st([(cx - 26, hy + 120), (cx - 90, hy + 158), (cx - 138, hy + 176)],
                2.4, swell=0.16))
    S.append(st([(cx - 138, hy + 176), (cx - 174, hy + 290), (cx - 186, hy + 420)],
                2.1, swell=0.16))
    S.append(st([(cx - 186, hy + 422), (cx - 196, hy + 446), (cx - 184, hy + 460),
                 (cx - 172, hy + 446)], 1.5, swell=0.1))
    # torso — elongated by the reach; hem riding up on the reaching side
    S.append(st([(cx - 110, hy + 200), (cx - 96, hy + 360), (cx - 104, hy + 540),
                 (cx - 100, hy + 640)], 2.2, swell=0.16))
    S.append(st([(cx + 112, hy + 196), (cx + 100, hy + 350), (cx + 108, hy + 520),
                 (cx + 104, hy + 600)], 2.2, swell=0.16))
    S.append(st([(cx - 98, hy + 648), (cx + 6, hy + 644), (cx + 104, hy + 602)],
                1.5, swell=0.1))                                          # hem, lifted right
    # legs — on his toes; calves working
    S.append(st([(cx - 98, hy + 652), (cx - 92, hy + 880), (cx - 102, hy + 1080),
                 (cx - 88, hy + 1216)], 2.4, swell=0.18))
    S.append(st([(cx + 102, hy + 606), (cx + 94, hy + 850), (cx + 102, hy + 1060),
                 (cx + 86, hy + 1212)], 2.4, swell=0.18))
    S.append(st([(cx + 4, hy + 664), (cx + 8, hy + 940), (cx + 6, hy + 1208)],
                1.9, lead=0.2, swell=0.16))
    # heels OFF the floor — the consequence: heel lines above the floor,
    # weight on the forefeet
    S.append(st([(cx - 88, hy + 1216), (cx - 102, hy + 1252), (cx - 48, hy + 1268),
                 (cx - 42, hy + 1238)], 1.7, swell=0.1))
    S.append(st([(cx + 86, hy + 1212), (cx + 72, hy + 1250), (cx + 124, hy + 1264),
                 (cx + 128, hy + 1234)], 1.7, swell=0.1))
    S.append(st([(cx - 96, hy + 1238), (cx - 78, hy + 1230)], 0.9, cs=True, ce=True))
    S.append(st([(cx + 80, hy + 1234), (cx + 98, hy + 1226)], 0.9, cs=True, ce=True))
    # THE BOOKCASE — right of him, close enough that the reach lands;
    # the consequence must touch its cause
    bx = 548
    S.append(st([(bx, 60), (bx + 2, 1380)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(bx + 220, 58), (bx + 222, 1380)], 2.2, swell=0.06, cs=True, ce=True))
    S.append(st([(bx - 4, 240), (bx + 110, 236), (bx + 226, 240)], 1.8, swell=0.08))
    S.append(st([(bx - 4, 560), (bx + 110, 556), (bx + 226, 560)], 1.8, swell=0.08))
    S.append(st([(bx - 4, 880), (bx + 110, 876), (bx + 226, 880)], 1.8, swell=0.08))
    # spines on the reachable shelf — a few, varied, one leaning
    for sx, h_, wgt in ((bx + 24, 188, 1.4), (bx + 52, 174, 1.2), (bx + 76, 192, 1.5),
                        (bx + 104, 180, 1.2), (bx + 158, 186, 1.4), (bx + 186, 170, 1.2)):
        S.append(st([(sx, 238 - h_ + 50), (sx + 2, 236)], wgt, swell=0.06,
                    cs=True, ce=True))
    S.append(st([(bx + 128, 70), (bx + 150, 236)], 1.3, swell=0.06, cs=True,
                ce=True))                                                 # the leaning one
    # the book being tipped — first spine on the shelf, top edge pulled
    # out to meet his fingertip (finger ends near (532, hy-142) = (532, -28))
    S.append(st([(bx - 14, 8), (bx + 8, 234)], 1.6, swell=0.08, cs=True, ce=True))
    S.append(st([(bx - 30, 16), (bx - 6, 238)], 1.6, swell=0.08, cs=True, ce=True))
    S.append(st([(bx - 30, 16), (bx - 14, 8)], 1.2, cs=True, ce=True))
    # floor
    S.append(st([(50, 1392), (420, 1386), (870, 1390)], 1.4, lead=0.08,
                tail=0.08, swell=0.06))
    return S


if __name__ == "__main__":
    for name, build in (("p5_folding_laundry", p5_folding),
                        ("p6_reaching_for_book", p6_reaching)):
        fa = render_strokes(build(), W, H)
        out = np.ones((H, W, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(
            os.path.join(HERE, f"{name}.png"))
        print(name, "done")
