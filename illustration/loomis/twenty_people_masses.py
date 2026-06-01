"""
TWENTY PEOPLE · THREE MASSES  (the human before anatomy — 7, 2026-05-30)
Professor: construction is no longer the bottleneck — DESIGN is. "Twenty people, three masses
only, thumbnail-sized, thirty seconds each. old / young / proud / timid / curious / stubborn /
tired / hopeful / lonely / arrogant ... through masses alone." Identity now lives in SHAPE, not
detail — so each thumbnail is just head + ribcage + pelvis (filled silhouette, a tiny neck to
join), and the STATE is carried by the line of action: head tilt, ribcage lift vs collapse,
pelvis settle, and the lean through the three masses. Exaggerated, fast, no limbs/faces/detail.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
SCRATCH="/sessions/nifty-keen-cerf/mnt/outputs"
W,H,SS=1480,1200,2
PAPER=(237,232,223); INK=(43,43,53); LABEL=(96,94,90); FAINT=(196,193,186)
CAMYAW=math.radians(-74); CY=2.05    # near-profile so the line of action / lean reads
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

HEAD0=(0.0,0.62); RIB0=(0.0,2.05); PEL0=(0.0,3.25)   # pelvis raised so the waist closes
HR=(0.44,0.52,0.50); RR=(0.60,0.86,0.56); PH=(0.50,0.40,0.50)
def draw3(ox,oy,sc,spec):
    hz,hy,hp,hs=spec['head']; rz,ry,rp,rsc=spec['rib']; pz,py,pp=spec['pelvis']
    hc=(HEAD0[0]+hz,HEAD0[1]+hy,0.0); rc=(RIB0[0]+rz,RIB0[1]+ry,0.0); pc=(PEL0[0]+pz,PEL0[1]+py,0.0)
    hrot=pit(hp); rrot=pit(rp); prot=pit(pp)
    hr=(HR[0]*hs,HR[1]*hs,HR[2]*hs); rr=(RR[0]*rsc,RR[1]*rsc,RR[2]*rsc)
    rtop=Vv(*rc)+rrot@Vv(0,-rr[1],0); hbot=Vv(*hc)+hrot@Vv(0,hr[1],0)
    rbot=Vv(*rc)+rrot@Vv(0,rr[1],0); ptop=Vv(*pc)+prot@Vv(0,-PH[1],0)
    fillT(box_pts(pc,PH,prot),ox,oy,sc)
    fillT(seg_pts(rbot,ptop,0.30,0.34),ox,oy,sc)        # WAIST — connect ribcage to pelvis (one body)
    fillT(ellip_pts(rc,rr,rrot),ox,oy,sc)
    fillT(seg_pts(rtop,hbot,0.15,0.13),ox,oy,sc)        # neck
    fillT(ellip_pts(hc,hr,hrot),ox,oy,sc)

# (label, head=(dz,dy,pitch,scale), rib=(dz,dy,pitch,rscale), pelvis=(dz,dy,pitch))
S=lambda l,h,r,p: dict(label=l,head=h,rib=r,pelvis=p)
# bolder line-of-action: dz = forward(+)/back(-) lean, cumulative up the chain; thumbnails exaggerate.
PEOPLE=[
 S('proud',     (-0.22,-0.10,-16,1.0),(-0.10,-0.10,-14,1.06),( 0.06, 0.0,  4)),  # back-stacked, chest up
 S('timid',     ( 0.30, 0.16, 22,0.96),( 0.16, 0.10, 20,0.80),(-0.08,0.05,10)),  # sunk, small, curled
 S('curious',   ( 0.62,-0.04, 10,1.0),( 0.26, 0.0,   8,0.98),(-0.06,0.0, -2)),   # head reaches forward
 S('stubborn',  ( 0.0,  0.10, 12,1.06),(-0.18,0.02, -4,1.08),(-0.12,0.0, -4)),   # chin tuck, planted, dig in
 S('tired',     ( 0.46, 0.14, 26,1.0),( 0.26, 0.08, 22,0.90),(-0.06,0.07,14)),   # forward C, sinking
 S('hopeful',   (-0.04,-0.20,-18,1.0),( 0.02,-0.12,-12,1.02),( 0.04,0.0, -2)),   # rising, opening, taller
 S('lonely',    ( 0.22, 0.14, 16,0.94),( 0.12, 0.08, 14,0.80),( 0.02,0.05, 6)),  # small, withdrawn forward
 S('arrogant',  (-0.40,-0.06,-18,1.0),(-0.22,0.0,   6,1.0 ),( 0.26,0.0, -8)),    # lean-back S, hips out
 S('old',       ( 0.56, 0.10, 30,0.94),( 0.34, 0.10, 26,0.74),(-0.08,0.07,16)),  # deep bow, shrunk
 S('young',     (-0.04,-0.10, -6,1.42),(0.0,  0.03, -4,0.80),( 0.0, 0.0,  2)),   # big head, light
 S('alert',     ( 0.18,-0.12, -4,1.0),( 0.12,-0.08, -6,1.02),(-0.02,0.0, -2)),   # up + forward, taut
 S('defeated',  ( 0.40, 0.28, 30,1.0),( 0.20, 0.16, 26,0.82),(-0.02,0.11,16)),   # deep slump
 S('eager',     ( 0.60,-0.10,  6,1.0),( 0.30,-0.04,  2,1.02),(-0.10,0.0, -4)),   # forward + up reach
 S('suspicious',(-0.30, 0.06,-10,1.0),(-0.20,0.02,   8,0.96),( 0.16,0.0, -6)),   # lean back, guarded
 S('content',   ( 0.02, 0.0,   2,1.0),( 0.0, 0.02,   0,1.0 ),( 0.0, 0.0,  0)),   # calm, balanced
 S('anxious',   ( 0.26, 0.06, 14,1.0),( 0.10,-0.08, 10,0.88),(-0.06,0.02, 6)),   # head fwd, shoulders hunched up
 S('bold',      (-0.10,-0.10,-12,1.0),( 0.20,-0.12,-14,1.10),( 0.10,0.0,  0)),   # chest thrust forward+up
 S('withdrawn', ( 0.22, 0.14, 14,1.0),(-0.14,0.06,  14,0.80),( 0.0, 0.05, 6)),   # pulled back + in, closed
 S('grieving',  ( 0.40, 0.34, 32,1.0),( 0.22, 0.22, 28,0.92),(-0.02,0.13,18)),   # heavy collapse, lowest
 S('defiant',   (-0.20,-0.12,-22,1.0),( 0.16,-0.10,-12,1.10),( 0.18,0.0, -6)),   # chin jut up, chest out, planted
]
COLS=[180,440,700,960,1220]; ROWS=[280,540,800,1060]; SC=44
for i,spec in enumerate(PEOPLE):
    ox=COLS[i%5]; oy=ROWS[i//5]; draw3(ox,oy,SC,spec)

def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'TWENTY PEOPLE  ·  THREE MASSES',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('thumbnails — a state in head, ribcage, pelvis alone. lift is hope; collapse is grief; the lean is the rest.'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,spec in enumerate(PEOPLE):
    ox=COLS[i%5]; oy=ROWS[i//5]
    D.text((ox*SS-44*SS,(oy+118)*SS),caps(spec['label']),fill=LABEL,font=F_SM)
D.line([(46*SS,1150*SS),(1434*SS,1150*SS)],fill=FAINT,width=max(1,int(1*SS)))
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/twenty_people_masses.png'); print('done',out.size)
