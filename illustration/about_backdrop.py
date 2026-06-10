"""
Hessentials — ABOUT backdrop drawing.

Translates the owned Merida interior (public/about/merida-moment-5.jpg) into a
made scratch-tone drawing on the brand cream (#f8f6f3) — the same photoreal ->
honest-fiction move as scene.py, but grounded on the site's own paper so the
drawing reads as DRAWN ONTO THE PAGE, not pasted on. Massed strokes follow the
luminance gradient (walls/arches read as form), the lit areas open to bare
cream so the essay column has somewhere to live, and the afternoon light is
carried by the bare paper, not by a scrim.

Evidence-only, no figure. Calm, light, spacious. Programmatic synthesis only.
"""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "public", "about", "merida-moment-5.jpg")
OUT = os.path.join(HERE, "..", "public", "about", "about-drawing.jpg")

CREAM = np.array([248, 246, 243], float)  # brand --cream-bg #f8f6f3
INK = np.array([31, 29, 27], float)       # brand ink #1f1d1b


def _g(a, r):
    return np.asarray(
        Image.fromarray(a.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),
        float,
    )


def load_gray(path, w, h):
    im = Image.open(path).convert("L")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    return np.asarray(im, float)


def paper(w, h, seed=7):
    """Brand cream with a barely-there tooth — paper, not a flat fill."""
    rng = np.random.default_rng(seed)
    img = np.ones((h, w, 3)) * CREAM
    img += rng.normal(0, 2.0, (h, w, 1))  # fine grain
    lf = rng.normal(0, 1, (h // 40 + 2, w // 40 + 2))
    lf = np.asarray(
        Image.fromarray(((lf - lf.min()) / (np.ptp(lf) + 1e-6) * 255).astype(np.uint8))
        .resize((w, h), Image.BICUBIC),
        float,
    ) / 255.0
    img += (lf[..., None] - 0.5) * 3.5  # faint uneven warmth
    return np.clip(img, 0, 255)


def scratch_on_cream(
    path, w, h, seed=5, n_strokes=70000, ss=2, gamma=1.45,
    edge_gain=0.85, follow=0.82, floor_cut=0.20,
    hi_protect=0.58, hi_strength=0.92, glow=0.35, sat=3.8,
):
    rng = np.random.default_rng(seed * 13 + 7)
    g = load_gray(path, w, h)
    L = g / 255.0
    detail = L - _g(g, 8) / 255.0
    Lc = np.clip(L + 0.35 * detail, 0, 1)

    bright = np.clip((Lc - hi_protect) / (1 - hi_protect + 1e-6), 0, 1)
    bright = _g(bright * 255, 2) / 255.0

    D = np.clip((1 - Lc) ** gamma, 0, 1)
    D = np.clip((D - floor_cut) / (1 - floor_cut), 0, 1)  # open the lights to bare cream

    gb = _g(g, 1.4) / 255.0
    gy, gx = np.gradient(gb)
    mag = np.sqrt(gx ** 2 + gy ** 2)
    mag = mag / (mag.max() + 1e-6)
    D = np.clip(D + edge_gain * mag * (1 - 0.7 * bright), 0, 1)
    D *= (1 - hi_strength * bright)  # protect the highlights

    ori = np.arctan2(gy, gx) + np.pi / 2

    W, Hpx = w * ss, h * ss
    canvas = np.zeros((Hpx, W), float)
    p = (D ** 1.4).flatten()
    s = p.sum() or 1.0
    p = p / s
    idx = rng.choice(p.size, size=n_strokes, p=p)
    iy, ix = np.divmod(idx, w)
    dens = D[iy, ix]
    th = ori[iy, ix]
    rand = rng.uniform(0, np.pi, n_strokes)
    ang = follow * th + (1 - follow) * rand + rng.normal(0, 0.25, n_strokes)
    ys = iy.astype(float) * ss + rng.uniform(0, ss, n_strokes)
    xs = ix.astype(float) * ss + rng.uniform(0, ss, n_strokes)
    Llen = (4 + dens * 12) * ss
    npts = 12
    t = np.linspace(-0.5, 0.5, npts)
    dx = np.cos(ang)[:, None] * Llen[:, None] * t[None, :]
    dy = np.sin(ang)[:, None] * Llen[:, None] * t[None, :]
    pix = np.clip((xs[:, None] + dx).ravel().astype(int), 0, W - 1)
    piy = np.clip((ys[:, None] + dy).ravel().astype(int), 0, Hpx - 1)
    np.add.at(canvas, (piy, pix), 0.6)
    np.add.at(canvas, (np.clip(piy + 1, 0, Hpx - 1), pix), 0.2)

    canvas = np.asarray(
        Image.fromarray((np.clip(canvas, 0, 6) / 6 * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS),
        float,
    ) / 255.0
    ink_a = 1 - np.exp(-sat * canvas)

    pg = paper(w, h, seed=seed * 3 + 1)
    if glow > 0:  # afternoon warmth in the bare light
        pg = np.clip(pg + bright[..., None] * glow * np.array([5.0, 3.0, 0.5]), 0, 255)
    out = pg * (1 - ink_a[..., None]) + INK * ink_a[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    aw, ah = Image.open(SRC).size
    LONG = 2000
    if aw >= ah:
        W, H = LONG, round(LONG * ah / aw)
    else:
        H, W = LONG, round(LONG * aw / ah)
    # Tuned for confident form over scratch density: strokes follow the
    # gradient harder (follow), the form EDGES carry more weight (edge_gain),
    # ink in the shadowed areas reads present (sat) — while the lit wall stays
    # bare cream (high floor_cut + protected highlights) for the essay column.
    scratch_on_cream(
        SRC, W, H, seed=5, n_strokes=60000, follow=0.92, edge_gain=1.4,
        floor_cut=0.30, hi_protect=0.54, hi_strength=0.93, glow=0.4, sat=7.0,
    ).save(OUT, quality=92)
    print(f"saved {OUT}  ({W}x{H}) from source {aw}x{ah}")
