"""
LIGHT & FORM — the form principle, then applied to the head.
Per the Standard: LIGHT = the lightest big value (bare paper left alone). SHADOW =
a FEW large soft shapes with a REAL turning edge (the terminator) — not a flat
fill, not smooth CG mud. Plus CORE shadow at the turn/pockets, REFLECTED light so
the shadow isn't dead, and CAST shadows. Massed in hatching so it reads DRAWN.

Left: a sphere with the 5 elements. Right: the Loomis front face lit upper-left.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/outputs/loomis")
from line_figure import stroke, SS, INK
from face_refined import face_strokes

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=1280,900
PAPER=np.array([237,232,223],float)
INK_SH=np.array([48,48,62],float)   # cool shadow ink (warm paper light -> cool shadow)
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.6*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)

def shade_to_ink(shadow, core, refl, mask, base=0.34):
    """Render the value ladder as DRAWN hatching: a light MID-TONE (halftone) band
    on the lit side of the turn, cross-hatch building toward the CORE at the
    terminator, REFLECTED light left lighter, clipped to mask."""
    h1=stripes(-0.5,6.0,1.5,1); h2=stripes(0.62,7.0,1.5,2); h3=stripes(1.5,6.0,1.4,3)
    half=np.clip((shadow-0.12)/0.33,0,1)               # mid-tone band starts off the light
    g = half*base*h1                                   # halftone (single, sparse)
    g = g + np.clip(shadow-0.45,0,1)*0.5*h2            # cross-hatch toward the core
    g = g + core*0.55*h3                               # core: darkest, at the turn
    g = g*(1-refl*0.85)                                # reflected light lifts the far edge
    return np.clip(g,0,1)*mask

# ---------------- SPHERE (the 5 elements) ----------------
def sphere(ox,oy,R):
    nx=(xx-ox)/R; ny=(yy-oy)/R; r2=nx*nx+ny*ny; z=np.sqrt(np.clip(1-r2,0,1))
    disc=(r2<=1).astype(float)
    L=np.array([-0.5,-0.5,0.70]); L/=np.linalg.norm(L)
    lam=np.clip(nx*L[0]+ny*L[1]+z*L[2],0,1)
    shadow=np.clip((1-lam-0.06)/0.5,0,1)*disc          # shadow family (terminator from the threshold)
    core=soft(((1-lam>0.55)&(1-lam<0.82)).astype(float)*disc,2)   # core-shadow crescent at the turn
    refl=soft((1-lam>0.86).astype(float)*disc,3)       # reflected light on the far rim
    # cast shadow on the ground (lower-right), crisp near edge
    cast=g2(ox+R*0.7,oy+R*1.06,R*0.9,R*0.34,1.0)
    cast=np.clip(cast-disc,0,1)
    return shadow,core,refl,disc,cast

# ---------------- HEAD shadow field ----------------
CX=470+150   # face centred in the right half (face_strokes drawn at cx=620)
def head_shadow():
    ox,oy,a,b=CX-2,400,168,244
    he=( ((xx-ox)/a)**2 + ((yy-oy)/b)**2 <= 1).astype(float); he=soft(he,6)
    # ONE clean terminator curve (right-of-centre, sweeping out at the jaw) -> the
    # light/shadow division is a single coherent shape with a real turning edge.
    ys=np.array([280,360,400,460,520,580,620,660,700])
    xs=np.array([CX+44,CX+30,CX+26,CX+30,CX+36,CX+54,CX+92,CX+128,CX+150])
    xterm=np.interp(np.arange(H), ys, xs)[:,None]
    shadow=np.clip((xx - xterm)/28.0 + 0.5, 0, 1) * he          # 0 lit .. 1 shadow
    # core: a band just inside the terminator (the form turning away)
    core=np.clip(1 - np.abs(xx - (xterm+20))/24.0, 0, 1) * he * (shadow>0.45)
    # a FEW clean cast/occlusion pockets (kept small, distinct)
    cast = (g2(CX,524,22,7,0.9) + g2(CX,608,30,6,0.7)            # under nose, under lip
            + g2(CX-44,416,15,11,0.45) + g2(CX+46,416,16,12,0.6) # eye sockets
            + g2(CX+78,620,58,30,0.6) + g2(CX+8,300,150,14,0.4)) # under jaw (shadow side), under hair
    core=np.clip(core + soft(cast,2)*he, 0, 1)
    # reflected light: lift the hatch near the far (right) turning edge so it isn't dead
    refl=soft( (((xx-ox)/a) > 0.66).astype(float)*he, 4)
    return shadow, core, refl, he

def head_silhouette(cx):
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.ellipse([cx-168,180,cx+168,540],fill=255)
    d.polygon([(cx-160,300),(cx-160,232),(cx-120,184),(cx-40,158),(cx+40,156),(cx+128,184),(cx+164,250),(cx+150,300)],fill=255)
    d.polygon([(cx-152,456),(cx-138,540),(cx-104,602),(cx,652),(cx+104,602),(cx+140,540),(cx+154,456)],fill=255)
    d.polygon([(cx-66,640),(cx+66,640),(cx+74,824),(cx+172,848),(cx-152,848),(cx-68,824)],fill=255)
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def render():
    out=np.ones((H,W,3))*PAPER
    # --- sphere study ---
    sh,co,re,disc,cast=sphere(210,300,120)
    # cast shadow: crisp at the contact point, softer farther away
    contact=np.clip(1-np.abs(xx-(210-30))/60,0,1)
    castg=cast*(0.34+0.16*contact)*stripes(-0.5,6,1.5,4)
    g=shade_to_ink(sh,co,re,disc,base=0.36) + castg
    g=np.clip(g,0,1) * (xx<350)               # keep the sphere study in the left panel
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    dctx=ImageDraw.Draw(Image.fromarray(out.astype(np.uint8)))
    # sphere outline + ground line (light)
    sm=Image.new("L",(W*SS,H*SS),0); sd=ImageDraw.Draw(sm)
    sd.ellipse([(210-120)*SS,(300-120)*SS,(210+120)*SS,(300+120)*SS],outline=255,width=int(1.6*SS))
    sd.line([(40*SS,420*SS),(332*SS,420*SS)],fill=255,width=int(1.4*SS))
    sa=np.asarray(sm.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-sa[...,None])+INK*sa[...,None]

    # --- head: line + light/form ---
    mask=head_silhouette(CX)
    sh,co,re,he=head_shadow()
    g=shade_to_ink(sh,co,re,mask,base=0.34)
    # cast shadow under the jaw onto the neck: crisp at the jaw, softening downward
    neck_cast=np.clip(1-(yy-664)/150,0,1)*(yy>664)*g2(CX+14,706,90,80,1.0)
    g=np.clip(g + soft(neck_cast,3)*mask*0.42*stripes(-0.5,6,1.5,7), 0,1)
    out=out*(1-(g)[...,None]) + INK_SH*(g)[...,None]
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(CX): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None]) + INK*fa[...,None]
    # eye catchlights
    cl=np.clip(soft(g2(CX-58-3,422,2.0,2.4,1.0)+g2(CX+58-3,422,2.0,2.4,1.0),0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)); dd=ImageDraw.Draw(img)
    dd.text((40,40),"FORM PRINCIPLE — light / halftone / terminator / core / reflected / cast",fill=(70,66,64))
    dd.text((560,40),"APPLIED — head lit upper-left, shadow massed as shapes",fill=(70,66,64))
    return img

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/light_form.png"); print("done")
