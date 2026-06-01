"""
SKETCH 201 · UNIT 1 — THE SILHOUETTE TEST   (2026-05-30)
Course turns: from inventing believable people (101) to reading why THIS body is this body.
Unit 1 question: if I remove every detail, can I still recognize the person?

  A1 FIVE NAMED SILHOUETTES — our own 101 cast (youth/elder/bruiser/aristocrat/brooder)
     reduced to pure black. Each distinctly POSED — silhouette + posture + body rhythm.
     Cover the names: still nameable?  (brand-clean: our cast, never real public figures.)
  A2 TWENTY UNKNOWN SILHOUETTES — twenty ordinary people, no labels, no archetype names.
     Can a viewer describe each one differently?
  A3 SILHOUETTE MEMORY — a reference held for a glance, then drawn from memory. We encode
     this honestly: the recalled figure keeps only the landmarks that survive a glance
     (overall mass, dominant posture, stance) and loses the fine ones. What survived? What vanished?

Engine = the 101 graduation surface (superellipse-swept torso, sloping shoulders, deltoid caps,
limb volumes), here flattened to pure silhouette + a per-figure POSE layer (arms/stance carry identity).
"""
import os, math, copy
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
SS = 2
PAPER=(237,232,223); INK=(33,31,29); GREY=(150,147,140); FAINT=(178,174,166); LBL=(96,94,90)
GHOST=(206,201,192)   # the "vanished" ghost in A3
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
    return [
      (ry0-rry*1.16, rrx*0.34, rrz*0.5, rx0, rz0),
      (ry0-rry*0.92, rrx*1.12, rrz*0.92, rx0, rz0),
      (ry0-rry*0.26, rrx*1.02, rrz*1.05, rx0, rz0),
      (ry0+rry*0.42, rrx*0.80, rrz*0.84, rx0*0.6+px0*0.4, rz0*0.6+pz0*0.4),
      (waistY, max(rrx*0.60,phx*0.54), rrz*0.66, (rx0+px0)/2, (rz0+pz0)/2),
      (peltop+phy*0.38, phx*0.96, phz*0.95, px0, pz0),
      (py0+phy*0.86, phx*0.80, phz*0.82, px0, pz0),
    ]
def torso(ox,oy,spec,nexp=2.6,nseg=58,col=INK):
    nodes=torso_nodes(spec); samples=catmull_nodes(nodes,max(2,nseg//(len(nodes)-1)))
    for i in range(len(samples)-1):
        y0,w0,d0,cx0,cz0=samples[i]; y1,w1,d1,cx1,cz1=samples[i+1]
        fillsil(super_ring(y0,w0,d0,cx0,cz0,nexp)+super_ring(y1,w1,d1,cx1,cz1,nexp),ox,oy,col)
    rry=spec['rib'][1][1]; _,sh_w,sh_d,scx,scz=nodes[1]; sh_y=nodes[1][0]
    for sgn in (-1,1): fillsil(sphere_pts((scx+sgn*sh_w*0.80,sh_y+rry*0.18,scz),rry*0.34),ox,oy,col)
    nk=spec['neck']; fillsil(seg_pts(nk[0],nk[1],nk[2]*1.15,nk[2]*1.0),ox,oy,col); fillsil(ellip_pts(*spec['head']),ox,oy,col)
def foot(b,ra,ox,oy,fwd=0.0,col=INK):
    bb=Vv(*b); fy=(GROUND-bb[1]); toe=bb+Vv(0,fy,0.60+fwd); heel=bb+Vv(0,fy,-0.12+fwd)
    fillsil(seg_pts(bb,(toe+heel)/2,ra*0.9,ra*0.55)+[toe,heel],ox,oy,col)
def limbs(ox,oy,spec,col=INK):
    for L in spec['legs']:
        a,k,b,r=L[0],L[1],L[2],L[3]; rh,rk,ra=r
        fillsil(sphere_pts(a,rh*1.15),ox,oy,col)   # hip cap — welds thigh into pelvis, closes the silhouette notch
        fillsil(seg_pts(a,k,rh,rk),ox,oy,col); fillsil(sphere_pts(k,rk*0.95),ox,oy,col); fillsil(seg_pts(k,b,rk*0.92,ra),ox,oy,col)
        foot(b,ra,ox,oy,L[4] if len(L)>4 else 0.0,col)
    for s,e,w,r in spec['arms']:
        rs,re_,rw=r
        fillsil(seg_pts(s,e,rs*0.74,re_),ox,oy,col); fillsil(sphere_pts(e,re_*0.92),ox,oy,col); fillsil(seg_pts(e,w,re_*0.9,rw),ox,oy,col)
def figure(ox,oy,spec,col=INK,shadow=True):
    if shadow: CV([projP((-1.7,GROUND,0),ox,oy),projP((1.8,GROUND,0),ox,oy)],0.8,FAINT)
    limbs(ox,oy,spec,col); torso(ox,oy,spec,col=col)
def font(px):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        try: return ImageFont.truetype(p,int(px*SS))
        except: pass
    return ImageFont.load_default()
def caps(s): return ' '.join(s.upper())
def header(title,sub):
    F_TTL=font(20); F_CAP=font(10)
    D.text((46*SS,40*SS),title,fill=INK,font=F_TTL); D.text((46*SS,74*SS),caps(sub),fill=LBL,font=F_CAP)
    D.line([(46*SS,100*SS),((W-46)*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
Lg=lambda hip,knee,ankle,r,fwd=0.0:(hip,knee,ankle,r,fwd); Ar=lambda sh,el,wr,r:(sh,el,wr,r)

def make_spec(head_s,rib_w,rib_h,pel_w,pel_h,axis,lean=0.0,stoop=0.0,armspread=1.0,legspread=1.0):
    pelcy=3.45; pelh=0.40*pel_h; ribry=0.86*rib_h; ribcy=pelcy-pelh-0.42*axis-ribry
    headry=0.55*head_s; headcy=ribcy-ribry-(0.34*axis)-headry
    def lz(y): return lean*(pelcy-y)/3.0
    rib=((lz(ribcy),ribcy,0.0),(0.60*rib_w,ribry,0.52*rib_w),pit(8*lean))
    pel=((0.0,pelcy,0.0),(0.50*pel_w,pelh,0.46*pel_w),pit(2*lean))
    head=((lz(headcy)+stoop,headcy,0.0),(0.46*head_s,headry,0.44*head_s),pit(10*lean+18*stoop))
    neck=((lz(ribcy-ribry)+stoop*0.5,ribcy-ribry+0.02,lz(headcy)+stoop),(0.0,headcy+headry,0.0),0.13+0.02*rib_w)
    legtop=pelcy+pelh*0.20; kneeY=pelcy+pelh*0.6+1.62*axis; ankY=min(kneeY+1.55*axis,GROUND-0.05)
    lr=(0.22*max(pel_w,0.8),0.16,0.12)
    lx=0.30*pel_w*legspread
    legs=[Lg((-lx,legtop,0),(-lx,kneeY,0.06),(-lx,ankY,0),lr),
          Lg(( lx,legtop,0),( lx,kneeY,0.06),( lx,ankY,0),lr)]
    sh=ribcy-ribry*0.86; ar=(0.18,0.13,0.10); axw=0.62*rib_w*armspread
    arms=[Ar((-axw,sh+0.05,0),(-axw-0.02,sh+0.95,0.05),(-axw-0.02,sh+1.85,0.05),ar),
          Ar(( axw,sh+0.05,0),( axw+0.02,sh+0.95,0.05),( axw+0.02,sh+1.85,0.05),ar)]
    return dict(head=head,rib=rib,pelvis=pel,neck=neck,legs=legs,arms=arms)

# ---------- POSE LAYER: posture carries identity in silhouette ----------
def _sh(spec, side):  # shoulder point for a side (-1 left, +1 right)
    return Vv(*spec['arms'][0 if side<0 else 1][0])
def set_arm(spec, side, elbow, wrist, r=(0.18,0.13,0.10)):
    i=0 if side<0 else 1; sh=spec['arms'][i][0]
    spec['arms'][i]=Ar(sh, tuple(elbow), tuple(wrist), r)
def pose(spec, kind):
    """rewrite arms/stance so the SILHOUETTE reads the attitude. operates in place, returns spec."""
    s=copy.deepcopy(spec)
    for side in (-1,1):
        sh=_sh(s,side); sx,sy,sz=sh
        if kind=='hands_hips':
            set_arm(s,side,(sx+side*0.12,sy+0.62,0.10),(sx+side*0.02,sy+0.96,0.18))  # elbow flares out, hand to hip -> triangle gap
        elif kind=='arms_crossed':
            set_arm(s,side,(sx+side*0.10,sy+0.78,0.30),(sx-side*0.30,sy+0.92,0.42))   # forearms cross center-front
        elif kind=='hands_pockets':
            set_arm(s,side,(sx+side*0.05,sy+0.85,0.06),(sx-side*0.10,sy+1.20,0.20))    # arms in, hands low+forward
        elif kind=='clasped_low':
            set_arm(s,side,(sx+side*0.02,sy+0.92,0.16),(-side*0.06,sy+1.40,0.30))      # hands meet low front
        elif kind=='lat_spread':
            set_arm(s,side,(sx+side*0.30,sy+0.80,0.05),(sx+side*0.42,sy+1.70,0.05))    # arms held off the body
        elif kind=='one_hip':   # asymmetric: leading arm on hip, other hangs
            if side<0: set_arm(s,side,(sx+0.12,sy+0.62,0.10),(sx+0.02,sy+0.96,0.18))
        # 'hang' = leave default
    return s
def cock_hip(spec, side=1, amt=0.22):
    """shift pelvis/weight to one side: contrapposto read in silhouette."""
    s=copy.deepcopy(spec)
    (pc,pr,prot)=s['pelvis']; pc=(pc[0]+side*amt, pc[1], pc[2]); s['pelvis']=(pc,pr,prot)
    legs=[]
    for j,L in enumerate(s['legs']):
        a,k,b,r,fwd=L; weighted = (a[0]<0)==(side<0)
        a=(a[0]+side*amt, a[1], a[2])
        if not weighted: k=(k[0]+side*amt*0.4,k[1]+0.05,k[2]); b=(b[0]+side*amt*0.7,b[1],b[2])
        legs.append(Lg(a,k,b,r,fwd))
    s['legs']=legs; return s

# ================= A1: FIVE NAMED SILHOUETTES =================
def A1():
    CAM[0]=Ry(rad(-14)); newimg(1480,860)
    header('FIVE NAMED SILHOUETTES','our own cast, pure black — silhouette + posture carries the name. cover the labels: still nameable?')
    cast=[
      ('the youth',    cock_hip(pose(make_spec(1.34,0.88,0.92,0.84,0.82,1.02), 'one_hip'), side=1, amt=0.20)),  # big head, loose, weight cocked
      ('the elder',    pose(make_spec(0.96,0.78,0.84,0.84,0.86,0.90, lean=0.20, stoop=0.18), 'clasped_low')),    # stooped, hands clasped low
      ('the bruiser',  pose(make_spec(0.82,1.40,1.0,1.08,0.94,0.84, legspread=1.45), 'lat_spread')),             # huge shoulders, planted wide, arms off body
      ('the aristocrat',pose(make_spec(1.0,0.90,1.14,0.82,0.94,1.24, lean=-0.06), 'hands_pockets')),             # tall thin, chin up, hands in pockets
      ('the brooder',  pose(make_spec(0.96,1.04,0.94,1.0,0.96,0.96, lean=0.14, stoop=0.14), 'arms_crossed')),    # forward curl, arms crossed, head down
    ]
    cols=[200,505,795,1075,1330]; F_SM=font(8.5)
    for i,(name,spec) in enumerate(cast):
        figure(cols[i],300,spec)
        D.text((cols[i]*SS-70*SS,712*SS),caps(name),fill=LBL,font=F_SM)
    img.resize((W,H),Image.LANCZOS).save(f'{OUT}/sketch201_u1_a1_named.png'); print('saved sketch201_u1_a1_named.png')

# ================= A2: TWENTY UNKNOWN SILHOUETTES =================
def A2():
    CAM[0]=Ry(rad(-14)); newimg(1560,2280)
    header('TWENTY UNKNOWN SILHOUETTES','no names, no archetypes — twenty ordinary people. can a viewer describe each one differently?')
    P=[
     pose(make_spec(1.0, 1.32,0.92,0.96,0.90,0.92, legspread=1.25),'hang'),
     pose(make_spec(0.92,0.80,1.14,0.80,0.92,1.26, lean=0.04),'hands_pockets'),
     cock_hip(pose(make_spec(1.30,0.88,0.82,0.92,0.86,0.82),'one_hip'),1,0.18),
     pose(make_spec(0.96,1.04,1.02,1.32,1.12,0.98),'hands_hips'),
     pose(make_spec(0.94,1.22,1.10,0.86,0.96,1.14, lean=-0.05),'lat_spread'),
     pose(make_spec(1.0, 0.92,0.96,0.92,0.96,1.0, lean=0.18, stoop=0.14),'arms_crossed'),
     pose(make_spec(0.86,1.10,0.90,1.14,0.88,0.86),'clasped_low'),
     pose(make_spec(1.08,0.82,1.06,0.80,0.90,1.12, lean=0.06),'hang'),
     pose(make_spec(0.98,1.0, 1.20,1.0, 1.18,1.20),'hands_hips'),
     cock_hip(pose(make_spec(1.16,0.96,0.78,0.94,0.82,0.80, stoop=0.06),'hang'),-1,0.16),
     pose(make_spec(0.90,1.16,0.98,1.0,0.92,0.88, legspread=1.2),'lat_spread'),
     pose(make_spec(1.02,0.84,1.16,0.82,0.90,1.22, lean=0.05),'clasped_low'),
     pose(make_spec(1.0,1.0,1.0,1.0,1.0,1.0),'hang'),                                   # the median person
     pose(make_spec(0.94,0.78,0.90,0.78,0.90,1.10, lean=0.24, stoop=0.20),'clasped_low'),# very stooped
     pose(make_spec(1.24,1.06,0.86,1.0,0.90,0.84),'hands_hips'),                          # big-headed broad
     cock_hip(pose(make_spec(0.98,0.86,1.10,0.86,0.96,1.18),'one_hip'),1,0.22),           # tall, weight-cocked
     pose(make_spec(0.90,1.30,1.02,1.16,1.0,0.86, legspread=1.3),'arms_crossed'),         # heavy, arms crossed
     pose(make_spec(1.06,0.90,0.94,0.86,0.92,1.0, lean=0.10),'hands_pockets'),
     pose(make_spec(0.96,1.08,1.12,0.90,0.96,1.16, lean=-0.08),'hang'),                   # chest-up tall
     pose(make_spec(1.40,0.82,0.72,0.86,0.78,0.74),'one_hip'),                            # child-scaled
    ]
    cols=[185,455,725,995,1265]; rows=[470,960,1450,1940];
    for i,spec in enumerate(P):
        figure(cols[i%5],rows[i//5],spec)
    img.resize((W,H),Image.LANCZOS).save(f'{OUT}/sketch201_u1_a2_twenty.png'); print('saved sketch201_u1_a2_twenty.png')

# ================= A3: SILHOUETTE MEMORY =================
def A3():
    CAM[0]=Ry(rad(-14)); newimg(1480,900)
    header('SILHOUETTE MEMORY','held for a glance, then drawn from memory — the mind keeps the big truths and drops the fine ones.')
    # the reference: specific, fully posed — a tall stooped figure, weight cocked, one hand on hip
    ref = cock_hip(pose(make_spec(1.04,0.86,1.12,0.92,0.94,1.16, lean=0.06, stoop=0.10),'one_hip'), side=1, amt=0.20)
    # the recalled: keeps only what survives a glance — overall TALL mass, the STOOP, the COCKED weight.
    # loses: exact head size (-> median), the lean nuance, the specific arm-on-hip (-> hangs), the hip-cock precision.
    recalled = pose(make_spec(1.0,0.88,1.10,0.94,0.96,1.14, stoop=0.10),'hang')
    F_MID=font(11); F_SM=font(8.5)
    # left: reference (ghost of the original under the recalled later)
    figure(400,400,ref)
    D.text((400*SS-86*SS,742*SS),caps('the reference'),fill=LBL,font=F_SM)
    # right: recalled, with the reference ghosted behind to show the gap
    figure(1040,400,ref,col=GHOST,shadow=False)   # faint ghost = what was actually there
    figure(1040,400,recalled)                      # solid = what memory returned
    D.text((1040*SS-86*SS,742*SS),caps('from memory'),fill=LBL,font=F_SM)
    # the verdict
    D.line([(740*SS,150*SS),(740*SS,700*SS)],fill=FAINT,width=max(1,int(1*SS)))
    sv=['SURVIVED','overall tall mass','the stoop','the cocked weight']
    vn=['VANISHED','exact head size','the lean','hand on the hip']
    for k,line in enumerate(sv):
        D.text((620*SS,(770+k*22)*SS),line if k else caps(line),fill=(INK if k==0 else LBL),font=(F_SM if k else F_MID))
    for k,line in enumerate(vn):
        D.text((860*SS,(770+k*22)*SS),line if k else caps(line),fill=(INK if k==0 else GREY),font=(F_SM if k else F_MID))
    img.resize((W,H),Image.LANCZOS).save(f'{OUT}/sketch201_u1_a3_memory.png'); print('saved sketch201_u1_a3_memory.png')

if __name__=='__main__':
    A1(); A2(); A3(); print('UNIT 1 done')
