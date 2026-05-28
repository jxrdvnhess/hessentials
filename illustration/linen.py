"""
Hessentials — drawing-on-linen candidate generator.
Programmatic synthesis (no diffusion): authored imperfection is the point.

Two sources:
  A) Re-ground Jordan's own hand-drawn face (fully owned, genuinely misregistered)
  B) Procedural blind-contour faces — one wandering navy line with authored
     overshoot, doubling-back, and per-feature misregistration.

Target per drawing-style-study.md: thin near-continuous navy line, features
recognizable but spatially displaced, raw woven-linen ground, huge negative
space, no shading, loose / off-center, intimate. NOT clean / symmetrical /
decorative / vector-like.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(OUT, exist_ok=True)

# Sampled from this.jpg
LINEN_RGB = np.array([190, 173, 152], float)
INK_RGB   = np.array([28, 31, 44], float)   # dark navy near-black

# ---------------------------------------------------------------- linen ground
def linen_ground(w, h, seed=0, tone=0.0):
    """Warm tan woven texture. tone shifts overall warmth/value slightly."""
    rng = np.random.default_rng(seed)
    base = LINEN_RGB + np.array([tone*6, tone*4, tone*2])
    img = np.ones((h, w, 3)) * base

    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    # woven tooth with WANDERING thread spacing (organic, not graph-paper).
    # Phase accumulates a noisy step so thread pitch drifts across the cloth.
    px = (3.0 + rng.normal(0, 0.9, w).cumsum()*0.0 + np.cumsum(0.9+rng.normal(0,0.18,w)))
    py = (np.cumsum(1.0+rng.normal(0,0.20,h)))
    warp = np.sin(px[None, :]*1.9) * (5.5 + rng.normal(0, 1.4, (1, w)))
    weft = np.sin(py[:, None]*1.7) * (5.5 + rng.normal(0, 1.4, (h, 1)))
    # broken threads: some rows/cols fade (slubs)
    warp *= (0.6 + 0.4*np.clip(np.sin(px[None,:]*0.13)+rng.normal(0,0.3,(1,w)),0,1))
    weft *= (0.6 + 0.4*np.clip(np.sin(py[:,None]*0.11)+rng.normal(0,0.3,(h,1)),0,1))
    img += (warp + weft)[..., None]

    # fiber grain (fine) + horizontal slub streaks (coarse)
    img += rng.normal(0, 5.5, (h, w, 1))
    slub = rng.normal(0, 1, (h, 1))
    slub = np.asarray(Image.fromarray(((slub-slub.min())/(np.ptp(slub)+1e-6)*255)
            .astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), float)/255.0
    img += (slub[..., None]-0.5) * 9.0

    # large-scale uneven dye (low-freq luminance drift)
    lf = rng.normal(0, 1, (h//40+2, w//40+2))
    lf = np.asarray(Image.fromarray(((lf-lf.min())/(np.ptp(lf)+1e-6)*255).astype(np.uint8))
                    .resize((w, h), Image.BICUBIC), float)/255.0
    img += (lf[..., None]-0.5) * 14.0

    # faint vignette so the panel feels lit, not flat
    cx, cy = w*0.5, h*0.46
    r = np.sqrt(((xx-cx)/(w*0.62))**2 + ((yy-cy)/(h*0.62))**2)
    img -= (np.clip(r-0.55, 0, 1)**1.6 * 20)[..., None]

    return np.clip(img, 0, 255)

def ink_on_linen(linen, ink_alpha):
    """Composite ink (alpha 0..1, HxW) onto linen by darkening toward INK_RGB,
    so the woven tooth still shows through the line (ink soaked into fabric)."""
    a = ink_alpha[..., None]
    out = linen*(1-a) + INK_RGB*a
    # let a little linen luminance modulate the ink (fabric breaking the stroke)
    lum = linen.mean(2, keepdims=True)/255.0
    out += (lum-0.62) * a * 18
    return np.clip(out, 0, 255)

# ----------------------------------------------------- stroke rendering helpers
def stroke_alpha(w, h, polylines, width=2.4, jitterblur=0.6, supersample=2):
    """Render polylines to a high-res alpha mask, with slight blur for ink feel."""
    W, H = w*supersample, h*supersample
    canvas = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(canvas)
    for pts, ww in polylines:
        p = [(x*supersample, y*supersample) for x, y in pts]
        lw = max(1, int(round(ww*supersample)))
        d.line(p, fill=255, width=lw, joint="curve")
        # round the ends/joints
        r = lw/2.0
        for (x, y) in (p[0], p[-1]):
            d.ellipse([x-r, y-r, x+r, y+r], fill=255)
    canvas = canvas.filter(ImageFilter.GaussianBlur(jitterblur*supersample))
    a = np.asarray(canvas.resize((w, h), Image.LANCZOS), float)/255.0
    return np.clip(a*1.15, 0, 1)

def wander(p0, p1, n, rng, drift=0.0, jitter=1.0, overshoot=0.0):
    """Points from p0->p1 with low-freq drift (proportion wander) + hi-freq
    tremor (hand). overshoot pushes a little past p1."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    if overshoot:
        p1 = p1 + d*overshoot
        d = p1 - p0
    t = np.linspace(0, 1, n)
    perp = np.array([-d[1], d[0]]);
    nrm = np.linalg.norm(perp)+1e-6; perp = perp/nrm
    # low freq drift (a couple of slow bows)
    lf = (np.sin(t*np.pi*rng.uniform(0.7,1.6)+rng.uniform(0,6))*rng.uniform(0.5,1.0)
          + np.sin(t*np.pi*rng.uniform(1.5,3)+rng.uniform(0,6))*rng.uniform(0.2,0.5))
    lf = lf*drift
    # hi freq tremor
    hf = np.cumsum(rng.normal(0, jitter, n)); hf -= np.linspace(hf[0], hf[-1], n)
    off = (lf + hf*0.6)[:, None]*perp
    base = p0[None,:] + t[:,None]*d[None,:]
    return base + off

def short_hatch(center, span, count, ang, rng, length=10):
    """Short repeated strokes (brow / lash texture)."""
    cx, cy = center
    out=[]
    for i in range(count):
        f = (i/(count-1)-0.5) if count>1 else 0
        bx = cx + np.cos(ang)*f*span + rng.normal(0,1.2)
        by = cy + np.sin(ang)*f*span + rng.normal(0,1.2)
        a2 = ang + np.pi/2 + rng.normal(0,0.25)
        L = length*rng.uniform(0.6,1.2)
        out.append(([(bx,by),(bx+np.cos(a2)*L, by+np.sin(a2)*L)], 1.6))
    return out

# --------------------------------------------------- B) procedural blind contour
# Modeled on this.jpg: an INTERIOR contour (brow -> nose ridge -> lips -> far
# cheek -> far brow), face oval only implied, downcast almond eyes, NO closed
# jaw outline (the closed jaw is what made v1 read as a hard mask). Soft long
# bows, low tremor, the line wanders and overshoots but never zig-zags.
def proc_face(w, h, seed):
    rng = np.random.default_rng(seed)
    fw = w*rng.uniform(0.26,0.32); fh = fw*rng.uniform(1.15,1.32)
    cx = w*rng.uniform(0.42,0.56); cy = h*rng.uniform(0.44,0.55)
    def P(dx, dy, mis=0.0):
        return (cx+dx*fw + rng.normal(0,mis*fw),
                cy+dy*fh + rng.normal(0,mis*fh))
    polys=[]
    def seg(a,b,n=46,drift=5,jit=0.55,ov=0.0,wd=2.2):
        polys.append((list(map(tuple, wander(a,b,n,rng,drift,jit,ov))), wd))
    def curve(pts,n=18,drift=3,jit=0.5,wd=2.1):
        for i in range(len(pts)-1):
            seg(pts[i],pts[i+1],n,drift,jit,0.0,wd)

    # --- the one searching interior line ---
    # left brow (high, hatched anchor) -> down the nose ridge
    lbrow_o=P(-0.34,-0.50,0.02); lbrow_i=P(-0.04,-0.42,0.03)
    bridge =P(-0.02,-0.30,0.03); nose_mid=P(-0.07,-0.04,0.04)
    nose_b =P(-0.10, 0.12,0.05); nostril=P(0.01,0.16,0.04)
    curve([lbrow_o,lbrow_i,bridge,nose_mid,nose_b], drift=5, jit=0.55, wd=2.2)
    seg(nose_b, nostril, 16, 3, 0.5, 0.10, 2.0)        # little nostril hook
    # lips — soft cupid + lower lip, a touch low (parted)
    m_l=P(-0.17,0.34,0.04); cupid=P(-0.01,0.31,0.03); m_r=P(0.17,0.35,0.05)
    low =P(0.0,0.45,0.04)
    curve([nostril,m_l,cupid,m_r], n=16, drift=3, jit=0.5, wd=2.1)
    curve([m_r,low,m_l], n=18, drift=4, jit=0.55, wd=2.0)   # lower lip back (crosses a hair)
    # up the far (right) cheek to the right brow
    cheek=P(0.30,0.10,0.05); rbrow_i=P(0.12,-0.40,0.05); rbrow_o=P(0.40,-0.46,0.03)
    curve([m_r,cheek,rbrow_i,rbrow_o], n=22, drift=6, jit=0.6, wd=2.2)
    # a single soft left cheek line that trails off (open, never closes the oval)
    seg(P(-0.26,-0.18,0.04), P(-0.30,0.22,0.05), 30, 7, 0.6, 0.0, 2.0)

    # --- downcast almond eyes (off-axis: the misregistration tell) ---
    def eye(ec, ew, eh, droop, mis):
        c=P(ec[0],ec[1],mis)
        top=[(c[0]-ew, c[1]+rng.normal(0,1)),
             (c[0]-ew*0.3, c[1]-eh), (c[0]+ew*0.4, c[1]-eh*0.8),
             (c[0]+ew, c[1]+droop)]
        bot=[(c[0]+ew, c[1]+droop),
             (c[0]+ew*0.2, c[1]+eh*0.5), (c[0]-ew*0.5, c[1]+eh*0.4),
             (c[0]-ew, c[1]+rng.normal(0,1))]
        curve(top, n=14, drift=2.5, jit=0.4, wd=2.0)
        curve(bot, n=14, drift=2.5, jit=0.4, wd=1.9)
        return c
    re=eye((0.20,-0.18), fw*0.13, fh*0.09, fh*0.02, 0.05)   # right eye
    le=eye((-0.20,-0.13), fw*0.13, fh*0.09, fh*0.02, 0.06)  # left eye, lower (off-axis)

    # brow hatches
    polys += short_hatch(lbrow_o, fw*0.30, 6,
              np.arctan2(lbrow_i[1]-lbrow_o[1], lbrow_i[0]-lbrow_o[0]), rng, length=fw*0.045)
    polys += short_hatch(rbrow_o, fw*0.30, 6,
              np.arctan2(rbrow_o[1]-rbrow_i[1], rbrow_o[0]-rbrow_i[0]), rng, length=fw*0.045)

    a = stroke_alpha(w,h,polys,width=rng.uniform(2.0,2.5),jitterblur=rng.uniform(0.5,0.75))
    linen = linen_ground(w,h,seed=seed*7+1,tone=rng.uniform(-0.6,0.6))
    out = ink_on_linen(linen, a*rng.uniform(0.85,0.94))
    return Image.fromarray(out.astype(np.uint8))

# ----------------------------------------------------------------------- render
if __name__ == "__main__":
    W, H = 1500, 1100   # closing-panel proportion, room for a line in the void
    for i, s in enumerate([3, 7, 19, 23, 31, 42], start=1):
        proc_face(W, H, seed=s).save(f"{OUT}/blindcontour_{i}.png")
    print("done:", sorted(os.listdir(OUT)))
