"""
PHASE 2 · SURFACE, STAGE 3  (the human before anatomy — 11, 2026-05-30)
Professor: only ONE thing is wrong now — the FRONT shoulder->chest transition. "The profile
says body; the front occasionally says construction solving a body." Remove every visible
corner: shoulder->chest, chest->waist, waist->hip. Stay in Stage 3 until the surface feels
inevitable. Three assignments, same five, no redesign:
  A1 SHOULDER TRANSITION       — front only; kill every corner.
  A2 SURFACE WITHOUT CONSTRUCTION — finished surface, nothing underneath; does the character survive?
  A3 TWENTY SURFACE ARCHETYPES — can architecture survive surface?

The fix for the corner: (1) cross-sections are ROUNDED SUPERELLIPSES (not hard ellipses) so the
edge never kinks; (2) a sloping TRAPEZIUS YOKE grows from the neck base down to each shoulder, so
the top reads as sloping shoulders not a flat plateau; (3) DELTOID CAPS (rounded) blend the
shoulder out of the chest. The torso is still one swept Catmull-Rom flow shoulder->chest->waist->hip.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
SS=2
PAPER=(237,232,223); INK=(43,43,53); GREY=(150,147,140); FAINT=(150,147,140); LBL=(96,94,90)
SCALE=62.0; YSHIFT=3.75; GROUND=7.55
EYE=np.eye(3)
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def pit(d): return Rx(rad(d))
def tilt(p,r): return Rz(rad(r))@Rx(rad(p))
def Vv(*a): return np.array(a,float)

CAM=[Ry(rad(-12))]
def projP(p,ox,oy):
    q=CAM[0]@((np.array(p,float)-Vv(0,YSHIFT,0))*SCALE); return (ox+q[0],oy+q[1])
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
        for k in range(16): th=2*math.pi*k/16; out.append(c+r*(math.cos(th)*u+math.sin(th)*v))
    return out

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
def catmull_nodes(nodes,n):
    P=[np.array(p,float) for p in nodes]; out=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)]; p1=P[i]; p2=P[i+1]; p3=P[min(i+2,len(P)-1)]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(P[-1]); return out

def superellipse_ring(y,w,d,cx,cz,nexp=2.6,n=30):
    # rounded-rectangle-ish section; nexp>2 = fuller shoulders/flanks, no kink
    pts=[]
    for t in np.linspace(0,2*math.pi,n,endpoint=False):
        ct=math.cos(t); st=math.sin(t)
        x=cx + w*math.copysign(abs(ct)**(2.0/nexp),ct)
        z=cz + d*math.copysign(abs(st)**(2.0/nexp),st)
        pts.append(Vv(x,y,z))
    return pts

def torso_nodes(spec):
    (rx0,ry0,rz0),(rrx,rry,rrz),_=spec['rib']
    (px0,py0,pz0),(phx,phy,phz),_=spec['pelvis']
    ribbot=ry0+rry; peltop=py0-phy; waistY=(ribbot+peltop)/2
    # (y, halfwidth, depth, cx, cz)  — NOTE top node is the NECK ROOT (narrow) so shoulders SLOPE
    return [
      (ry0-rry*1.16, rrx*0.34, rrz*0.5, rx0, rz0),     # neck root (narrow top -> sloping shoulders)
      (ry0-rry*0.92, rrx*1.12, rrz*0.92, rx0, rz0),    # shoulders (wide, but reached by a slope)
      (ry0-rry*0.26, rrx*1.02, rrz*1.05, rx0, rz0),    # chest (deepest)
      (ry0+rry*0.42, rrx*0.80, rrz*0.84, rx0*0.6+px0*0.4, rz0*0.6+pz0*0.4),  # under-ribs
      (waistY,       max(rrx*0.60,phx*0.54), rrz*0.66, (rx0+px0)/2, (rz0+pz0)/2),  # waist
      (peltop+phy*0.38, phx*0.96, phz*0.95, px0, pz0), # hips
      (py0+phy*0.86, phx*0.80, phz*0.82, px0, pz0),    # hip base
    ]

def torso(ox,oy,spec,nseg=58,nexp=2.6):
    nodes=torso_nodes(spec)
    samples=catmull_nodes(nodes,max(2,nseg//(len(nodes)-1)))
    for i in range(len(samples)-1):
        y0,w0,d0,cx0,cz0=samples[i]; y1,w1,d1,cx1,cz1=samples[i+1]
        fillsil(superellipse_ring(y0,w0,d0,cx0,cz0,nexp)+superellipse_ring(y1,w1,d1,cx1,cz1,nexp),ox,oy)
    # deltoid caps: round the shoulder out of the chest (kills the top-outer corner)
    _,sh_w,sh_d,scx,scz = nodes[1]; sh_y=nodes[1][0]
    for sgn in (-1,1):
        fillsil(sphere_pts((scx+sgn*sh_w*0.80, sh_y+rry_of(spec)*0.18, scz),rry_of(spec)*0.34),ox,oy)
    nk=spec['neck']; fillsil(seg_pts(nk[0],nk[1],nk[2]*1.15,nk[2]*1.0),ox,oy)
    fillsil(ellip_pts(*spec['head']),ox,oy)
def rry_of(spec): return spec['rib'][1][1]

def foot(b,ra,ox,oy):
    bb=Vv(*b); fy=(GROUND-bb[1]); toe=bb+Vv(0,fy,0.60); heel=bb+Vv(0,fy,-0.12)
    fillsil(seg_pts(bb,(toe+heel)/2,ra*0.9,ra*0.55)+[toe,heel],ox,oy)
def limbs(ox,oy,spec,faint=False):
    if faint:
        for (a,k,b,r) in spec['legs']: CV([projP(a,ox,oy),projP(k,ox,oy)],1.1,GREY); CV([projP(k,ox,oy),projP(b,ox,oy)],1.1,GREY)
        for (s,e,w,r) in spec['arms']: CV([projP(s,ox,oy),projP(e,ox,oy)],1.1,GREY); CV([projP(e,ox,oy),projP(w,ox,oy)],1.1,GREY)
        return
    for (a,k,b,r) in spec['legs']:
        rh,rk,ra=r
        fillsil(seg_pts(a,k,rh,rk),ox,oy); fillsil(sphere_pts(k,rk*0.95),ox,oy); fillsil(seg_pts(k,b,rk*0.92,ra),ox,oy); foot(b,ra,ox,oy)
    for (s,e,w,r) in spec['arms']:
        rs,re_,rw=r
        fillsil(seg_pts(s,e,rs*0.74,re_),ox,oy); fillsil(sphere_pts(e,re_*0.92),ox,oy); fillsil(seg_pts(e,w,re_*0.9,rw),ox,oy)
def figure(ox,oy,spec,mode='full',nseg=58):
    CV([projP((-1.7,GROUND,0),ox,oy),projP((1.8,GROUND,0),ox,oy)],0.8,FAINT)
    if mode=='surface': limbs(ox,oy,spec,faint=True); torso(ox,oy,spec,nseg)
    elif mode=='clean': limbs(ox,oy,spec); torso(ox,oy,spec,nseg)
    else: limbs(ox,oy,spec); torso(ox,oy,spec,nseg)

Lg=lambda hip,knee,ankle,r:(hip,knee,ankle,r); Ar=lambda sh,el,wr,r:(sh,el,wr,r)
PEOPLE=[
 ('the youth','growing toward the world', dict(
    head=((0.00,0.55,0.02),(0.50,0.60,0.52),pit(-8)), rib=((0.02,2.02,-0.04),(0.60,0.82,0.50),pit(-9)),
    pelvis=((0.00,3.45,0.0),(0.52,0.40,0.46),pit(3)), neck=((0.02,1.28,-0.02),(0.0,1.08,0.0),0.16),
    legs=[Lg((-0.34,3.95,0.02),(-0.34,5.55,0.10),(-0.33,7.20,0.02),(0.24,0.17,0.12)),
          Lg((0.34,3.95,0.02),(0.34,5.55,0.10),(0.33,7.20,0.02),(0.24,0.17,0.12))],
    arms=[Ar((-0.62,1.62,0.0),(-0.72,2.55,0.10),(-0.74,3.45,0.10),(0.18,0.13,0.10)),
          Ar((0.62,1.62,0.0),(0.72,2.55,0.10),(0.74,3.45,0.10),(0.18,0.13,0.10))])),
 ('the elder','time bent him', dict(
    head=((0.20,1.00,0.78),(0.42,0.52,0.46),pit(14)), rib=((0.08,2.05,0.22),(0.56,0.66,0.46),pit(17)),
    pelvis=((-0.06,3.45,-0.06),(0.56,0.40,0.46),tilt(12,-4)), neck=((0.06,1.45,0.42),(0.16,1.24,0.6),0.13),
    legs=[Lg((-0.28,4.0,0.0),(-0.30,5.5,0.34),(-0.24,7.05,0.16),(0.18,0.13,0.10)),
          Lg((0.24,4.05,0.06),(0.30,5.55,0.40),(0.34,7.10,0.22),(0.18,0.13,0.10))],
    arms=[Ar((-0.5,1.68,0.18),(-0.5,2.55,0.55),(-0.46,3.4,0.82),(0.15,0.11,0.085)),
          Ar((0.46,1.7,0.2),(0.5,2.57,0.6),(0.52,3.4,0.86),(0.15,0.11,0.085))])),
 ('the bruiser','hard to move', dict(
    head=((0.0,1.18,0.08),(0.48,0.56,0.50),pit(3)), rib=((0.0,2.22,0.0),(0.98,0.92,0.80),pit(0)),
    pelvis=((0.0,3.55,0.0),(0.78,0.42,0.60),pit(0)), neck=((0.0,1.68,0.04),(0.0,1.60,0.06),0.32),
    legs=[Lg((-0.5,4.0,0.0),(-0.62,5.6,0.06),(-0.7,7.25,0.0),(0.36,0.26,0.19)),
          Lg((0.5,4.0,0.0),(0.62,5.6,0.06),(0.7,7.25,0.0),(0.36,0.26,0.19))],
    arms=[Ar((-1.02,1.95,0.0),(-1.12,2.75,0.08),(-1.06,3.6,0.08),(0.28,0.22,0.17)),
          Ar((1.02,1.95,0.0),(1.12,2.75,0.08),(1.06,3.6,0.08),(0.28,0.22,0.17))])),
 ('the aristocrat','organized', dict(
    head=((0.0,0.18,-0.06),(0.46,0.56,0.48),pit(-5)), rib=((0.0,2.05,-0.10),(0.62,1.00,0.54),pit(-6)),
    pelvis=((0.02,3.5,0.0),(0.54,0.40,0.46),tilt(-2,3)), neck=((0.0,1.22,-0.08),(0.0,0.74,-0.06),0.13),
    legs=[Lg((0.30,4.0,0.0),(0.28,5.6,0.0),(0.26,7.30,0.0),(0.23,0.16,0.12)),
          Lg((-0.30,4.05,0.0),(-0.40,5.55,0.14),(-0.34,7.30,0.06),(0.22,0.16,0.115))],
    arms=[Ar((-0.64,1.52,-0.05),(-0.62,2.5,-0.02),(-0.60,3.55,0.0),(0.17,0.12,0.09)),
          Ar((0.64,1.52,-0.05),(0.62,2.5,-0.02),(0.60,3.55,0.0),(0.17,0.12,0.09))])),
 ('the brooder','weight pulled him down', dict(
    head=((0.16,1.18,0.70),(0.46,0.54,0.50),pit(14)), rib=((0.06,2.28,0.18),(0.84,0.82,0.66),pit(15)),
    pelvis=((-0.02,3.62,-0.04),(0.72,0.46,0.56),tilt(14,6)), neck=((0.06,1.66,0.40),(0.14,1.46,0.58),0.16),
    legs=[Lg((0.34,4.1,0.0),(0.34,5.7,0.02),(0.33,7.40,0.0),(0.32,0.22,0.16)),
          Lg((-0.30,3.95,0.0),(-0.44,5.5,0.20),(-0.30,7.15,0.06),(0.29,0.19,0.14))],
    arms=[Ar((-0.80,1.92,0.12),(-0.84,2.85,0.26),(-0.80,3.85,0.34),(0.25,0.19,0.14)),
          Ar((0.80,1.94,0.14),(0.86,2.87,0.28),(0.82,3.85,0.36),(0.25,0.19,0.14))])),
]
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
def caps(s): return ' '.join(s.upper())
def header(title,sub):
    F_TTL=font(20); F_CAP=font(10)
    D.text((46*SS,40*SS),title,fill=INK,font=F_TTL)
    D.text((46*SS,74*SS),caps(sub),fill=LBL,font=F_CAP)
    D.line([(46*SS,100*SS),((W-46)*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
def labels(cols,y):
    F_SM=font(8.5); F_IT=font(10.5)
    for i,(name,sub,spec) in enumerate(PEOPLE):
        D.text((cols[i]*SS-62*SS,y*SS),caps(name),fill=LBL,font=F_SM)
        D.text((cols[i]*SS-62*SS,(y+22)*SS),sub,fill=GREY,font=F_IT)

cols=[205,505,790,1075,1340]
# A1 SHOULDER TRANSITION (front only)
CAM[0]=Ry(rad(-12)); newimg(1480,1080)
header('FIVE PEOPLE · SHOULDER TRANSITION','front only — shoulder into chest into waist into hip, with no corner left to point at.')
for i,(n,s,spec) in enumerate(PEOPLE): figure(cols[i],460,spec,'surface')
labels(cols,932)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/shoulder_transition.png'); print('saved shoulder_transition.png')

# A2 SURFACE WITHOUT CONSTRUCTION (finished surface, front)
CAM[0]=Ry(rad(-12)); newimg(1480,1080)
header('FIVE PEOPLE · SURFACE WITHOUT CONSTRUCTION','nothing underneath — only the finished surface. if the character survives, the architecture was internalized.')
for i,(n,s,spec) in enumerate(PEOPLE): figure(cols[i],460,spec,'clean')
labels(cols,932)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/surface_no_construction.png'); print('saved surface_no_construction.png')

# A3 TWENTY SURFACE ARCHETYPES — reuse the archetype proportions, now SURFACED
def arch_spec(a):
    # build a five-people-style spec from architecture knobs (proportional)
    hs=a['head_s']; rw,rh=a['rib_w'],a['rib_h']; pw,ph=a['pel_w'],a['pel_h']; ax=a.get('axis',1.0)
    pelcy=3.45; pelh=0.40*ph; ribry=0.86*rh; ribcy=pelcy-pelh-0.40*ax-ribry
    headry=0.55*hs; headcy=ribcy-ribry-(0.30*ax)-headry
    rib=((0.0,ribcy,0.0),(0.60*rw,ribry,0.52*rw),pit(0))
    pel=((0.0,pelcy,0.0),(0.50*pw,pelh,0.46*pw),pit(0))
    head=((0.0,headcy,0.0),(0.46*hs,headry,0.44*hs),pit(0))
    neck=((0.0,ribcy-ribry+0.02,0.0),(0.0,headcy+headry,0.0),0.14)
    legtop=pelcy+pelh; kneeY=legtop+1.7*ax; ankY=kneeY+1.6*ax
    lr=(0.22*pw,0.16,0.12)
    legs=[Lg((-0.30*pw,legtop,0),(-0.30*pw,kneeY,0.06),(-0.30*pw,min(ankY,GROUND-0.05),0),lr),
          Lg(( 0.30*pw,legtop,0),( 0.30*pw,kneeY,0.06),( 0.30*pw,min(ankY,GROUND-0.05),0),lr)]
    sh=ribcy-ribry*0.9; ar=(0.18,0.13,0.10)
    arms=[Ar((-0.60*rw,sh,0),(-0.66*rw,sh+0.95,0.06),(-0.66*rw,sh+1.85,0.06),ar),
          Ar(( 0.60*rw,sh,0),( 0.66*rw,sh+0.95,0.06),( 0.66*rw,sh+1.85,0.06),ar)]
    return dict(head=head,rib=rib,pelvis=pel,neck=neck,legs=legs,arms=arms)
ARCH=[
 ('teacher',dict(head_s=1.06,rib_w=0.92,rib_h=1.0,pel_w=0.92,pel_h=1.0,axis=1.06)),
 ('farmer',dict(head_s=0.94,rib_w=1.14,rib_h=0.96,pel_w=1.20,pel_h=1.06,axis=0.92)),
 ('poet',dict(head_s=0.98,rib_w=0.78,rib_h=1.02,pel_w=0.78,pel_h=0.92,axis=1.20)),
 ('boxer',dict(head_s=0.80,rib_w=1.30,rib_h=1.04,pel_w=1.02,pel_h=0.92,axis=0.86)),
 ('child',dict(head_s=1.60,rib_w=0.84,rib_h=0.74,pel_w=0.86,pel_h=0.78,axis=0.72)),
 ('king',dict(head_s=1.04,rib_w=1.14,rib_h=1.06,pel_w=1.02,pel_h=1.0,axis=1.16)),
 ('servant',dict(head_s=0.96,rib_w=0.86,rib_h=0.88,pel_w=0.92,pel_h=0.92,axis=0.94)),
 ('inventor',dict(head_s=1.22,rib_w=0.88,rib_h=0.96,pel_w=0.84,pel_h=0.92,axis=1.04)),
 ('sailor',dict(head_s=0.92,rib_w=1.22,rib_h=1.0,pel_w=1.10,pel_h=0.98,axis=0.94)),
 ('judge',dict(head_s=0.90,rib_w=1.28,rib_h=1.12,pel_w=1.30,pel_h=1.12,axis=0.96)),
 ('monk',dict(head_s=1.0,rib_w=1.0,rib_h=1.04,pel_w=1.04,pel_h=1.06,axis=0.98)),
 ('soldier',dict(head_s=0.92,rib_w=1.08,rib_h=1.06,pel_w=0.96,pel_h=0.98,axis=1.10)),
 ('dancer',dict(head_s=0.98,rib_w=0.82,rib_h=1.04,pel_w=0.86,pel_h=0.88,axis=1.22)),
 ('merchant',dict(head_s=0.98,rib_w=1.16,rib_h=0.98,pel_w=1.22,pel_h=1.04,axis=0.92)),
 ('hunter',dict(head_s=0.98,rib_w=0.96,rib_h=1.0,pel_w=0.92,pel_h=0.94,axis=1.08)),
 ('scholar',dict(head_s=1.16,rib_w=0.84,rib_h=0.96,pel_w=0.86,pel_h=0.94,axis=1.02)),
 ('blacksmith',dict(head_s=0.86,rib_w=1.34,rib_h=1.06,pel_w=1.08,pel_h=0.96,axis=0.88)),
 ('nomad',dict(head_s=0.98,rib_w=0.94,rib_h=0.94,pel_w=0.94,pel_h=0.92,axis=1.04)),
 ('priest',dict(head_s=1.0,rib_w=1.04,rib_h=1.10,pel_w=1.06,pel_h=1.08,axis=1.10)),
 ('jester',dict(head_s=1.14,rib_w=0.86,rib_h=0.92,pel_w=0.96,pel_h=0.86,axis=1.06)),
]
CAM[0]=Ry(rad(-12)); newimg(1480,1260)
header('TWENTY ARCHETYPES · SURFACE','can architecture survive surface? the proportions are wrapped — the shapes must still be the people.')
gcols=[180,440,700,960,1220]; grows=[300,560,820,1080]; F_SM=font(8.5)
for i,(name,a) in enumerate(ARCH):
    ox=gcols[i%5]; oy=grows[i//5]; figure(ox,oy,arch_spec(a),'clean',nseg=46)
    D.text((ox*SS-46*SS,(oy+150)*SS),caps(name),fill=LBL,font=F_SM)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/twenty_surface_archetypes.png'); print('saved twenty_surface_archetypes.png')
print('done')
