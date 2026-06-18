"""
501-14 — FIVE MEN PAINTING THE SAME WALL. INSTRUMENT, NOT ASSET.

Faculty exercise: same page, same wall, same task — different
inhabitants. Not costumes, not ages, not identities. Different ways
of standing. The question: how much of a person can posture alone
carry?

The working hypothesis, operationalized: if presence is created when
posture reveals attention, then attention should be expressible as
posture PARAMETERS — and six attentions should produce six men from
one rig with nothing added.

(The assignment names six states under a five-man title; all six are
brought. The deeply absorbed man is v5, unchanged — he was already
him.)

  impatient   — weight rocked forward, overreaching, body ahead of
                the task, free hand on the hip
  meticulous  — close to the work, choked grip, neat feet, the small
                careful stroke
  distracted  — body at the wall, attention gone; head turned away,
                the pole drifting
  tired       — everything sags toward the floor; the arm still up
                because the wall doesn't care
  absorbed    — v5 (presence_figure), the settled counterpose
  twenty yrs  — economy of motion; stands further back, hand in
                pocket, nothing wasted
"""
import os
import numpy as np
from PIL import Image
from about_figure import render_strokes, PAPER, INK, SAMPLES
from about_scenes import s, scaled
from charm_studies import presence_figure

PW, PH = 470, 800
K, DY = 0.42, 70


def man(cx, bow=0.3, slump=0.0, head_pitch=0.4, head_turn=0.0,
        reach=1.0, stance=1.0, knees=0.0, heels=0.0, free_arm="hang",
        prox=0.0, waist=0.0, hair=0.0, tuck=False, sleeves=False,
        pool=0.0):
    """One inhabitant, ~16 strokes. Everything is posture.

    bow        spine curve 0..1          slump      shoulders+head drop 0..1
    head_pitch -1 down .. 1 up           head_turn  0 back-view .. 1 away
    reach      arm raise 0.4..1.2        stance     feet spread multiplier
    knees      softness 0..1             heels      0 flat .. 1 forward/toes
    free_arm   hang | hip | pocket       prox       toward wall (x shift of work)
    """
    S = []
    def a(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
        S.append(dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                      smoothing=sm, cap_start=cs, cap_end=ce))

    hr = 78
    hy = 116 + 84 * slump - 22 * head_pitch
    tx = head_turn * 36           # head shifts toward where he looks

    # head + high nape + ear (ear migrates with the turn)
    a([(cx - hr * .86 + tx, hy + 64), (cx - hr * .97 + tx, hy - 12),
       (cx - hr * .6 + tx, hy - 70), (cx + hr * .05 + tx, hy - 82),
       (cx + hr * .7 + tx, hy - 56), (cx + hr * .99 + tx, hy + 2),
       (cx + hr * .86 + tx, hy + 62)], 2.6, swell=0.16)
    a([(cx - hr * .64 + tx * 1.4, hy + 30 + 8 * head_pitch),
       (cx - hr * .04 + tx * 1.4, hy + 40 + 12 * head_pitch),
       (cx + hr * .62 + tx * 1.4, hy + 26 + 8 * head_pitch)], 1.8, swell=0.1)
    a([(cx + hr * (.99 - .5 * head_turn) + tx, hy + 4),
       (cx + hr * (1.12 - .5 * head_turn) + tx, hy + 22),
       (cx + hr * (.95 - .5 * head_turn) + tx, hy + 38)], 1.3, swell=0.08)
    if hair > 0.15:
        a([(cx - hr * .26 + tx, hy - 60 + 18 * (1 - hair)),
           (cx - hr * .36 + tx, hy - 12), (cx - hr * .38 + tx, hy + 14 * hair)],
          0.9, swell=0.08)
    if hair > 0.55:
        a([(cx + hr * .2 + tx, hy - 64 + 14 * (1 - hair)),
           (cx + hr * .28 + tx, hy - 16), (cx + hr * .25 + tx, hy + 10 * hair)],
          0.9, swell=0.08)

    sh_y = 300 + 74 * slump
    # left side: neck → working shoulder → arm to the grip
    fist = (cx - 150 - 40 * (reach - 1) - prox, 218 - 200 * (reach - 1) + 170 * slump)
    a([(cx - 30 + tx * .5, hy + 84), (cx - 56, sh_y - 52 + 10 * bow),
       (cx - 102, sh_y - 10)], 2.4, swell=0.2)
    a([(cx - 102, sh_y - 10), (cx - 132, (sh_y + fist[1]) / 2 - 20),
       fist], 2.6, swell=0.2)
    a([(fist[0] + 6, fist[1] + 8), (fist[0] - 8, fist[1] - 4),
       (fist[0] - 4, fist[1] - 24), (fist[0] + 14, fist[1] - 22)], 1.7, swell=0.1)

    # right side: neck → dropped shoulder → back, bowed by `bow`
    a([(cx + 32 + tx * .5, hy + 88), (cx + 92, sh_y + 52),
       (cx + 134 + 30 * bow + waist, 480 + 20 * bow),
       (cx + 140 + 14 * bow + waist, 620), (cx + 122 + waist * .6, 748)],
      2.6, swell=0.22)
    # free arm
    if free_arm == "hang":
        a([(cx + 88, sh_y + 60), (cx + 148, 540), (cx + 144, 700),
           (cx + 128, 792)], 2.0, lead=0.18, swell=0.16)
        a([(cx + 128, 794), (cx + 138, 818), (cx + 126, 832), (cx + 114, 816)],
          1.6, swell=0.1)
    elif free_arm == "hip":
        a([(cx + 88, sh_y + 60), (cx + 168, 480), (cx + 120, 600),
           (cx + 96, 640)], 2.0, lead=0.18, swell=0.16)              # akimbo
    else:  # pocket
        a([(cx + 88, sh_y + 60), (cx + 140, 520), (cx + 116, 640)], 2.0,
          lead=0.18, swell=0.16)
        a([(cx + 96, 648), (cx + 134, 642)], 1.1, cs=True, ce=True)   # pocket seam

    # torso left + hem
    a([(cx - 76, sh_y + 48), (cx - 96 - waist * .8, 500),
       (cx - 110 - waist * .6, 742)], 2.2, swell=0.18)
    if tuck:
        a([(cx - 104, 744), (cx + 4, 748 + 6 * slump), (cx + 116, 738)], 1.4,
          swell=0.08)
    else:
        a([(cx - 110 - waist * .6, 768), (cx + 4, 776 + 8 * slump),
           (cx + 122 + waist * .6, 760)], 1.5, swell=0.1)
    if sleeves:
        a([(cx + 142 + waist * .3, 632), (cx + 122, 642)], 1.0, cs=True, ce=True)

    # legs — weight under the neck unless rocked forward
    spread = 1.0 * stance
    kx = 55 * knees
    a([(cx + 120, 742), (cx + 84 + kx, 1000), (cx + (54 + 30 * (spread - 1)), 1260),
       (cx + (44 + 40 * (spread - 1)), 1418 - 6 * heels)], 2.4, swell=0.18)
    a([(cx - 108, 754), (cx - 120 - 14 * knees, 1010 + 30 * knees),
       (cx - (96 + 26 * (spread - 1)), 1280),
       (cx - (92 + 34 * (spread - 1)), 1404 - 6 * heels)], 2.4, swell=0.2)
    a([(cx + 2, 772), (cx + 12 + kx * .5, 1080), (cx + 18, 1414)], 1.9,
      lead=0.2, swell=0.16)

    if pool > 0.1:
        a([(cx + 28, 1392), (cx + 52 + 30 * (spread - 1), 1386)], 0.9,
          cs=True, ce=True)
        a([(cx - 104 - 26 * (spread - 1), 1378), (cx - 72, 1384)], 0.9,
          cs=True, ce=True)

    # feet — heels carry the temperament
    wy = 1418 - 6 * heels
    fy = 1404 - 6 * heels
    a([(cx + (44 + 40 * (spread - 1)), wy), (cx + 62 + 40 * (spread - 1), wy + 24 + 8 * heels),
       (cx + 12, wy + 28), (cx + 6, wy + 6)], 1.7, swell=0.1)
    a([(cx - (92 + 34 * (spread - 1)), fy), (cx - 118 - 34 * (spread - 1), fy + 26),
       (cx - 64, fy + 34), (cx - 58, fy + 8)], 1.7, swell=0.1)
    return S, fist


POSTURES = {
    "impatient": (dict(bow=0.05, head_pitch=0.8, reach=1.18, stance=1.3,
                       heels=1.0, free_arm="hip", knees=0.0), -26, -60),
    "meticulous": (dict(bow=0.5, head_pitch=0.6, reach=0.92, stance=0.55,
                        free_arm="hang", knees=0.0), -78, -16),
    "distracted": (dict(bow=0.2, head_pitch=0.05, head_turn=1.0, reach=0.9,
                        stance=1.0, free_arm="hang", knees=0.2), 30, 42),
    "tired": (dict(bow=1.0, slump=1.0, head_pitch=-0.9, reach=0.5,
                   stance=1.15, free_arm="hang", knees=0.8), 12, 0),
    "absorbed (v5)": (None, 0, 0),
    "twenty years": (dict(bow=0.3, head_pitch=0.3, reach=0.9, stance=1.05,
                          free_arm="pocket", knees=0.1), 64, 0),
}


def wall_and_pole(fist, prox=0.0):
    """The same wall for everyone: working edge + roller at the top of
    the pole, panel-local coordinates (figure space, pre-scaling)."""
    S = []
    ex = -330 - prox
    S.append(s([(ex, -120), (ex + 4, 480), (ex - 2, 1100), (ex + 2, 1460)],
               1.1, lead=0.04, tail=0.05, swell=0.05, cs=True))           # edge
    top = (ex + 64, -36)
    S.append(s([top, ((top[0] + fist[0]) / 2, (top[1] + fist[1]) / 2 + 12),
                fist, (fist[0] + 8, fist[1] + 30)], 1.5, swell=0.06, cs=True))
    S.append(s([(top[0] - 46, top[1] - 14), (top[0], top[1] - 18),
                (top[0] + 46, top[1] - 15)], 1.7, swell=0.1))
    S.append(s([(top[0] - 48, top[1]), (top[0] - 2, top[1] - 4),
                (top[0] + 44, top[1] - 1)], 1.7, swell=0.1))
    return S


def shear(strokes, sx):
    """Lean the whole body: top drifts sx px toward the wall (negative)
    or away (positive); feet stay planted."""
    out = []
    for st in strokes:
        st2 = dict(st)
        st2["ctrl"] = [(x + sx * (1 - y / 1450.0), y) for (x, y) in st["ctrl"]]
        out.append(st2)
    return out


if __name__ == "__main__":
    panels = []
    for name, (kw, dx, lean_x) in POSTURES.items():
        if kw is None:
            fig = presence_figure(0)
            fist = (-150, 216)
            kw_prox = 0.0
        else:
            fig, fist = man(0, **kw)
            kw_prox = kw.get("prox", 0.0)
        fig = shear(fig, lean_x)
        if lean_x:
            fr = 1 - (fist[1] / 1450.0)
            fist = (fist[0] + lean_x * fr, fist[1])
        S = [dict(t, ctrl=[(x + dx, y) for (x, y) in t["ctrl"]]) for t in fig]
        S += wall_and_pole((fist[0] + dx, fist[1]), kw_prox + dx)
        S = scaled(S, K, PW // 2 + 60, DY)
        fa = render_strokes(S, PW, PH)
        out = np.ones((PH, PW, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        panels.append(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))

    gap = 14
    sheet = Image.new("RGB", (PW * 6 + gap * 7, PH + gap * 2),
                      tuple(int(v) for v in PAPER))
    for i, p in enumerate(panels):
        sheet.paste(p, (gap + i * (PW + gap), gap))
    sheet.save(os.path.join(SAMPLES, "five_men_painting_sheet.png"))
    print("done:", ", ".join(POSTURES))
