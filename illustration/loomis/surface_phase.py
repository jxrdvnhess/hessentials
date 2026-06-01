"""
PHASE 2 · SURFACE  (the human before anatomy — 9, 2026-05-30)
Professor opened Phase 2: SURFACE (not anatomy). "A ribcage is not a chest; a pelvis is not
hips; a mannequin is not a person. How does a human body WRAP around those masses?" Construction
must become invisible. Three assignments, the SAME five characters, masses & proportions
UNCHANGED:
  A1 SURFACE WRAP  — wrap a torso envelope (chest / waist / hip) around rib+pelvis. Limbs faint.
  A2 LIMB VOLUME   — replace stick limbs with simple tapered volumes (upper/fore, thigh/calf),
                     so the limbs feel ATTACHED, not hung.
  A3 FULL MANNEQUIN— everything unified: head, torso envelope, limb volume, weight, overlap.
End-test: cover the labels — do youth/elder/bruiser/aristocrat/brooder still read from the
surface alone? If identity needs the construction lines, the construction is carrying too much.

Method: the torso is a LOFT — horizontal cross-sections (shoulder, chest, low-ribs, WAIST pinch,
hip, hip-base) whose width/depth/centre come from the existing rib & pelvis masses; consecutive
sections filled as bands -> a continuous body envelope WITH a real waist (each band convex, so
the waist band stays narrow). Limbs = tapered filled volumes. -30 camera, near side = +x.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
SCRATCH="/sessions/nifty-keen-cerf/mnt/outputs"
SS=2
PAPER=(237,232,223); INK=(43,43,53); GREY=(150,147,140); FAINT=(150,147,140); LBL=(96,94,90)
SCALE=62.0; YSHIFT=3.75; CAMYAW=math.radians(-30); GROUND=7.55
EYE=np.eye(3)
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def pit(d): return Rx(rad(d))
def tilt(p,r): return Rz(rad(r))@Rx(rad(p))
def Vv(*a): return np.array(a,float)

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
def ring(center,hx,hz,n=22):
    c=Vv(*center); return [c+Vv(hx*math.cos(t),0,hz*math.sin(t)) for t in np.linspace(0,2*math.pi,n,endpoint=False)]
def ellip_pts(center,radii,rot):
    rx,ry,rz=radii; c=Vv(*center); out=[]
    for i in range(9):
        th=math.pi*(i+0.5)/9
        for j in range(18):
            ph=2*math.pi*j/18
            out.append(c+rot@Vv(rx*math.sin(th)*math.cos(ph),ry*math.cos(th),rz*math.sin(th)*math.sin(ph)))
    return out
def sphere_pts(center,r): return ellip_pts(center,(r,r,r),EYE)
def seg_pts(a,b,ra,rb):
    a=Vv(*a); b=Vv(*b); ax=b-a
    if np.linalg.norm(ax)<1e-6: return [a]
    u,v=basis(ax); out=[]
    for c,r in ((a,ra),(b,rb)):
        for k in range(14): th=2*math.pi*k/14; out.append(c+r*(math.cos(th)*u+math.sin(th)*v))
    return out

def cross_sections(spec):
    (rx0,ry0,rz0),(rrx,rry,rrz),_=spec['rib']
    (px0,py0,pz0),(phx,phy,phz),_=spec['pelvis']
    ribbot=ry0+rry; peltop=py0-phy; waistY=(ribbot+peltop)/2
    def lean(y):
        t=(y-ry0)/((py0)-ry0+1e-9); t=max(0,min(1,t))
        return (rx0+(px0-rx0)*t, rz0+(pz0-pz0)*t)
    secs=[]
    def add(y,hx,hz):
        cx,cz=lean(y); secs.append(((cx,y,rz0+ (pz0-rz0)*max(0,min(1,(y-ry0)/((py0)-ry0+1e-9)))),hx,hz))
    add(ry0-rry*0.86, rrx*1.16, rrz*0.92)   # shoulders (broader)
    add(ry0-rry*0.30, rrx*1.02, rrz*1.02)   # chest (deepest)
    add(ry0+rry*0.34, rrx*0.84, rrz*0.86)   # low ribs
    add(waistY,       max(rrx,phx)*0.60, max(rrz,phz)*0.66)  # WAIST pinch
    add(peltop+phy*0.30, phx*1.04, phz*1.0)  # hips (broadest below waist)
    add(py0+phy*0.78, phx*0.86, phz*0.86)    # hip base
    return secs

img=None; D=None; W=H=0
def newimg(w,h):
    global img,D,W,H; W,H=w,h
    img=Image.new("RGB",(W*SS,H*SS),PAPER); D=ImageDraw.Draw(img)
def fillsil(samples,ox,oy,col=INK):
    poly=[(x*SS,y*SS) for x,y in hull([projP(p,ox,oy) for p in samples])]
    if len(poly)>=3: D.polygon(poly,fill=col)
def CV(scr,w,col=INK,closed=False):
    pts=[(x*SS,y*SS) for x,y in scr]
    if closed: pts=pts+[pts[0]]
    if len(pts)>=2: D.line(pts,fill=col,width=max(1,int(w*SS)),joint="curve")
def stick(a,b,ox,oy,col=GREY):
    CV([projP(a,ox,oy),projP(b,ox,oy)],1.1,col)

def torso_envelope(ox,oy,spec):
    secs=cross_sections(spec)
    for i in range(len(secs)-1):
        (c0,hx0,hz0)=secs[i]; (c1,hx1,hz1)=secs[i+1]
        fillsil(ring(c0,hx0,hz0)+ring(c1,hx1,hz1),ox,oy)
    nk=spec['neck']; fillsil(seg_pts(nk[0],nk[1],nk[2]*1.25,nk[2]*1.05),ox,oy)
    fillsil(ellip_pts(*spec['head']),ox,oy)
def limb_volumes(ox,oy,spec):
    for (a,knee,b,r) in spec['legs']:
        rh,rk,ra=r
        fillsil(seg_pts(a,knee,rh,rk),ox,oy); fillsil(sphere_pts(knee,rk*0.96),ox,oy); fillsil(seg_pts(knee,b,rk*0.92,ra),ox,oy)
        bb=Vv(*b); fy=(GROUND-bb[1]); fc=bb+Vv(0,fy*0.5,0.40)
        fillsil([fc+Vv(sx*ra*0.95,sy*max(fy*0.5,0.05),sz*0.6) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)],ox,oy)
    for (sh,el,wr,r) in spec['arms']:
        rs,re_,rw=r
        fillsil(sphere_pts(sh,rs*0.95),ox,oy); fillsil(seg_pts(sh,el,rs*0.82,re_),ox,oy)
        fillsil(sphere_pts(el,re_*0.95),ox,oy); fillsil(seg_pts(el,wr,re_*0.9,rw),ox,oy)
def limb_sticks(ox,oy,spec):
    for (a,knee,b,r) in spec['legs']: stick(a,knee,ox,oy); stick(knee,b,ox,oy)
    for (sh,el,wr,r) in spec['arms']: stick(sh,el,ox,oy); stick(el,wr,ox,oy)

def render(ox,oy,spec,level):
    # ground
    CV([projP((-1.7,GROUND,0),ox,oy),projP((1.8,GROUND,0),ox,oy)],0.8,FAINT)
    if level=='surface':
        limb_sticks(ox,oy,spec); torso_envelope(ox,oy,spec)
    elif level=='limb':
        limb_volumes(ox,oy,spec); torso_envelope(ox,oy,spec)
    else: # full
        limb_volumes(ox,oy,spec); torso_envelope(ox,oy,spec)

Lg=lambda hip,knee,ankle,r:(hip,knee,ankle,r); Ar=lambda sh,el,wr,r:(sh,el,wr,r)
PEOPLE=[
 ('the youth','growing toward the world', dict(
    head=((0.00,0.55,0.02),(0.50,0.60,0.52),pit(-8)), rib=((0.02,2.02,-0.04),(0.60,0.82,0.50),pit(-9)),
    pelvis=((0.00,3.45,0.0),(0.52,0.40,0.46),pit(3)), neck=((0.02,1.28,-0.02),(0.0,1.08,0.0),0.16),
    legs=[Lg((-0.34,3.95,0.02),(-0.34,5.55,0.10),(-0.33,7.20,0.02),(0.24,0.17,0.12)),
          Lg((0.34,3.95,0.02),(0.34,5.55,0.10),(0.33,7.20,0.02),(0.24,0.17,0.12))],
    arms=[Ar((-0.62,1.55,0.0),(-0.72,2.55,0.10),(-0.74,3.45,0.10),(0.18,0.13,0.10)),
          Ar((0.62,1.55,0.0),(0.72,2.55,0.10),(0.74,3.45,0.10),(0.18,0.13,0.10))])),
 ('the elder','time bent him', dict(
    head=((0.20,1.00,0.78),(0.42,0.52,0.46),pit(14)), rib=((0.08,2.05,0.22),(0.56,0.66,0.46),pit(17)),
    pelvis=((-0.06,3.45,-0.06),(0.56,0.40,0.46),tilt(12,-4)), neck=((0.06,1.45,0.42),(0.16,1.24,0.6),0.13),
    legs=[Lg((-0.28,4.0,0.0),(-0.30,5.5,0.34),(-0.24,7.05,0.16),(0.18,0.13,0.10)),
          Lg((0.24,4.05,0.06),(0.30,5.55,0.40),(0.34,7.10,0.22),(0.18,0.13,0.10))],
    arms=[Ar((-0.5,1.62,0.18),(-0.5,2.55,0.55),(-0.46,3.4,0.82),(0.15,0.11,0.085)),
          Ar((0.46,1.64,0.2),(0.5,2.57,0.6),(0.52,3.4,0.86),(0.15,0.11,0.085))])),
 ('the bruiser','hard to move', dict(
    head=((0.0,1.18,0.08),(0.48,0.56,0.50),pit(3)), rib=((0.0,2.22,0.0),(0.98,0.92,0.80),pit(0)),
    pelvis=((0.0,3.55,0.0),(0.78,0.42,0.60),pit(0)), neck=((0.0,1.68,0.04),(0.0,1.60,0.06),0.32),
    legs=[Lg((-0.5,4.0,0.0),(-0.62,5.6,0.06),(-0.7,7.25,0.0),(0.36,0.26,0.19)),
          Lg((0.5,4.0,0.0),(0.62,5.6,0.06),(0.7,7.25,0.0),(0.36,0.26,0.19))],
    arms=[Ar((-1.02,1.85,0.0),(-1.12,2.75,0.08),(-1.06,3.6,0.08),(0.28,0.22,0.17)),
          Ar((1.02,1.85,0.0),(1.12,2.75,0.08),(1.06,3.6,0.08),(0.28,0.22,0.17))])),
 ('the aristocrat','organized', dict(
    head=((0.0,0.18,-0.06),(0.46,0.56,0.48),pit(-5)), rib=((0.0,2.05,-0.10),(0.62,1.00,0.54),pit(-6)),
    pelvis=((0.02,3.5,0.0),(0.54,0.40,0.46),tilt(-2,3)), neck=((0.0,1.22,-0.08),(0.0,0.74,-0.06),0.13),
    legs=[Lg((0.30,4.0,0.0),(0.28,5.6,0.0),(0.26,7.30,0.0),(0.23,0.16,0.12)),
          Lg((-0.30,4.05,0.0),(-0.40,5.55,0.14),(-0.34,7.30,0.06),(0.22,0.16,0.115))],
    arms=[Ar((-0.64,1.45,-0.05),(-0.62,2.5,-0.02),(-0.60,3.55,0.0),(0.17,0.12,0.09)),
          Ar((0.64,1.45,-0.05),(0.62,2.5,-0.02),(0.60,3.55,0.0),(0.17,0.12,0.09))])),
 ('the brooder','weight pulled him down', dict(
    head=((0.16,1.18,0.70),(0.46,0.54,0.50),pit(14)), rib=((0.06,2.28,0.18),(0.84,0.82,0.66),pit(15)),
    pelvis=((-0.02,3.62,-0.04),(0.72,0.46,0.56),tilt(14,6)), neck=((0.06,1.66,0.40),(0.14,1.46,0.58),0.16),
    legs=[Lg((0.34,4.1,0.0),(0.34,5.7,0.02),(0.33,7.40,0.0),(0.32,0.22,0.16)),
          Lg((-0.30,3.95,0.0),(-0.44,5.5,0.20),(-0.30,7.15,0.06),(0.29,0.19,0.14))],
    arms=[Ar((-0.80,1.82,0.12),(-0.84,2.85,0.26),(-0.80,3.85,0.34),(0.25,0.19,0.14)),
          Ar((0.80,1.84,0.14),(0.86,2.87,0.28),(0.82,3.85,0.36),(0.25,0.19,0.14))])),
]
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
def caps(s): return ' '.join(s.upper())

def sheet(level,fname,title,subtitle):
    newimg(1480,1080)
    cols=[205,505,790,1075,1340]; cy=440
    for i,(name,sub,spec) in enumerate(PEOPLE): render(cols[i],cy,spec,level)
    F_TTL=font(20); F_SM=font(8.5); F_IT=font(10.5); F_CAP=font(10)
    D.text((46*SS,40*SS),title,fill=INK,font=F_TTL)
    D.text((46*SS,74*SS),caps(subtitle),fill=LBL,font=F_CAP)
    D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
    for i,(name,sub,spec) in enumerate(PEOPLE):
        D.text((cols[i]*SS-62*SS,902*SS),caps(name),fill=LBL,font=F_SM)
        D.text((cols[i]*SS-62*SS,924*SS),sub,fill=GREY,font=F_IT)
    D.line([(46*SS,980*SS),(1434*SS,980*SS)],fill=FAINT,width=max(1,int(1*SS)))
    out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
    out.save(f'{OUT}/{fname}'); print('saved',fname)

sheet('surface','surface_wrap.png','FIVE PEOPLE · SURFACE WRAP',
      'a body wraps the masses — chest, waist, hip. no muscles. can a believable torso emerge?')
sheet('limb','limb_volume.png','FIVE PEOPLE · LIMB VOLUME',
      'stick limbs become tapered volumes — do the limbs feel attached, not hung?')
sheet('full','full_mannequin.png','FIVE PEOPLE · FULL MANNEQUIN',
      'everything unified — cover the labels: do youth, elder, bruiser, aristocrat, brooder still read?')
print('done')
