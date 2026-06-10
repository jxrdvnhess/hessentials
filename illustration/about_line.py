"""
Hessentials — ABOUT backdrop, LINE attempt (Sketch 201/301 vocabulary).

NOT a scene. A few confident contour lines on the brand cream, with the page
itself doing most of the work (huge negative space, left open for the essay).
Method comes straight from the course studies: Catmull-Rom contour (a52 "the
intentional object", a50 "the two boughs"), but drawn with a LIVING hand —
smoothed tremor + a little overshoot so the line searches and resolves rather
than sits there mechanically. 201: meaning is in the relationship between a
few marks, not in rendering. 301: keep it economical and a touch ambiguous —
two quiet objects sharing a surface, the eye finishes them.

Ink #1f1d1b on cream #f8f6f3. Programmatic synthesis only.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "about", "about-line.jpg")

CREAM = np.array([248, 246, 243], float)
INK = np.array([31, 29, 27], float)


def cmr(nodes, n=26, closed=False):
    P = [np.array(p, float) for p in nodes]
    P = ([P[-1]] + P + [P[0], P[1]]) if closed else ([P[0]] + P + [P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2 = t * t
            t3 = t2 * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(P[-2])
    return np.array(out)


def living(nodes, rng, n=26, closed=False, tremor=0.9, drift=2.0, overshoot=0.0):
    """Catmull-Rom contour + a hand: low-freq drift (proportion wander) and
    hi-freq tremor, with optional overshoot past an open end."""
    pts = cmr(nodes, n, closed)
    m = len(pts)

    def sm(k):
        k = max(1, min(k, m))  # kernel never longer than the path
        z = rng.normal(0, 1, m)
        return np.convolve(z, np.ones(k) / k, mode="same")

    pts = pts + np.stack([sm(7) * tremor + sm(29) * drift,
                          sm(7) * tremor + sm(29) * drift], 1)
    if overshoot and not closed:
        d = pts[-1] - pts[-2]
        pts = np.vstack([pts, pts[-1] + d * overshoot])
    return [tuple(p) for p in pts]


def compose(w=2000, h=1143, seed=4):
    rng = np.random.default_rng(seed)
    main, faint = [], []

    # --- the pear (intentional object), centre-right, resting on the surface ---
    pear = [(1276, 566), (1248, 590), (1226, 638), (1216, 694), (1236, 740),
            (1283, 752), (1336, 736), (1353, 686), (1332, 632), (1300, 586)]
    main.append((living(pear, rng, closed=True, tremor=0.8, drift=2.2), 3.1))
    # stem — a thin mark that reaches up and overshoots (the living tail)
    main.append((living([(1281, 566), (1287, 536), (1296, 512)], rng,
                         n=20, tremor=0.6, drift=1.2, overshoot=0.5), 2.1))
    # one leaf off the stem
    main.append((living([(1294, 520), (1322, 506), (1336, 516), (1316, 530), (1296, 524)],
                        rng, n=18, closed=True, tremor=0.6, drift=1.0), 1.9))

    # --- a fig, smaller, nestled to the right: the relationship (201) ---
    fig = [(1502, 652), (1544, 664), (1561, 702), (1548, 742), (1502, 756),
           (1456, 742), (1442, 702), (1460, 664)]
    main.append((living(fig, rng, closed=True, tremor=0.8, drift=1.8), 3.0))
    main.append((living([(1502, 652), (1500, 640), (1505, 632)], rng,
                        n=12, tremor=0.5, drift=0.8, overshoot=0.4), 1.8))

    # --- the surface they share: one long quiet line, kept faint ---
    faint.append((living([(1006, 748), (1180, 743), (1360, 750), (1545, 752), (1748, 747)],
                         rng, n=40, tremor=0.7, drift=2.6, overshoot=0.3), 2.0))

    a_main = stroke_alpha(w, h, main, width=3.0, jitterblur=0.55, supersample=3)
    a_faint = stroke_alpha(w, h, faint, width=2.0, jitterblur=0.7, supersample=3)

    # paper: brand cream with the barest grain
    img = np.ones((h, w, 3)) * CREAM + rng.normal(0, 1.6, (h, w, 1))
    a = np.clip(a_main + a_faint * 0.5, 0, 1)[..., None]
    out = np.clip(img, 0, 255) * (1 - a) + INK * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    compose().save(OUT, quality=92)
    print("saved", OUT)
