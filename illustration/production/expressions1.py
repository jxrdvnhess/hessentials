"""
501-P EXPRESSION STUDIES — tranche 1 of the twenty. Six faces, six
emotions, no rooms, no objects, no theories. Observe, draw, judge.

The first front-facing faces in the corpus. Each is hand-placed, not
rigged — different face shapes, different ages. Emotion carried where
it actually lives: the brows, the lids, the mouth's asymmetry, the
head's tilt. Asymmetry everywhere; the corpse lesson holds for faces
more than anywhere.

  E1 relief        — eyes closed, brows lifted and softening, the
                     exhale mouth; chin slightly up
  E2 concentration — brows drawn down and in, lids narrowed, mouth
                     small and held; everything converges
  E3 exhaustion    — heavy half lids, slack brows, the under-eye
                     weight, mouth slightly open; an older face
  E4 amusement     — one brow up, crescent eyes pushed up from below,
                     the smile wider on one side
  E5 uncertainty   — inner brows raised, eyes aside, mouth pulled
                     small to one corner
  E6 contentment   — an older woman; soft closed eyes, the smallest
                     symmetric smile earned by round cheeks
"""
import os
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from about_figure import render_strokes, PAPER, INK

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PH = 400, 500


def st(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


def e1_relief():
    S = []
    # head, chin lifted — the jaw rises, more throat shows
    S.append(st([(128, 318), (116, 232), (140, 142), (200, 112), (262, 140),
                 (286, 230), (272, 316), (236, 366), (196, 378), (156, 360)],
                2.2, swell=0.14))
    S.append(st([(138, 168), (196, 134), (258, 166)], 1.6, swell=0.1))      # hairline
    S.append(st([(120, 250), (108, 270), (118, 292)], 1.2, swell=0.08))     # ear
    S.append(st([(276, 248), (290, 268), (280, 290)], 1.2, swell=0.08))
    # brows lifted, softening outward
    S.append(st([(150, 226), (172, 214), (194, 220)], 1.4, swell=0.1))
    S.append(st([(212, 218), (234, 212), (256, 222)], 1.4, swell=0.1))
    # eyes closed — two settled curves, lashes down
    S.append(st([(154, 252), (174, 260), (194, 254)], 1.5, swell=0.1))
    S.append(st([(212, 252), (232, 258), (252, 250)], 1.5, swell=0.1))
    # nose — one quiet stroke
    S.append(st([(202, 258), (198, 292), (206, 300)], 1.1, swell=0.08))
    # the exhale mouth — parted, soft, corners loose
    S.append(st([(170, 330), (200, 338), (232, 328)], 1.5, swell=0.1))
    S.append(st([(180, 344), (202, 348), (224, 342)], 1.0, swell=0.06))
    return S


def e2_concentration():
    S = []
    S.append(st([(126, 300), (118, 210), (146, 128), (204, 102), (260, 130),
                 (284, 212), (274, 302), (240, 360), (200, 372), (160, 356)],
                2.2, swell=0.14))
    S.append(st([(134, 150), (200, 118), (264, 152)], 1.6, swell=0.1))
    S.append(st([(150, 142), (162, 196)], 0.8, swell=0.06))                 # hair fall
    # brows down and in — the convergence
    S.append(st([(150, 230), (176, 222), (198, 232)], 1.7, swell=0.12))
    S.append(st([(212, 232), (234, 220), (258, 226)], 1.7, swell=0.12))
    S.append(st([(200, 226), (204, 238)], 0.9, swell=0.06))                 # the knit
    # narrowed lids, iris marks just under them
    S.append(st([(156, 252), (176, 248), (196, 252)], 1.4, swell=0.1))
    S.append(st([(214, 252), (234, 246), (252, 250)], 1.4, swell=0.1))
    S.append(st([(174, 254), (177, 261)], 1.8, cs=True, ce=True))
    S.append(st([(231, 253), (234, 260)], 1.8, cs=True, ce=True))
    S.append(st([(204, 256), (200, 296), (208, 304)], 1.1, swell=0.08))
    # mouth held small, a touch off-center
    S.append(st([(182, 332), (204, 336), (222, 330)], 1.5, swell=0.1))
    return S


def e3_exhaustion():
    S = []
    # a longer, older face
    S.append(st([(132, 322), (122, 220), (146, 130), (202, 104), (258, 132),
                 (280, 222), (272, 324), (240, 382), (202, 394), (164, 380)],
                2.2, swell=0.14))
    S.append(st([(142, 152), (202, 124), (260, 154)], 1.4, swell=0.08))     # thin hairline
    # slack brows — flat, fallen
    S.append(st([(152, 238), (174, 238), (196, 240)], 1.3, swell=0.08))
    S.append(st([(214, 240), (236, 238), (256, 240)], 1.3, swell=0.08))
    # heavy half lids — the line IS the lid, eyes barely beneath
    S.append(st([(156, 258), (176, 260), (194, 258)], 1.6, swell=0.1))
    S.append(st([(214, 258), (234, 260), (252, 258)], 1.6, swell=0.1))
    S.append(st([(160, 274), (176, 278), (192, 274)], 0.9, swell=0.06))     # under-eye
    S.append(st([(216, 274), (232, 278), (248, 274)], 0.9, swell=0.06))
    S.append(st([(204, 262), (198, 304), (208, 312)], 1.1, swell=0.08))
    # cheek lines — the day, recorded
    S.append(st([(160, 320), (152, 344)], 0.8, swell=0.05))
    S.append(st([(246, 320), (254, 344)], 0.8, swell=0.05))
    # mouth open slightly, fallen at the corners
    S.append(st([(176, 344), (202, 350), (228, 344)], 1.4, swell=0.1))
    S.append(st([(186, 358), (204, 362), (220, 357)], 0.9, swell=0.06))
    return S


def e4_amusement():
    S = []
    # a younger, rounder face, tilted a few degrees
    S.append(st([(134, 296), (124, 212), (150, 136), (208, 112), (264, 142),
                 (284, 224), (270, 306), (236, 354), (196, 364), (158, 348)],
                2.2, swell=0.14))
    S.append(st([(140, 162), (204, 128), (266, 168)], 1.6, swell=0.1))
    S.append(st([(258, 150), (276, 210), (272, 262)], 1.2, swell=0.08))     # hair past ear
    # one brow up — the tell
    S.append(st([(150, 218), (174, 206), (196, 214)], 1.5, swell=0.1))      # raised
    S.append(st([(214, 228), (236, 222), (256, 228)], 1.4, swell=0.1))      # resting
    # crescent eyes — pushed up from below by the smile
    S.append(st([(154, 248), (174, 242), (194, 248)], 1.5, swell=0.1))
    S.append(st([(158, 256), (174, 252), (190, 256)], 0.9, swell=0.06))     # lower push
    S.append(st([(214, 250), (232, 244), (250, 250)], 1.5, swell=0.1))
    S.append(st([(218, 258), (232, 254), (246, 258)], 0.9, swell=0.06))
    S.append(st([(202, 252), (198, 288), (206, 296)], 1.1, swell=0.08))
    # the smile, wider on the left; one cheek crease
    S.append(st([(162, 316), (196, 332), (232, 322)], 1.7, swell=0.12))
    S.append(st([(156, 306), (162, 318)], 0.9, swell=0.06))                 # crease
    return S


def e5_uncertainty():
    S = []
    S.append(st([(130, 304), (120, 214), (146, 132), (202, 106), (258, 134),
                 (282, 216), (272, 306), (238, 360), (198, 372), (160, 356)],
                2.2, swell=0.14))
    S.append(st([(138, 154), (200, 122), (262, 156)], 1.6, swell=0.1))
    # inner brows raised — the oblique worry
    S.append(st([(154, 234), (178, 222), (198, 218)], 1.5, swell=0.1))
    S.append(st([(212, 218), (234, 224), (256, 234)], 1.5, swell=0.1))
    # eyes open, looking aside — pupils carried right
    S.append(st([(154, 248), (174, 242), (194, 248)], 1.4, swell=0.1))
    S.append(st([(158, 260), (176, 264), (192, 260)], 1.0, swell=0.06))
    S.append(st([(214, 246), (234, 240), (252, 246)], 1.4, swell=0.1))
    S.append(st([(218, 258), (236, 262), (250, 258)], 1.0, swell=0.06))
    S.append(st([(184, 250), (188, 258)], 2.2, cs=True, ce=True))           # pupil, right
    S.append(st([(242, 248), (246, 256)], 2.2, cs=True, ce=True))           # pupil, right
    S.append(st([(202, 254), (198, 292), (206, 300)], 1.1, swell=0.08))
    # mouth pulled small to one corner
    S.append(st([(186, 332), (208, 336), (224, 328), (230, 322)], 1.4, swell=0.1))
    return S


def e6_contentment():
    S = []
    # an older woman — rounder, the bun from somewhere familiar
    S.append(st([(136, 298), (126, 216), (152, 142), (206, 118), (260, 146),
                 (280, 222), (268, 300), (236, 348), (198, 358), (162, 344)],
                2.2, swell=0.14))
    S.append(st([(144, 166), (204, 134), (262, 170)], 1.5, swell=0.1))
    S.append(st([(196, 112), (216, 96), (240, 102), (244, 122)], 1.4, swell=0.1))  # bun
    # soft brows, soft closed eyes
    S.append(st([(154, 228), (176, 222), (196, 226)], 1.3, swell=0.08))
    S.append(st([(214, 226), (236, 220), (254, 226)], 1.3, swell=0.08))
    S.append(st([(158, 250), (176, 256), (192, 250)], 1.4, swell=0.1))
    S.append(st([(216, 250), (232, 256), (248, 250)], 1.4, swell=0.1))
    S.append(st([(202, 254), (198, 288), (206, 296)], 1.1, swell=0.08))
    # round cheeks — two short rises
    S.append(st([(150, 290), (158, 280)], 0.9, swell=0.06))
    S.append(st([(248, 288), (242, 278)], 0.9, swell=0.06))
    # the smallest smile, very nearly symmetric — earned here
    S.append(st([(174, 318), (200, 326), (228, 317)], 1.5, swell=0.1))
    return S


if __name__ == "__main__":
    faces = [("E1 relief", e1_relief), ("E2 concentration", e2_concentration),
             ("E3 exhaustion", e3_exhaustion), ("E4 amusement", e4_amusement),
             ("E5 uncertainty", e5_uncertainty), ("E6 contentment", e6_contentment)]
    panels = []
    for name, build in faces:
        fa = render_strokes(build(), PW, PH)
        out = np.ones((PH, PW, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        panels.append(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))
    gap = 12
    sheet = Image.new("RGB", (PW * 3 + gap * 4, PH * 2 + gap * 3),
                      tuple(int(v) for v in PAPER))
    for i, p in enumerate(panels):
        sheet.paste(p, (gap + (i % 3) * (PW + gap), gap + (i // 3) * (PH + gap)))
    sheet.save(os.path.join(HERE, "expressions1_sheet.png"))
    print("done")
