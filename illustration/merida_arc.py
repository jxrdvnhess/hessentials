"""
The Merida arc — confident-line register, figures INSIDE their world.

The bare-linen figure was a training state. The destination is the figure in a
room: the light, the arch, the depth. Atmosphere returns as RESTRAINT, not
density — never the scratch engine. The rule:

    light  = absence of mark (bare linen)
    shadow = a few soft committed tonal masses (warm, lost edges)
    structure = a few sure lines (arch, doorframe, floor seam)

Every mark is a decision you could defend, not texture to fill space.

Beats: breakfast (open, warm) · pool (distance, keep the gap) · notebook
(contemplation, golden hour) ← calibrating · dinner (night) · bedroom (close).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS, INK
from linen import linen_ground

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")

W, H = 1300, 950
WARM_SHADOW = np.array([96, 74, 62], float)   # warm umber — never gray

def shadows_alpha(w, h, shadows):
    acc = np.zeros((h, w))
    for s in shadows:
        m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
        if s["kind"] == "poly":
            d.polygon(s["pts"], fill=255)
        else:
            d.ellipse(s["box"], fill=255)
        arr = np.asarray(m.filter(ImageFilter.GaussianBlur(s["blur"])), float)/255.0
        acc = np.maximum(acc, arr*s["strength"])
    return np.clip(acc, 0, 1)

def render_interior(strokes, shadows, w, h, seed=0, tone=0.4, rake=0.55):
    linen = linen_ground(w, h, seed=seed, tone=tone)          # warm light ground
    # raking light: the dim interior gathers toward the upper-left and fades to
    # bare linen toward the bright doorway (lower-right). This soft warm gradient
    # IS the low glow — restrained tone, not scratch.
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    grad = np.clip(0.60*(1-xx/w) + 0.50*(1-yy/h) - 0.40, 0, 1)
    grad = np.asarray(Image.fromarray((grad*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(45)), float)/255.0 * rake
    sh = np.clip(np.maximum(grad, shadows_alpha(w, h, shadows)), 0, 1)
    ground = linen*(1-sh[..., None]) + WARM_SHADOW*sh[..., None]
    # line layer (figure + structure), committed strokes
    main = Image.new("L", (w*SS, h*SS), 0); md = ImageDraw.Draw(main)
    for s in strokes:
        stroke(md, **s)
    a = np.asarray(main.resize((w, h), Image.LANCZOS), float)/255.0
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, 1, (h, w))
    grain = np.asarray(Image.fromarray(((grain-grain.min())/(np.ptp(grain)+1e-6)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float)/255.0
    a = np.clip(a*(0.9+0.2*grain), 0, 1)
    out = ground*(1-a[..., None]) + INK*a[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

# ----------------------------------------------------------- the notebook beat
def beat_notebook():
    sm = 0.5
    S = []
    # ===== structure — a few sure lines; the lit doorway stays bare linen =====
    # arched doorway, right-of-centre: bright courtyard light beyond (bare)
    S.append(dict(ctrl=[(846,766),(844,556)], w=6, lead=0.10, swell=0.3, cap_start=True, smoothing=sm))            # left doorframe
    S.append(dict(ctrl=[(844,556),(902,420),(988,352),(1078,420),(1130,556)], w=6, lead=0.12, tail=0.12, swell=0.3, smoothing=sm))  # arch
    S.append(dict(ctrl=[(1130,556),(1134,766)], w=6, tail=0.10, swell=0.3, cap_end=True, smoothing=sm))            # right doorframe
    S.append(dict(ctrl=[(150,768),(846,762)], w=5, lead=0.12, swell=0.25, cap_start=True, smoothing=sm))           # floor/wall seam
    S.append(dict(ctrl=[(986,352),(986,432)], w=4, lead=0.2, tail=0.3, swell=0.3, smoothing=sm))                    # a pendant cord
    S.append(dict(ctrl=[(972,432),(986,464),(1000,432)], w=5, lead=0.25, tail=0.25, swell=0.3, smoothing=sm))       # pendant shade
    # ===== the figure — reclined low, loose, legs extended toward the light,
    # gazing level out. Bigger, sitting at the edge of light and shadow. =====
    # line of action: extended feet -> legs -> reclined torso -> turned head
    S.append(dict(ctrl=[(486,690),(432,572),(388,470),(366,420)], w=11, tail=0.16, swell=0.44, smoothing=sm))       # reclined back, leaning back
    S.append(dict(ctrl=[(366,420),(356,372),(362,334),(406,328),(426,366)], w=8.5, lead=0.10, tail=0.22, swell=0.35, smoothing=sm))  # head, back of skull to face-side
    S.append(dict(ctrl=[(426,366),(422,404),(398,424)], w=6, lead=0.18, tail=0.34, swell=0.3, phase=0.6, smoothing=sm))             # jaw, gaze level right (no face)
    S.append(dict(ctrl=[(362,334),(400,326),(424,350)], w=5.5, lead=0.22, tail=0.3, swell=0.5, phase=1.0, smoothing=sm))            # hair
    S.append(dict(ctrl=[(398,440),(440,566),(490,672)], w=7.5, lead=0.14, tail=0.24, swell=0.35, phase=1.0, smoothing=sm))          # chest/front of torso
    S.append(dict(ctrl=[(486,676),(624,716),(704,730)], w=9.5, lead=0.14, swell=0.42, smoothing=sm))               # thigh extended forward
    S.append(dict(ctrl=[(704,730),(824,754),(884,762)], w=8, lead=0.12, swell=0.42, cap_end=True, smoothing=sm))    # shin/foot, legs really out, crop
    # near arm arriving AT the notebook (welded), notebook reads as a notebook
    S.append(dict(ctrl=[(400,464),(436,576),(496,660),(536,668)], w=7.5, lead=0.12, tail=0.07, swell=0.4, smoothing=0.7))
    S.append(dict(ctrl=[(516,648),(606,658)], w=4.6, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))      # notebook top
    S.append(dict(ctrl=[(520,676),(602,688)], w=4.0, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))      # notebook bottom
    S.append(dict(ctrl=[(560,650),(562,682)], w=3.2, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))       # notebook spine
    # the low chair — just enough to seat him
    S.append(dict(ctrl=[(348,466),(340,664)], w=6, lead=0.14, swell=0.3, cap_end=True, smoothing=sm))               # chair back behind torso
    S.append(dict(ctrl=[(344,668),(492,684)], w=6, lead=0.2, swell=0.3, smoothing=sm))                              # seat
    # ===== shadow accents (the rake gradient does the atmosphere) — just a darker
    # corner and a beam band; light stays bare =====
    shadows = [
        dict(kind="poly", pts=[(0,0),(420,0),(300,260),(0,360)], blur=80, strength=0.34),       # upper-left corner accent
        dict(kind="poly", pts=[(0,0),(1300,0),(1300,80),(0,150)], blur=60, strength=0.24),       # faint top beam band
    ]
    return S, shadows

if __name__ == "__main__":
    S, shadows = beat_notebook()
    render_interior(S, shadows, W, H, seed=3).save(f"{OUT}/arc_notebook_interior.png")
    print("done")
