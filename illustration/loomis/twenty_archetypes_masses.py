"""
TWENTY ARCHETYPES · THREE MASSES  (the human before anatomy — 8, 2026-05-30)
Professor: posture has a ceiling — tilt separates hope from grief (opposite directions) but not
proud from arrogant (both lean up). The new lever is ARCHITECTURE: "shape + proportion =
personality. Emotions come and go; architecture stays. Character design begins when identity
survives mood." Assignment: twenty ARCHETYPES, three masses, but now built DIFFERENTLY — head
dominance, ribcage bulk, axis height/width, pelvis breadth do the work; posture kept mild.
 child = huge head / tiny body; boxer = small head / barrel ribcage; poet = tall, narrow,
 head-light; king = tall vertical axis, broad chest; judge = monumental block; etc.
Each mass is independently scaled (w,h per mass) + the whole axis stretched/compressed; only a
little tilt. Filled silhouettes, near-profile so the axis reads. No limbs/faces/detail.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
SCRATCH="/sessions/nifty-keen-cerf/mnt/outputs"
W,H,SS=1480,1240,2
PAPER=(237,232,223); INK=(43,43,53); LABEL=(96,94,90); FAINT=(196,193,186)
CAMYAW=math.radians(-74); CY=2.05
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rad(d): return math.radians(d)
def pit(d): return Rx(rad(d))
def Vv(*a): return np.array(a,float)

img=Image.new("RGB",(W*SS,H*SS),PAPER); D=ImageDraw.Draw(img)
def projT(p,ox,oy,sc):
    q=Ry(CAMYAW)@((np.array(p,float)-Vv(0,CY,0))*sc); return (ox+q[0],oy+q[1])
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
    for i in range(7):
        th=math.pi*(i+0.5)/7
        for j in range(16):
            ph=2*math.pi*j/16
            out.append(c+rot@Vv(rx*math.sin(th)*math.cos(ph),ry*math.cos(th),rz*math.sin(th)*math.sin(ph)))
    return out
def box_pts(center,half,rot):
    hx,hy,hz=half; c=Vv(*center)
    return [c+rot@Vv(sx*hx,sy*hy,sz*hz) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
def seg_pts(a,b,ra,rb):
    a=Vv(*a); b=Vv(*b); ax=b-a
    if np.linalg.norm(ax)<1e-6: return [a]
    u,v=basis(ax); out=[]
    for c,r in ((a,ra),(b,rb)):
        for k in range(12): th=2*math.pi*k/12; out.append(c+r*(math.cos(th)*u+math.sin(th)*v))
    return out
def fillT(samples,ox,oy,sc,col=INK):
    poly=[(x*SS,y*SS) for x,y in hull([projT(p,ox,oy,sc) for p in samples])]
    if len(poly)>=3: D.polygon(poly,fill=col)

# base anchors (y down). architecture stretches these per archetype.
HHE=0.52; RWH=(0.60,0.86,0.56); PWH=(0.50,0.42,0.50)
def draw3(ox,oy,sc,a):
    # a: dict of architecture knobs
    hs=a['head_s']; rw,rh=a['rib_w'],a['rib_h']; pw,ph=a['pel_w'],a['pel_h']
    necklen=a.get('neck',0.16); axis=a.get('axis',1.0)            # axis>1 = taller/leaner
    leanH,leanR,leanP=a.get('lean',(0,0,0))                       # mild posture
    tH,tR,tP=a.get('tilt',(0,0,0))
    # stack from the ground (pelvis bottom fixed near y=3.7) upward, so taller axis grows UP
    pel_cy=3.45; pelh=PWH[1]*ph
    rib_ry=RWH[1]*rh
    rib_cy=pel_cy - pelh - (0.18*axis) - rib_ry                   # waist gap scales with axis
    head_ry=HHE*hs
    head_cy=rib_cy - rib_ry - (necklen+0.10)*axis - head_ry
    hc=(leanH,head_cy,0.0); rc=(leanR,rib_cy,0.0); pc=(leanP,pel_cy,0.0)
    hrot=pit(tH); rrot=pit(tR); prot=pit(tP)
    hr=(HHE*hs*0.86,head_ry,HHE*hs*0.80)
    rr=(RWH[0]*rw,rib_ry,RWH[2]*rw)
    pelhalf=(PWH[0]*pw,pelh,PWH[2]*pw)
    rbot=Vv(*rc)+rrot@Vv(0,rib_ry,0); ptop=Vv(*pc)+prot@Vv(0,-pelh,0)
    rtop=Vv(*rc)+rrot@Vv(0,-rib_ry,0); hbot=Vv(*hc)+hrot@Vv(0,head_ry,0)
    fillT(box_pts(pc,pelhalf,prot),ox,oy,sc)
    fillT(seg_pts(rbot,ptop,RWH[0]*rw*0.5,PWH[0]*pw*0.7),ox,oy,sc)   # waist
    fillT(ellip_pts(rc,rr,rrot),ox,oy,sc)
    fillT(seg_pts(rtop,hbot,0.13+0.02*hs,0.12),ox,oy,sc)            # neck
    fillT(ellip_pts(hc,hr,hrot),ox,oy,sc)

A=lambda l,**k: dict(label=l,**k)
# architecture is the star; tilt kept small. (head_s, rib_w, rib_h, pel_w, pel_h, axis, neck, lean, tilt)
PEOPLE=[
 A('teacher',  head_s=1.06,rib_w=0.92,rib_h=1.0, pel_w=0.92,pel_h=1.0, axis=1.06,neck=0.20,lean=(0.02,0,0),tilt=(6,2,0)),
 A('farmer',   head_s=0.94,rib_w=1.14,rib_h=0.96,pel_w=1.20,pel_h=1.06,axis=0.92,neck=0.10,lean=(0.10,0.04,0),tilt=(8,8,2)),
 A('poet',     head_s=0.98,rib_w=0.78,rib_h=1.02,pel_w=0.78,pel_h=0.92,axis=1.20,neck=0.24,lean=(0.06,0.02,0),tilt=(10,6,0)),
 A('boxer',    head_s=0.80,rib_w=1.30,rib_h=1.04,pel_w=1.02,pel_h=0.92,axis=0.86,neck=0.04,lean=(0.04,0,0),tilt=(2,-2,0)),
 A('child',    head_s=1.60,rib_w=0.84,rib_h=0.74,pel_w=0.86,pel_h=0.78,axis=0.72,neck=0.08,lean=(0,0,0),tilt=(-4,-2,0)),
 A('king',     head_s=1.04,rib_w=1.14,rib_h=1.06,pel_w=1.02,pel_h=1.0, axis=1.16,neck=0.18,lean=(-0.04,0,0),tilt=(-8,-6,2)),
 A('servant',  head_s=0.96,rib_w=0.86,rib_h=0.88,pel_w=0.92,pel_h=0.92,axis=0.94,neck=0.12,lean=(0.16,0.06,0),tilt=(18,12,6)),
 A('inventor', head_s=1.22,rib_w=0.88,rib_h=0.96,pel_w=0.84,pel_h=0.92,axis=1.04,neck=0.18,lean=(0.30,0.04,0),tilt=(12,6,0)),
 A('sailor',   head_s=0.92,rib_w=1.22,rib_h=1.0, pel_w=1.10,pel_h=0.98,axis=0.94,neck=0.08,lean=(0.06,0,0),tilt=(4,4,-2)),
 A('judge',    head_s=0.90,rib_w=1.28,rib_h=1.12,pel_w=1.30,pel_h=1.12,axis=0.96,neck=0.06,lean=(0,0,0),tilt=(-2,0,0)),
 A('monk',     head_s=1.0, rib_w=1.0, rib_h=1.04,pel_w=1.04,pel_h=1.06,axis=0.98,neck=0.04,lean=(0.08,0.04,0),tilt=(10,8,2)),
 A('soldier',  head_s=0.92,rib_w=1.08,rib_h=1.06,pel_w=0.96,pel_h=0.98,axis=1.10,neck=0.14,lean=(-0.04,0,0),tilt=(-6,-4,0)),
 A('dancer',   head_s=0.98,rib_w=0.82,rib_h=1.04,pel_w=0.86,pel_h=0.88,axis=1.22,neck=0.22,lean=(-0.06,0.02,0),tilt=(-8,4,4)),
 A('merchant', head_s=0.98,rib_w=1.16,rib_h=0.98,pel_w=1.22,pel_h=1.04,axis=0.92,neck=0.10,lean=(0.06,0.05,0),tilt=(4,4,0)),
 A('hunter',   head_s=0.98,rib_w=0.96,rib_h=1.0, pel_w=0.92,pel_h=0.94,axis=1.08,neck=0.14,lean=(0.20,0.02,0),tilt=(10,4,0)),
 A('scholar',  head_s=1.16,rib_w=0.84,rib_h=0.96,pel_w=0.86,pel_h=0.94,axis=1.02,neck=0.18,lean=(0.18,0.06,0),tilt=(16,10,2)),
 A('blacksmith',head_s=0.86,rib_w=1.34,rib_h=1.06,pel_w=1.08,pel_h=0.96,axis=0.88,neck=0.04,lean=(0.08,0.02,0),tilt=(6,2,0)),
 A('nomad',    head_s=0.98,rib_w=0.94,rib_h=0.94,pel_w=0.94,pel_h=0.92,axis=1.04,neck=0.12,lean=(0.10,0.03,0),tilt=(8,4,2)),
 A('priest',   head_s=1.0, rib_w=1.04,rib_h=1.10,pel_w=1.06,pel_h=1.08,axis=1.10,neck=0.16,lean=(-0.02,0,0),tilt=(-4,-2,0)),
 A('jester',   head_s=1.14,rib_w=0.86,rib_h=0.92,pel_w=0.96,pel_h=0.86,axis=1.06,neck=0.18,lean=(-0.10,0.03,0),tilt=(-12,6,8)),
]
COLS=[180,440,700,960,1220]; ROWS=[300,560,820,1080]; SC=42
for i,a in enumerate(PEOPLE):
    draw3(COLS[i%5],ROWS[i//5],SC,a)

def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'TWENTY ARCHETYPES  ·  THREE MASSES',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('not mood — architecture. head dominance, ribcage bulk, axis height build the person; identity survives mood.'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,a in enumerate(PEOPLE):
    ox=COLS[i%5]; oy=ROWS[i//5]
    D.text((ox*SS-46*SS,(oy+150)*SS),caps(a['label']),fill=LABEL,font=F_SM)
D.line([(46*SS,1190*SS),(1434*SS,1190*SS)],fill=FAINT,width=max(1,int(1*SS)))
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/twenty_archetypes_masses.png'); print('done',out.size)
