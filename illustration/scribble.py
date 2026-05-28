"""
Hessentials — SCRATCH-TONE / scribble portrait (v4).

The register Jordan pulled: portraits built not from a clean contour but from
thousands of short, overlapping strokes that MASS into value. It is the union of
his whole arc — tone made out of line. Value still obeys the Form Principle
(light/halftone/shadow over a real head); the head emerges from a scratch field.

Method: build a continuous value field (ovoid lambert + planar accents + hair +
background vignette), then scatter short strokes with probability proportional
to local darkness and accumulate them into ink. Programmatic, no diffusion.
"""
import numpy as np
from PIL import Image, ImageFilter
from face import face
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(OUT, exist_ok=True)

GROUND = np.array([233, 227, 217], float)   # warm pale paper/linen
INK    = np.array([32, 29, 33], float)      # warm near-black

def _soft(m, r):
    return np.asarray(Image.fromarray((m*255).clip(0,255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(r)), float)/255.0

def value_field(emotion, w, h, seed, scale, pos, light):
    """Return darkness map D in [0,1] (1 = darkest) + head mask + (cx,cy,Hh)."""
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
    lam = np.clip((Nx*L[0]+Ny*L[1]+Nz*L[2])/nlen, 0, 1)
    dark = (1 - (0.20 + 0.80*lam))          # darkness on the big form

    brow_y=cy-0.17*Hh; eye_y=cy-0.06*Hh; nose_y=cy+0.16*Hh; mouth_y=cy+0.30*Hh
    def blob(px, py, sx, sy, d, ang=0.0):
        ca, sa = np.cos(ang), np.sin(ang)
        u = ((xx-px)*ca+(yy-py)*sa)/sx; v=(-(xx-px)*sa+(yy-py)*ca)/sy
        return np.exp(-(u**2+v**2))*d
    acc = np.zeros((h, w))
    acc += blob(cx-a*0.40, eye_y, a*0.30, Hh*0.06, 0.45)
    acc += blob(cx+a*0.40, eye_y, a*0.30, Hh*0.06, 0.45)
    acc += blob(cx-a*0.16, nose_y-Hh*0.02, a*0.13, Hh*0.20, 0.38, ang=0.05)
    acc += blob(cx+a*0.02, nose_y+Hh*0.02, a*0.22, Hh*0.05, 0.30)
    acc += blob(cx, mouth_y+Hh*0.04, a*0.30, Hh*0.045, 0.34)
    acc += blob(cx+a*0.58, eye_y+Hh*0.04, a*0.34, Hh*0.34, 0.50, ang=0.12)
    dark = np.clip(dark + acc, 0, 1) * inside

    # hair: dark cap over the crown / above the brow, inside the head
    hair = (inside & (yy < brow_y + Hh*0.02)).astype(float)
    hair *= _soft((inside & (yy < brow_y - Hh*0.05)).astype(float), Hh*0.03)*0.9 + 0.3
    dark = np.clip(dark + hair*0.7, 0, 1)

    # background scratch field: medium base + darker corners, so the lit face
    # reads as a light shape carved out of a dark scratch field
    cxn=(xx-w*0.5)/(w*0.6); cyn=(yy-h*0.5)/(h*0.6)
    vign = np.clip(np.sqrt(cxn**2+cyn**2)-0.2, 0, 1)**1.3
    bg = (0.28 + 0.45*vign) * (~inside)
    D = np.clip(dark + bg, 0, 1)
    D = _soft(D, Hh*0.008)
    return D, inside, (cx, cy, Hh)

def scribble_portrait(emotion, w=920, h=1180, seed=0, scale=0.60, pos=(0.5, 0.46),
                      tilt=-5, turn=0.12, light=(-0.6, -0.5, 0.55),
                      n_strokes=140000, ss=2, with_line=False):
    rng = np.random.default_rng(seed*9+3)
    D, mask, (cx, cy, Hh) = value_field(emotion, w, h, seed, scale, pos, light)

    W, Hpx = w*ss, h*ss
    canvas = np.zeros((Hpx, W), float)             # ink accumulation
    p = (D**1.6).flatten(); p = p/ p.sum()         # sharpen toward the darks
    idx = rng.choice(p.size, size=n_strokes, p=p)
    ys, xs = np.divmod(idx, w)
    ys = ys.astype(float)*ss + rng.uniform(0, ss, n_strokes)
    xs = xs.astype(float)*ss + rng.uniform(0, ss, n_strokes)
    dens = D[(ys/ss).astype(int).clip(0,h-1), (xs/ss).astype(int).clip(0,w-1)]
    # darker areas get slightly longer strokes; orientation mostly random with a
    # gentle global bias (hatch feel)
    base_ang = rng.uniform(0, np.pi)
    ang = np.where(rng.random(n_strokes) < 0.5,
                   base_ang + rng.normal(0, 0.5, n_strokes),
                   rng.uniform(0, np.pi, n_strokes))
    L = (5 + dens*14) * ss
    npts = 14
    t = np.linspace(-0.5, 0.5, npts)
    dx = np.cos(ang)[:, None]*L[:, None]*t[None, :]
    dy = np.sin(ang)[:, None]*L[:, None]*t[None, :]
    px = (xs[:, None] + dx).ravel()
    py = (ys[:, None] + dy).ravel()
    pix = np.clip(px.astype(int), 0, W-1)
    piy = np.clip(py.astype(int), 0, Hpx-1)
    np.add.at(canvas, (piy, pix), 0.6)
    # neighbour add for a hair of weight (thin nib, not 1px sharp)
    np.add.at(canvas, (np.clip(piy+1,0,Hpx-1), pix), 0.22)

    canvas = np.asarray(Image.fromarray((np.clip(canvas,0,6)/6*255).astype(np.uint8))
                        .resize((w, h), Image.LANCZOS), float)/255.0
    ink_a = 1 - np.exp(-6.0*canvas)               # overlaps saturate to dark
    out = GROUND*(1-ink_a[...,None]) + INK*ink_a[...,None]

    if with_line:
        from linen import stroke_alpha
        polys = face(emotion, seed, tilt, turn)
        ln = [([ (float(cx+x*Hh), float(cy+y*Hh)) for x,y in
                 np.stack([pl[:,0],pl[:,1]],1)], max(1.4, ww*(Hh/520.0)*0.8))
              for pl, ww, life, ov in polys]
        la = stroke_alpha(w, h, ln, width=1.0, jitterblur=0.5)*0.5
        out = out*(1-la[...,None]) + INK*la[...,None]

    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__ == "__main__":
    from face import EMOTIONS
    scribble_portrait(EMOTIONS["melancholy"], seed=14).save(f"{OUT}/scratch_melancholy.png")
    scribble_portrait(EMOTIONS["pensive"], seed=33, light=(-0.5,-0.55,0.6)).save(f"{OUT}/scratch_pensive.png")
    print("done:", [f for f in sorted(os.listdir(OUT)) if f.startswith("scratch")])
