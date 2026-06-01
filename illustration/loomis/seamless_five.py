"""
SKETCH 101 · FINAL — SEAMLESS FIGURE  (the human before anatomy — 13, 2026-05-30)
Professor's last assignment: the original five as FINISHED seamless mannequins — front, profile,
walking — no labels mid-grid, no construction, no callouts. "Make me forget where one part ends
and another begins." The only remaining seam is the HIP. Fix it and 101 is complete.

HIP FIX (same logic that solved the shoulder): the torso and legs must OVERLAP, not abut.
 - the torso's lowest swept node is pushed DOWN to the crotch level (not stopping at hip-top);
 - the thigh tops start UP INSIDE the pelvis (overlapping it) with a fattened top radius, so the
   thigh fuses into the hip mass with no blank band.
Engine = refined superellipse swept torso + sloping shoulders + deltoid caps + limb volumes
+ walk() stride. Front cam Ry(-12), profile Ry(-90), walk 3/4 Ry(-52).
"""
import os, math, copy
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
def super_ring(y,w,d,cx,cz,nexp=2.6,n=30):
    pts=[]
    for t in np.linspace(0,2*math.pi,n,endpoint=False):
        ct=math.cos(t); st=math.sin(t)
        x=cx+w*math.copysign(abs(ct)**(2.0/nexp),ct); z=cz+d*math.copysign(abs(st)**(2.0/nexp),st)
        pts.append(Vv(x,y,z))
    return pts
def torso_nodes(spec):
    (rx0,ry0,rz0),(rrx,rry,rrz),_=spec['rib']
    (px0,py0,pz0),(phx,phy,phz),_=spec['pelvis']
    ribbot=ry0+rry; peltop=py0-phy; waistY=(ribbot+peltop)/2
    crotch=py0+phy*1.18           # HIP FIX: torso flows down to crotch level
    return [
      (ry0-rry*1.16, rrx*0.34, rrz*0.5, rx0, rz0),
      (ry0-rry*0.92, rrx*1.12, rrz*0.92, rx0, rz0),
      (ry0-rry*0.26, rrx*1.02, rrz*1.05, rx0, rz0),
      (ry0+rry*0.42, rrx*0.80, rrz*0.84, rx0*0.6+px0*0.4, rz0*0.6+pz0*0.4),
      (waistY, max(rrx*0.60,phx*0.54), rrz*0.66, (rx0+px0)/2, (rz0+pz0)/2),
      (peltop+phy*0.45, phx*0.98, phz*0.96, px0, pz0),     # hips (broadest)
      (crotch, phx*0.62, phz*0.74, px0, pz0),              # crotch — torso fuses to legs here
    ]
def torso(ox,oy,spec,nexp=2.6,nseg=60):
    nodes=torso_nodes(spec); samples=catmull_nodes(nodes,max(2,nseg//(len(nodes)-1)))
    for i in range(len(samples)-1):
        y0,w0,d0,cx0,cz0=samples[i]; y1,w1,d1,cx1,cz1=samples[i+1]
        fillsil(super_ring(y0,w0,d0,cx0,cz0,nexp)+super_ring(y1,w1,d1,cx1,cz1,nexp),ox,oy)
    rry=spec['rib'][1][1]; _,sh_w,sh_d,scx,scz=nodes[1]; sh_y=nodes[1][0]
    for sgn in (-1,1): fillsil(sphere_pts((scx+sgn*sh_w*0.80,sh_y+rry*0.18,scz),rry*0.34),ox,oy)
    nk=spec['neck']; fillsil(seg_pts(nk[0],nk[1],nk[2]*1.15,nk[2]*1.0),ox,oy); fillsil(ellip_pts(*spec['head']),ox,oy)
def foot(b,ra,ox,oy):
    # ankle b -> a small flat wedge to the ground, modest toe; ankle sphere fuses shin to foot
    bb=Vv(*b); fy=max(GROUND-bb[1],0.02)
    ankle=bb; toe=Vv(bb[0],GROUND,bb[2]+0.42); heel=Vv(bb[0],GROUND,bb[2]-0.10)
    fillsil(sphere_pts(ankle,ra*0.92),ox,oy)                 # ankle ball (no detached blob)
    fillsil([ankle+Vv(ra*0.5,0,0),ankle-Vv(ra*0.5,0,0),
             toe+Vv(ra*0.45,0,0),toe-Vv(ra*0.45,0,0),
             heel+Vv(ra*0.45,0,0),heel-Vv(ra*0.45,0,0)],ox,oy)  # low wedge, sits ON ground
def limbs(ox,oy,spec):
    for L in spec['legs']:
        a,k,b,r=L[0],L[1],L[2],L[3]; rh,rk,ra=r
        # thigh top sphere sits UP inside the pelvis to fuse (no seam)
        fillsil(sphere_pts(a,rh*1.05),ox,oy)
        fillsil(seg_pts(a,k,rh,rk),ox,oy); fillsil(sphere_pts(k,rk*0.95),ox,oy); fillsil(seg_pts(k,b,rk*0.92,ra),ox,oy)
        foot(b,ra,ox,oy)
    for s,e,w,r in spec['arms']:
        rs,re_,rw=r
        fillsil(seg_pts(s,e,rs*0.74,re_),ox,oy); fillsil(sphere_pts(e,re_*0.92),ox,oy); fillsil(seg_pts(e,w,re_*0.9,rw),ox,oy)
def figure(ox,oy,spec):
    CV([projP((-1.7,GROUND,0),ox,oy),projP((1.8,GROUND,0),ox,oy)],0.8,FAINT)
    limbs(ox,oy,spec); torso(ox,oy,spec)
def make_spec(head_s,rib_w,rib_h,pel_w,pel_h,axis,lean=0.0,stoop=0.0,armspread=1.0,legspread=1.0):
    pelcy=3.45; pelh=0.40*pel_h; ribry=0.86*rib_h; ribcy=pelcy-pelh-0.42*axis-ribry
    headry=0.55*head_s; headcy=ribcy-ribry-(0.34*axis)-headry
    def lz(y): return lean*(pelcy-y)/3.0
    rib=((lz(ribcy),ribcy,0.0),(0.60*rib_w,ribry,0.52*rib_w),pit(8*lean))
    pel=((0.0,pelcy,0.0),(0.50*pel_w,pelh,0.46*pel_w),pit(2*lean))
    head=((lz(headcy)+stoop,headcy,0.0),(0.46*head_s,headry,0.44*head_s),pit(10*lean+18*stoop))
    neck=((lz(ribcy-ribry)+stoop*0.5,ribcy-ribry+0.02,lz(headcy)+stoop),(0.0,headcy+headry,0.0),0.13+0.02*rib_w)
    crotch=pelcy+pelh*1.18
    legtop=crotch-0.12*axis; kneeY=pelcy+pelh+1.55*axis; ankY=min(kneeY+1.5*axis,GROUND-0.05)
    lr=(0.23*max(pel_w,0.8),0.16,0.12)
    lx=0.26*pel_w*legspread
    legs=[(( -lx,legtop,0),(-lx,kneeY,0.06),(-lx,ankY,0),lr),
          (( lx,legtop,0),( lx,kneeY,0.06),( lx,ankY,0),lr)]
    sh=ribcy-ribry*0.86; ar=(0.18,0.13,0.10); axw=0.62*rib_w*armspread
    arms=[((-axw,sh+0.05,0),(-axw-0.02,sh+0.95,0.05),(-axw-0.02,sh+1.85,0.05),ar),
          (( axw,sh+0.05,0),( axw+0.02,sh+0.95,0.05),( axw+0.02,sh+1.85,0.05),ar)]
    return dict(head=head,rib=rib,pelvis=pel,neck=neck,legs=legs,arms=arms)
def walk(spec0,phase):
    s=copy.deepcopy(spec0); fore=0.55*phase
    def shift(leg,dz,bend):
        a,k,b,r=leg; a=Vv(*a)+Vv(0,0,dz*0.25); k=Vv(*k)+Vv(0,0,dz*0.7); b=Vv(*b)+Vv(0,0,dz)
        return (tuple(a),tuple(k),tuple(b),r)
    s['legs']=[shift(s['legs'][0],-fore,abs(phase)),shift(s['legs'][1],fore,abs(phase))]
    def sw(arm,dz):
        sh,el,wr,r=arm; el=Vv(*el)+Vv(0,0,dz); wr=Vv(*wr)+Vv(0,0,dz*1.7); return (sh,tuple(el),tuple(wr),r)
    s['arms']=[sw(s['arms'][0],fore),sw(s['arms'][1],-fore)]
    return s
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
def caps(s): return ' '.join(s.upper())

FIVE=[('the youth',make_spec(1.30,0.86,0.90,0.84,0.82,1.05)),
      ('the elder',make_spec(0.96,0.78,0.84,0.84,0.86,0.92, lean=0.16, stoop=0.14)),
      ('the bruiser',make_spec(0.84,1.34,1.0,1.06,0.94,0.86, legspread=1.15)),
      ('the aristocrat',make_spec(1.0,0.92,1.10,0.84,0.94,1.20, lean=-0.04)),
      ('the brooder',make_spec(0.96,1.06,0.94,1.0,0.96,0.96, lean=0.12, stoop=0.10))]
phases=[-0.7,0.5,-0.6,0.6,-0.5]

newimg(1480,1500)
F_TTL=font(20); F_CAP=font(10); F_SM=font(8.5); F_RL=font(9)
D.text((46*SS,40*SS),'FIVE PEOPLE · THE SEAMLESS FIGURE',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('front · profile · walking — no construction, no joints. only the person.'),fill=LBL,font=F_CAP)
D.line([(46*SS,100*SS),(1434*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
cols=[200,485,770,1055,1340]
rowY=[460,940]   # front+profile row, walking row
# row 1: front (left of pair) + profile (right of pair) per person, tight
for i,(name,spec) in enumerate(FIVE):
    CAM[0]=Ry(rad(-12)); figure(cols[i]-46,rowY[0],spec)
    CAM[0]=Ry(rad(-90)); figure(cols[i]+60,rowY[0],spec)
# row 2: walking, 3/4
for i,(name,spec) in enumerate(FIVE):
    CAM[0]=Ry(rad(-52)); figure(cols[i],rowY[1],walk(spec,phases[i]))
# labels only at the base
for i,(name,spec) in enumerate(FIVE):
    D.text((cols[i]*SS-58*SS,1432*SS),caps(name),fill=LBL,font=F_SM)
D.text((46*SS,430*SS),caps('front / profile'),fill=GREY,font=F_RL)
D.text((46*SS,912*SS),caps('walking'),fill=GREY,font=F_RL)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/seamless_five.png'); print('saved seamless_five.png',(W,H))
print('done')
