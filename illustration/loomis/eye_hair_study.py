"""
EYE + HAIR STUDIES (researched).
EYE: the eyeball is a SPHERE; the lids wrap it like latitude lines and have
THICKNESS — the upper lid's underside is in shadow, the lower lid's top plane
catches light. A soft cast shadow from the upper lid falls across the top of the
iris. Iris = limbal ring + pupil + a catchlight straddling both, on the light
side. Tear duct (caruncle) at the inner corner. The eye sits in a socket.
HAIR: think in MASSES (front / side / top), flow lines along the growth, shadow
at the roots and under overlapping clumps, one or two BARE highlight shapes for
gloss — never individual strands. Light from the upper-left throughout.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=1280,720
PAPER=np.array([237,232,223],float); INK_SH=np.array([50,50,64],float)
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.4*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)

def draw(strokes):
    im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
    for s in strokes: stroke(d,**s)
    return np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0

def eye_strokes(ex,ey):
    S=[]
    def a(c,w,lead=0.16,tail=0.22,swell=0.32,sm=0.62,cs=False,ce=False):
        S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # upper lid (strongest), arcing over the ball; inner corner low, outer slightly up
    a([(ex-150,ey+14),(ex-60,ey-44),(ex+40,ey-50),(ex+150,ey-12)],5.0,lead=0.1,tail=0.2,swell=0.4)
    # upper-lid THICKNESS (underside plane, just inside/below the lid)
    a([(ex-120,ey+8),(ex-40,ey-30),(ex+50,ey-34),(ex+130,ey-6)],2.0,lead=0.3,tail=0.3,swell=0.16)
    # lower lid (lighter) + its top-plane thickness (a thin lit line just under)
    a([(ex-150,ey+16),(ex-50,ey+58),(ex+60,ey+52),(ex+150,ey-8)],2.6,lead=0.2,tail=0.28,swell=0.2)
    a([(ex-120,ey+26),(ex-40,ey+50),(ex+60,ey+44)],1.3,lead=0.34,tail=0.34,swell=0.12)
    # crease above the upper lid (the orbital fold)
    a([(ex-120,ey-30),(ex-30,ey-66),(ex+70,ey-70),(ex+150,ey-40)],1.6,lead=0.32,tail=0.32,swell=0.14)
    # iris (limbal ring) + pupil; top tucked under the upper lid
    a([(ex-58,ey-18),(ex-58,ey+44)],0.1)  # placeholder (drawn as ellipse below)
    # tear duct / caruncle (inner corner)
    a([(ex-150,ey+12),(ex-162,ey+2),(ex-152,ey-6)],2.0,lead=0.3,tail=0.32,swell=0.16)
    # brow
    a([(ex-150,ey-86),(ex-40,ey-104),(ex+80,ey-92),(ex+150,ey-74)],6.0,lead=0.12,tail=0.22,swell=0.46)
    return S

def render():
    out=np.ones((H,W,3))*PAPER
    ex,ey=330,340
    # --- EYE shading (built before line): eyeball sphere, lid cast shadow, socket ---
    # eye-opening mask (almond) to contain eyeball shading
    opening=( ((xx-ex)/170)**2 + ((yy-(ey+2))/64)**2 <=1 ).astype(float)
    iris=( ((xx-(ex-6))/58)**2 + ((yy-(ey+6))/58)**2 <=1 ).astype(float)*opening
    pupil=( ((xx-(ex-6))/24)**2 + ((yy-(ey+6))/24)**2 <=1 ).astype(float)
    # cast shadow from the upper lid across the top of the eyeball/iris (soft crescent)
    castlid=soft(np.clip(opening*(yy<ey+6),0,1)*np.clip(1-(ey+6-yy)/52,0,1),3)
    # eyeball white shaded as a sphere (shadow to the right), iris darker, limbal ring + pupil dark
    g = castlid*0.30*stripes(-0.5,6,1.5,1)
    g = g + iris*0.42*stripes(0.5,5,1.4,2)                 # iris tone
    g = g + soft((iris-soft(iris,3)).clip(0,1),1)*0.5      # limbal ring (rim of iris)
    g = g + pupil*0.95                                     # pupil dark
    g = g + soft((opening*(xx>ex+60)).astype(float),3)*0.12*stripes(-0.5,6,1.5,3)  # white shadow side
    g = g + soft(g2(ex,ey-92,150,30,0.5),4)*0.4*stripes(0.6,6,1.4,4)               # socket shadow under brow
    g=np.clip(g,0,1)
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    # catchlight straddling iris+pupil, upper-left, bare paper
    cl=np.clip(soft(g2(ex-22,ey-12,7,8,1.0),0.6),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    ea=draw(eye_strokes(ex,ey))
    out=out*(1-ea[...,None]) + INK*ea[...,None]
    # iris + pupil circles as line (clean)
    im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
    d.ellipse([(ex-6-58)*SS,(ey+6-58)*SS,(ex-6+58)*SS,(ey+6+58)*SS],outline=255,width=int(2.0*SS))
    d.ellipse([(ex-6-24)*SS,(ey+6-24)*SS,(ex-6+24)*SS,(ey+6+24)*SS],outline=255,width=int(2.0*SS))
    ia=np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0; ia=ia*opening   # clip iris line to opening (under lid)
    out=out*(1-ia[...,None]) + INK*ia[...,None]
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]          # re-assert catchlight on top

    # --- HAIR mass study (right) ---
    hx,hy=860,360
    crown=Image.new("L",(W*SS,H*SS),0); cd=ImageDraw.Draw(crown)
    cd.ellipse([(hx-150)*SS,(hy-150)*SS,(hx+150)*SS,(hy+110)*SS],outline=120,width=int(1.3*SS))  # cranium (faint)
    cra=np.asarray(crown.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-(cra*0.5)[...,None]) + np.array([150,146,138],float)*(cra*0.5)[...,None]
    # hair masses (filled silhouette) sitting ON the cranium with volume above
    hairmask=Image.new("L",(W,H),0); hd=ImageDraw.Draw(hairmask)
    hd.polygon([(hx-150,hy-10),(hx-168,hy-120),(hx-110,hy-186),(hx-10,hy-208),(hx+110,hy-188),
                (hx+170,hy-110),(hx+150,hy+10),(hx+120,hy-70),(hx+40,hy-150),(hx-70,hy-150),(hx-130,hy-70)],fill=255)
    hm=(soft(np.asarray(hairmask,float)/255.0,2)>0.5).astype(float)
    # shadow at roots + shadow side + under clumps; one bare highlight band
    hsh = soft(g2(hx-90,hy-90,60,70,0.7)+g2(hx+10,hy-40,120,40,0.5)+g2(hx+90,hy-100,60,90,0.6),6)*hm
    hi  = soft(g2(hx-20,hy-150,80,30,1.0,-0.2),5)   # gloss band (left bare)
    hg=np.clip(hsh*0.5*stripes(-1.0,5,1.6,5) - hi*0.8,0,1)*hm
    out=out*(1-hg[...,None]) + INK_SH*hg[...,None]
    # flow strokes + silhouette (clumps from the crown/part outward)
    hs=[]
    def ha(c,w): hs.append(dict(ctrl=c,w=w,lead=0.3,tail=0.3,swell=0.2,smoothing=0.6))
    ha([(hx-150,hy+8),(hx-166,hy-118),(hx-108,hy-186),(hx-10,hy-208)],3.2)       # silhouette L
    ha([(hx-10,hy-208),(hx+108,hy-188),(hx+170,hy-108),(hx+150,hy+8)],3.4)       # silhouette R
    ha([(hx-40,hy-200),(hx-60,hy-120),(hx-90,hy-30)],2.0)                        # flow: top->side L
    ha([(hx+10,hy-204),(hx+10,hy-110),(hx-6,hy-30)],1.8)
    ha([(hx+50,hy-196),(hx+80,hy-110),(hx+96,hy-30)],2.0)                        # flow R
    ha([(hx-90,hy-150),(hx-30,hy-176),(hx+40,hy-178),(hx+100,hy-150)],1.6)       # part/crown line
    for fx in (-110,-66,-20,30,80,120):
        ha([(hx+fx,hy-150),(hx+fx*1.05,hy-90),(hx+fx*1.1,hy-30)],1.2)            # finer flow within clumps
    ha=draw(hs)
    out=out*(1-ha[...,None]) + INK*ha[...,None]

    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)); dd=ImageDraw.Draw(img)
    dd.text((40,40),"EYE — sphere + wrapping lids w/ thickness, lid cast shadow, limbal ring, catchlight, caruncle",fill=(70,66,64))
    dd.text((720,40),"HAIR — masses + flow, shadow at roots, one bare gloss band",fill=(70,66,64))
    return img

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/eye_hair_study.png"); print("done")
