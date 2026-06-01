"""
SKETCH 101 · GRADUATION GATE  (the human before anatomy — 12, 2026-05-30)
Professor: at the doorway between 101 and 201. Three tests:
  A1 ARCHETYPES · ARCHITECTURE REVISION — separate the mid-cluster (teacher/monk/servant/
     priest/sailor/soldier/nomad) that kept collapsing. NOT surface — give each its own BUILD
     + a secondary idea, so shuffled-with-labels-covered they're still nameable.
  A2 TEN NEW PEOPLE — ten brand-new distinct humans (no archetype names) across the proportion
     space; a viewer should describe each differently.
  A3 FIVE WALKING — the original five in an ordinary walk; identity must survive MOTION
     (the bruiser walking is still the bruiser).
Engine = the refined surface (superellipse swept torso + sloping shoulders + deltoid caps +
limb volumes), proven to make construction invisible. Walk adds pelvis/shoulder counter-
rotation + a fore/back leg stride.
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
    return [
      (ry0-rry*1.16, rrx*0.34, rrz*0.5, rx0, rz0),
      (ry0-rry*0.92, rrx*1.12, rrz*0.92, rx0, rz0),
      (ry0-rry*0.26, rrx*1.02, rrz*1.05, rx0, rz0),
      (ry0+rry*0.42, rrx*0.80, rrz*0.84, rx0*0.6+px0*0.4, rz0*0.6+pz0*0.4),
      (waistY, max(rrx*0.60,phx*0.54), rrz*0.66, (rx0+px0)/2, (rz0+pz0)/2),
      (peltop+phy*0.38, phx*0.96, phz*0.95, px0, pz0),
      (py0+phy*0.86, phx*0.80, phz*0.82, px0, pz0),
    ]
def torso(ox,oy,spec,nexp=2.6,nseg=58):
    nodes=torso_nodes(spec); samples=catmull_nodes(nodes,max(2,nseg//(len(nodes)-1)))
    for i in range(len(samples)-1):
        y0,w0,d0,cx0,cz0=samples[i]; y1,w1,d1,cx1,cz1=samples[i+1]
        fillsil(super_ring(y0,w0,d0,cx0,cz0,nexp)+super_ring(y1,w1,d1,cx1,cz1,nexp),ox,oy)
    rry=spec['rib'][1][1]; _,sh_w,sh_d,scx,scz=nodes[1]; sh_y=nodes[1][0]
    for sgn in (-1,1): fillsil(sphere_pts((scx+sgn*sh_w*0.80,sh_y+rry*0.18,scz),rry*0.34),ox,oy)
    nk=spec['neck']; fillsil(seg_pts(nk[0],nk[1],nk[2]*1.15,nk[2]*1.0),ox,oy); fillsil(ellip_pts(*spec['head']),ox,oy)
def foot(b,ra,ox,oy,fwd=0.0):
    bb=Vv(*b); fy=(GROUND-bb[1]); toe=bb+Vv(0,fy,0.60+fwd); heel=bb+Vv(0,fy,-0.12+fwd)
    fillsil(seg_pts(bb,(toe+heel)/2,ra*0.9,ra*0.55)+[toe,heel],ox,oy)
def limbs(ox,oy,spec):
    for L in spec['legs']:
        a,k,b,r=L[0],L[1],L[2],L[3]; rh,rk,ra=r
        fillsil(seg_pts(a,k,rh,rk),ox,oy); fillsil(sphere_pts(k,rk*0.95),ox,oy); fillsil(seg_pts(k,b,rk*0.92,ra),ox,oy)
        foot(b,ra,ox,oy,L[4] if len(L)>4 else 0.0)
    for s,e,w,r in spec['arms']:
        rs,re_,rw=r
        fillsil(seg_pts(s,e,rs*0.74,re_),ox,oy); fillsil(sphere_pts(e,re_*0.92),ox,oy); fillsil(seg_pts(e,w,re_*0.9,rw),ox,oy)
def figure(ox,oy,spec):
    CV([projP((-1.7,GROUND,0),ox,oy),projP((1.8,GROUND,0),ox,oy)],0.8,FAINT)
    limbs(ox,oy,spec); torso(ox,oy,spec)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
def caps(s): return ' '.join(s.upper())
def header(title,sub):
    F_TTL=font(20); F_CAP=font(10)
    D.text((46*SS,40*SS),title,fill=INK,font=F_TTL); D.text((46*SS,74*SS),caps(sub),fill=LBL,font=F_CAP)
    D.line([(46*SS,100*SS),((W-46)*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
Lg=lambda hip,knee,ankle,r,fwd=0.0:(hip,knee,ankle,r,fwd); Ar=lambda sh,el,wr,r:(sh,el,wr,r)

def make_spec(head_s,rib_w,rib_h,pel_w,pel_h,axis,lean=0.0,stoop=0.0,armspread=1.0,legspread=1.0):
    """proportional body. lean=whole fwd drift, stoop=head fwd extra."""
    pelcy=3.45; pelh=0.40*pel_h; ribry=0.86*rib_h; ribcy=pelcy-pelh-0.42*axis-ribry
    headry=0.55*head_s; headcy=ribcy-ribry-(0.34*axis)-headry
    def lz(y): return lean*(pelcy-y)/3.0
    rib=((lz(ribcy),ribcy,0.0),(0.60*rib_w,ribry,0.52*rib_w),pit(8*lean))
    pel=((0.0,pelcy,0.0),(0.50*pel_w,pelh,0.46*pel_w),pit(2*lean))
    head=((lz(headcy)+stoop,headcy,0.0),(0.46*head_s,headry,0.44*head_s),pit(10*lean+18*stoop))
    neck=((lz(ribcy-ribry)+stoop*0.5,ribcy-ribry+0.02,lz(headcy)+stoop),(0.0,headcy+headry,0.0),0.13+0.02*rib_w)
    legtop=pelcy+pelh*0.6; kneeY=legtop+1.62*axis; ankY=min(kneeY+1.55*axis,GROUND-0.05)
    lr=(0.22*max(pel_w,0.8),0.16,0.12)
    lx=0.30*pel_w*legspread
    legs=[Lg((-lx,legtop,0),(-lx,kneeY,0.06),(-lx,ankY,0),lr),
          Lg(( lx,legtop,0),( lx,kneeY,0.06),( lx,ankY,0),lr)]
    sh=ribcy-ribry*0.86; ar=(0.18,0.13,0.10); axw=0.62*rib_w*armspread
    arms=[Ar((-axw,sh+0.05,0),(-axw-0.02,sh+0.95,0.05),(-axw-0.02,sh+1.85,0.05),ar),
          Ar(( axw,sh+0.05,0),( axw+0.02,sh+0.95,0.05),( axw+0.02,sh+1.85,0.05),ar)]
    return dict(head=head,rib=rib,pelvis=pel,neck=neck,legs=legs,arms=arms)

# ================= A1: ARCHETYPES, MID-CLUSTER SEPARATED =================
# the seven that rhymed, now each a distinct build + secondary idea:
MID=[
 ('teacher',  make_spec(1.06,0.94,1.04,0.92,1.0, 1.10, lean=0.05, stoop=0.05, armspread=0.95)),  # tall-ish, slight attentive head-forward, narrow
 ('monk',     make_spec(0.98,1.06,0.96,1.16,1.12,0.90, lean=0.10, armspread=1.05)),               # low, round, heavy belly/hips, sunk
 ('servant',  make_spec(0.94,0.82,0.84,0.86,0.88,0.86, lean=0.06, stoop=0.10)),                   # small, compressed, deferential head-down
 ('priest',   make_spec(1.0, 1.0, 1.14,1.18,1.16,1.16)),                                          # tall + robe-wide hips, vertical, monumental lower
 ('sailor',   make_spec(0.90,1.26,0.96,1.06,0.92,0.86, legspread=1.35)),                          # stocky barrel, WIDE planted stance, short
 ('soldier',  make_spec(0.92,1.18,1.10,0.92,0.98,1.16, lean=-0.04)),                              # broad shoulders, narrow waist, tall, chest-up
 ('nomad',    make_spec(0.96,0.84,1.0, 0.84,0.90,1.20, lean=0.08)),                               # lean wiry tall, thin, slight forward
]
# plus the already-strong ones for context
STRONG=[
 ('child',    make_spec(1.60,0.84,0.74,0.86,0.78,0.72)),
 ('boxer',    make_spec(0.80,1.32,1.04,1.02,0.92,0.86, legspread=1.2)),
 ('judge',    make_spec(0.90,1.28,1.12,1.30,1.12,0.96)),
 ('poet',     make_spec(0.98,0.78,1.02,0.78,0.92,1.22, lean=0.05)),
 ('king',     make_spec(1.04,1.16,1.06,1.02,1.0, 1.18)),
 ('scholar',  make_spec(1.22,0.86,0.96,0.86,0.94,1.02, stoop=0.10)),
]
CAM[0]=Ry(rad(-12)); newimg(1480,1560)
header('ARCHETYPES · ARCHITECTURE REVISION','the middle cluster, rebuilt — each a different body. shuffle them, cover the names: still nameable?')
ALL=MID+STRONG
gcols=[180,440,700,960,1220]; grows=[420,1080]; F_SM=font(8.5)   # rows far enough apart for full-height figures
for i,(name,spec) in enumerate(ALL[:10]):
    ox=gcols[i%5]; oy=grows[i//5]; figure(ox,oy,spec); D.text((ox*SS-46*SS,(oy+250)*SS),caps(name),fill=LBL,font=F_SM)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/archetypes_revised.png'); print('saved archetypes_revised.png')

# ================= A2: TEN NEW PEOPLE (no archetype names) =================
NEW=[
 ('A', make_spec(1.0, 1.30,0.92,0.96,0.90,0.92, legspread=1.25)),   # broad short stocky
 ('B', make_spec(0.92,0.80,1.12,0.80,0.92,1.26, lean=0.04)),        # very tall thin
 ('C', make_spec(1.30,0.88,0.82,0.92,0.86,0.82)),                   # big-headed compact
 ('D', make_spec(0.96,1.04,1.02,1.30,1.10,0.98)),                   # pear / wide-hip
 ('E', make_spec(0.94,1.20,1.08,0.86,0.96,1.14, lean=-0.05)),       # V-taper athletic
 ('F', make_spec(1.0, 0.92,0.96,0.92,0.96,1.0,  lean=0.16, stoop=0.12)), # hunched/curled
 ('G', make_spec(0.86,1.10,0.90,1.12,0.88,0.88)),                   # squat round
 ('H', make_spec(1.08,0.82,1.06,0.80,0.90,1.10, lean=0.06)),        # lanky head-forward
 ('I', make_spec(0.98,1.0, 1.18,1.0, 1.16,1.20)),                   # long-torso monumental
 ('J', make_spec(1.14,0.96,0.78,0.94,0.82,0.80, stoop=0.06)),       # child-adjacent, soft
]
CAM[0]=Ry(rad(-12)); newimg(1480,1560)
header('TEN NEW PEOPLE','no names, no archetypes — ten humans. can a viewer describe each one differently?')
for i,(name,spec) in enumerate(NEW):
    ox=gcols[i%5]; oy=grows[i//5]; figure(ox,oy,spec)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/ten_new_people.png'); print('saved ten_new_people.png')

# ================= A3: FIVE WALKING =================
def walk(spec0,phase):
    """give a standing spec a plain walking stride: fore/back legs, pelvis+shoulder counter-rotate,
    arms swing opposite the legs. phase in [-1,1] = how far through the step."""
    import copy
    s=copy.deepcopy(spec0)
    fore=0.55*phase     # +z forward for the leading foot
    # legs: lead leg forward (knee straighter), trail leg back (knee bent), feet planted on ground
    (a0,k0,b0,r0,_)=s['legs'][0]; (a1,k1,b1,r1,_)=s['legs'][1]
    def shift(a,k,b,dz,bend):
        a=Vv(*a)+Vv(0,0,dz*0.3); k=Vv(*k)+Vv(0,0,dz*0.7+bend*0.1,); b=Vv(*b)+Vv(0,0,dz)
        return (tuple(a),tuple(k),tuple(b))
    la,lk,lb=shift(a0,k0,b0,-fore,abs(phase)); ra,rk,rb=shift(a1,k1,b1,fore,abs(phase))
    s['legs']=[Lg(la,lk,lb,r0,-fore*0.0),Lg(ra,rk,rb,r1,fore*0.0)]
    # arms swing opposite legs (left arm forward when left leg back)
    (s0,e0,w0,ar0)=s['arms'][0]; (s1,e1,w1,ar1)=s['arms'][1]
    def swing(sh,el,wr,dz):
        el=Vv(*el)+Vv(0,0,dz); wr=Vv(*wr)+Vv(0,0,dz*1.7); return (sh,tuple(el),tuple(wr))
    a0s=swing(s0,e0,w0,fore); a1s=swing(s1,e1,w1,-fore)
    s['arms']=[Ar(*a0s,ar0),Ar(*a1s,ar1)]
    return s
CAM[0]=Ry(rad(-58))   # 3/4 so the stride reads in depth
fivespec=[('the youth',make_spec(1.30,0.86,0.90,0.84,0.82,1.05)),
          ('the elder',make_spec(0.96,0.78,0.84,0.84,0.86,0.92, lean=0.16, stoop=0.14)),
          ('the bruiser',make_spec(0.84,1.34,1.0,1.06,0.94,0.86, legspread=1.15)),
          ('the aristocrat',make_spec(1.0,0.92,1.10,0.84,0.94,1.20, lean=-0.04)),
          ('the brooder',make_spec(0.96,1.06,0.94,1.0,0.96,0.96, lean=0.12, stoop=0.10))]
phases=[-0.7,0.5,-0.6,0.6,-0.5]
newimg(1480,1080)
header('FIVE PEOPLE · WALKING','ordinary walking — identity is the same when it moves. the bruiser walking is still the bruiser.')
cols=[205,505,790,1075,1340]
for i,(name,spec) in enumerate(fivespec):
    figure(cols[i],440,walk(spec,phases[i]))
    D.text((cols[i]*SS-62*SS,932*SS),caps(name),fill=LBL,font=F_SM)
img.resize((W,H),Image.LANCZOS).save(f'{OUT}/five_walking.png'); print('saved five_walking.png')
print('done')
