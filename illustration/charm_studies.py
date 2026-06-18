"""
501-13 — CHARM STUDIES on the painter figure. INSTRUMENT, NOT ASSET.

Faculty direction: the figure's job is not to become more important
(the 90/10 ratio is probably correct) but to become more lovable.
Less technical illustration, more Jansson / Blake / Sempé / Steinberg
inhabitant: affection won with two lines instead of twenty, posture
memorable before anatomy.

Four panels, same painting stance, same scale:

  v0  the current rig figure (baseline)
  v1  ECONOMY — same proportions, the stroke count roughly halved;
      long continuous contours instead of dutiful part-by-part lines
  v2  ECONOMY + STORYBOOK — head a shade larger, weight shift
      amplified, feet splayed; the heel-drift the faculty liked,
      promoted from accident to posture
  v3  v2 + ABSORPTION — head craned up at the work, slight backward
      lean; the body shaped by attention rather than by anatomy

The charm hypothesis under test: affection lives where observation
overrides the rig. v1 tests economy alone; v2 adds observed posture;
v3 adds the verb (looking) to the body itself.
"""
import os
import numpy as np
from PIL import Image
from about_figure import figure_strokes, render_strokes, save_paper, PAPER, INK, SAMPLES
from about_scenes import s, scaled

PW, PH = 560, 800   # one panel
K = 0.46            # figure scale inside panel
DY = 60


def charm_figure(cx, head=1.0, weight=1.0, crane=0.0, observed=False):
    """The charm rig: ~17 strokes against the canonical ~40.

    head   — head-size multiplier (1.0 canonical, 1.15 storybook)
    weight — weight-shift amplifier (1.0 canonical, 1.6 amplified)
    crane  — upward attention: head rise + backward lean, 0..1
    """
    S = []
    def a(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
        S.append(dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                      smoothing=sm, cap_start=cs, cap_end=ce))

    hr = 74 * head                 # head half-width
    hy = 130 - 26 * crane          # head center rises as he cranes
    lean = 14 * crane              # hips drift forward of shoulders
    hip = 10 * weight              # weight-shift offset

    # head — the canonical contour survives (it was already good);
    # nape kept high so the head reads as hair-over-skull, not balloon
    a([(cx - hr * 0.86, hy + 66), (cx - hr * 0.97, hy - 12), (cx - hr * 0.62, hy - 70),
       (cx + hr * 0.05, hy - 82), (cx + hr * 0.7, hy - 58), (cx + hr * 0.99, hy + 2),
       (cx + hr * 0.86, hy + 64)], 2.6, swell=0.16)
    a([(cx - hr * 0.66, hy + 38 - 8 * crane), (cx - hr * 0.05, hy + 50 - 14 * crane),
       (cx + hr * 0.64, hy + 34 - 6 * crane)], 1.8, swell=0.1)          # nape, high
    a([(cx + hr * 0.99, hy + 4), (cx + hr * 1.12, hy + 22), (cx + hr * 0.95, hy + 38)],
      1.3, swell=0.08)                                                   # one ear
    if observed:
        # the observed details the rig-deletion went cold without:
        # hair direction (two light strokes) and the collar's back arc
        a([(cx - hr * 0.28, hy - 62), (cx - hr * 0.38, hy - 14), (cx - hr * 0.4, hy + 26)],
          0.9, swell=0.08)
        a([(cx + hr * 0.22, hy - 66), (cx + hr * 0.3, hy - 18), (cx + hr * 0.27, hy + 22)],
          0.9, swell=0.08)
        a([(cx - 36, hy + 96), (cx - 2, hy + 88), (cx + 38, hy + 98)], 1.3, swell=0.08)

    # neck → shoulder, left side (short, its own line; shoulders kept
    # low so he has a neck — hunch was reading as a sack)
    a([(cx - 30, hy + 80), (cx - 56, 264 - 10 * crane), (cx - 106, 315 - 12 * crane)],
      2.4, swell=0.2)
    # the raised arm — the VERB. A clear diagonal with air between the
    # arm and the head; the grip is out at arm's length, never beside
    # the ear.
    a([(cx - 106, 315 - 12 * crane), (cx - 138, 262 - 14 * crane),
       (cx - 152, 228 - 16 * crane)], 2.6, swell=0.2)
    a([(cx - 76, 338 - 10 * crane), (cx - 110, 286 - 12 * crane),
       (cx - 124, 254 - 14 * crane)], 1.8, lead=0.22, swell=0.14)
    # fist — small closed knot at the pole, clear of the head
    a([(cx - 146, 236 - 16 * crane), (cx - 160, 224 - 16 * crane),
       (cx - 158, 202 - 16 * crane), (cx - 138, 200 - 16 * crane),
       (cx - 132, 220 - 16 * crane)], 1.7, swell=0.1)
    # right contour — neck into trap into hanging arm, ONE line
    # (shoulder dropped to keep the neck)
    a([(cx + 32, hy + 84), (cx + 104, 330), (cx + 146, 440), (cx + 152, 610),
       (cx + 138, 786)], 2.6, swell=0.22)
    a([(cx + 138, 788), (cx + 148, 812), (cx + 136, 826), (cx + 124, 810)],
      1.6, swell=0.1)                                                   # blunt hand
    # torso left — armpit to hip, leaning with the crane
    a([(cx - 100, 340), (cx - 116 + lean * 0.4, 480),
       (cx - 104 + lean + hip, 740)], 2.2, swell=0.18)
    # hem — one tilted hint
    a([(cx - 102 + lean + hip, 748), (cx + 6 + lean, 760), (cx + 122 + lean, 744)],
      1.5, swell=0.1)
    # legs — outer lines only, weight leg plumb, free leg drifting
    a([(cx + 120 + lean, 748), (cx + 112 + hip, 1010), (cx + 104 + hip, 1290),
       (cx + 102 + hip, 1420)], 2.4, swell=0.18)
    a([(cx - 100 + lean + hip, 752), (cx - 86, 1020), (cx - 64 - hip, 1290),
       (cx - 56 - hip * 1.4, 1424)], 2.4, swell=0.2)
    # inner leg — ONE line for both
    a([(cx + 12 + lean, 766), (cx + 22, 1060), (cx + 26, 1420)], 1.9,
      lead=0.2, swell=0.16)
    # feet — splayed with the weight; the heel-drift, promoted
    a([(cx - 60 - hip * 1.4, 1424), (cx - 84 - hip * 2.2, 1448),
       (cx - 30, 1452), (cx - 24, 1430)], 1.7, swell=0.1)
    a([(cx + 102 + hip, 1420), (cx + 116 + hip * 1.6, 1446), (cx + 50, 1450),
       (cx + 46, 1426)], 1.7, swell=0.1)
    return S


def presence_figure(cx):
    """v5 — PRESENCE. Built from the fashion-croquis + Sempé study
    (2026-06-11): posture is identity.

    The three mechanisms v4 lacked:
      counterpose — shoulders and hips tilt in OPPOSITION; the raised-
        arm shoulder rides high, the free shoulder drops, the weight
        hip rises against them
      plumb — the weight ankle lands under the pit of the neck, so he
        is settled, not planted
      spine — a soft continuous curve, never a vertical; the long
        right line runs neck → shoulder → back → hip in one breath

    Same economy as v4 (~20 strokes), same observed details. Nothing
    added; everything re-weighted.
    """
    S = []
    def a(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
        S.append(dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                      smoothing=sm, cap_start=cs, cap_end=ce))

    hr, hy = 80, 112    # storybook head, crane held

    # head — observed: contour, high nape, ear, two hair strokes
    a([(cx - hr * 0.86, hy + 66), (cx - hr * 0.97, hy - 12), (cx - hr * 0.62, hy - 70),
       (cx + hr * 0.05, hy - 82), (cx + hr * 0.7, hy - 58), (cx + hr * 0.99, hy + 2),
       (cx + hr * 0.86, hy + 64)], 2.6, swell=0.16)
    a([(cx - hr * 0.66, hy + 32), (cx - hr * 0.05, hy + 42), (cx + hr * 0.64, hy + 28)],
      1.8, swell=0.1)
    a([(cx + hr * 0.99, hy + 4), (cx + hr * 1.12, hy + 22), (cx + hr * 0.95, hy + 38)],
      1.3, swell=0.08)
    a([(cx - hr * 0.28, hy - 62), (cx - hr * 0.38, hy - 14), (cx - hr * 0.4, hy + 20)],
      0.9, swell=0.08)
    a([(cx + hr * 0.22, hy - 66), (cx + hr * 0.3, hy - 18), (cx + hr * 0.27, hy + 16)],
      0.9, swell=0.08)
    a([(cx - 36, hy + 100), (cx - 2, hy + 92), (cx + 38, hy + 102)], 1.3, swell=0.08)  # collar

    # left side — neck to HIGH shoulder, then the working arm
    a([(cx - 30, hy + 86), (cx - 54, 246), (cx - 102, 292)], 2.4, swell=0.2)
    a([(cx - 102, 292), (cx - 136, 248), (cx - 152, 216)], 2.6, swell=0.2)
    a([(cx - 74, 318), (cx - 108, 270), (cx - 124, 242)], 1.8, lead=0.22, swell=0.14)
    a([(cx - 146, 224), (cx - 160, 212), (cx - 158, 190), (cx - 138, 188),
       (cx - 132, 208)], 1.7, swell=0.1)                                  # fist

    # right side — the Sempé line: neck → DROPPED shoulder → soft back
    # → hip, one breath, gently bowed
    a([(cx + 32, hy + 90), (cx + 92, 352), (cx + 134, 480), (cx + 140, 620),
       (cx + 122, 748)], 2.6, swell=0.22)
    # the hanging arm — eased off the dropped shoulder, hand low
    a([(cx + 88, 360), (cx + 148, 540), (cx + 144, 700), (cx + 128, 792)],
      2.0, lead=0.18, swell=0.16)
    a([(cx + 128, 794), (cx + 138, 818), (cx + 126, 832), (cx + 114, 816)],
      1.6, swell=0.1)
    # torso left — waist eased in, hip out (counterpose against shoulders)
    a([(cx - 76, 348), (cx - 96, 500), (cx - 110, 742)], 2.2, swell=0.18)
    # hem — tilted WITH the weight hip (right hip rides high)
    a([(cx - 108, 756), (cx + 4, 760), (cx + 120, 740)], 1.5, swell=0.1)

    # weight leg (right) — ankle pulled under the neck pit: settled
    a([(cx + 120, 742), (cx + 84, 1000), (cx + 54, 1260), (cx + 44, 1422)],
      2.4, swell=0.18)
    # free leg (left) — knee drifting out, soft break, heel landing easy
    a([(cx - 108, 754), (cx - 120, 1010), (cx - 104, 1060), (cx - 96, 1280),
       (cx - 92, 1408)], 2.4, swell=0.2)
    # inner line, one for both
    a([(cx + 2, 772), (cx + 12, 1080), (cx + 18, 1418)], 1.9, lead=0.2, swell=0.16)

    # feet — weight foot flat beneath him; free foot easy, heel out,
    # a breath off the ground
    a([(cx + 42, 1422), (cx + 60, 1446), (cx + 10, 1450), (cx + 4, 1428)],
      1.7, swell=0.1)
    a([(cx - 92, 1408), (cx - 118, 1434), (cx - 64, 1442), (cx - 58, 1416)],
      1.7, swell=0.1)
    return S


def pole_and_roller(cx, crane=0.0):
    S = []
    top_x = cx - 250 - 30 * crane
    gy = 218 - 16 * crane
    S.append(s([(top_x, 30), ((top_x + cx - 146) / 2, (30 + gy) / 2 + 14),
                (cx - 146, gy), (cx - 136, gy + 32)], 1.5, swell=0.06, cs=True))
    S.append(s([(top_x - 48, 16), (top_x, 12), (top_x + 48, 15)], 1.7, swell=0.1))
    S.append(s([(top_x - 50, 32), (top_x - 2, 28), (top_x + 46, 31)], 1.7, swell=0.1))
    return S


if __name__ == "__main__":
    panels = []
    variants = [
        ("v0 rig", None),
        ("v1 economy", dict(head=1.0, weight=1.0, crane=0.0)),
        ("v2 storybook", dict(head=1.08, weight=1.6, crane=0.0)),
        ("v3 absorption", dict(head=1.08, weight=1.6, crane=1.0)),
        ("v4 synthesis", dict(head=1.08, weight=1.6, crane=0.6, observed=True)),
    ]
    for name, kw in variants:
        if kw is None:
            S = scaled(figure_strokes(0, left_arm="raised"), K, PW // 2 + 20, DY)
            S += scaled(pole_and_roller(0), K, PW // 2 + 20, DY)
        else:
            S = scaled(charm_figure(0, **kw), K, PW // 2 + 20, DY)
            S += scaled(pole_and_roller(0, kw.get("crane", 0)), K, PW // 2 + 20, DY)
        fa = render_strokes(S, PW, PH)
        out = np.ones((PH, PW, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        panels.append(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))

    gap = 16
    sheet = Image.new("RGB", (PW * len(panels) + gap * (len(panels) + 1), PH + gap * 2),
                      tuple(int(v) for v in PAPER))
    for i, p in enumerate(panels):
        sheet.paste(p, (gap + i * (PW + gap), gap))
    sheet.save(os.path.join(SAMPLES, "charm_studies_sheet.png"))
    print("done")
