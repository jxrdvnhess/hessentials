"""
TEN HEADS · WHAT SURVIVES  (Sketch 101, 2026-05-30)
Professor: construction is working; now it's DESIGN JUDGMENT. Three redlines:
 1. The NOSE is winning every argument — reduce a nose crease or two, and STRENGTHEN the
    brow transition. Redistribute authority; don't add. The brow is an equal participant.
 2. The LOOKING-UP head was weakest — the perspective wasn't pushed: tip up and the underside
    should matter, jaw dominate, chin project, brow foreshorten. -> add real PERSPECTIVE.
 3. Assignment: TEN heads, extreme attitudes (up / down / tilt / 3-4), and remove ONE-THIRD
    more lines than feels comfortable. The question being trained: if I remove this line,
    does the form survive?  -> crease threshold pushed to 44deg; value carries the rest.

Same verified solid (ring backing + connected face-mask). Changes: brow dihedral strengthened,
nose pulled back + its flank creases thinned, a focal PERSPECTIVE projection with per-pixel
ray-plane depth (so extreme attitudes foreshorten honestly), and harder subtraction.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W,H,SS=1240,1140,2
PAPER=(237,232,223); INK=(44,44,58); FAINT=(171,168,161); LABEL=(96,94,90)
V_LIGHT=np.array(PAPER,float); V_HALF=np.array((206,200,190),float)
V_UNDER=np.array((177,171,161),float); V_DEEP=np.array((150,144,135),float)
CREASE=math.radians(44)        # remove a third more: a line only where planes truly turn
FOC=380.0                      # camera distance -> perspective (foreshortening on the extremes)

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def A(*p): return np.array(p,float)
def mir(p): return np.array((-p[0],p[1],p[2]),float)

APEX=(0,-130,-30)
RINGS=[
 (-108,42,28,0,-64,-94,52,66),(-60,58,60,2,-72,-110,58,75),(-6,74,78,10,-68,-114,60,78),
 (18,60,76,14,-60,-104,60,78),(40,64,72,12,-46,-94,64,72),(80,62,54,6,-22,-76,47,55),
 (104,54,48,10,-8,-60,40,44),(120,46,42,13,2,-46,20,22)]
BASE=(0,128,20)
def ring_verts(r):
    y,zf,zc,zs,zb,zbk,ax,wx=r
    return [A(0,y,zf),A(ax,y,zc),A(wx,y,zs),A(ax,y,zb),A(0,y,zbk),A(-ax,y,zb),A(-wx,y,zs),A(-ax,y,zc)]

# brow crest pushed FORWARD + under-brow dropped BACK/DOWN -> stronger brow authority.
# nose pulled BACK (tip 108->100) -> stops dominating every read.
V={
 'hair_c':(0,-64,64),'hair_o':(60,-52,32),
 'browC_c':(0,-5,95),'browC_r':(42,-5,89),'browC_o':(60,-2,60),     # crest forward
 'browU_c':(0,15,79),'browU_r':(38,15,75),'browU_o':(56,15,51),     # under dropped/back
 'skBot_r':(50,33,59),'skMedB_r':(22,35,71),
 'nRoot_c':(0,5,86),'nTip_c':(0,52,100),'nSide_r':(13,35,80),'nWing_r':(25,60,74),'nBase_c':(0,63,83),
 'zygo_r':(60,32,64),'cheekE_r':(67,30,22),'cheekL_r':(44,66,58),'mC_r':(30,82,66),
 'lipB_c':(0,94,80),'lipB_r':(22,93,70),
 'chT_c':(0,104,70),'chT_r':(18,104,60),'ch_c':(0,120,54),'ch_r':(13,118,48),
}
MASK=[
 ['hair_c','hair_o','browC_o','browC_c'],
 ['browC_c','browC_r','browU_r','browU_c'], ['browC_r','browC_o','browU_o','browU_r'],
 # socket: ONE recessed plane per side (+ medial tie to nose) — fewer ticks
 ['browU_c','browU_r','skMedB_r','nRoot_c'], ['browU_r','browU_o','skBot_r','skMedB_r'],
 # nose: front slab + one side + under, flanks softened into the cheek
 ['nRoot_c','nTip_c','nSide_r'], ['nSide_r','nTip_c','nWing_r'], ['nTip_c','nWing_r','nBase_c'],
 ['nRoot_c','nSide_r','skMedB_r'], ['nSide_r','nWing_r','skMedB_r'],
 # cheek + zygoma: the decisive corner, few big planes
 ['browU_o','cheekE_r','zygo_r'], ['browU_o','zygo_r','skBot_r'],
 ['skBot_r','zygo_r','cheekL_r'], ['skMedB_r','skBot_r','cheekL_r'],
 ['skMedB_r','cheekL_r','mC_r','nWing_r'], ['zygo_r','cheekE_r','cheekL_r'],
 ['nBase_c','nWing_r','mC_r','lipB_r'], ['nBase_c','lipB_r','lipB_c'],
 ['lipB_c','lipB_r','chT_r','chT_c'], ['chT_c','chT_r','ch_r','ch_c'],
 ['lipB_r','mC_r','cheekL_r','chT_r'], ['chT_r','cheekL_r','ch_r'],
]
def build_faces():
    F=[]
    Rg=[ring_verts(r) for r in RINGS]; ap=A(*APEX); bs=A(*BASE)
    # crown + base caps as 4 larger faces (not 8-fans) -> fewer radiating lines on top/underside
    for j in range(4): F.append(([ap,Rg[0][(2*j+2)%8],Rg[0][2*j+1],Rg[0][2*j]],True))
    for i in range(len(Rg)-1):
        t=Rg[i]; b=Rg[i+1]
        for j in range(8): F.append(([t[j],t[(j+1)%8],b[(j+1)%8],b[j]],True))
    for j in range(4): F.append(([bs,Rg[-1][2*j],Rg[-1][2*j+1],Rg[-1][(2*j+2)%8]],True))
    for keys in MASK:
        pts=[A(*V[k]) for k in keys]
        F.append((pts,False)); F.append(([mir(p) for p in reversed(pts)],False))
    return F
FACES=build_faces()
LIGHT=np.array([-0.68,-0.40,0.62]); LIGHT/=np.linalg.norm(LIGHT)

def newell(poly):
    n=np.zeros(3)
    for i in range(len(poly)):
        a=poly[i]; b=poly[(i+1)%len(poly)]
        n[0]+=(a[1]-b[1])*(a[2]+b[2]); n[1]+=(a[2]-b[2])*(a[0]+b[0]); n[2]+=(a[0]-b[0])*(a[1]+b[1])
    nn=np.linalg.norm(n); return n/nn if nn>1e-9 else n
def notan(s):
    if s>0.30: return V_LIGHT
    if s>0.00: return V_HALF
    if s>-0.30: return V_UNDER
    return V_DEEP

CANVAS=np.full((H*SS,W*SS,3),PAPER,float)
def raster_head(cx,cy,sc,yaw,pitch,roll=0):
    Rm=Rz(rad(roll))@Ry(rad(yaw))@Rx(rad(pitch)); f=FOC      # model units
    def proj(p): s=f/(f-p[2]); return (cx+p[0]*sc*s, cy+p[1]*sc*s)
    faces=[]; allx=[]; ally=[]
    for pts,cull in FACES:
        rp=[Rm@p for p in pts]; nrm=newell(rp)
        if cull and nrm[2]<=0.02: continue
        nf=nrm if nrm[2]>=0 else -nrm
        col=notan(float(np.dot(nf,LIGHT)))
        sxy=[proj(p) for p in rp]; sx=[q[0] for q in sxy]; sy=[q[1] for q in sxy]
        allx+=sx; ally+=sy; faces.append((rp,nf,col,sx,sy))
    if not faces: return
    pad=3
    x0=max(0,int(min(allx))-pad); y0=max(0,int(min(ally))-pad)
    x1=min(W*SS,int(max(allx))+pad); y1=min(H*SS,int(max(ally))+pad)
    tw,th=x1-x0,y1-y0
    if tw<=0 or th<=0: return
    zbuf=np.full((th,tw),-1e18); fid=np.full((th,tw),-1,int); lut=np.zeros((len(faces),3))
    lx=np.arange(tw)[None,:]+x0; ly=np.arange(th)[:,None]+y0
    # per-pixel ray-plane depth under perspective:  x=U(f-z), y=V(f-z)
    U=(lx-cx)/(sc*f); Vv=(ly-cy)/(sc*f)
    for k,(rp,nrm,col,sx,sy) in enumerate(faces):
        lut[k]=col
        m=Image.new('L',(tw,th),0)
        ImageDraw.Draw(m).polygon([(sx[i]-x0,sy[i]-y0) for i in range(len(sx))],fill=255)
        mask=np.asarray(m)>0
        if not mask.any(): continue
        a,b,c=nrm; d=float(np.dot(nrm,rp[0]))         # plane in model units
        G=a*U+b*Vv; den=(c-G)
        den=np.where(np.abs(den)<1e-6,1e-6,den)
        z=(d-G*f)/den                                  # camera z (SS units); larger=nearer
        upd=mask&(z>zbuf); zbuf[upd]=z[upd]; fid[upd]=k
    rgb=np.where(fid[...,None]>=0, lut[np.clip(fid,0,len(faces)-1)], np.array(PAPER,float))
    fn=np.array([f_[1] for f_ in faces]); fnrm=fn[np.clip(fid,0,len(faces)-1)]
    ct=math.cos(CREASE); ed=np.zeros((th,tw),bool)
    def mark(aF,bF,aN,bN,sl):
        diff=aF!=bF; bg=(aF<0)|(bF<0); dot=np.sum(aN*bN,axis=-1)
        cr=diff&(bg|(dot<ct)); ed[sl[0]]|=cr; ed[sl[1]]|=cr
    mark(fid[:, :-1],fid[:,1:],fnrm[:, :-1],fnrm[:,1:],(np.s_[:, :-1],np.s_[:,1:]))
    mark(fid[:-1,:],fid[1:,:],fnrm[:-1,:],fnrm[1:,:],(np.s_[:-1,:],np.s_[1:,:]))
    rgb[ed]=np.array(INK,float)
    paint=(fid>=0)|ed
    CANVAS[y0:y1,x0:x1][paint]=rgb[paint]

# ---- TEN heads: extreme attitudes ----
HEADS=[
 ('extreme up',        dict(yaw=-8, pitch=-44,roll=0)),
 ('up · turned',       dict(yaw=-30,pitch=-40,roll=0)),
 ('extreme 3/4',       dict(yaw=-64,pitch=-4, roll=0)),
 ('3/4 · up',          dict(yaw=-56,pitch=-24,roll=0)),
 ('3/4 · down',        dict(yaw=-56,pitch=26, roll=0)),
 ('extreme down',      dict(yaw=-10,pitch=44, roll=0)),
 ('down · turned',     dict(yaw=-30,pitch=40, roll=0)),
 ('extreme tilt',      dict(yaw=-20,pitch=-4, roll=34)),
 ('tilt · 3/4',        dict(yaw=-44,pitch=6,  roll=26)),
 ('tilt · up',         dict(yaw=-22,pitch=-26,roll=30)),
]
cols=[160,398,636,874,1112]; rows=[400,800]; SCALE=0.92
for i,(name,rot) in enumerate(HEADS):
    raster_head(cols[i%5]*SS,rows[i//5]*SS,SCALE*SS,**rot)

img=Image.fromarray(np.clip(CANVAS,0,255).astype(np.uint8)); D=ImageDraw.Draw(img)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())

D.text((46*SS,40*SS),'TEN HEADS  ·  WHAT SURVIVES',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('extreme attitudes — if the form survives without the line, the line was decoration'),
       fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1194*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,rot) in enumerate(HEADS):
    cx=cols[i%5]; cy=rows[i//5]
    D.text((cx*SS-52*SS,(cy+168)*SS),caps(name),fill=LABEL,font=F_SM)
D.line([(46*SS,1052*SS),(1194*SS,1052*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,1068*SS),caps('brow and nose now share authority — the side head carries the weight'),
       fill=LABEL,font=F_CAP)

out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/head_ten.png'); print('done',out.size)
