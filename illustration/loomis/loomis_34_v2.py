"""
LOOMIS 3/4 v2 — corrected to the references (RapidFireArt + master sheet):
  * DOMINANT round cranium ball; the face is COMPACT beneath it (not elongated).
  * Clear SIDE-PLANE disc on the visible side, with the EAR inside its lower-front.
  * STRONG ANGULAR masculine jaw: cheekbone -> jaw corner -> solid wide chin.
  * Heavy straight brows, features set low, strong straight nose bridge.
Faint construction under the finished head. Head faces our LEFT. Light front-left.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=1000,1120
PAPER=np.array([237,232,223],float); INK_SH=np.array([52,52,66],float)
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.4*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)
def catmull(pts,n=90):
    pts=np.array(pts,float); P=np.vstack([pts[0],pts,pts[-1]]); out=[]; seg=max(10,n//(len(pts)-1))
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,seg):
            t2,t3=t*t,t*t*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    return np.array(out)

BX,BY,R=470,372,170     # big cranium ball
def construction(d):
    def fl(pts,w=1.4): p=catmull(pts,90); d.line([(x*SS,y*SS) for x,y in p],fill=120,width=int(w*SS),joint="curve")
    def C(cx,cy,a,b,w=1.4): d.ellipse([(cx-a)*SS,(cy-b)*SS,(cx+a)*SS,(cy+b)*SS],outline=120,width=int(w*SS))
    C(BX,BY,R,R)                                   # the BALL (dominant)
    C(BX+96,BY-6,52,116)                           # SIDE-PLANE disc (visible side, right)
    fl([(BX-6,BY-R),(BX-46,BY-60),(BX-52,BY+58),(BX-44,BY+150),(BX-30,BY+R)],1.7)   # center line
    fl([(BX-170,BY+78),(BX-52,BY+58),(BX+96,BY-2),(BX+138,BY-10)],1.7)              # brow line wraps
    # angular jaw to chin
    fl([(BX-150,BY+70),(BX-140,BY+150),(BX-70,BY+248),(BX-30,BY+268)])
    fl([(BX+150,BY+30),(BX+150,BY+150),(BX+70,BY+250),(BX-30,BY+268)])
    for yy0 in (BY+58, BY+158, BY+268): fl([(BX-160,yy0),(BX+170,yy0)],1.0)         # thirds
    C(BX-58,BY+92,32,18); C(BX+44,BY+80,22,15)     # eye sockets

def face_strokes():
    S=[]; bx,by=BX,BY
    def a(c,w,lead=0.16,tail=0.22,swell=0.32,sm=0.58,cs=False,ce=False):
        S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # FRONT profile edge (left): forehead -> heavy brow -> bridge -> nose TIP -> lips -> chin
    a([(bx-58,by-150),(bx-128,by-40),(bx-150,by+58),(bx-150,by+96),    # forehead -> brow/temple
       (bx-128,by+120),(bx-118,by+150),(bx-128,by+170),               # bridge
       (bx-138,by+186),(bx-112,by+200),                               # nose tip (projecting) -> under-nose
       (bx-104,by+222),(bx-110,by+238),(bx-96,by+250),(bx-66,by+268)],3.4,lead=0.1,tail=0.16,swell=0.32)  # lips -> chin
    a([(bx-138,by+186),(bx-112,by+196),(bx-92,by+186)],2.2,lead=0.3,tail=0.32,swell=0.16)   # near nostril/base
    # TOP+BACK silhouette = the HAIR's own outer edge (ONE line, no separate bald-crown
    #   line -> kills the cap look), continuing down the back of the skull to the nape.
    a([(bx-58,by-150),(bx-66,by-202),(bx-8,by-234),(bx+64,by-238),(bx+140,by-212),(bx+202,by-138),
       (bx+222,by-36),(bx+222,by+58),(bx+196,by+150),(bx+168,by+196)],3.4,lead=0.1,tail=0.18,swell=0.36)
    a([(bx+168,by+196),(bx+150,by+236),(bx+96,by+268),(bx+18,by+276),(bx-30,by+268)],3.6,lead=0.06,tail=0.18,swell=0.34) # ANGULAR jaw -> chin
    a([(bx+138,by-4),(bx+146,by+96),(bx+120,by+170)],1.8,lead=0.32,tail=0.34,swell=0.14)    # side-plane front edge (the turn)
    a([(bx+30,by+150),(bx+70,by+128)],1.4,lead=0.36,tail=0.36,swell=0.12)                   # cheekbone accent
    a([(bx-46,by-150),(bx+8,by-166),(bx+72,by-156)],1.5,lead=0.3,tail=0.32,swell=0.12)      # hairline (hair meets the forehead)
    for p in [((bx-8,by-210),(bx+58,by-194),(bx+130,by-160)),((bx+30,by-226),(bx+104,by-202),(bx+168,by-150))]:
        a(list(p),1.2,lead=0.36,tail=0.36,swell=0.1)                                        # a couple hair flow strands
    # HEAVY STRAIGHT BROWS (masculine)
    a([(bx-132,by+50),(bx-84,by+40),(bx-40,by+52)],5.2,lead=0.1,tail=0.2,swell=0.48)        # near brow
    a([(bx+8,by+44),(bx+44,by+38),(bx+78,by+50)],4.0,lead=0.16,tail=0.24,swell=0.42)        # far brow
    # EYES set low under the brow — near full, far compressed; lids+iris+duct
    a([(bx-126,by+78),(bx-86,by+86),(bx-50,by+74)],3.0,lead=0.14,tail=0.26,swell=0.32)      # near upper lid
    a([(bx-120,by+96),(bx-86,by+100),(bx-56,by+92)],1.5,lead=0.32,tail=0.34,swell=0.14)     # near lower lid
    a([(bx-96,by+82),(bx-86,by+76),(bx-76,by+82)],1.6,lead=0.3,tail=0.3,swell=0.14)         # near iris top
    a([(bx-96,by+82),(bx-86,by+94),(bx-76,by+82)],1.8,lead=0.3,tail=0.3,swell=0.14)         # near iris bottom
    a([(bx-90,by+86),(bx-82,by+86)],2.2,cs=True,ce=True,swell=0.1)                          # near pupil
    a([(bx-128,by+80),(bx-136,by+86)],1.4,cs=True,ce=True,swell=0.12)                       # tear duct
    a([(bx+8,by+74),(bx+40,by+82),(bx+70,by+72)],2.5,lead=0.18,tail=0.28,swell=0.3)         # far upper lid
    a([(bx+14,by+90),(bx+40,by+95),(bx+64,by+88)],1.3,lead=0.34,tail=0.34,swell=0.12)       # far lower lid
    a([(bx+32,by+80),(bx+40,by+75),(bx+50,by+80)],1.4,lead=0.3,tail=0.3,swell=0.12)         # far iris top
    a([(bx+32,by+80),(bx+40,by+88),(bx+50,by+80)],1.5,lead=0.3,tail=0.3,swell=0.12)         # far iris bottom
    a([(bx+37,by+82),(bx+43,by+82)],2.0,cs=True,ce=True,swell=0.1)                          # far pupil
    # NOSE ridge (strong, straight) from the brow down to the tip
    a([(bx-44,by+50),(bx-62,by+150),(bx-96,by+182)],2.2,lead=0.24,tail=0.36,swell=0.16)
    a([(bx-92,by+186),(bx-70,by+196),(bx-50,by+184)],1.8,lead=0.32,tail=0.34,swell=0.14)    # far wing
    # MOUTH (low third), shifted to the front; far corner recedes
    a([(bx-104,by+240),(bx-56,by+248),(bx+10,by+236)],3.2,lead=0.14,tail=0.22,swell=0.36)   # seam
    a([(bx-94,by+232),(bx-56,by+226),(bx-14,by+230),(bx+8,by+228)],1.8,lead=0.3,tail=0.3,swell=0.14)  # upper lip
    a([(bx-92,by+256),(bx-54,by+264),(bx-2,by+252)],2.0,lead=0.3,tail=0.3,swell=0.16)       # lower lip
    # EAR inside the side-plane lower-front
    a([(bx+138,by+40),(bx+168,by+74),(bx+158,by+136),(bx+138,by+128)],2.6,lead=0.24,tail=0.3,swell=0.22)  # helix
    a([(bx+142,by+62),(bx+136,by+100),(bx+148,by+120)],1.4,lead=0.34,tail=0.34,swell=0.12)  # antihelix
    # NECK (thick, masculine) + shoulders
    a([(bx-30,by+268),(bx-44,by+344),(bx-30,by+430)],2.8,lead=0.2,tail=0.34,swell=0.24)
    a([(bx+96,by+268),(bx+116,by+352),(bx+120,by+440)],3.2,lead=0.18,tail=0.34,swell=0.28)
    a([(bx-30,by+430),(bx-120,by+460),(bx-210,by+486)],3.0,lead=0.2,tail=0.3,swell=0.24)
    a([(bx+120,by+440),(bx+204,by+466),(bx+290,by+490)],3.2,lead=0.18,tail=0.3,swell=0.26)
    return S

def silhouette():
    bx,by=BX,BY; im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.polygon([(bx-58,by-150),(bx-128,by-40),(bx-150,by+96),(bx-118,by+150),(bx-138,by+186),(bx-110,by+238),(bx-66,by+268),
               (bx+18,by+276),(bx+96,by+268),(bx+168,by+196),(bx+222,by+58),(bx+214,by-58),(bx+158,by-150),(bx+54,by-176)],fill=255)
    d.polygon([(bx-58,by-150),(bx-60,by-208),(bx+40,by-238),(bx+150,by-214),(bx+214,by-120),(bx+214,by-58),(bx+158,by-150),(bx+54,by-176)],fill=255) # hair
    d.polygon([(bx-30,by+264),(bx+96,by+268),(bx+120,by+440),(bx+290,by+490),(bx-210,by+486),(bx-30,by+430)],fill=255)  # neck+shoulders
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def head_shadow():
    bx,by=BX,BY; ox,oy,a,b=bx+14,by+60,196,250
    he=( ((xx-ox)/a)**2 + ((yy-oy)/b)**2 <=1).astype(float); he=soft(he,6)
    ys=np.array([by-120,by-30,by+40,by+110,by+180,by+250,by+280])
    xs=np.array([bx+60,bx+46,bx+44,bx+58,bx+82,bx+110,bx+124])   # terminator x per row
    xterm=np.interp(np.arange(H),ys,xs)[:,None]
    shadow=np.clip((xx-xterm)/30.0+0.5,0,1)*he
    core=np.clip(1-np.abs(xx-(xterm+18))/22.0,0,1)*he*(shadow>0.5)
    cast=(g2(bx-96,by+196,18,6,0.6)+g2(bx-40,by+258,28,6,0.55)        # under near nostril/lip
          +g2(bx-86,by+84,16,9,0.4)+g2(bx+40,by+82,14,8,0.45)         # eye sockets
          +g2(bx+120,by+250,52,28,0.5)+g2(bx+40,by-30,150,16,0.38))   # under far jaw, under hair
    core=np.clip(core+soft(cast,2)*he,0,1)
    refl=soft((((xx-ox)/a)>0.70).astype(float)*he,4)
    return shadow,core,refl

def shade_to_ink(shadow,core,refl,mask,base=0.26):
    h1=stripes(-0.5,6,1.5,1); h2=stripes(0.62,7,1.5,2); h3=stripes(1.5,6,1.4,3)
    half=np.clip((shadow-0.14)/0.34,0,1)
    g=half*base*h1 + np.clip(shadow-0.5,0,1)*0.40*h2 + core*0.46*h3
    return np.clip(g*(1-refl*0.85),0,1)*mask

def render():
    out=np.ones((H,W,3))*PAPER
    cim=Image.new("L",(W*SS,H*SS),0); cd=ImageDraw.Draw(cim); construction(cd)
    ca=np.asarray(cim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-(ca*0.28)[...,None]) + np.array([150,146,138],float)*(ca*0.28)[...,None]   # very faint construction
    mask=silhouette(); sh,co,re=head_shadow()
    g=shade_to_ink(sh,co,re,mask)
    # HAIR as a value-mass (darker on the crown), with a bare gloss band -> reads as hair, not a cap
    hairband=soft(g2(BX+56,BY-126,166,96,1.0),5)*mask*(yy<BY-52)
    gloss=soft(g2(BX-4,BY-186,120,22,1.0,-0.15),5)
    g=np.clip(g + (hairband*0.42 - gloss*0.75)*stripes(-1.0,5,1.6,5), 0,1)
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None]) + INK*fa[...,None]
    cl=np.clip(soft(g2(BX-90,BY+84,2.2,2.6,1.0)+g2(BX+38,BY+80,1.7,2.0,1.0),0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/loomis_34_v2.png"); print("done")
