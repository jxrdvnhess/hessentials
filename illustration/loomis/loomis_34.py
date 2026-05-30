"""
LOOMIS 3/4 — faithful construction, then the head solid on top.
Fixing the abstract drift: a SOLID round cranium BALL, the visible SIDE-PLANE
oval sliced on the side, the CROSS (center line curving toward the turn + brow
line wrapping), the JAW attached, and the THIRDS. Head faces our LEFT. Features
placed ON the construction: near eye fuller, far eye compressed at the side-plane
edge, nose projecting off the center line, ear on the side plane. Solid Loomis
proportions, not elongated. Light kept restrained (selective on the side plane).
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=1240,940
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
def catmull(pts,n=80):
    pts=np.array(pts,float); P=np.vstack([pts[0],pts,pts[-1]]); out=[]; seg=max(10,n//(len(pts)-1))
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,seg):
            t2,t3=t*t,t*t*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    return np.array(out)

# --- shared Loomis 3/4 landmarks, parameterised by ball-centre bx (faces LEFT) ---
def LM(bx):
    R=150; by=320
    return dict(R=R, bc=(bx,by),
        cross=(bx-48,by+38),
        tophead=(bx,by-R), chin=(bx-26,by+300), nose=(bx-46,by+158),
        )

def construction(d, bx):
    def fl(pts,w=1.4,c=120): p=catmull(pts,90); d.line([(x*SS,y*SS) for x,y in p],fill=c,width=int(w*SS),joint="curve")
    def C(cx,cy,a,b,w=1.4):
        d.ellipse([(cx-a)*SS,(cy-b)*SS,(cx+a)*SS,(cy+b)*SS],outline=120,width=int(w*SS))
    R=150; by=320
    C(bx,by,R,R)                                              # the BALL (cranium)
    # visible SIDE-PLANE oval (sliced on the side facing away from the turn = right)
    C(bx+78,by-6,40,118,)                                     # side-plane disc (seen at an angle)
    # CROSS: center line (curves left toward the turn) + brow line (wraps), as ellipse arcs
    fl([(bx,by-R),(bx-44,by-40),(bx-48,by+38),(bx-44,by+120),(bx-30,by+R)],1.7)   # center line
    fl([(bx-150,by+52),(bx-48,by+38),(bx+90,by-2),(bx+118,by-10)],1.7)            # brow line wrapping
    # JAW from brow sides to chin (thirds), attached below the ball
    fl([(bx-150,by+44),(bx-150,by+150),(bx-104,by+250),(bx-26,by+300)])           # near jaw -> chin
    fl([(bx+118,by-8),(bx+128,by+120),(bx+78,by+232),(bx-26,by+300)])             # far jaw -> chin
    # THIRDS guidelines: brow / nose-base / chin
    for yy0 in (by+38, by+158, by+300):
        fl([(bx-150,yy0),(bx+150,yy0)],1.0)
    # hairline (a third above the brow) + eye sockets on the eye line
    fl([(bx-120,by-72),(bx-10,by-92),(bx+96,by-64)],1.1)
    C(bx-86,by+78,30,18); C(bx+30,by+66,22,15)                # eye sockets (near bigger, far compressed)

def face_strokes(bx):
    R=150; by=320; S=[]
    def a(c,w,lead=0.16,tail=0.22,swell=0.32,sm=0.6,cs=False,ce=False):
        S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # FRONT profile edge (left): forehead->brow->nose bridge->TIP->lips->chin (off the centre line)
    a([(bx-118,by-96),(bx-150,by-10),(bx-150,by+44),(bx-128,by+92),(bx-96,by+150),(bx-78,by+158),
       (bx-58,by+190),(bx-50,by+212),(bx-66,by+226),(bx-58,by+250),(bx-70,by+270),(bx-40,by+300)],3.2,lead=0.12,tail=0.16,swell=0.32)
    a([(bx-78,by+158),(bx-56,by+172),(bx-40,by+162)],2.2,lead=0.3,tail=0.32,swell=0.16)   # near nostril/base
    # CRANIUM + side-plane edge + far jaw to chin
    a([(bx-118,by-96),(bx-30,by-122),(bx+70,by-104),(bx+128,by-26),(bx+138,by+86),(bx+108,by+176),
       (bx+58,by+254),(bx-4,by+296),(bx-40,by+300)],3.8,lead=0.1,tail=0.2,swell=0.36)
    a([(bx+118,by-20),(bx+126,by+96),(bx+96,by+182)],1.8,lead=0.32,tail=0.34,swell=0.14) # side-plane front edge (the turn)
    # HAIR — a rounded mass hugging the cranium (modest volume, no brim/hat), swept right
    a([(bx-118,by-96),(bx-126,by-152),(bx-56,by-182),(bx+52,by-172),(bx+124,by-116),(bx+138,by-96)],3.2,lead=0.2,tail=0.24,swell=0.4)
    a([(bx-104,by-100),(bx-40,by-138),(bx+44,by-134)],1.8,lead=0.3,tail=0.3,swell=0.16)   # hairline (follows the brow curve)
    for p in [((bx-64,by-138),(bx+12,by-118),(bx+92,by-100)),((bx-30,by-162),(bx+48,by-150),(bx+112,by-118))]:
        a(list(p),1.4,lead=0.34,tail=0.34,swell=0.12)                                     # sweep clumps (curved flow)
    # BROWS (near fuller, far compressed)
    a([(bx-128,by+30),(bx-86,by+18),(bx-46,by+30)],4.6,lead=0.12,tail=0.22,swell=0.46)
    a([(bx+6,by+24),(bx+40,by+18),(bx+70,by+30)],3.4,lead=0.18,tail=0.26,swell=0.4)
    # EYES on the eye line — near (left) full, far (right) compressed; lids+iris+duct
    a([(bx-120,by+62),(bx-84,by+70),(bx-52,by+58)],2.8,lead=0.16,tail=0.26,swell=0.32)    # near upper lid
    a([(bx-114,by+78),(bx-84,by+84),(bx-56,by+76)],1.5,lead=0.32,tail=0.34,swell=0.14)    # near lower lid
    a([(bx-94,by+66),(bx-84,by+60),(bx-74,by+66)],1.6,lead=0.3,tail=0.3,swell=0.14)       # near iris top
    a([(bx-94,by+66),(bx-84,by+78),(bx-74,by+66)],1.8,lead=0.3,tail=0.3,swell=0.14)       # near iris bottom
    a([(bx-88,by+70),(bx-80,by+70)],2.2,cs=True,ce=True,swell=0.1)                        # near pupil
    a([(bx-122,by+64),(bx-130,by+70)],1.4,cs=True,ce=True,swell=0.12)                     # tear duct
    a([(bx+4,by+58),(bx+34,by+66),(bx+62,by+56)],2.4,lead=0.18,tail=0.28,swell=0.3)       # far upper lid
    a([(bx+10,by+72),(bx+34,by+77),(bx+58,by+70)],1.3,lead=0.34,tail=0.34,swell=0.12)     # far lower lid
    a([(bx+26,by+64),(bx+34,by+59),(bx+44,by+64)],1.4,lead=0.3,tail=0.3,swell=0.12)       # far iris top
    a([(bx+26,by+64),(bx+34,by+72),(bx+44,by+64)],1.5,lead=0.3,tail=0.3,swell=0.12)       # far iris bottom
    a([(bx+31,by+66),(bx+37,by+66)],2.0,cs=True,ce=True,swell=0.1)                        # far pupil
    # NOSE ridge (front plane) from the cross to the tip
    a([(bx-46,by+34),(bx-60,by+128),(bx-84,by+156)],2.0,lead=0.26,tail=0.36,swell=0.16)
    a([(bx-40,by+162),(bx-20,by+170),(bx-4,by+160)],1.8,lead=0.32,tail=0.34,swell=0.14)   # far wing
    # MOUTH (lower third), shifted toward the front; far corner recedes
    a([(bx-96,by+228),(bx-50,by+236),(bx+14,by+224)],3.2,lead=0.14,tail=0.22,swell=0.36)  # seam
    a([(bx-86,by+220),(bx-50,by+214),(bx-8,by+218),(bx+12,by+216)],1.8,lead=0.3,tail=0.3,swell=0.14)  # upper lip
    a([(bx-84,by+246),(bx-48,by+254),(bx+4,by+242)],2.0,lead=0.3,tail=0.3,swell=0.16)     # lower lip
    # EAR on the side plane
    a([(bx+116,by+44),(bx+142,by+78),(bx+132,by+136),(bx+114,by+144)],2.6,lead=0.24,tail=0.3,swell=0.22)
    # NECK + shoulders
    a([(bx-40,by+300),(bx-58,by+372),(bx-44,by+452)],2.8,lead=0.2,tail=0.34,swell=0.24)
    a([(bx+58,by+254),(bx+78,by+346),(bx+84,by+452)],3.0,lead=0.18,tail=0.34,swell=0.26)
    a([(bx-44,by+452),(bx-130,by+480),(bx-210,by+506)],3.0,lead=0.2,tail=0.3,swell=0.24)
    a([(bx+84,by+452),(bx+166,by+480),(bx+250,by+506)],3.2,lead=0.18,tail=0.3,swell=0.26)
    return S

def silhouette(bx):
    R=150; by=320; im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.polygon([(bx-118,by-96),(bx-150,by-10),(bx-128,by+92),(bx-78,by+158),(bx-50,by+212),(bx-70,by+270),
               (bx-40,by+300),(bx-4,by+296),(bx+58,by+254),(bx+108,by+176),(bx+138,by+86),(bx+128,by-26),(bx+70,by-104),(bx-30,by-122)],fill=255)
    d.polygon([(bx-118,by-96),(bx-126,by-152),(bx-56,by-182),(bx+52,by-172),(bx+124,by-116),(bx+138,by-96),(bx+70,by-104),(bx-30,by-122)],fill=255) # hair
    d.polygon([(bx-40,by+296),(bx+58,by+254),(bx+84,by+452),(bx+250,by+506),(bx-210,by+506),(bx-44,by+452)],fill=255)               # neck+shoulders
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def head_shadow(bx):
    R=150; by=320; ox,oy,a,b=bx+6,by+70,176,238
    he=( ((xx-ox)/a)**2 + ((yy-oy)/b)**2 <=1).astype(float); he=soft(he,6)
    ys=np.array([by-100,by-20,by+40,by+110,by+180,by+260,by+300])
    xs=np.array([bx+58,bx+44,bx+40,bx+52,bx+74,bx+96,bx+110])     # terminator x per row
    xterm=np.interp(np.arange(H),ys,xs)[:,None]
    shadow=np.clip((xx-xterm)/30.0+0.5,0,1)*he
    core=np.clip(1-np.abs(xx-(xterm+18))/22.0,0,1)*he*(shadow>0.45)
    cast=(g2(bx-40,by+170,18,6,0.7)+g2(bx-40,by+248,28,6,0.6)        # under near nostril/lip
          +g2(bx-84,by+66,16,9,0.4)+g2(bx+34,by+64,14,8,0.45)        # eye sockets
          +g2(bx+70,by+250,52,28,0.5)+g2(bx+30,by-30,140,16,0.4))    # under far jaw, under hair
    core=np.clip(core+soft(cast,2)*he,0,1)
    refl=soft((((xx-ox)/a)>0.68).astype(float)*he,4)
    return shadow,core,refl

def shade_to_ink(shadow,core,refl,mask,base=0.26):
    h1=stripes(-0.5,6,1.5,1); h2=stripes(0.62,7,1.5,2); h3=stripes(1.5,6,1.4,3)
    half=np.clip((shadow-0.14)/0.34,0,1)
    g=half*base*h1 + np.clip(shadow-0.5,0,1)*0.40*h2 + core*0.46*h3
    return np.clip(g*(1-refl*0.85),0,1)*mask

def render():
    out=np.ones((H,W,3))*PAPER
    # left: construction (faint)
    cim=Image.new("L",(W*SS,H*SS),0); cd=ImageDraw.Draw(cim); construction(cd,300)
    ca=np.asarray(cim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-(ca*0.55)[...,None]) + np.array([150,146,138],float)*(ca*0.55)[...,None]
    # right: finished head built on the construction
    bx=820
    mask=silhouette(bx); sh,co,re=head_shadow(bx)
    g=shade_to_ink(sh,co,re,mask)
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(bx): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None]) + INK*fa[...,None]
    by=320
    cl=np.clip(soft(g2(820-86,by+68,2.2,2.6,1.0)+g2(820+31,by+64,1.7,2.0,1.0),0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)); dd=ImageDraw.Draw(img)
    dd.text((60,40),"LOOMIS 3/4 CONSTRUCTION — ball + side-plane + cross + jaw + thirds",fill=(70,66,64))
    dd.text((720,40),"BUILT ON IT — solid Loomis head, 3/4",fill=(70,66,64))
    return img

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/loomis_34.png"); print("done")
