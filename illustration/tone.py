"""
Hessentials — TONAL illustrator (v3). The leap past single-line work.

Applies Andrew Loomis's Form Principle (Creative Illustration, 1947):
form is revealed by light, organized into GROUPED VALUES —
  light  ->  halftone  ->  core (form) shadow  ->  reflected light  ->  cast shadow
— with a limited value set and CONTROLLED EDGES (hard / soft / lost). Lights
are kept together, shadows kept together; reflected light never competes with
the lights. Rendered warm on linen (sepia, never gray), with the living ink
line laid on top.

This is programmatic synthesis (PIL/NumPy), no diffusion.
"""
import numpy as np
from PIL import Image, ImageFilter
from linen import linen_ground, ink_on_linen, stroke_alpha
from face import face, EMOTIONS
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(OUT, exist_ok=True)

# warm value ramp (linen light -> warm umber-navy dark). NOT gray.
def value_to_rgb(v, linen_rgb):
    """v in 0..1 (0 dark shadow, 1 full light). Warm sepia ramp."""
    dark = np.array([54, 47, 52], float)     # warm near-black navy
    mid  = np.array([120, 101, 90], float)    # umber halftone
    v = np.clip(v, 0, 1)
    lo = dark + (mid-dark)*np.clip(v/0.55, 0, 1)[..., None]
    hi = mid + (linen_rgb-mid)*np.clip((v-0.55)/0.45, 0, 1)[..., None]
    return np.where(v[..., None] < 0.55, lo, hi)

def soft(mask, r):
    return np.asarray(Image.fromarray((mask*255).clip(0,255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(r)), float)/255.0

def render_tonal(emotion, w=1500, h=1100, seed=0, scale=0.52, pos=(0.58, 0.52),
                 tilt=-5, turn=0.12, light=(-0.55, -0.62, 0.56), tone=0.0,
                 with_line=True):
    rng = np.random.default_rng(seed*5+2)
    Hh = h*scale
    cx, cy = w*pos[0], h*pos[1]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)

    # ---- implied head ovoid (the big form) ----
    # The ovoid is the whole head incl. forehead: centred above the brow so
    # the eyes fall on the head's midline (Loomis proportion).
    cyo = cy - 0.06*Hh
    a = Hh*0.31                      # half width
    b = Hh*0.52                      # half height (forehead..chin)
    X = (xx-cx); Yo = (yy-cyo)
    nx = X/a; ny = Yo/b
    rr = nx**2 + ny**2
    inside = rr <= 1.0
    z = np.sqrt(np.clip(1-rr, 0, 1))            # front bulge
    Nx, Ny, Nz = nx, ny, np.clip(z*1.15, 1e-3, None)
    nlen = np.sqrt(Nx**2+Ny**2+Nz**2)+1e-6
    Nx, Ny, Nz = Nx/nlen, Ny/nlen, Nz/nlen
    L = np.array(light, float); L /= np.linalg.norm(L)
    lam = np.clip(Nx*L[0]+Ny*L[1]+Nz*L[2], 0, 1)   # lambert on the big form
    shade = 0.20 + 0.80*lam                          # ambient floor

    # ---- planar accents: where the form turns (Loomis planes) ----
    # feature pixel-Y in line-face coords (brow -0.17, eye -0.06, nose 0.16...)
    brow_y=cy-0.17*Hh; eye_y=cy-0.06*Hh; nose_y=cy+0.16*Hh
    mouth_y=cy+0.30*Hh; chin_y=cy+0.50*Hh
    def blob(px, py, sx, sy, depth, ang=0.0):
        ca, sa = np.cos(ang), np.sin(ang)
        u = ((X-px)*ca+((yy-py))*sa)/sx; v=(-(X-px)*sa+((yy-py))*ca)/sy
        return np.exp(-(u**2+v**2))*depth
    acc = np.zeros((h, w))
    acc += blob(cx-a*0.40, eye_y, a*0.30, Hh*0.06, 0.42)    # left eye socket
    acc += blob(cx+a*0.40, eye_y, a*0.30, Hh*0.06, 0.42)    # right eye socket
    acc += blob(cx, brow_y+Hh*0.02, a*0.62, Hh*0.04, 0.22)  # brow-ridge shadow under
    acc += blob(cx-a*0.16, nose_y-Hh*0.02, a*0.13, Hh*0.20, 0.40, ang=0.05) # nose side plane (cast by light L)
    acc += blob(cx+a*0.02, nose_y+Hh*0.02, a*0.22, Hh*0.05, 0.34)  # under-nose shadow
    acc += blob(cx, mouth_y+Hh*0.04, a*0.30, Hh*0.045, 0.34) # under lower lip
    acc += blob(cx+a*0.58, eye_y+Hh*0.04, a*0.34, Hh*0.34, 0.50, ang=0.12) # shadow-side cheek/jaw plane
    acc += blob(cx+a*0.30, chin_y-Hh*0.02, a*0.34, Hh*0.10, 0.30) # under-cheekbone toward jaw
    acc = soft(acc, Hh*0.010)
    shade = np.clip(shade - acc, 0.0, 1.0)

    # ---- reflected light inside the shadow near the form's dark rim ----
    rim = np.clip((rr-0.58)/0.42, 0, 1) * (lam < 0.34)
    shade = np.clip(shade + soft(rim*0.18, Hh*0.02), 0, 1)

    # ---- group / quantize into a limited value set (massing) ----
    edges = np.array([0.0, 0.26, 0.46, 0.66, 0.84, 1.01])
    centers = np.array([0.14, 0.34, 0.54, 0.74, 0.92])
    idx = np.clip(np.digitize(shade, edges)-1, 0, 4)
    grouped = centers[idx]
    # keep continuous modeling so it isn't posterized-flat (Loomis: massed,
    # not flat) — soften the band boundaries
    grouped = soft(grouped, Hh*0.006)*0.7 + shade*0.3

    # ---- cast shadow under the jaw (harder edge) on the linen ground ----
    cast = blob(cx+a*0.15, cy+b*1.06, a*0.62, b*0.20, 1.0, ang=-0.15)
    cast = soft((cast>0.35).astype(float), Hh*0.02)*0.22

    # ---- composite: tone darkens linen inside head; edges controlled ----
    linen = linen_ground(w, h, seed=seed*7+9, tone=tone)
    head_rgb = value_to_rgb(grouped, np.array([190,173,152.]))
    # head mask with LOST edges on the lit/top side, firmer on shadow/bottom
    m = inside.astype(float)
    m = soft(m, Hh*0.02)
    lost = np.clip((-(Ny) + (-Nx))*0.5, 0, 1)       # top-left lit side -> lose edge
    m = m * (1 - 0.45*soft(lost*(rr>0.7), Hh*0.03))
    out = linen*(1-m[...,None]) + head_rgb*m[...,None]
    out = out*(1-cast[...,None]) + np.array([70,60,62.])*cast[...,None]
    out = np.clip(out, 0, 255)

    # ---- living ink line on top ----
    if with_line:
        polys = face(emotion, seed, tilt, turn)
        px = []
        for pl, ww, life, ov in polys:
            pts = np.stack([cx + pl[:,0]*Hh, cy + pl[:,1]*Hh], 1)
            px.append(([(float(x),float(y)) for x,y in pts], max(1.4, ww*(Hh/520.0)*0.9)))
        la = stroke_alpha(w, h, px, width=1.0, jitterblur=0.6)
        out = out*(1-(la*0.7)[...,None]) + np.array([40,36,46.])*(la*0.7)[...,None]

    return Image.fromarray(out.astype(np.uint8))


def render_notan(emotion, w=900, h=1200, seed=0, scale=0.62, pos=(0.5, 0.46),
                 tilt=-5, turn=0.12, light=(-0.62, -0.45, 0.55), tone=0.0,
                 ground=(232, 226, 216), darks=(26, 24, 30)):
    """Two-value NOTAN — the squint view, Loomis's PATTERN taken to its limit.
    The head splits into one light mass and one dark mass with a HARD edge;
    features read as crisp dark marks inside the light. This is the bold
    black/white shape-design register (cf. the notan references)."""
    Hh = h*scale
    cx, cy = w*pos[0], h*pos[1]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    cyo = cy - 0.06*Hh
    a, b = Hh*0.31, Hh*0.52
    nx = (xx-cx)/a; ny = (yy-cyo)/b
    rr = nx**2 + ny**2
    inside = rr <= 1.0
    z = np.sqrt(np.clip(1-rr, 0, 1))
    Nx, Ny, Nz = nx, ny, np.clip(z*1.15, 1e-3, None)
    nlen = np.sqrt(Nx**2+Ny**2+Nz**2)+1e-6
    L = np.array(light, float); L /= np.linalg.norm(L)
    lam = (Nx*L[0]+Ny*L[1]+Nz*L[2])/nlen
    # ONE hard terminator: shadow mass where the form turns from the light
    shadow = inside & (lam < 0.18)
    # cast shadow shape under the jaw, connected to the dark mass
    cu = (xx-cx-a*0.18)/(a*0.7); cv = (yy-(cy+b*1.02))/(b*0.22)
    cast = (cu**2+cv**2) < 1.0
    mass = shadow | cast
    mass = soft(mass.astype(float), Hh*0.004) > 0.5     # crisp but anti-aliased
    out = np.where(mass[..., None], np.array(darks, float), np.array(ground, float))

    # features as crisp dark marks inside the LIGHT mass (the line, thresholded)
    polys = face(emotion, seed, tilt, turn)
    px = [([ (float(cx+x*Hh), float(cy+y*Hh)) for x, y in
             np.stack([pl[:, 0], pl[:, 1]], 1) ], max(2.0, ww*(Hh/520.0)))
          for pl, ww, life, ov in polys]
    la = stroke_alpha(w, h, px, width=1.0, jitterblur=0.35)
    la = (la > 0.35).astype(float)                       # crisp ink, not soft
    out = out*(1-la[..., None]) + np.array(darks, float)*la[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    # tone modeling (Form Principle)
    render_tonal(EMOTIONS["melancholy"], seed=14, with_line=False).save(f"{OUT}/tone_only.png")
    render_tonal(EMOTIONS["melancholy"], seed=14, with_line=True ).save(f"{OUT}/tone_line.png")
    render_tonal(EMOTIONS["serene"],     seed=21, with_line=True ).save(f"{OUT}/tone_serene.png")
    # notan (Pattern / two-value mass design)
    render_notan(EMOTIONS["melancholy"], seed=14).save(f"{OUT}/notan_melancholy.png")
    render_notan(EMOTIONS["serene"],     seed=21).save(f"{OUT}/notan_serene.png")
    print("done:", sorted(os.listdir(OUT)))
