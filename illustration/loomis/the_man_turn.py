"""
THE TURN (Jordan's note, 2026-05-30): "stopped drawing a person, started drawing an object —
now make the object MOVE." Same volume mannequin, rotated in space + a gentle contrapposto so
the masses turn instead of standing frontal. Ribcage & pelvis COUNTER-rotate (independent
masses); weight on one leg. Left: a box and an egg stepped front -> 3/4 -> side to show I can
turn a form. A small real 3D projection drives it (silhouette = convex hull of the projected
surface, so tapered ends stay rounded). Construction only — no skin, no features.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=980,1360; SC=3
PAPER=np.array([237,232,223],float)
INKc=(44,44,58); FAINT=(154,151,144)
def Rx(a):c,s=math.cos(a),math.sin(a);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a):c,s=math.cos(a),math.sin(a);return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a):c,s=math.cos(a),math.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d):return math.radians(d)

img=Image.new("RGB",(W*SC,H*SC),tuple(PAPER.astype(int))); D=ImageDraw.Draw(img)
def CV(scr,w,col=INKc,closed=False):
    pts=[(x*SC,y*SC) for x,y in scr]
    if closed: pts=pts+[pts[0]]
    D.line(pts,fill=col,width=max(1,int(w*SC)),joint="curve")

CAMYAW=rad(18)
def projP(p,ox,oy):
    q=Ry(CAMYAW)@p; return (ox+q[0],oy+q[1]),q[2]
def basis(axis):
    axis=axis/(np.linalg.norm(axis)+1e-9)
    ref=np.array([0,0,1.0]) if abs(axis[2])<0.9 else np.array([0,1.0,0])
    u=np.cross(axis,ref); u/=np.linalg.norm(u)+1e-9; v=np.cross(axis,u); return u,v
def ring_scr(center,r,axis,ox,oy,n=32):
    u,v=basis(axis); out=[]
    for t in np.linspace(0,2*math.pi,n,endpoint=False):
        s,_=projP(center+r*(math.cos(t)*u+math.sin(t)*v),ox,oy); out.append(s)
    return out
def draw_ring(center,r,axis,ox,oy,w=1.1,col=INKc): CV(ring_scr(center,r,axis,ox,oy),w,col,closed=True)
def hull(points):
    pts=sorted(set((round(x,2),round(y,2)) for x,y in points))
    if len(pts)<3: return pts
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def silhouette(surface_pts,ox,oy,w=2.4):
    scr=[projP(p,ox,oy)[0] for p in surface_pts]; CV(hull(scr),w,INKc,closed=True)

def draw_tube(spine,radii,ox,oy,w=2.4,contours=2,sub=7):
    C=[];Rr=[]
    for i in range(len(spine)-1):
        for k in range(sub): t=k/sub; C.append(spine[i]*(1-t)+spine[i+1]*t); Rr.append(radii[i]*(1-t)+radii[i+1]*t)
    C.append(spine[-1]); Rr.append(radii[-1])
    surf=[]
    for i in range(len(C)):
        axis=C[min(i+1,len(C)-1)]-C[max(i-1,0)]
        if np.linalg.norm(axis)<1e-6: axis=np.array([0,1.0,0])
        u,v=basis(axis)
        for t in np.linspace(0,2*math.pi,16,endpoint=False):
            surf.append(C[i]+Rr[i]*(math.cos(t)*u+math.sin(t)*v))
    silhouette(surf,ox,oy,w)
    if contours:
        for k in range(1,contours+1):
            t=k/(contours+1); i=int(t*(len(C)-1)); axis=C[min(i+1,len(C)-1)]-C[max(i-1,0)]
            draw_ring(C[i],Rr[i],axis,ox,oy,1.0)
def draw_egg(center,rx,ry,rot,ox,oy,w=2.6,contour=True):
    prof=[(-0.98,0.20),(-0.8,0.55),(-0.5,0.85),(-0.18,0.98),(0.18,1.0),(0.5,0.95),(0.8,0.72),(0.98,0.34)]
    surf=[]
    for fy,fr in prof:
        c=center+rot@np.array([0,fy*ry,0]); axis=rot@np.array([0,1.0,0]); u,v=basis(axis)
        for t in np.linspace(0,2*math.pi,20,endpoint=False):
            surf.append(c+rx*fr*(math.cos(t)*u+math.sin(t)*v))
    silhouette(surf,ox,oy,w)
    if contour:
        for fy,fr in ((-0.30,0.93),(0.30,0.97)):
            c=center+rot@np.array([0,fy*ry,0]); draw_ring(c,rx*fr,rot@np.array([0,1.0,0]),ox,oy,1.1)
        cc=[projP(center+rot@np.array([0,fy*ry,rx*fr]),ox,oy)[0] for fy,fr in prof]; CV(cc,1.1)
def draw_box(center,h,rot,ox,oy,w=2.4,open_top=False):
    hx,hy,hz=h
    combo=[(sy,sx,sz) for sy in(-1,1) for sx in(-1,1) for sz in(-1,1)]
    idx={c:i for i,c in enumerate(combo)}; cw=[center+rot@np.array([sx*hx,sy*hy,sz*hz],float) for (sy,sx,sz) in combo]
    edges=[]
    for sy in(-1,1):
        for sx in(-1,1): edges.append((idx[(sy,sx,-1)],idx[(sy,sx,1)]))
        for sz in(-1,1): edges.append((idx[(sy,-1,sz)],idx[(sy,1,sz)]))
    for sx in(-1,1):
        for sz in(-1,1): edges.append((idx[(-1,sx,sz)],idx[(1,sx,sz)]))
    for e0,e1 in edges:
        s0,d0=projP(cw[e0],ox,oy); s1,d1=projP(cw[e1],ox,oy); near=(d0+d1)/2>-1
        CV([s0,s1],w if near else 1.4,INKc if near else FAINT)
    if open_top: draw_ring(center+rot@np.array([0,-hy,0]),hx,rot@np.array([0,1.0,0]),ox,oy,1.5)
def draw_sphere(center,r,ox,oy,w=1.9):
    s,_=projP(center,ox,oy); D.ellipse([(s[0]-r)*SC,(s[1]-r)*SC,(s[0]+r)*SC,(s[1]+r)*SC],outline=INKc,width=max(1,int(w*SC)))
    draw_ring(center,r,np.array([0,1.0,0]),ox,oy,0.9); draw_ring(center,r,np.array([1.0,0,0]),ox,oy,0.9)

# ===================== LEFT: ROTATION STUDIES =====================
for j,ang in enumerate((2,32,66)):
    draw_box(np.array([0,0,0]),(54,40,40),Ry(rad(ang)),120,210+j*200,2.2,open_top=True)
for j,ang in enumerate((2,30,60)):
    draw_egg(np.array([0,0,0]),50,74,Ry(rad(ang))@Rz(rad(6)),120,860+j*175,2.3)

# ===================== RIGHT: THE MANNEQUIN, TURNED + CONTRAPPOSTO =====================
OX,OY=655,70; U=150
def Y(h): return h*U
Rrib=Rz(rad(6))@Ry(rad(8)); Rpel=Rz(rad(-6))@Ry(rad(3))
Rc=np.array([-4,Y(1.95),0]); Pc=np.array([4,Y(3.4),0])
draw_egg(Rc,92,112,Rrib,OX,OY,2.6)
arch=[Rc+Rrib@np.array([-46,98,42]),Rc+Rrib@np.array([0,150,54]),Rc+Rrib@np.array([46,98,42])]
CV([projP(p,OX,OY)[0] for p in arch],1.5)
shL=Rc+Rrib@np.array([-108,-48,0]); shR=Rc+Rrib@np.array([108,-48,0]); nkBase=Rc+Rrib@np.array([0,-96,8])
CV([projP(Rc+Rrib@np.array([-24,-56,6]),OX,OY)[0],projP(shL,OX,OY)[0]],1.9)
CV([projP(Rc+Rrib@np.array([ 24,-56,6]),OX,OY)[0],projP(shR,OX,OY)[0]],1.9)
draw_sphere(shL,32,OX,OY); draw_sphere(shR,32,OX,OY)
draw_tube([np.array([2,Y(1.04),8]),nkBase],[27,30],OX,OY,2.2,contours=1,sub=5)
headC=np.array([2,Y(0.5),8]); Rhead=Ry(rad(16))@Rz(rad(3))
draw_egg(headC,44,52,Rhead,OX,OY,2.5)
draw_ring(headC,44,Rhead@np.array([0,1.0,0]),OX,OY,1.1)             # brow plane
jL=headC+Rhead@np.array([-22,52,20]); jR=headC+Rhead@np.array([22,52,20]); chin=headC+Rhead@np.array([0,62,32])
CV([projP(headC+Rhead@np.array([-44,20,8]),OX,OY)[0],projP(jL,OX,OY)[0],projP(chin,OX,OY)[0]],1.6)
CV([projP(headC+Rhead@np.array([ 44,20,8]),OX,OY)[0],projP(jR,OX,OY)[0],projP(chin,OX,OY)[0]],1.6)
draw_tube([Rc+Rrib@np.array([0,104,0]),Pc+Rpel@np.array([0,-78,0])],[58,62],OX,OY,2.2,contours=1,sub=5)
draw_box(Pc,(80,70,46),Rpel,OX,OY,2.6,open_top=True)
hipL=Pc+Rpel@np.array([-52,52,4]); hipR=Pc+Rpel@np.array([52,52,4])
# ARMS
elL=shL+np.array([-26,Y(1.32),18]); wrL=elL+np.array([-8,Y(0.92),12])
elR=shR+np.array([ 22,Y(1.32),22]); wrR=elR+np.array([ 10,Y(0.92),16])
for sh,el,wr,sg in ((shL,elL,wrL,-1),(shR,elR,wrR,1)):
    draw_tube([sh,el],[32,21],OX,OY,2.3,contours=2,sub=6); draw_sphere(el,18,OX,OY)
    draw_tube([el,wr],[22,13],OX,OY,2.3,contours=2,sub=6); draw_sphere(wr,12,OX,OY)
    draw_tube([wr,wr+np.array([sg*4,42,10])],[12,9],OX,OY,2.0,contours=0,sub=3)   # hand mitt (a volume)
# LEGS — weight leg straight (figure right = x+), relaxed leg knee out+forward
knW=hipR+np.array([2,Y(2.55),2]);  anW=knW+np.array([0,Y(1.5),2]);  ftA=anW
knX=hipL+np.array([-8,Y(2.5),22]); anX=knX+np.array([4,Y(1.5),-8]); ftB=anX
for hip,kn,an in ((hipR,knW,anW),(hipL,knX,anX)):
    draw_tube([hip,kn],[45,27],OX,OY,2.5,contours=2,sub=7); draw_sphere(kn,24,OX,OY)
    draw_tube([kn,an],[33,16],OX,OY,2.5,contours=2,sub=7); draw_sphere(an,14,OX,OY)
    draw_box(an+np.array([0,26,18]),(14,8,34),Ry(rad(2)),OX,OY,2.0)               # foot block (seated on ankle)

img2=img.resize((W,H),Image.LANCZOS); dd=ImageDraw.Draw(img2)
try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",16)
except: f=ImageFont.load_default()
dd.line([(300,40),(300,1318)],fill=(154,151,144),width=1)
for tx,ty,s_ in [(58,330,"box — front · 3/4 · side"),(58,1015,"egg — turning + tilting"),
                 (350,1326,"the mannequin, turned 18° + contrapposto  ·  ribcage & pelvis counter-rotate")]:
    dd.text((tx,ty),s_,fill=(96,94,90),font=f)
os.makedirs(OUT,exist_ok=True); img2.save(f"{OUT}/the_man_turn.png"); print("done")
