"""
VOLUME DRILL (Jordan's office-hours note, 2026-05-30): stop drawing the OUTLINE of a man,
build him from VOLUMES and connect them. Left = the vocabulary (ribcage egg, pelvis box,
head ball — each drawn THROUGH with cross-contours so it reads as a 3D form, not a symbol).
Right = a mannequin from those primitives ONLY (boxes / cylinders / spheres): shoulders
~2.5 heads (not 3+), limbs that TAPER (wide at the joint above -> narrow below), TWO-MASS
torso (ribcage egg + pelvis box separated by a real waist), neck plugging UP into the
ribcage. Clean construction line. No skin outline, no features, no anatomy. Just the forms.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=980,1360; SC=3
PAPER=np.array([237,232,223],float); GREY=np.array([150,146,138],float)
INKc=(44,44,58); FORM=(150,146,138)
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(arr,r): return np.asarray(Image.fromarray((np.clip(arr,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d

# ---- build the faint form-shadow base FIRST (so masses read solid, lit from upper-left) ----
def base():
    R,U,TOP=640,150,60
    def Y(h): return TOP+h*U
    sh=( g2(R+46,Y(1.95),42,108,0.30)                          # ribcage shadow side
        +g2(R+42,Y(3.4),34,72,0.26)                            # pelvis shadow side
        +g2(R-137,Y(2.3),20,150,0.20)+g2(R+137,Y(2.3),22,150,0.26)   # arms
        +g2(R-66,Y(5.0),24,150,0.22)+g2(R+66,Y(5.0),24,150,0.24)     # thighs
        +g2(R-52,Y(6.9),16,120,0.20)+g2(R+52,Y(6.9),16,120,0.22)     # calves
        +g2(204,420,30,104,0.26)+g2(204,720,26,60,0.20) )      # vocabulary masses
    g=np.clip(soft(sh,6)*0.5,0,1)
    out=np.ones((H,W,3))*PAPER
    out=out*(1-g[...,None])+GREY*g[...,None]
    # head-unit guides + divider
    cim=Image.new("L",(W,H),0); cd=ImageDraw.Draw(cim)
    for h in range(0,9):
        cd.line([(R-150,Y(h)),(R-122,Y(h))],fill=80,width=1); cd.text((R-176,Y(h)-6),str(h),fill=105)
    cd.line([(312,40),(312,1318)],fill=60,width=1)
    ca=np.asarray(cim,float)/255.0
    out=out*(1-(ca*0.55)[...,None]) + GREY*(ca*0.55)[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

img=base().resize((W*SC,H*SC),Image.LANCZOS)
D=ImageDraw.Draw(img)
def E(cx,cy,rx,ry,w,col=INKc): D.ellipse([(cx-rx)*SC,(cy-ry)*SC,(cx+rx)*SC,(cy+ry)*SC],outline=col,width=max(1,int(w*SC)))
def ARC(cx,cy,rx,ry,a0,a1,w,col=INKc): D.arc([(cx-rx)*SC,(cy-ry)*SC,(cx+rx)*SC,(cy+ry)*SC],a0,a1,fill=col,width=max(1,int(w*SC)))
def CV(pts,w,col=INKc): D.line([(x*SC,y*SC) for x,y in pts],fill=col,width=max(1,int(w*SC)),joint="curve")
def LN(p,q,w,col=INKc): D.line([p[0]*SC,p[1]*SC,q[0]*SC,q[1]*SC],fill=col,width=max(1,int(w*SC)))

# ---------- VOLUME PRIMITIVES (crisp construction) ----------
def cylinder(x0,y0,r0,x1,y1,r1,w=2.4,contours=2):
    CV([(x0-r0,y0),(0.5*(x0-r0)+0.5*(x1-r1),0.5*(y0+y1)),(x1-r1,y1)],w)             # left wall
    CV([(x0+r0,y0),(0.5*(x0+r0)+0.5*(x1+r1),0.5*(y0+y1)),(x1+r1,y1)],w)             # right wall
    for k in range(1,contours+1):
        t=k/(contours+1); cxk=x0+(x1-x0)*t; cyk=y0+(y1-y0)*t; rk=r0+(r1-r0)*t
        ARC(cxk,cyk,rk,rk*0.30,0,180,1.3)                                           # front cross-contour (turns)
def sphere(cx,cy,r,w=2.0):
    E(cx,cy,r,r,w)
    ARC(cx,cy,r,r*0.34,0,180,1.2); ARC(cx,cy,r*0.34,r,-90,90,1.2)                   # h + v cross-contours
def egg(cx,cy,rx,ry,w=2.6,bottomV=True):
    E(cx,cy,rx,ry,w)
    ARC(cx,cy-ry*0.16,rx*0.92,ry*0.22,0,180,1.4); ARC(cx,cy+ry*0.30,rx*0.74,ry*0.18,0,180,1.4)
    CV([(cx-rx*0.26,cy-ry*0.96),(cx-rx*0.14,cy+ry*0.4),(cx,cy+ry*0.74)],1.2)        # centre contour
    if bottomV: CV([(cx-rx*0.52,cy+ry*0.50),(cx,cy+ry*0.95),(cx+rx*0.52,cy+ry*0.50)],1.5)  # rib arch
def pelvis_box(cx,cy,topw,botw,h,w=2.6):
    tT=cy-h/2; tB=cy+h/2
    CV([(cx-topw,tT),(cx-botw,tB)],w); CV([(cx+topw,tT),(cx+botw,tB)],w)
    CV([(cx-botw,tB),(cx,tB+h*0.13),(cx+botw,tB)],w)                                # pubic arch
    E(cx,tT,topw,topw*0.34,1.6)                                                     # open rim (3D bucket)
    CV([(cx,tT-topw*0.30),(cx,tB-h*0.16)],1.1)                                      # centre contour
    return (cx-topw*0.62,cy+h*0.26),(cx+topw*0.62,cy+h*0.26)
def head_ball(cx,cy,r,w=2.6):
    E(cx,cy,r,r*1.14,w)                                                             # cranial ball
    CV([(cx+r*0.60,cy-r*0.64),(cx+r*0.70,cy),(cx+r*0.56,cy+r*0.52)],1.5)            # SIDE-PLANE cut
    ARC(cx,cy,r,r*0.32,0,180,1.3)                                                   # brow cross-contour
    CV([(cx,cy-r*1.14),(cx,cy+r*0.86)],1.1)                                         # centre line
    CV([(cx-r*0.52,cy+r*0.5),(cx-r*0.28,cy+r*1.14),(cx,cy+r*1.28)],1.7)             # jaw wedge L
    CV([(cx+r*0.52,cy+r*0.5),(cx+r*0.28,cy+r*1.14),(cx,cy+r*1.28)],1.7)             # jaw wedge R

# =================== LEFT: THE VOCABULARY ===================
L=204
head_ball(L,150,46)
egg(L,420,82,108)
pelvis_box(L,720,86,46,150)
egg(L,985,58,78,w=2.2); pelvis_box(L,1205,62,34,112,w=2.2)
cylinder(L,1063,40,L,1149,44,w=1.8,contours=1)                                      # the waist BETWEEN the two masses

# =================== RIGHT: THE MANNEQUIN ===================
R=640; U=150; TOP=60
def Y(h): return TOP+h*U
HW=46
head_ball(R,Y(0.46),HW)
cylinder(R,Y(1.02),28,R,Y(1.36),30,w=2.2,contours=1)                                # neck -> plugs into ribcage
rc_cx,rc_cy,rc_rx,rc_ry=R,Y(1.95),96,112
egg(rc_cx,rc_cy,rc_rx,rc_ry)
SHW=115                                                                             # shoulders = 2.5 heads
CV([(R-30,Y(1.42)),(R-SHW+10,Y(1.46))],1.9); CV([(R+30,Y(1.42)),(R+SHW-10,Y(1.46))],1.9)  # clavicle yoke
sphere(R-SHW,Y(1.5),34); sphere(R+SHW,Y(1.5),34)                                    # deltoids
cylinder(R,Y(2.66),58,R,Y(3.0),62,w=2.2,contours=1)                                 # WAIST (narrow connector)
hipL,hipR=pelvis_box(R,Y(3.42),86,52,150)
for s,sx in ((-1,R-SHW),(1,R+SHW)):                                                 # ARMS taper
    elx=sx+s*6; wrx=sx+s*2
    cylinder(sx,Y(1.66),34,elx,Y(3.0),22); sphere(elx,Y(3.06),20)
    cylinder(elx,Y(3.12),24,wrx,Y(4.0),14); sphere(wrx,Y(4.04),13)
    CV([(wrx-14,Y(4.1)),(wrx-12,Y(4.5)),(wrx+2,Y(4.62))],1.7); CV([(wrx+14,Y(4.1)),(wrx+12,Y(4.5)),(wrx+2,Y(4.62))],1.7)
for s,(hx,hy) in ((-1,hipL),(1,hipR)):                                              # LEGS taper
    kx=R+s*42; ax=R+s*30
    cylinder(hx,hy,46,kx,Y(5.96),28); sphere(kx,Y(6.04),26)
    cylinder(kx,Y(6.12),34,ax,Y(7.5),17); sphere(ax,Y(7.54),15)
    CV([(ax,Y(7.6)),(ax-s*4,Y(7.92)),(ax+s*46,Y(8.0)),(ax+s*52,Y(8.04))],2.1)
    CV([(ax,Y(7.66)),(ax-s*12,Y(8.0)),(ax+s*52,Y(8.04))],1.6)

img=img.resize((W,H),Image.LANCZOS)
dd=ImageDraw.Draw(img)
try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",16)
except: f=ImageFont.load_default()
for tx,ty,s_ in [(150,212,"head — ball + side plane"),(150,552,"ribcage — egg, drawn through"),
                 (150,812,"pelvis — box, open rim"),(150,1270,"two masses + a waist"),
                 (440,1322,"mannequin from volumes  ·  shoulders 2.5 heads  ·  limbs taper  ·  neck into ribcage")]:
    dd.text((tx,ty),s_,fill=(96,94,90),font=f)
os.makedirs(OUT,exist_ok=True); img.save(f"{OUT}/the_man_volumes.png"); print("done")
