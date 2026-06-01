"""
FIVE PEOPLE · SILHOUETTE ONLY  (the human before anatomy — 6, 2026-05-30)
Professor: "Remove all construction lines, internal lines, spine, clavicle — everything. Leave
only the outer SILHOUETTE. If a stranger can identify the youth / elder / bruiser / aristocrat
/ brooder from shape alone, you've entered character design. If not, the answer isn't more
detail — it's stronger MASS DESIGN." (Also the brand's own north star: pure silhouette, charged
negative space.) So the figure becomes the UNION of all its masses filled solid ink — head,
neck, ribcage, pelvis, both legs, both arms — keeping the real gaps (between the legs, under the
arms, the neck) because each convex part is filled separately and the union forms the shape.
No outlines, no chain, no plumb, no ground. Masses identical to the overlap page.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
SCRATCH="/sessions/nifty-keen-cerf/mnt/outputs"
W,H,SS=1480,1080,2
PAPER=(237,232,223); INK=(43,43,53); LABEL=(96,94,90); GREY=(150,147,140); FAINT=(196,193,186)
SCALE=62.0; YSHIFT=3.75; CAMYAW=math.radians(-30); GROUND=7.55
EYE=np.eye(3)
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def pit(d): return Rx(rad(d))
def tilt(p,r): return Rz(rad(r))@Rx(rad(p))
def Vv(*a): return np.array(a,float)

img=Image.new("RGB",(W*SS,H*SS),PAPER); D=ImageDraw.Draw(img)
def projP(p,ox,oy):
    q=Ry(CAMYAW)@((np.array(p,float)-Vv(0,YSHIFT,0))*SCALE); return (ox+q[0],oy+q[1])
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
def basis(axis):
    axis=axis/(np.linalg.norm(axis)+1e-9)
    ref=Vv(0,0,1.0) if abs(axis[2])<0.9 else Vv(0,1.0,0)
    u=np.cross(axis,ref); u/=np.linalg.norm(u)+1e-9; v=np.cross(axis,u); return u,v
def ellip_pts(center,radii,rot):
    rx,ry,rz=radii; c=Vv(*center); out=[]
    for i in range(9):
        th=math.pi*(i+0.5)/9
        for j in range(20):
            ph=2*math.pi*j/20
            out.append(c+rot@Vv(rx*math.sin(th)*math.cos(ph),ry*math.cos(th),rz*math.sin(th)*math.sin(ph)))
    return out
def sphere_pts(center,r): return ellip_pts(center,(r,r,r),EYE)
def box_pts(center,half,rot):
    hx,hy,hz=half; c=Vv(*center)
    return [c+rot@Vv(sx*hx,sy*hy,sz*hz) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
def seg_pts(a,b,ra,rb):
    a=Vv(*a); b=Vv(*b); ax=b-a
    if np.linalg.norm(ax)<1e-6: return [a]
    u,v=basis(ax); out=[]
    for c,r in ((a,ra),(b,rb)):
        for k in range(14):
            th=2*math.pi*k/14; out.append(c+r*(math.cos(th)*u+math.sin(th)*v))
    return out
def fillsil(samples3d,ox,oy,col=INK):
    poly=[(x*SS,y*SS) for x,y in hull([projP(p,ox,oy) for p in samples3d])]
    if len(poly)>=3: D.polygon(poly,fill=col)

def silhouette(ox,oy,spec):
    # UNION of every mass, filled solid -> the outer shape only
    fillsil(box_pts(*spec['pelvis']),ox,oy)
    fillsil(ellip_pts(*spec['rib']),ox,oy)
    nk=spec['neck']; fillsil(seg_pts(nk[0],nk[1],nk[2],nk[2]*0.95),ox,oy)
    fillsil(ellip_pts(*spec['head']),ox,oy)
    for (a,knee,b,r) in spec['legs']:
        rh,rk,ra=r
        fillsil(seg_pts(a,knee,rh,rk),ox,oy); fillsil(sphere_pts(knee,rk),ox,oy); fillsil(seg_pts(knee,b,rk*0.92,ra),ox,oy)
        bb=Vv(*b); fy=(GROUND-bb[1]); fc=bb+Vv(0,fy*0.5,0.42); fillsil(box_pts(fc,(ra*0.95,max(fy*0.5,0.05),0.62),EYE),ox,oy)
    for (sh,el,wr,r) in spec['arms']:
        rs,re_,rw=r
        fillsil(sphere_pts(sh,rs),ox,oy); fillsil(seg_pts(sh,el,rs*0.85,re_),ox,oy)
        fillsil(sphere_pts(el,re_),ox,oy); fillsil(seg_pts(el,wr,re_*0.9,rw),ox,oy)

Lg=lambda hip,knee,ankle,r:(hip,knee,ankle,r); Ar=lambda sh,el,wr,r:(sh,el,wr,r)
PEOPLE=[
 ('the youth','growing toward the world', dict(
    head=((0.00,0.55,0.02),(0.50,0.60,0.52),pit(-8)), rib=((0.02,2.02,-0.04),(0.60,0.82,0.50),pit(-9)),
    pelvis=((0.00,3.45,0.0),(0.52,0.40,0.46),pit(3)), neck=((0.02,1.28,-0.02),(0.0,1.08,0.0),0.16),
    legs=[Lg((-0.34,3.95,0.02),(-0.34,5.55,0.10),(-0.33,7.20,0.02),(0.24,0.17,0.12)),
          Lg((0.34,3.95,0.02),(0.34,5.55,0.10),(0.33,7.20,0.02),(0.24,0.17,0.12))],
    arms=[Ar((-0.62,1.55,0.0),(-0.72,2.55,0.10),(-0.74,3.45,0.10),(0.16,0.12,0.09)),
          Ar((0.62,1.55,0.0),(0.72,2.55,0.10),(0.74,3.45,0.10),(0.16,0.12,0.09))])),
 ('the elder','time bent him', dict(
    head=((0.20,1.00,0.78),(0.42,0.52,0.46),pit(14)), rib=((0.08,2.05,0.22),(0.56,0.66,0.46),pit(17)),
    pelvis=((-0.06,3.45,-0.06),(0.56,0.40,0.46),tilt(12,-4)), neck=((0.06,1.45,0.42),(0.16,1.24,0.6),0.13),
    legs=[Lg((-0.28,4.0,0.0),(-0.30,5.5,0.34),(-0.24,7.05,0.16),(0.20,0.14,0.11)),
          Lg((0.24,4.05,0.06),(0.30,5.55,0.40),(0.34,7.10,0.22),(0.20,0.14,0.11))],
    arms=[Ar((-0.5,1.62,0.18),(-0.5,2.55,0.55),(-0.46,3.4,0.82),(0.14,0.11,0.08)),
          Ar((0.46,1.64,0.2),(0.5,2.57,0.6),(0.52,3.4,0.86),(0.14,0.11,0.08))])),
 ('the bruiser','hard to move', dict(
    head=((0.0,1.18,0.08),(0.48,0.56,0.50),pit(3)), rib=((0.0,2.22,0.0),(0.98,0.92,0.80),pit(0)),
    pelvis=((0.0,3.55,0.0),(0.78,0.42,0.60),pit(0)), neck=((0.0,1.68,0.04),(0.0,1.60,0.06),0.32),
    legs=[Lg((-0.5,4.0,0.0),(-0.62,5.6,0.06),(-0.7,7.25,0.0),(0.34,0.25,0.18)),
          Lg((0.5,4.0,0.0),(0.62,5.6,0.06),(0.7,7.25,0.0),(0.34,0.25,0.18))],
    arms=[Ar((-1.02,1.85,0.0),(-1.12,2.75,0.08),(-1.06,3.6,0.08),(0.27,0.21,0.16)),
          Ar((1.02,1.85,0.0),(1.12,2.75,0.08),(1.06,3.6,0.08),(0.27,0.21,0.16))])),
 ('the aristocrat','organized', dict(
    head=((0.0,0.18,-0.06),(0.46,0.56,0.48),pit(-5)), rib=((0.0,2.05,-0.10),(0.62,1.00,0.54),pit(-6)),
    pelvis=((0.02,3.5,0.0),(0.54,0.40,0.46),tilt(-2,3)), neck=((0.0,1.22,-0.08),(0.0,0.74,-0.06),0.13),
    legs=[Lg((0.30,4.0,0.0),(0.28,5.6,0.0),(0.26,7.30,0.0),(0.22,0.16,0.12)),
          Lg((-0.30,4.05,0.0),(-0.40,5.55,0.14),(-0.34,7.30,0.06),(0.21,0.15,0.11))],
    arms=[Ar((-0.64,1.45,-0.05),(-0.62,2.5,-0.02),(-0.60,3.55,0.0),(0.16,0.12,0.085)),
          Ar((0.64,1.45,-0.05),(0.62,2.5,-0.02),(0.60,3.55,0.0),(0.16,0.12,0.085))])),
 ('the brooder','weight pulled him down', dict(
    head=((0.16,1.18,0.70),(0.46,0.54,0.50),pit(14)), rib=((0.06,2.28,0.18),(0.84,0.82,0.66),pit(15)),
    pelvis=((-0.02,3.62,-0.04),(0.72,0.46,0.56),tilt(14,6)), neck=((0.06,1.66,0.40),(0.14,1.46,0.58),0.16),
    legs=[Lg((0.34,4.1,0.0),(0.34,5.7,0.02),(0.33,7.40,0.0),(0.30,0.21,0.15)),
          Lg((-0.30,3.95,0.0),(-0.44,5.5,0.20),(-0.30,7.15,0.06),(0.27,0.18,0.13))],
    arms=[Ar((-0.80,1.82,0.12),(-0.84,2.85,0.26),(-0.80,3.85,0.34),(0.24,0.18,0.13)),
          Ar((0.80,1.84,0.14),(0.86,2.87,0.28),(0.82,3.85,0.36),(0.24,0.18,0.13))])),
]
cols=[205,505,790,1075,1340]; cy=440
for i,(name,sub,spec) in enumerate(PEOPLE): silhouette(cols[i],cy,spec)

def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_IT=font(10.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'FIVE PEOPLE  ·  SILHOUETTE ONLY',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('no construction, no chain — only the outer shape. cover the labels: can you still name them?'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,sub,spec) in enumerate(PEOPLE):
    D.text((cols[i]*SS-62*SS,902*SS),caps(name),fill=LABEL,font=F_SM)
    D.text((cols[i]*SS-62*SS,924*SS),sub,fill=GREY,font=F_IT)
D.line([(46*SS,980*SS),(1434*SS,980*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,996*SS),'if the shape alone tells you who he is, the mass design is doing the work.',fill=LABEL,font=F_IT)
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/five_people_silhouette.png'); print('done',out.size)
