"""
Hessentials — SCENE translator (v5). Drawing scenes that establish emotion.

Takes an owned source photograph and re-renders the SCENE in our drawn vision —
scratch-tone (massed strokes that follow the forms), line, or notan — warm on
linen. This is the photoreal -> honest-fiction move: the structure of a real,
owned scene becomes a drawing that declares itself made. Programmatic synthesis
of existing material, no diffusion.

The strokes are oriented along the image's edges (perpendicular to the
luminance gradient), so walls, arches, water and figures read as form rather
than noise — the difference between a scene and a smudge.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from linen import linen_ground
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples", "scenes")
os.makedirs(OUT, exist_ok=True)

INK = np.array([34, 30, 30], float)     # warm near-black

def _g(a, r):
    return np.asarray(Image.fromarray(a.clip(0,255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(r)), float)

def load_gray(path, w, h):
    im = Image.open(path).convert("L")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    return np.asarray(im, float)

def scene_scratch(path, w=1240, h=698, seed=0, n_strokes=150000, ss=2,
                  gamma=1.35, edge_gain=0.9, follow=0.8, tone=0.0,
                  floor_cut=0.10, hi_protect=0.70, hi_strength=0.85,
                  glow=0.0, sat=5.5):
    """Scratch-tone translation of a scene.

    floor_cut   drops the faint mid-tones so the lights open to bare linen
    hi_protect  luminance above this is treated as light: strokes suppressed
    glow        warms/brightens the protected highlights (sun pouring in)
    """
    rng = np.random.default_rng(seed*13+7)
    g = load_gray(path, w, h)
    L = g/255.0
    detail = L - _g(g, 8)/255.0
    Lc = np.clip(L + 0.35*detail, 0, 1)

    # how "light" each pixel is (0 in shadow, 1 in the brightest highlights)
    bright = np.clip((Lc - hi_protect)/(1 - hi_protect + 1e-6), 0, 1)
    bright = _g(bright*255, 2)/255.0

    D = np.clip((1 - Lc)**gamma, 0, 1)
    D = np.clip((D - floor_cut)/(1 - floor_cut), 0, 1)   # open the lights

    gb = _g(g, 1.4)/255.0
    gy, gx = np.gradient(gb)
    mag = np.sqrt(gx**2 + gy**2); mag = mag/(mag.max()+1e-6)
    D = np.clip(D + edge_gain*mag*(1 - 0.7*bright), 0, 1) # fewer edge strokes in light
    D *= (1 - hi_strength*bright)                         # protect the highlights

    ori = np.arctan2(gy, gx) + np.pi/2

    W, Hpx = w*ss, h*ss
    canvas = np.zeros((Hpx, W), float)
    p = (D**1.4).flatten(); s = p.sum()
    if s <= 0: s = 1.0
    p = p/s
    idx = rng.choice(p.size, size=n_strokes, p=p)
    iy, ix = np.divmod(idx, w)
    dens = D[iy, ix]
    th = ori[iy, ix]
    rand = rng.uniform(0, np.pi, n_strokes)
    ang = follow*th + (1-follow)*rand + rng.normal(0, 0.25, n_strokes)
    ys = iy.astype(float)*ss + rng.uniform(0, ss, n_strokes)
    xs = ix.astype(float)*ss + rng.uniform(0, ss, n_strokes)
    Llen = (4 + dens*12) * ss
    npts = 12
    t = np.linspace(-0.5, 0.5, npts)
    dx = np.cos(ang)[:, None]*Llen[:, None]*t[None, :]
    dy = np.sin(ang)[:, None]*Llen[:, None]*t[None, :]
    pix = np.clip((xs[:, None]+dx).ravel().astype(int), 0, W-1)
    piy = np.clip((ys[:, None]+dy).ravel().astype(int), 0, Hpx-1)
    np.add.at(canvas, (piy, pix), 0.6)
    np.add.at(canvas, (np.clip(piy+1,0,Hpx-1), pix), 0.2)

    canvas = np.asarray(Image.fromarray((np.clip(canvas,0,6)/6*255).astype(np.uint8))
                        .resize((w, h), Image.LANCZOS), float)/255.0
    ink_a = 1 - np.exp(-sat*canvas)
    linen = linen_ground(w, h, seed=seed*3+1, tone=tone)
    if glow > 0:
        linen = np.clip(linen + bright[...,None]*glow*np.array([20,15,7.]), 0, 255)
    out = linen*(1-ink_a[...,None]) + INK*ink_a[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

def scene_notan(path, w=1240, h=698, thresh=0.42, seed=0,
                ground=(232,226,216), dark=(28,25,28)):
    """Two-value notan translation (the squint / Pattern view of the scene)."""
    g = load_gray(path, w, h)/255.0
    g = _g(g*255, 1.5)/255.0
    mass = g < thresh
    mass = np.asarray(Image.fromarray((mass*255).astype(np.uint8))
                      .filter(ImageFilter.MedianFilter(5)), float)/255.0 > 0.5
    out = np.where(mass[...,None], np.array(dark,float), np.array(ground,float))
    return Image.fromarray(out.astype(np.uint8))

if __name__ == "__main__":
    SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "public", "home")
    scene_scratch(f"{SRC}/merida-moment-3.jpg", seed=3).save(f"{OUT}/scene3_scratch.png")
    print("done:", sorted(os.listdir(OUT)))
