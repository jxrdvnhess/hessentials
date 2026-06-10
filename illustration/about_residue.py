"""
Hessentials — ABOUT backdrop, RESIDUE attempt (Sketch 101/201/301).

Not an illustration of an object. The visual residue of a decision.

One short passage of a line, attempted three times: a faint first ghost, a
near-twin that was let go (erased — rubbed down to graphite haze, with a small
hesitation still in it), and the one that was kept (resolved, confident). The
meaning is entirely relational: remove the kept line and it's only searching;
remove the rejected ones and it's only a line. Together they are the trace of
someone deciding what stays and what goes — and because the attempts are nearly
identical, the viewer has to look to tell which was right. That looking is the
point: the image causes discernment instead of symbolizing it.

Graphite-on-cream, warm gray, real tooth. Programmatic synthesis only — the
erasure is an actual operation in the make, not a decorative draft-mark.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "about", "about-residue.jpg")

CREAM = np.array([248, 246, 243], float)
GRAPHITE = np.array([66, 62, 58], float)   # warm graphite, not ink


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


def living(nodes, rng, n=26, tremor=0.8, drift=1.8, overshoot=0.0):
    pts = cmr(nodes, n)
    m = len(pts)

    def sm(k):
        k = max(1, min(k, m))
        return np.convolve(rng.normal(0, 1, m), np.ones(k) / k, mode="same")

    pts = pts + np.stack([sm(7) * tremor + sm(29) * drift,
                          sm(7) * tremor + sm(29) * drift], 1)
    if overshoot:
        d = pts[-1] - pts[-2]
        pts = np.vstack([pts, pts[-1] + d * overshoot])
    return [tuple(p) for p in pts]


def composite(canvas, alpha, color, rng, grain=0.18):
    """Lay graphite over the canvas. Grain gives the stroke a tooth so it
    reads as pencil pressed into paper, not a vector fill."""
    a = alpha.copy()
    if grain:
        g = rng.normal(0, 1, a.shape)
        g = np.asarray(Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-6) * 255)
                       .astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0
        a = a * (1 - grain + grain * g)
    a = a[..., None]
    return canvas * (1 - a) + color * a


def smudge(alpha, blur, fade):
    """Erase: rub the stroke down to a haze."""
    h = np.asarray(Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(blur)), float) / 255.0
    return h * fade


def compose(w=2000, h=1143, seed=7):
    rng = np.random.default_rng(seed)
    canvas = np.ones((h, w, 3)) * CREAM + rng.normal(0, 1.5, (h, w, 1))

    # The same short line, found three times. Center-right; the essay lives
    # in the open cream to the left.
    kept = living([(1245, 596), (1378, 579), (1512, 584), (1648, 571)],
                  rng, tremor=0.7, drift=1.4, overshoot=0.35)
    # the let-go twin: nearly identical, sitting just below, but with a small
    # hesitation at the third node (the thing that was "technically fine but
    # energetically off") — visibly present, but rubbed down.
    rejected = living([(1247, 636), (1380, 621), (1458, 638), (1516, 624), (1650, 614)],
                      rng, tremor=0.9, drift=1.7)
    # an even fainter first ghost above — the search starting
    ghost = living([(1250, 568), (1384, 553), (1510, 560), (1646, 547)],
                   rng, tremor=1.4, drift=2.8)

    a_kept = stroke_alpha(w, h, [(kept, 3.0)], width=3.0, jitterblur=0.6, supersample=3)
    a_rej = stroke_alpha(w, h, [(rejected, 2.6)], width=2.6, jitterblur=0.7, supersample=3)
    a_ghost = stroke_alpha(w, h, [(ghost, 2.2)], width=2.2, jitterblur=0.9, supersample=3)

    # ghost: faintest. rejected: rubbed down to a haze + a few graphite specks
    # left by the eraser. kept: confident, full pressure.
    canvas = composite(canvas, a_ghost * 0.13, GRAPHITE, rng, grain=0.3)
    # the rejected line is visibly present but rubbed: a partly-erased pencil
    # line (more presence than a ghost, less than the kept) + an eraser haze.
    canvas = composite(canvas, smudge(a_rej, blur=1.4, fade=0.46), GRAPHITE, rng, grain=0.4)
    # eraser crumbs: a scatter of faint specks along the rejected line
    ys, xs = np.where(a_rej > 0.3)
    if len(xs):
        pick = rng.choice(len(xs), size=min(70, len(xs)), replace=False)
        speck = np.zeros((h, w))
        for i in pick:
            yy = int(ys[i] + rng.normal(0, 6)); xx = int(xs[i] + rng.normal(0, 6))
            if 0 <= yy < h and 0 <= xx < w:
                speck[yy, xx] = rng.uniform(0.2, 0.5)
        speck = np.asarray(Image.fromarray((speck * 255).astype(np.uint8))
                           .filter(ImageFilter.GaussianBlur(0.8)), float) / 255.0
        canvas = composite(canvas, speck, GRAPHITE, rng, grain=0.0)
    canvas = composite(canvas, a_kept * 0.92, GRAPHITE, rng, grain=0.16)

    # a small, dry registration tick to the left of the passage — the page was
    # being worked, not composed. Very faint.
    tick = stroke_alpha(w, h, [([(1196, 584), (1198, 612)], 2.0)],
                        width=2.0, jitterblur=0.5, supersample=3)
    canvas = composite(canvas, tick * 0.35, GRAPHITE, rng, grain=0.2)

    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    compose().save(OUT, quality=92)
    print("saved", OUT)
