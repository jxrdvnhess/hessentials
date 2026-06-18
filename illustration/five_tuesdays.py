"""
501-15 — ONE MAN. FIVE TUESDAYS. INSTRUMENT, NOT ASSET.

Faculty exercise: the same inhabitant, the same wall, the same task —
five Tuesdays across five years. Not five personalities. Not five
moods. The question: what changes?

Working hypothesis under test (faculty, elevated after 501-14):

> Presence is not personality.
> Presence is accumulated evidence of a life.

Design principle: real people are accumulations of habits, so the
panels are built as INVARIANTS + SLOW DRIFT, never as variation.
What stays: the same shirt (once it unturned untucked, it stays
untucked — a habit, visible by repetition), the same shoes, the same
wall, the same tool. What drifts, monotonically, the way bodies and
practices actually drift: distance from the wall grows (the 501-14
finding — mastery is spatial), the reach economizes, the spine bows a
little, the waist thickens, the hair thins, the sleeves stay rolled
after year two, the trousers pool a little by year five because they
are the same trousers.

Year one he stands close, tucked in, working harder than the wall
requires. Year five he stands back, hand in pocket, and the stroke
is smaller because none of it is wasted. Almost nothing changes on
any single Tuesday. Everything changes across five.
"""
import os
import numpy as np
from PIL import Image
from about_figure import render_strokes, PAPER, INK, SAMPLES
from about_scenes import scaled
from five_men_painting import man, wall_and_pole, shear, PW, PH, K, DY

TUESDAYS = {
    # name: (params, dx from wall, lean)
    "year one": (dict(bow=0.12, head_pitch=0.6, reach=1.1, stance=0.8,
                      free_arm="hang", tuck=True, hair=1.0, waist=0,
                      sleeves=False), -48, -24),
    "year two": (dict(bow=0.2, head_pitch=0.5, reach=1.02, stance=0.9,
                      free_arm="hang", tuck=False, hair=0.85, waist=2,
                      sleeves=True), -16, -10),
    "year three": (dict(bow=0.3, head_pitch=0.45, reach=0.97, stance=1.0,
                        free_arm="hang", tuck=False, hair=0.68, waist=6,
                        sleeves=True), 8, 0),
    "year four": (dict(bow=0.38, head_pitch=0.35, reach=0.92, stance=1.02,
                       free_arm="hang", tuck=False, hair=0.52, waist=9,
                       sleeves=True, pool=0.3), 30, 0),
    "year five": (dict(bow=0.45, head_pitch=0.3, reach=0.88, stance=1.05,
                       free_arm="pocket", tuck=False, hair=0.42, waist=12,
                       sleeves=True, pool=0.6), 54, 0),
}

if __name__ == "__main__":
    panels = []
    for name, (kw, dx, lean_x) in TUESDAYS.items():
        fig, fist = man(0, **kw)
        fig = shear(fig, lean_x)
        if lean_x:
            fr = 1 - (fist[1] / 1450.0)
            fist = (fist[0] + lean_x * fr, fist[1])
        S = [dict(t, ctrl=[(x + dx, y) for (x, y) in t["ctrl"]]) for t in fig]
        S += wall_and_pole((fist[0] + dx, fist[1]), dx)
        S = scaled(S, K, PW // 2 + 60, DY)
        fa = render_strokes(S, PW, PH)
        out = np.ones((PH, PW, 3)) * PAPER
        out = out * (1 - fa[..., None]) + INK * fa[..., None]
        panels.append(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))

    gap = 14
    sheet = Image.new("RGB", (PW * 5 + gap * 6, PH + gap * 2),
                      tuple(int(v) for v in PAPER))
    for i, p in enumerate(panels):
        sheet.paste(p, (gap + i * (PW + gap), gap))
    sheet.save(os.path.join(SAMPLES, "five_tuesdays_sheet.png"))
    print("done:", ", ".join(TUESDAYS))
