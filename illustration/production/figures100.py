"""
501-P — THE PEOPLE DEBT. 100 figures: 50 men, 50 women.
No props. No stories. No environments. Four contact sheets of 25,
uncurated — good, bad, awkward, all shown.

Three view families (back / front / profile), two sexes, with every
earned tool active: counterpose, weight under the neck pit, spine as
curve, drape vs fit, splayed feet, head pitch and turn, age in the
waist and hair. Per-figure seeded variation on every landmark so the
rig cannot hide: if sameness shows across a sheet, that is a finding,
not an accident.

Figure space ~1500 tall, rendered small (panel 300x520). The question
on trial: can Hessentials draw human beings as confidently as it now
draws moments?
"""
import os
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from about_figure import render_strokes, PAPER, INK

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PH = 300, 520
K, DY = 0.305, 30


def st(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


def scale_strokes(S, k, dx, dy, wmin=0.55):
    out = []
    for t in S:
        t2 = dict(t)
        t2["ctrl"] = [(x * k + dx, y * k + dy) for (x, y) in t["ctrl"]]
        t2["w"] = max(wmin, t["w"] * k * 1.5)
        out.append(t2)
    return out


def head_back(S, r, hy, hair, tilt):
    S.append(st([(-r * .86 + tilt, hy + 64), (-r * .97 + tilt, hy - 10),
                 (-r * .6 + tilt, hy - 68), (r * .05 + tilt, hy - 80),
                 (r * .7 + tilt, hy - 56), (r * .99 + tilt, hy + 2),
                 (r * .86 + tilt, hy + 62)], 2.5, swell=0.16))
    S.append(st([(-r * .62 + tilt, hy + 34), (tilt, hy + 44),
                 (r * .6 + tilt, hy + 30)], 1.7, swell=0.1))
    if hair == 1:    # bun
        S.append(st([(-r * .1 + tilt, hy + 40), (r * .15 + tilt, hy + 58),
                     (r * .38 + tilt, hy + 74), (r * .12 + tilt, hy + 90),
                     (-r * .1 + tilt, hy + 72)], 1.5, swell=0.1))
    elif hair == 2:  # long fall
        S.append(st([(-r * .9 + tilt, hy + 20), (-r * 1.02 + tilt, hy + 150),
                     (-r * .9 + tilt, hy + 260)], 1.3, swell=0.08))
        S.append(st([(r * .92 + tilt, hy + 18), (r * 1.04 + tilt, hy + 148),
                     (r * .9 + tilt, hy + 256)], 1.3, swell=0.08))
    elif hair == 3:  # short, two direction strokes
        S.append(st([(-r * .28 + tilt, hy - 44), (-r * .36 + tilt, hy + 8)],
                    0.8, swell=0.06))
        S.append(st([(r * .22 + tilt, hy - 48), (r * .3 + tilt, hy + 4)],
                    0.8, swell=0.06))


def figure_any(rng, sex, view):
    """One person. All numbers drawn from ranges the course earned."""
    S = []
    female = sex == "w"
    h_r = rng.uniform(66, 80) * (0.94 if female else 1.0)
    hy = rng.uniform(108, 132)
    sh = rng.uniform(128, 168) * (0.82 if female else 1.0)   # shoulder half-width
    waist = rng.uniform(78, 110) * (0.88 if female else 1.0)
    hip = waist * (rng.uniform(1.12, 1.3) if female else rng.uniform(0.95, 1.08))
    age_w = rng.uniform(0, 14) if rng.random() < 0.4 else 0   # the waist of years
    lean = rng.uniform(-22, 22)
    wshift = rng.uniform(6, 22) * rng.choice([-1, 1])         # weight side
    pitch = rng.uniform(-18, 14)
    tilt = rng.uniform(-14, 14)
    dress = female and rng.random() < 0.55
    hair = rng.choice([1, 2, 3]) if female else rng.choice([0, 3, 3])
    arm_mode = rng.choice(["hang", "hang", "pocket", "hip"])
    hem = 750 + rng.uniform(-20, 20)
    sh_y = 300 + rng.uniform(-16, 24) - pitch

    if view == "back" or view == "front":
        head_back(S, h_r, hy + pitch, hair, tilt)
        if view == "front":
            fy = hy + pitch
            S.append(st([(-h_r * .42 + tilt, fy - 4 + rng.uniform(-4, 4)),
                         (-h_r * .14 + tilt, fy - 10)], 0.9, swell=0.06))
            S.append(st([(h_r * .12 + tilt, fy - 10),
                         (h_r * .4 + tilt, fy - 4 + rng.uniform(-4, 4))], 0.9, swell=0.06))
            S.append(st([(-h_r * .36 + tilt, fy + 12), (-h_r * .12 + tilt, fy + 16)],
                        1.0, swell=0.06))
            S.append(st([(h_r * .1 + tilt, fy + 16), (h_r * .34 + tilt, fy + 12)],
                        1.0, swell=0.06))
            S.append(st([(tilt, fy + 18), (tilt - 3, fy + 40), (tilt + 4, fy + 46)],
                        0.9, swell=0.06))
            mw = rng.uniform(16, 26)
            S.append(st([(-mw + tilt, fy + 66), (tilt, fy + 70 + rng.uniform(-3, 4)),
                         (mw + tilt, fy + 64)], 1.1, swell=0.07))
        # neck + shoulders (asymmetric always)
        d = rng.uniform(8, 26)
        S.append(st([(-24 + tilt * .5, hy + pitch + 78), (-26, sh_y - 56)], 1.4))
        S.append(st([(26 + tilt * .5, hy + pitch + 78), (30, sh_y - 52)], 1.4))
        S.append(st([(-26, sh_y - 56), (-sh * .6, sh_y - 30 + d * .4), (-sh, sh_y + d)],
                    2.3, swell=0.15))
        S.append(st([(30, sh_y - 52), (sh * .6, sh_y - 26), (sh, sh_y - d * .3)],
                    2.3, swell=0.15))
        # arms
        for side, mode in ((-1, "hang"), (1, arm_mode)):
            x0 = sh * side
            if mode == "hang":
                S.append(st([(x0, sh_y + (d if side < 0 else -d * .3)),
                             (x0 + side * rng.uniform(8, 26), 520),
                             (x0 - side * rng.uniform(0, 14), 700),
                             (x0 - side * 12, 782)], 2.0, swell=0.16))
                S.append(st([(x0 - side * 12, 784), (x0 - side * 4, 812),
                             (x0 - side * 22, 822)], 1.4, swell=0.1))
            elif mode == "pocket":
                S.append(st([(x0, sh_y - d * .3), (x0 + side * 14, 500),
                             (x0 - side * 12, 620)], 2.0, swell=0.16))
                S.append(st([(x0 - side * 30, 642), (x0 + side * 4, 636)],
                            1.0, cs=True, ce=True))
            else:  # hip
                S.append(st([(x0, sh_y - d * .3), (x0 + side * 36, 470),
                             (x0 - side * 28, 590), (x0 - side * 52, 622)],
                            2.0, swell=0.16))
        # torso
        if dress:
            hemy = hem + rng.uniform(180, 300)
            S.append(st([(-sh * .68, sh_y + 60), (-waist, 520),
                         (-hip - 24, hemy - 60), (-hip - 34, hemy)], 2.2, swell=0.16))
            S.append(st([(sh * .68, sh_y + 64), (waist, 524),
                         (hip + 26, hemy - 56), (hip + 36, hemy + 6)], 2.2, swell=0.16))
            S.append(st([(-hip - 34, hemy + 2), (0, hemy + 14), (hip + 36, hemy + 6)],
                        1.5, swell=0.1))
            legy0 = hemy + 12
        else:
            S.append(st([(-sh * .68, sh_y + 60), (-waist - age_w, 520),
                         (-hip, hem)], 2.2, swell=0.16))
            S.append(st([(sh * .68, sh_y + 64), (waist + age_w, 524), (hip, hem - 10)],
                        2.2, swell=0.16))
            S.append(st([(-hip, hem + 8), (0, hem + 16), (hip, hem - 4)], 1.4,
                        swell=0.09))
            legy0 = hem + 12
        # legs — weight under the neck pit
        S.append(st([(hip * .9, legy0), (wshift + 38, (legy0 + 1410) / 2),
                     (wshift + 30, 1410)], 2.2, swell=0.16))
        S.append(st([(-hip * .9, legy0), (-hip * .9 - rng.uniform(0, 18),
                     (legy0 + 1400) / 2), (-wshift - 56, 1400)], 2.2, swell=0.16))
        if not dress or rng.random() < 0.5:
            S.append(st([(wshift * .2, legy0 + 14), (wshift * .4, 1100),
                         (wshift * .5 + 6, 1404)], 1.6, lead=0.2, swell=0.13))
        S.append(st([(wshift + 30, 1410), (wshift + 46, 1436), (wshift - 14, 1442),
                     (wshift - 20, 1414)], 1.5, swell=0.1))
        S.append(st([(-wshift - 56, 1400), (-wshift - 78, 1428), (-wshift - 22, 1436),
                     (-wshift - 16, 1406)], 1.5, swell=0.1))
    else:  # profile
        fwd = rng.choice([-1, 1])  # facing direction
        S.append(st([(-60 * fwd, hy + 66 + pitch), (-70 * fwd, hy + 8 + pitch),
                     (-44 * fwd, hy - 50 + pitch), (8 * fwd, hy - 68 + pitch),
                     (56 * fwd, hy - 46 + pitch), (70 * fwd, hy + 10 + pitch),
                     (62 * fwd, hy + 50 + pitch)], 2.4, swell=0.15))
        S.append(st([(62 * fwd, hy + 50 + pitch), (76 * fwd, hy + 66 + pitch),
                     (68 * fwd, hy + 78 + pitch), (78 * fwd, hy + 94 + pitch),
                     (64 * fwd, hy + 108 + pitch), (44 * fwd, hy + 122 + pitch)],
                    1.8, swell=0.12))
        if hair == 2:
            S.append(st([(-66 * fwd, hy + 10 + pitch), (-80 * fwd, hy + 140 + pitch),
                         (-66 * fwd, hy + 250 + pitch)], 1.3, swell=0.08))
        bow = rng.uniform(10, 60)
        S.append(st([(36 * fwd, hy + 128 + pitch), (26 * fwd, sh_y - 40)], 1.4))
        S.append(st([(-30 * fwd, hy + 100 + pitch), (-(54 + bow * .5) * fwd, sh_y - 10),
                     (-(70 + bow) * fwd, 520), (-(50 + bow * .7) * fwd, 700),
                     (-(40 + bow * .5) * fwd, hem)], 2.3, swell=0.16))      # the back
        S.append(st([(26 * fwd, sh_y - 40), (66 * fwd, sh_y + 10)], 2.0, swell=0.13))
        S.append(st([(66 * fwd, sh_y + 10), (76 * fwd, 520), (60 * fwd, 700),
                     (54 * fwd, 790)], 2.0, swell=0.15))                    # near arm
        S.append(st([(54 * fwd, 792), (62 * fwd, 818), (48 * fwd, 828)], 1.4, swell=0.1))
        S.append(st([(60 * fwd, sh_y + 30), (84 * fwd, 540), (70 * fwd, hem - 20)],
                    1.6, swell=0.12))                                       # chest/front
        if dress:
            hemy = hem + rng.uniform(160, 280)
            S.append(st([(-(40 + bow * .5) * fwd, hem), (-(64 + bow * .4) * fwd, hemy)],
                        2.0, swell=0.14))
            S.append(st([(70 * fwd, hem - 20), (96 * fwd, hemy - 8)], 2.0, swell=0.14))
            S.append(st([(-(64 + bow * .4) * fwd, hemy + 2), (20 * fwd, hemy + 12),
                         (96 * fwd, hemy - 6)], 1.4, swell=0.09))
            legy0 = hemy
        else:
            legy0 = hem
        S.append(st([(-(20) * fwd, legy0 + 8), (-(30) * fwd, 1080),
                     (-(38) * fwd, 1408)], 2.2, swell=0.15))
        S.append(st([(40 * fwd, legy0), (52 * fwd, 1090), (44 * fwd, 1404)],
                    2.2, swell=0.15))
        S.append(st([(-(38) * fwd, 1410), (-(10) * fwd, 1438), (54 * fwd, 1440),
                     (50 * fwd, 1412)], 1.5, swell=0.1))
    return S


if __name__ == "__main__":
    rng = np.random.default_rng(61126)
    sheets = [("men", "m"), ("men", "m"), ("women", "w"), ("women", "w")]
    views = ["back", "front", "profile"]
    for si, (label, sex) in enumerate(sheets, 1):
        gap = 8
        sheet = Image.new("RGB", (PW * 5 + gap * 6, PH * 5 + gap * 6),
                          tuple(int(v) for v in PAPER))
        for i in range(25):
            view = views[i % 3]
            S = figure_any(rng, sex, view)
            S = scale_strokes(S, K, PW // 2, DY)
            fa = render_strokes(S, PW, PH)
            out = np.ones((PH, PW, 3)) * PAPER
            out = out * (1 - fa[..., None]) + INK * fa[..., None]
            p = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
            sheet.paste(p, (gap + (i % 5) * (PW + gap), gap + (i // 5) * (PH + gap)))
        name = f"figures100_sheet{si}_{label}.png"
        sheet.save(os.path.join(HERE, name))
        print(name, "done")
