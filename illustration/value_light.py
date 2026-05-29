"""
STAGE 4 — value & light. Built body (stage 3) in the built room (stage 1) under
one warm raking light from the doorway.

THE MOVE IS AN INVERSION: light is the linen you LEAVE ALONE. You do not fill the
figure and hunt for shadow inside the fill (that's the flat-shape failure). You
leave the lit side as untouched bright linen and lay a few soft warm shapes only
on the shadow side, with one clear terminator where the light breaks across him.

GATE B WITH TEETH (checked in code, not by feel — the lock, built as a reflex now
on every gate, not once):
  B1 linen-on-lit  — there is untouched bright linen on the lit side of the body.
  B2 terminator    — a real light->shadow edge lives ON the form (not just a floor
                     shadow): a transition band exists inside the figure.
  B3 two-values    — squint: a light shape AND a shadow shape read as two things,
                     i.e. lit-region and shadow-region luminance are clearly apart.
Plus: light reads (room glow + direction) and the body survives head-covered.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS, INK
from linen import linen_ground
from figure_construction import capsule, ellipse_poly

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1300, 950
WARM = np.array([92, 70, 58], float)        # room shadow
WARM_FIG = np.array([74, 55, 47], float)    # figure shadow (deeper)

def figure_masses(hide_head=False):
    shoulder=(414,392); waist=(508,548); crotch=(572,632)
    hip_n=(578,616); hip_f=(560,634); knee_n=(764,654); ankle_n=(902,708)
    knee_f=(736,694); ankle_f=(866,746); elbowP=(366,506); wristP=(322,642)
    elbowN=(492,540); handN=(616,628)
    M=[]
    M.append(ellipse_poly(467,470,80,56, np.arctan2(156,94)))        # ribcage
    M.append(ellipse_poly(540,590,52,48, np.arctan2(84,64)))         # pelvis
    M.append(capsule(hip_n,knee_n,30,24)); M.append(capsule(knee_n,ankle_n,23,16))
    M.append(capsule(ankle_n,(ankle_n[0]+34,ankle_n[1]+6),15,7))
    M.append(capsule(hip_f,knee_f,28,22)); M.append(capsule(knee_f,ankle_f,21,15))
    M.append(capsule(ankle_f,(ankle_f[0]+32,ankle_f[1]+6),14,7))
    M.append(capsule(shoulder,elbowP,24,20)); M.append(capsule(elbowP,wristP,20,15))
    M.append(capsule((426,406),elbowN,21,16)); M.append(capsule(elbowN,handN,16,11))
    if not hide_head:
        M.append(capsule(shoulder,(388,352),18,16)); M.append(ellipse_poly(360,298,42,50,-0.18))
    action=[(404,372),(452,470),(520,560),(576,628)]
    hands=[(wristP[0]+dx-6,wristP[1]+8,wristP[0]+dx-10,wristP[1]+34) for dx in (-10,0,10,20)]
    return M, action, hands

def fill_mask(polys):
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    for p in polys: d.polygon([(float(x),float(y)) for x,y in p], fill=255)
    return np.asarray(im,float)/255.0

def soft(a,r):
    return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0

# THREE GUARDS on changing any lock (an honest fix vs a quiet goalpost move):
#   1. A change to the test is only honest if you would make the same change when
#      it causes you to FAIL, not only when it lets you pass.
#   2. The IMAGE has to move, not just the number. If only the metric changed, you
#      fudged it.
#   3. Your EYE is the final word over the readout. The number serves the eye,
#      never the reverse.
def gate_B(img, fig, sh, dim, verbose=True):
    """The lock. Measure, don't feel. (See the three guards above.)"""
    lum = img.mean(2)
    figm = fig > 0.5
    lit  = figm & (sh < 0.18)
    shad = figm & (sh > 0.65)
    band = figm & (sh > 0.25) & (sh < 0.75)
    # reference = bare, UN-DIMMED linen (what "light = linen left alone" looks like)
    bright_ref = np.median(lum[(fig < 0.03) & (dim < 0.12)])
    litL = lum[lit].mean() if lit.sum() else 0.0
    shadL = lum[shad].mean() if shad.sum() else 0.0
    # B1: is there UNTOUCHED bright linen on the lit side? Measure the fraction of
    # the lit side at/above linen brightness (a filled figure scores ~0 -> fails;
    # a bare lit side with a few lines on it scores high -> passes). Mean would be
    # wrongly dragged down by the contour lines, so fraction is the honest test.
    frac_linen = (lum[lit] >= 0.95*bright_ref).mean() if lit.sum() else 0.0
    B1 = lit.sum() > 0.06*figm.sum() and frac_linen >= 0.5
    B2 = band.sum() > 0.03*figm.sum()                              # a terminator lives on the form
    B3 = (shad.sum() > 0.06*figm.sum()) and (litL - shadL) >= 26   # two clearly separate values
    if verbose:
        print(f"  B1 linen-on-lit : {'PASS' if B1 else 'FAIL'}  ({100*frac_linen:.0f}% of the lit side is untouched linen)")
        print(f"  B2 terminator   : {'PASS' if B2 else 'FAIL'}  (transition band {100*band.sum()/figm.sum():.0f}% of body)")
        print(f"  B3 two-values   : {'PASS' if B3 else 'FAIL'}  (lit {litL:.0f} - shadow {shadL:.0f} = {litL-shadL:.0f})")
    return B1 and B2 and B3

def render_lit(hide_head=False, seed=4, verbose=True):
    M, action, hands = figure_masses(hide_head)
    fig = soft((fill_mask(M) > 0.5).astype(float), 2.0)
    ys, xs = np.where(fig > 0.4); cx, cy = xs.mean(), ys.mean()
    figw, figh = xs.max()-xs.min(), ys.max()-ys.min()
    yy, xx = np.mgrid[0:H, 0:W].astype(float)

    linen = linen_ground(W, H, seed=seed, tone=0.5)              # the BRIGHT base = light

    # ---- room: light rakes from the doorway (right); dim gathers left ----
    dim = np.clip((560-xx)/430, 0, 1)*0.82 + 0.12*(1-yy/H)
    dim = soft(np.clip(dim-0.05,0,1), 42) * 0.8
    glow = soft(np.clip(1-np.hypot((xx-1085)/400,(yy-470)/420),0,1), 40)
    cs = Image.new("L",(W,H),0); dd=ImageDraw.Draw(cs)
    for p in M:
        pts=[(float(x-70),760.0) for x,y in p if y>560]
        if len(pts)>=3: dd.polygon(pts, fill=255)
    cast = soft(np.asarray(cs,float)/255.0,24)*(yy>706)*(xx<620)*0.20

    out = linen.copy()
    out = out*(1-dim[...,None]) + WARM*dim[...,None]
    out = np.clip(out + glow[...,None]*np.array([40,28,13.]), 0, 255)
    out = out*(1-cast[...,None]) + WARM*cast[...,None]

    # ---- INVERSION: tone ONLY the shadow side; lit side = untouched bright linen ----
    # light from the right (doorway) -> shadow is the LEFT/away side. Mostly
    # horizontal split so the legs & chest-top (facing the light) stay bare linen;
    # a little underside weight so the shadow sits under the form, not as a wall.
    t = (cx-xx)*0.80 + (yy-cy)*0.34
    scale = 0.80*figw*0.5 + 0.34*figh*0.5
    thr = np.quantile(t[fig>0.4], 0.52)                          # ~52% lit (linen), ~48% shadow
    sh = np.clip((t-thr)/(0.13*scale), 0, 1)                     # tighter terminator band
    sh = soft(sh*fig, 5)
    sh = np.where(sh < 0.16, 0.0, sh)                            # LEAVE THE LIGHT ALONE: lit side = exactly bare linen
    k = (sh*fig*0.85)[..., None]
    figcol = linen*(1-k) + WARM_FIG*k                            # lit = linen (left alone); shadow = warm
    m = fig[..., None]
    out = out*(1-m) + figcol*m

    # ---- a few committed lines: doorway, floor, figure contour, action line ----
    def ink(strokes):
        im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
        for s in strokes: stroke(d, **s)
        return np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    struct=[dict(ctrl=[(1018,742),(1016,548)],w=5,cap_start=True,swell=0.3,smoothing=0.7),
            dict(ctrl=[(1016,548),(1070,430),(1148,372),(1210,470)],w=5,lead=0.12,tail=0.12,swell=0.3,smoothing=0.7),
            dict(ctrl=[(150,744),(1018,738)],w=4.5,cap_start=True,swell=0.25,smoothing=0.8)]
    edge=(fig>0.45).astype(float); edge=np.clip(edge-soft(edge,1.6),0,1)
    a_struct=ink(struct)
    a_action=ink([dict(ctrl=action,w=6,lead=0.1,tail=0.16,swell=0.4,smoothing=0.72)]
                +[dict(ctrl=[(x0,y0),(x1,y1)],w=3.6,cap_start=True,cap_end=True,swell=0.2,smoothing=0.9) for (x0,y0,x1,y1) in hands])
    a_line=np.clip(soft(edge,0.6)*0.85 + a_struct + a_action, 0, 1)
    out = out*(1-a_line[...,None]) + INK*a_line[...,None]

    img = np.clip(out,0,255)
    if verbose: gate_B(img, fig, sh, dim)
    return Image.fromarray(img.astype(np.uint8))

if __name__ == "__main__":
    print("gate B —", "head:")
    render_lit(False).save(f"{OUT}/stage4_lit.png")
    print("  head-covered:")
    render_lit(True).save(f"{OUT}/stage4_lit_headless.png")
    print("done")
