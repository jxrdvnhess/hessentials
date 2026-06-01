"""
FIVE PEOPLE · ONE CHAIN  (the human before anatomy — 4, 2026-05-30)
Professor: the masses currently COEXIST; next they must COMMUNICATE. "Keep every mass exactly
as it is. Introduce only: the SPINE, the CLAVICLE line, the SHOULDER line. Nothing else. One
continuous chain. Make head, ribcage, pelvis, arms, legs feel like one organism instead of
five stacked objects." So no mass moves; three connectors are added, and crucially each is
DERIVED from the masses' own rotations, so the chain reflects how they already lean:
 - SPINE: occiput -> C7 -> mid-thoracic -> T12 -> lumbar -> sacrum, each point taken from the
   head / ribcage / pelvis rotation, so the spine bows exactly as the masses bow.
 - SHOULDER line: across the existing shoulders, riding the ribcage tilt.
 - CLAVICLE: sternal notch -> each shoulder, tying the arms into the chest.
The connectors are drawn as the heavier through-line; the mass contours are lightened so the
ORGANISM reads, not the parts. (Masses identical to five_people_arms.py.)
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
SCRATCH="/sessions/nifty-keen-cerf/mnt/outputs"
W,H,SS=1480,1080,2
PAPER=(237,232,223); INK=(46,46,58); CHAIN=(40,40,52); FAINT=(186,183,176); GREY=(168,165,158); LABEL=(96,94,90)
SCALE=62.0; YSHIFT=3.75; CAMYAW=math.radians(-30); GROUND=7.55
EYE=np.eye(3)
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def pit(d): return Rx(rad(d))
def tilt(p,r): return Rz(rad(r))@Rx(rad(p))
def V(*a): return np.array(a,float)

img=Image.new("RGB",(W*SS,H*SS),PAPER); D=ImageDraw.Draw(img)
def projP(p,ox,oy):
    q=Ry(CAMYAW)@((np.array(p,float)-V(0,YSHIFT,0))*SCALE); return (ox+q[0],oy+q[1])
def projZ(p): return (Ry(CAMYAW)@((np.array(p,float)-V(0,YSHIFT,0))*SCALE))[2]
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
def basis(axis):
    axis=axis/(np.linalg.norm(axis)+1e-9)
    ref=V(0,0,1.0) if abs(axis[2])<0.9 else V(0,1.0,0)
    u=np.cross(axis,ref); u/=np.linalg.norm(u)+1e-9; v=np.cross(axis,u); return u,v
def ellipsoid(center,radii,rot,ox,oy,w=1.8,contour=True):
    rx,ry,rz=radii; c=V(*center); surf=[]
    for i in range(7):
        th=math.pi*(i+0.5)/7
        for j in range(18):
            ph=2*math.pi*j/18
            surf.append(c+rot@V(rx*math.sin(th)*math.cos(ph),ry*math.cos(th),rz*math.sin(th)*math.sin(ph)))
    CV(hull([projP(p,ox,oy) for p in surf]),w,GREY,closed=True)
    if contour:
        eq=[c+rot@V(rx*math.cos(t),0,rz*math.sin(t)) for t in np.linspace(0,2*math.pi,42)]
        CV([projP(p,ox,oy) for p in eq],0.9,FAINT)
        mer=[c+rot@V(0,ry*math.cos(t),rz*math.sin(t)) for t in np.linspace(0,2*math.pi,42)]
        CV([projP(p,ox,oy) for p in mer],0.9,FAINT)
def boxv(center,half,rot,ox,oy,w=1.6):
    hx,hy,hz=half; c=V(*center)
    combo=[(sx,sy,sz) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
    cw=[c+rot@V(sx*hx,sy*hy,sz*hz) for (sx,sy,sz) in combo]
    for a in range(8):
        for b in range(a+1,8):
            if sum(1 for k in range(3) if combo[a][k]!=combo[b][k])==1:
                near=(projZ(cw[a])+projZ(cw[b]))/2 > -2
                CV([projP(cw[a],ox,oy),projP(cw[b],ox,oy)], w if near else 1.0, GREY if near else FAINT)
def ringp(center,r,axis,ox,oy,w=0.9,col=FAINT):
    u,v=basis(V(*axis)); pts=[V(*center)+r*(math.cos(t)*u+math.sin(t)*v) for t in np.linspace(0,2*math.pi,30)]
    CV([projP(p,ox,oy) for p in pts],w,col,closed=True)
def taper(a,b,ra,rb,ox,oy,w=1.7,col=GREY):
    a=V(*a); b=V(*b); ax=b-a
    if np.linalg.norm(ax)<1e-6: return
    u,_=basis(ax)
    CV([projP(a+u*ra,ox,oy),projP(b+u*rb,ox,oy)],w,col); CV([projP(a-u*ra,ox,oy),projP(b-u*rb,ox,oy)],w,col)
def limb(a,knee,b,r,ox,oy,foot=False):
    rh,rk,ra=r
    taper(a,knee,rh,rk,ox,oy); ellipsoid(knee,(rk,rk,rk),EYE,ox,oy,1.3,contour=False)
    taper(knee,b,rk*0.92,ra,ox,oy); ringp(a,rh,V(*knee)-V(*a),ox,oy)
    if foot:
        bb=V(*b); fy=(GROUND-bb[1]); fc=bb+V(0,fy*0.5,0.42); boxv(fc,(ra*0.95,max(fy*0.5,0.05),0.62),EYE,ox,oy,1.4)
def arm(sh,el,wr,r,ox,oy):
    rs,re_,rw=r
    ellipsoid(sh,(rs,rs,rs),EYE,ox,oy,1.3,contour=False); taper(sh,el,rs*0.85,re_,ox,oy)
    ellipsoid(el,(re_,re_,re_),EYE,ox,oy,1.2,contour=False); taper(el,wr,re_*0.9,rw,ox,oy)
def catmull(P):
    P=[V(*p) for p in P]; out=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)]; p1=P[i]; p2=P[i+1]; p3=P[min(i+2,len(P)-1)]
        for t in np.linspace(0,1,14):
            t2=t*t; t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    return out

def connect(spec,ox,oy):
    """the only new marks: spine + shoulder line + clavicle, all DERIVED from the masses."""
    rc=V(*spec['rib'][0]); rr=spec['rib'][1]; rrot=spec['rib'][2]
    pc=V(*spec['pelvis'][0]); ph=spec['pelvis'][1]; prot=spec['pelvis'][2]
    hc=V(*spec['head'][0]); hr=spec['head'][1]; hrot=spec['head'][2]
    shL=V(*spec['arms'][0][0]); shR=V(*spec['arms'][1][0])
    occiput = hc + hrot@V(0, hr[1]*0.55, -hr[2]*0.78)
    C7      = (shL+shR)/2 + rrot@V(0,-0.04,-0.12)
    midT    = rc + rrot@V(0, -rr[1]*0.15, -rr[2]*0.72)
    T12     = rc + rrot@V(0,  rr[1]*0.92, -rr[2]*0.42)
    sacrum  = pc + prot@V(0, -ph[1]*0.9, -ph[2]*0.6)
    lumbar  = (T12+sacrum)/2 + V(0,0,0.14)                      # slight forward lumbar curve
    notch   = rc + rrot@V(0, -rr[1]*0.74, rr[2]*0.55)           # sternal notch (front-top)
    # spine — one continuous chain, head to sacrum (the through-line)
    CV([projP(p,ox,oy) for p in catmull([occiput,C7,midT,T12,lumbar,sacrum])],2.7,CHAIN)
    # shoulder line (rides the ribcage tilt, across the real shoulders) + clavicles
    CV([projP(shL,ox,oy),projP(shR,ox,oy)],2.2,CHAIN)
    CV([projP(shL,ox,oy),projP(notch,ox,oy)],1.7,CHAIN); CV([projP(shR,ox,oy),projP(notch,ox,oy)],1.7,CHAIN)
    # small nodes where the chain hinges (reads as joints of one organism)
    for nd in (occiput,C7,sacrum,notch):
        s=projP(nd,ox,oy); D.ellipse([(s[0]-2.0)*SS,(s[1]-2.0)*SS,(s[0]+2.0)*SS,(s[1]+2.0)*SS],fill=CHAIN)

def figure(ox,oy,spec):
    px=spec.get('plumb',0.0)
    CV([projP((px,-1.2,0),ox,oy),projP((px,GROUND+0.1,0),ox,oy)],0.7,FAINT)
    CV([projP((-1.7,GROUND,0),ox,oy),projP((1.8,GROUND,0),ox,oy)],0.8,FAINT)
    for lg in spec['legs']: limb(lg[0],lg[1],lg[2],lg[3],ox,oy,foot=True)
    pc,ph,pr=spec['pelvis']; boxv(pc,ph,pr,ox,oy)
    rc,rr,rrot=spec['rib']; ellipsoid(rc,rr,rrot,ox,oy)
    nk=spec['neck']; taper(nk[0],nk[1],nk[2],nk[2]*0.95,ox,oy)
    hc,hr,hrot=spec['head']; ellipsoid(hc,hr,hrot,ox,oy)
    for (sh,el,wr,r) in spec['arms']: arm(sh,el,wr,r,ox,oy)
    connect(spec,ox,oy)            # the chain on top — the organism

Lg=lambda hip,knee,ankle,r:(hip,knee,ankle,r); Ar=lambda sh,el,wr,r:(sh,el,wr,r)
PEOPLE=[
 ('the youth','growing toward the world', dict(plumb=0.0,
    head=((0.00,0.55,0.02),(0.50,0.60,0.52),pit(-8)), rib=((0.02,2.02,-0.04),(0.60,0.82,0.50),pit(-9)),
    pelvis=((0.00,3.45,0.0),(0.52,0.40,0.46),pit(3)), neck=((0.02,1.28,-0.02),(0.0,1.08,0.0),0.16),
    legs=[Lg((-0.34,3.95,0.02),(-0.34,5.55,0.10),(-0.33,7.20,0.02),(0.24,0.17,0.12)),
          Lg((0.34,3.95,0.02),(0.34,5.55,0.10),(0.33,7.20,0.02),(0.24,0.17,0.12))],
    arms=[Ar((-0.62,1.55,0.0),(-0.72,2.55,0.10),(-0.74,3.45,0.10),(0.16,0.12,0.09)),
          Ar((0.62,1.55,0.0),(0.72,2.55,0.10),(0.74,3.45,0.10),(0.16,0.12,0.09))])),
 ('the elder','time bent him', dict(plumb=-0.05,
    head=((0.20,1.00,0.78),(0.42,0.52,0.46),pit(14)), rib=((0.08,2.05,0.22),(0.56,0.66,0.46),pit(17)),
    pelvis=((-0.06,3.45,-0.06),(0.56,0.40,0.46),tilt(12,-4)), neck=((0.06,1.45,0.42),(0.16,1.24,0.6),0.13),
    legs=[Lg((-0.28,4.0,0.0),(-0.30,5.5,0.34),(-0.24,7.05,0.16),(0.20,0.14,0.11)),
          Lg((0.24,4.05,0.06),(0.30,5.55,0.40),(0.34,7.10,0.22),(0.20,0.14,0.11))],
    arms=[Ar((-0.5,1.62,0.18),(-0.5,2.55,0.55),(-0.46,3.4,0.82),(0.14,0.11,0.08)),
          Ar((0.46,1.64,0.2),(0.5,2.57,0.6),(0.52,3.4,0.86),(0.14,0.11,0.08))])),
 ('the bruiser','hard to move', dict(plumb=0.0,
    head=((0.0,1.18,0.08),(0.48,0.56,0.50),pit(3)), rib=((0.0,2.22,0.0),(0.98,0.92,0.80),pit(0)),
    pelvis=((0.0,3.55,0.0),(0.78,0.42,0.60),pit(0)), neck=((0.0,1.68,0.04),(0.0,1.60,0.06),0.32),
    legs=[Lg((-0.5,4.0,0.0),(-0.62,5.6,0.06),(-0.7,7.25,0.0),(0.34,0.25,0.18)),
          Lg((0.5,4.0,0.0),(0.62,5.6,0.06),(0.7,7.25,0.0),(0.34,0.25,0.18))],
    arms=[Ar((-1.02,1.85,0.0),(-1.12,2.75,0.08),(-1.06,3.6,0.08),(0.27,0.21,0.16)),
          Ar((1.02,1.85,0.0),(1.12,2.75,0.08),(1.06,3.6,0.08),(0.27,0.21,0.16))])),
 ('the aristocrat','organized', dict(plumb=0.12,
    head=((0.0,0.18,-0.06),(0.46,0.56,0.48),pit(-5)), rib=((0.0,2.05,-0.10),(0.62,1.00,0.54),pit(-6)),
    pelvis=((0.02,3.5,0.0),(0.54,0.40,0.46),tilt(-2,3)), neck=((0.0,1.22,-0.08),(0.0,0.74,-0.06),0.13),
    legs=[Lg((0.30,4.0,0.0),(0.28,5.6,0.0),(0.26,7.30,0.0),(0.22,0.16,0.12)),
          Lg((-0.30,4.05,0.0),(-0.40,5.55,0.14),(-0.34,7.30,0.06),(0.21,0.15,0.11))],
    arms=[Ar((-0.64,1.45,-0.05),(-0.62,2.5,-0.02),(-0.60,3.55,0.0),(0.16,0.12,0.085)),
          Ar((0.64,1.45,-0.05),(0.62,2.5,-0.02),(0.60,3.55,0.0),(0.16,0.12,0.085))])),
 ('the brooder','weight pulled him down', dict(plumb=0.10,
    head=((0.16,1.18,0.70),(0.46,0.54,0.50),pit(14)), rib=((0.06,2.28,0.18),(0.84,0.82,0.66),pit(15)),
    pelvis=((-0.02,3.62,-0.04),(0.72,0.46,0.56),tilt(14,6)), neck=((0.06,1.66,0.40),(0.14,1.46,0.58),0.16),
    legs=[Lg((0.34,4.1,0.0),(0.34,5.7,0.02),(0.33,7.40,0.0),(0.30,0.21,0.15)),
          Lg((-0.30,3.95,0.0),(-0.44,5.5,0.20),(-0.30,7.15,0.06),(0.27,0.18,0.13))],
    arms=[Ar((-0.80,1.82,0.12),(-0.84,2.85,0.26),(-0.80,3.85,0.34),(0.24,0.18,0.13)),
          Ar((0.80,1.84,0.14),(0.86,2.87,0.28),(0.82,3.85,0.36),(0.24,0.18,0.13))])),
]
cols=[205,505,790,1075,1340]; cy=440
for i,(name,sub,spec) in enumerate(PEOPLE): figure(cols[i],cy,spec)

def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_IT=font(10.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'FIVE PEOPLE  ·  ONE CHAIN',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('same masses — spine, clavicle, shoulder line only. five objects become one organism.'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,sub,spec) in enumerate(PEOPLE):
    D.text((cols[i]*SS-62*SS,902*SS),caps(name),fill=LABEL,font=F_SM)
    D.text((cols[i]*SS-62*SS,924*SS),sub,fill=GREY,font=F_IT)
D.line([(46*SS,980*SS),(1434*SS,980*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,996*SS),'the spine carries the head into the pelvis; the shoulder line answers the ribcage. the parts now agree.',fill=LABEL,font=F_IT)
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/five_people_connected.png'); print('done',out.size)
