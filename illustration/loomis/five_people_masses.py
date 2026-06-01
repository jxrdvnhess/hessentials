"""
FIVE PEOPLE · THREE MASSES  (Sketch 101 -> the body, 2026-05-30)
Professor handed off the head curriculum and opened the body one: THE HUMAN BEFORE ANATOMY.
"The body is not anatomy; the body is mass distribution. Same question as the head: can I
identify the person before the details arrive?" Assignment 1: five people from only
  HEAD · RIBCAGE · PELVIS
No arms, no legs, no muscle, no features. Arms/legs are seductive — they let you FAKE
character; a slouched ribcage or a pelvis carrying weight cannot be faked. Character must
exist before gesture.

So: three construction masses (head ovoid, ribcage egg, pelvis box) stacked on a SPINE
line-of-action, drawn as transparent volumes (the volume-mannequin idiom), against a faint
PLUMB vertical + GROUND so lean and weight read. Five postures authored:
 YOUTH — big cranium, small lifted ribcage, narrow, reaching UP (growing toward the world).
 ELDER — forward head, compressed ribcage, pelvis carrying weight, a bow (lived in).
 BRUISER — head sunk into shoulders, barrel ribcage, wide stable pelvis (hard to move).
 ARISTOCRAT — elevated head, long neck, lifted ribcage, vertical alignment (organized).
 BROODER — forward head, collapsed ribcage, pelvis carrying the load, settling down (heavy).
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W,H,SS=1480,940,2
PAPER=(237,232,223); INK=(46,46,58); FAINT=(178,175,168); GREY=(150,147,140); LABEL=(96,94,90)
SCALE=78.0; YSHIFT=2.05; CAMYAW=math.radians(-30)

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def pitch(d): return Rx(rad(d))

img=Image.new("RGB",(W*SS,H*SS),PAPER); D=ImageDraw.Draw(img)
def projP(p,ox,oy):
    q=Ry(CAMYAW)@((np.array(p,float)-np.array([0,YSHIFT,0]))*SCALE)
    return (ox+q[0], oy+q[1])
def projZ(p):
    return (Ry(CAMYAW)@((np.array(p,float)-np.array([0,YSHIFT,0]))*SCALE))[2]
def CV(scr,w,col=INK,closed=False):
    pts=[(x*SS,y*SS) for x,y in scr]
    if closed: pts=pts+[pts[0]]
    if len(pts)>=2: D.line(pts,fill=col,width=max(1,int(w*SS)),joint="curve")
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

def ellipsoid(center,radii,rot,ox,oy,w=2.2,contour=True):
    rx,ry,rz=radii; c=np.array(center,float); surf=[]
    for i in range(7):
        th=math.pi*(i+0.5)/7
        for j in range(18):
            ph=2*math.pi*j/18
            surf.append(c+rot@np.array([rx*math.sin(th)*math.cos(ph),ry*math.cos(th),rz*math.sin(th)*math.sin(ph)]))
    CV(hull([projP(p,ox,oy) for p in surf]),w,INK,closed=True)
    if contour:
        eq=[c+rot@np.array([rx*math.cos(t),0,rz*math.sin(t)]) for t in np.linspace(0,2*math.pi,42)]
        CV([projP(p,ox,oy) for p in eq],1.0,GREY)
        mer=[c+rot@np.array([0,ry*math.cos(t),rz*math.sin(t)]) for t in np.linspace(0,2*math.pi,42)]
        CV([projP(p,ox,oy) for p in mer],1.0,GREY)

def boxv(center,half,rot,ox,oy,w=2.0):
    hx,hy,hz=half; c=np.array(center,float)
    combo=[(sx,sy,sz) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
    cw=[c+rot@np.array([sx*hx,sy*hy,sz*hz],float) for (sx,sy,sz) in combo]
    for a in range(8):
        for b in range(a+1,8):
            if sum(1 for k in range(3) if combo[a][k]!=combo[b][k])==1:
                near=(projZ(cw[a])+projZ(cw[b]))/2 > -2
                CV([projP(cw[a],ox,oy),projP(cw[b],ox,oy)], w if near else 1.2, INK if near else FAINT)

def tube(p0,p1,r,ox,oy,w=1.8):
    a=np.array(p0,float); b=np.array(p1,float); ax=b-a; n=np.linalg.norm(ax)
    if n<1e-6: return
    u=np.cross(ax,[0,0,1.0]);
    if np.linalg.norm(u)<1e-6: u=np.array([1.0,0,0])
    u=u/np.linalg.norm(u)
    CV([projP(a+u*r,ox,oy),projP(b+u*r,ox,oy)],w,INK)
    CV([projP(a-u*r,ox,oy),projP(b-u*r,ox,oy)],w,INK)

def spine(pts,ox,oy,w=2.4):
    # smooth line of action through control pts (catmull-rom)
    P=[np.array(p,float) for p in pts]; out=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)]; p1=P[i]; p2=P[i+1]; p3=P[min(i+2,len(P)-1)]
        for t in np.linspace(0,1,12):
            t2=t*t; t3=t2*t
            q=0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3)
            out.append(projP(q,ox,oy))
    CV(out,w,INK)

def figure(ox,oy,spec):
    # plumb + ground (read lean/weight against vertical)
    px=spec['plumb']
    CV([projP((px,-1.0,0),ox,oy),projP((px,4.4,0),ox,oy)],0.8,FAINT)
    gy=spec['ground']
    CV([(projP((-1.3,gy,0),ox,oy)),(projP((1.5,gy,0),ox,oy))],0.9,FAINT)
    # spine line of action
    spine(spec['spine'],ox,oy)
    # pelvis box
    pc,ph,pr=spec['pelvis']; boxv(pc,ph,pr,ox,oy,2.0)
    # ribcage egg
    rc,rr,rrot=spec['rib']; ellipsoid(rc,rr,rrot,ox,oy,2.3)
    # neck
    tube(spec['neck'][0],spec['neck'][1],spec['neck'][2],ox,oy,1.7)
    # head ovoid
    hc,hr,hrot=spec['head']; ellipsoid(hc,hr,hrot,ox,oy,2.2)

# ---------- the five, authored as three-mass postures (y down; +z forward) ----------
def P(*a): return np.array(a,float)
PEOPLE=[
 ('the youth','growing toward the world', dict(
    plumb=0.0, ground=3.95,
    head=((0.00,0.42,0.02),(0.50,0.60,0.52),pitch(-8)),
    rib =((0.02,1.95,-0.05),(0.60,0.82,0.50),pitch(-10)),
    pelvis=((0.00,3.35,0.0),(0.52,0.40,0.46),pitch(4)),
    neck=((0.02,1.18,-0.02),(0.0,0.95,0.0),0.16),
    spine=[(0.0,3.5,0.05),(0.02,2.7,-0.04),(0.02,1.95,-0.05),(0.02,1.2,-0.02),(0.0,0.95,0.0)])),
 ('the elder','lived in', dict(
    plumb=0.0, ground=3.95,
    head=((0.12,0.95,0.66),(0.44,0.54,0.48),pitch(12)),
    rib =((0.05,2.05,0.14),(0.70,0.74,0.55),pitch(15)),
    pelvis=((-0.04,3.45,-0.10),(0.60,0.42,0.48),pitch(13)),
    neck=((0.04,1.42,0.34),(0.12,1.22,0.5),0.15),
    spine=[(-0.04,3.55,-0.10),(0.0,2.75,0.06),(0.05,2.05,0.14),(0.10,1.45,0.4),(0.12,1.2,0.62)])),
 ('the bruiser','hard to move', dict(
    plumb=0.0, ground=3.95,
    head=((0.0,1.05,0.08),(0.48,0.56,0.50),pitch(3)),
    rib =((0.0,2.18,0.0),(0.98,0.92,0.80),pitch(0)),
    pelvis=((0.0,3.48,0.0),(0.74,0.42,0.58),pitch(0)),
    neck=((0.0,1.55,0.04),(0.0,1.46,0.06),0.30),
    spine=[(0.0,3.55,0.0),(0.0,2.9,0.0),(0.0,2.18,0.0),(0.0,1.55,0.03),(0.0,1.42,0.05)])),
 ('the aristocrat','organized', dict(
    plumb=0.0, ground=3.95,
    head=((0.0,0.10,-0.06),(0.46,0.56,0.48),pitch(-5)),
    rib =((0.0,2.00,-0.10),(0.62,1.00,0.54),pitch(-6)),
    pelvis=((0.0,3.45,0.0),(0.54,0.40,0.46),pitch(-2)),
    neck=((0.0,1.12,-0.08),(0.0,0.66,-0.06),0.13),
    spine=[(0.0,3.5,0.0),(0.0,2.7,-0.05),(0.0,2.0,-0.10),(0.0,1.15,-0.08),(0.0,0.62,-0.06)])),
 ('the brooder','heavy before emotional', dict(
    plumb=0.0, ground=4.0,
    head=((0.14,1.02,0.72),(0.46,0.54,0.50),pitch(14)),
    rib =((0.06,2.22,0.20),(0.76,0.74,0.60),pitch(17)),
    pelvis=((-0.04,3.55,-0.06),(0.66,0.44,0.50),pitch(15)),
    neck=((0.05,1.55,0.42),(0.13,1.34,0.6),0.16),
    spine=[(-0.04,3.62,-0.06),(0.0,2.82,0.08),(0.06,2.22,0.20),(0.11,1.6,0.46),(0.14,1.3,0.68)])),
]
cols=[200,500,775,1050,1335]; cy=470
for i,(name,sub,spec) in enumerate(PEOPLE):
    figure(cols[i],cy,spec)

def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_IT=font(10.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'FIVE PEOPLE  ·  THREE MASSES',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('head · ribcage · pelvis — no arms, no legs, no features. character before gesture.'),
       fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,sub,spec) in enumerate(PEOPLE):
    D.text((cols[i]*SS-60*SS,720*SS),caps(name),fill=LABEL,font=F_SM)
    D.text((cols[i]*SS-60*SS,742*SS),sub,fill=GREY,font=F_IT)
D.line([(46*SS,800*SS),(1434*SS,800*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,816*SS),'a slouched ribcage cannot be faked — the body is mass distribution before it is anatomy.',
       fill=LABEL,font=F_IT)
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/five_people_masses.png'); print('done',out.size)
