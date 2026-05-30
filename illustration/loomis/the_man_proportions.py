"""
FULL MALE FIGURE — correct 8-HEAD proportions (fixing the head-heavy build).
Head-unit guides 0-8; landmarks chin=1, nipple=2, navel=3, crotch=4 (midpoint),
knee~6, ankle~7.5, sole=8. Masses in proportion (Loomis head, deltoid/elbow/
wrist/knee/ankle spheres, ribcage egg, pelvis box, limb cylinders), surface line.
Construction/sketch phase. (Detailed face #3 drops onto this skeleton later.)
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=600,1360; CX=275; U=150; TOP=58           # U = one head height
PAPER=np.array([237,232,223],float); INK_SH=np.array([54,54,68],float); GREY=np.array([150,146,138],float)
yy,xx=np.mgrid[0:H,0:W].astype(float); cx=CX
def Y(h): return TOP+h*U                        # y at head-unit h
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.2*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)
def poly(pts):
    im=Image.new("L",(W,H),0); ImageDraw.Draw(im).polygon([(float(x),float(y)) for x,y in pts],fill=255)
    return np.asarray(im,float)/255.0

S=[]
def a(c,w,lead=0.18,tail=0.24,swell=0.3,sm=0.58,cs=False,ce=False): S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))

# landmark y's
y_chin=Y(1); y_nip=Y(2); y_nav=Y(3); y_crotch=Y(4); y_knee=Y(6); y_ankle=Y(7.5); y_sole=Y(8)
y_brow=Y(0.62); y_shoulder=Y(1.35); y_elbow=y_nav; y_wrist=y_crotch; y_hand=Y(4.6)
HEADR=70

def figure():
    # ---- HEAD (Loomis, simplified) ----
    a([(cx-46,Y(0.18)),(cx-64,Y(0.5)),(cx-58,Y(0.86)),(cx-30,y_chin-6),(cx,y_chin)],3.0,lead=0.14,tail=0.18,swell=0.3)
    a([(cx,y_chin),(cx+30,y_chin-6),(cx+58,Y(0.86)),(cx+64,Y(0.5)),(cx+46,Y(0.18))],3.0,lead=0.14,tail=0.18,swell=0.3)
    a([(cx-46,Y(0.18)),(cx,Y(0.05)),(cx+46,Y(0.18))],2.6,lead=0.2,tail=0.2,swell=0.26)        # cranium top
    a([(cx-40,Y(0.2)),(cx,Y(0.36)),(cx+40,Y(0.2))],1.2,lead=0.3,tail=0.3,swell=0.1)            # hairline
    a([(cx-44,y_brow),(cx-20,y_brow-3),(cx-2,y_brow)],2.2,lead=0.14,tail=0.2,swell=0.4); a([(cx+2,y_brow),(cx+20,y_brow-3),(cx+44,y_brow)],2.2,lead=0.14,tail=0.2,swell=0.4)
    a([(cx-40,y_brow+18),(cx-20,y_brow+22),(cx-2,y_brow+18)],1.4,lead=0.2,tail=0.28,swell=0.2); a([(cx+2,y_brow+18),(cx+20,y_brow+22),(cx+40,y_brow+18)],1.4,lead=0.2,tail=0.28,swell=0.2)  # eyes
    a([(cx-6,y_brow+8),(cx-8,Y(0.84)),(cx-16,Y(0.9))],1.4,lead=0.24,tail=0.32,swell=0.16); a([(cx+6,y_brow+8),(cx+8,Y(0.84)),(cx+16,Y(0.9))],1.2,lead=0.26,tail=0.34,swell=0.14)  # nose
    a([(cx-22,y_chin-28),(cx,y_chin-24),(cx+22,y_chin-28)],1.8,lead=0.16,tail=0.24,swell=0.3)  # mouth
    a([(cx-30,Y(0.78)),(cx-64,Y(0.6))],1.6,lead=0.3,tail=0.3,swell=0.14); a([(cx+30,Y(0.78)),(cx+64,Y(0.6))],1.6,lead=0.3,tail=0.3,swell=0.14)  # jaw to ear region
    # ---- NECK + SHOULDERS — finished: SCM -> sternal pit, Adam's apple, clavicles, trapezius ----
    a([(cx-27,y_chin),(cx-31,Y(1.18)),(cx-33,y_shoulder-6)],2.0,lead=0.2,tail=0.3,swell=0.18); a([(cx+27,y_chin),(cx+31,Y(1.18)),(cx+33,y_shoulder-6)],2.0,lead=0.2,tail=0.3,swell=0.18)  # neck sides
    a([(cx-22,y_chin+4),(cx-12,Y(1.2)),(cx-5,y_shoulder-4)],1.4,lead=0.24,tail=0.3,swell=0.14); a([(cx+22,y_chin+4),(cx+12,Y(1.2)),(cx+5,y_shoulder-4)],1.4,lead=0.24,tail=0.3,swell=0.14)  # SCM V -> pit
    a([(cx-6,y_shoulder-6),(cx,y_shoulder-1),(cx+6,y_shoulder-6)],1.2,lead=0.3,tail=0.3,swell=0.1)  # sternal pit hollow
    a([(cx-4,Y(1.15)),(cx-3,Y(1.24))],0.9,cs=True,ce=True,swell=0.06); a([(cx+4,Y(1.15)),(cx+3,Y(1.24))],0.9,cs=True,ce=True,swell=0.06)  # Adam's apple
    a([(cx-6,y_shoulder-1),(cx-62,y_shoulder),(cx-120,y_shoulder-6)],1.4,lead=0.26,tail=0.3,swell=0.12); a([(cx+6,y_shoulder-1),(cx+62,y_shoulder),(cx+120,y_shoulder-6)],1.4,lead=0.26,tail=0.3,swell=0.12)  # clavicles (pit -> deltoid)
    # ---- SHOULDERS / TORSO — wider (~2.7 heads), ROUNDED shoulders, fuller, less pinched ----
    sh=206; wst=76; hip=110
    a([(cx-54,y_shoulder-18),(cx-118,y_shoulder-8),(cx-170,Y(1.46)),(cx-sh,Y(1.74)),(cx-178,Y(2.04)),(cx-122,Y(2.4)),(cx-wst,Y(2.86)),(cx-hip,y_nav+34),(cx-hip+10,y_crotch-8)],2.8,lead=0.14,tail=0.18,swell=0.24)  # left torso (rounded deltoid -> V-taper)
    a([(cx+54,y_shoulder-18),(cx+118,y_shoulder-8),(cx+170,Y(1.46)),(cx+sh,Y(1.74)),(cx+178,Y(2.04)),(cx+122,Y(2.4)),(cx+wst,Y(2.86)),(cx+hip,y_nav+34),(cx+hip-10,y_crotch-8)],2.8,lead=0.14,tail=0.18,swell=0.24)  # right torso
    a([(cx-118,y_shoulder-8),(cx-54,y_shoulder-20),(cx,y_shoulder-14),(cx+54,y_shoulder-20),(cx+118,y_shoulder-8)],2.0,lead=0.2,tail=0.2,swell=0.18)  # trapezius yoke (slopes)
    a([(cx,y_shoulder-6),(cx,y_crotch-6)],1.0,lead=0.4,tail=0.4,swell=0.08)
    a([(cx-8,Y(1.98)),(cx-66,Y(2.02)),(cx-118,Y(1.86))],1.6,lead=0.2,tail=0.28,swell=0.16); a([(cx+8,Y(1.98)),(cx+66,Y(2.02)),(cx+118,Y(1.86))],1.6,lead=0.2,tail=0.28,swell=0.16)  # pecs (wider)
    for hh in (2.32,2.56,2.8): a([(cx-46,Y(hh)),(cx,Y(hh)+3),(cx+46,Y(hh))],1.0,lead=0.34,tail=0.34,swell=0.08)
    a([(cx-6,y_nav),(cx+6,y_nav)],1.4,cs=True,ce=True,swell=0.1)
    a([(cx-hip+8,y_crotch-26),(cx-34,y_crotch),(cx,y_crotch+4)],1.2,lead=0.3,tail=0.32,swell=0.1); a([(cx+hip-8,y_crotch-26),(cx+34,y_crotch),(cx,y_crotch+4)],1.2,lead=0.3,tail=0.32,swell=0.1)
    # ---- ARMS — fuller; elbow just below 3, wrist at crotch (4), hand ~2/3 head ----
    AE=Y(3.12); AW=y_crotch; AH=Y(4.62)
    for s in (-1,1):
        a([(cx+s*sh,Y(1.62)),(cx+s*214,Y(2.05)),(cx+s*204,AE-8)],2.4,lead=0.16,tail=0.2,swell=0.22)       # upper arm outer
        a([(cx+s*128,Y(1.9)),(cx+s*172,Y(2.25)),(cx+s*182,AE-8)],1.8,lead=0.24,tail=0.24,swell=0.16)      # upper arm inner
        a([(cx+s*204,AE+4),(cx+s*210,Y(3.52)),(cx+s*188,AW)],2.2,lead=0.18,tail=0.22,swell=0.18)          # forearm outer (mass near elbow)
        a([(cx+s*182,AE+6),(cx+s*186,Y(3.6)),(cx+s*180,AW)],1.7,lead=0.24,tail=0.24,swell=0.14)           # forearm inner
        a([(cx+s*188,AW),(cx+s*196,Y(4.34)),(cx+s*186,AH)],1.8,lead=0.2,tail=0.24,swell=0.12)             # hand outer
        a([(cx+s*180,AW),(cx+s*176,Y(4.34)),(cx+s*184,AH)],1.6,lead=0.24,tail=0.24,swell=0.1)             # hand inner
        for fxx in (0,1,2): a([(cx+s*(180+fxx*5),Y(4.42)),(cx+s*(180+fxx*5),AH)],0.8,cs=True,ce=True,swell=0.05)
        a([(cx+s*204,AE-4),(cx+s*184,AE)],1.1,cs=True,ce=True,swell=0.08)                                 # elbow crease
    # ---- LEGS — developed: full thigh (quad+adductor), real knee, calf gastroc, wedge feet ----
    for s in (-1,1):
        a([(cx+s*hip,y_crotch-6),(cx+s*128,Y(4.62)),(cx+s*116,Y(5.0)),(cx+s*82,Y(5.6)),(cx+s*58,y_knee)],2.6,lead=0.14,tail=0.2,swell=0.22)  # thigh outer (quad bulge high)
        a([(cx+s*10,y_crotch+10),(cx+s*30,Y(4.72)),(cx+s*40,Y(5.4)),(cx+s*40,y_knee)],2.0,lead=0.24,tail=0.22,swell=0.16)                     # thigh inner (adductor)
        a([(cx+s*88,Y(4.88)),(cx+s*70,Y(5.5)),(cx+s*56,Y(5.92))],1.2,lead=0.34,tail=0.34,swell=0.1)                                           # vastus/rectus separation
        a([(cx+s*58,y_knee),(cx+s*52,Y(6.06)),(cx+s*40,Y(6.06)),(cx+s*40,y_knee)],1.6,lead=0.2,tail=0.26,swell=0.14)                          # knee mass
        a([(cx+s*48,y_knee-4),(cx+s*49,y_knee+10)],1.0,cs=True,ce=True,swell=0.06)                                                            # kneecap
        a([(cx+s*58,Y(6.1)),(cx+s*76,Y(6.42)),(cx+s*64,Y(6.92)),(cx+s*40,Y(7.22)),(cx+s*34,y_ankle)],2.4,lead=0.16,tail=0.2,swell=0.2)        # calf outer (gastroc, high)
        a([(cx+s*40,Y(6.1)),(cx+s*34,Y(6.7)),(cx+s*30,y_ankle)],1.9,lead=0.22,tail=0.22,swell=0.16)                                           # shin (inner, straighter)
        a([(cx+s*62,Y(6.5)),(cx+s*50,Y(6.98))],1.1,lead=0.34,tail=0.34,swell=0.08)                                                            # gastroc inner edge
        a([(cx+s*30,y_ankle-4),(cx+s*37,y_ankle+5)],1.0,cs=True,ce=True,swell=0.06)                                                           # lateral malleolus
        a([(cx+s*34,y_ankle),(cx+s*30,y_sole-10),(cx+s*32,y_sole),(cx+s*80,y_sole+4),(cx+s*88,y_sole+10)],2.0,lead=0.16,tail=0.2,swell=0.14)  # foot top -> toes
        a([(cx+s*32,y_sole),(cx+s*22,y_sole+8),(cx+s*44,y_sole+13),(cx+s*88,y_sole+10)],1.6,lead=0.22,tail=0.22,swell=0.12)                   # heel/sole underside
        for tx in (0,1,2,3): a([(cx+s*(66+tx*6),y_sole+7),(cx+s*(66+tx*6),y_sole+12)],0.7,cs=True,ce=True,swell=0.04)                         # toe hints
    return sh,wst,hip

def render():
    sh,wst,hip=figure()
    out=np.ones((H,W,3))*PAPER
    # construction masses + head-unit guides (faint)
    cim=Image.new("L",(W*2,H*2),0); cd=ImageDraw.Draw(cim); s2=2
    def ce_(c,a_,b,w=1): cd.ellipse([(c[0]-a_)*s2,(c[1]-b)*s2,(c[0]+a_)*s2,(c[1]+b)*s2],outline=255,width=int(w*s2))
    def cl_(p,q,w=1,col=255): cd.line([(p[0]*s2,p[1]*s2),(q[0]*s2,q[1]*s2)],fill=col,width=int(w*s2))
    ce_((cx,Y(0.5)),HEADR,76)                                # head ball
    ce_((cx,Y(2.05)),104,88)                                 # ribcage egg (wider)
    cl_((cx-102,y_nav+12),(cx+102,y_nav+12)); cl_((cx-128,y_crotch),(cx+128,y_crotch)); cl_((cx-102,y_nav+12),(cx-128,y_crotch)); cl_((cx+102,y_nav+12),(cx+128,y_crotch))  # pelvis box (2 heads)
    for (px,py,r) in [(cx-182,Y(1.52),37),(cx+182,Y(1.52),37),(cx-204,Y(3.12),24),(cx+204,Y(3.12),24),
                      (cx-184,y_crotch,15),(cx+184,y_crotch,15),(cx-56,y_knee,28),(cx+56,y_knee,28),
                      (cx-31,y_ankle,16),(cx+31,y_ankle,16)]:
        ce_((px,py),r,r)                                     # deltoid/elbow/wrist/knee/ankle spheres
    for h in range(0,9):
        cl_((26,Y(h)),(54,Y(h)),1); cd.text((10,Y(h)*s2-8),str(h),fill=255)
    ca=np.asarray(cim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-(ca*0.34)[...,None]) + GREY*(ca*0.34)[...,None]
    # body mask (matches the wider silhouette) for clipping the form shadow
    body=poly([(cx-62,y_shoulder-26),(cx-214,Y(2.05)),(cx-208,Y(3.12)),(cx-188,y_crotch),(cx-196,Y(4.62)),(cx-176,Y(4.62)),
               (cx-112,y_crotch-6),(cx-122,Y(4.7)),(cx-58,y_knee),(cx-74,Y(6.3)),(cx-32,y_ankle),(cx-82,y_sole+10),
               (cx,y_sole+14),(cx+82,y_sole+10),(cx+32,y_ankle),(cx+74,Y(6.3)),(cx+58,y_knee),(cx+122,Y(4.7)),(cx+112,y_crotch-6),
               (cx+176,Y(4.62)),(cx+196,Y(4.62)),(cx+188,y_crotch),(cx+208,Y(3.12)),(cx+214,Y(2.05)),(cx+62,y_shoulder-26)])
    body=np.clip(body+g2(cx,Y(0.5),HEADR+6,82,1.0),0,1)
    mask=(soft(body,2)>0.5).astype(float)
    g=soft(np.clip((xx-(cx+46))/130,0,1),3)*0.15*mask*stripes(-0.5,6,1.5,3)
    g=np.clip(g+soft(g2(cx+76,Y(2.1),28,92,0.3)+g2(cx+34,Y(5),24,150,0.28)+g2(cx+22,Y(6.7),18,120,0.26)
        +g2(cx,Y(2.32),46,8,0.2)+g2(cx,Y(2.56),46,8,0.2)+g2(cx+88,Y(1.92),26,42,0.3)
        +g2(cx,y_shoulder-3,15,9,0.55)                                   # sternal pit (dark)
        +g2(cx-24,Y(1.2),10,36,0.28)+g2(cx+26,Y(1.2),11,36,0.36)         # SCM sides (R deeper)
        +g2(cx,y_chin+16,38,14,0.34)                                     # under-jaw cast on the neck
        +g2(cx-50,y_shoulder+8,52,12,0.26)+g2(cx+50,y_shoulder+8,52,12,0.3)  # supraclavicular hollow
        +g2(cx+168,Y(1.74),30,42,0.34)+g2(cx-168,Y(1.74),26,42,0.22)        # deltoid form
        +g2(cx-58,Y(1.97),52,15,0.36)+g2(cx+58,Y(1.97),52,16,0.42)          # under each PEC (mass)
        +g2(cx,Y(1.9),11,26,0.3)                                            # sternum gap between pecs
        +g2(cx-26,Y(2.42),22,7,0.24)+g2(cx+26,Y(2.42),22,7,0.28)            # ab block shadows
        +g2(cx-26,Y(2.66),22,7,0.24)+g2(cx+26,Y(2.66),22,7,0.28),5)*mask*0.5*stripes(-0.5,6,1.5,3),0,1)
    out=out*(1-g[...,None])+INK_SH*g[...,None]
    im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
    for s in S: stroke(d,**s)
    fa=np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None])+INK*fa[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/the_man_proportions.png"); print("done")
