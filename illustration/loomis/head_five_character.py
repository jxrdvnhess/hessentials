"""
FIVE HEADS · FROM IMAGINATION  (Sketch 101, 2026-05-30)
Professor: construction is no longer the bottleneck — it's becoming automatic. The next, much
harder question: "Can you make two correctly-constructed heads FEEL different?" Assignment:
five heads from imagination, same rules (NO value, NO features, NO reference), each a different
AGE, PERSONALITY and ATTITUDE — built from the masses alone: cranial mass, brow, nose, jaw,
silhouette. Character has to come from PROPORTION and SILHOUETTE, not from features.

So the head is now PARAMETRIC: one CHAR dict of knobs (cranium size/width/rear-mass, face
length, jaw width/length, brow projection, nose length/projection, cheekbone width) drives the
same verified solid. Five presets become five people. Line-only renderer from page 6 (heavier
silhouette + thin internal creases + short-edge filter). Pitch sign is correct now
(+pitch = looking up).  [Visual 'weight/leaning' in a tilt is the NEXT lesson, not solved here.]
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W,H,SS=1240,820,2
PAPER=(237,232,223); INK=(44,44,58); FAINT=(171,168,161); LABEL=(96,94,90)
CREASE=math.radians(62); FOC=380.0

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def Av(*p): return np.array(p,float)
def mir(p): return np.array((-p[0],p[1],p[2]),float)

APEX=(0,-130,-30)
RINGS=[
 (-108,42,28,0,-64,-94,52,66),(-60,58,60,2,-72,-110,58,75),(-6,74,78,10,-68,-114,60,78),
 (18,60,76,14,-60,-104,60,78),(40,64,72,12,-46,-94,64,72),(80,62,54,6,-22,-76,47,55),
 (104,54,48,10,-8,-60,40,44),(120,46,42,13,2,-46,20,22)]
BASE=(0,128,20)
def ring_verts(r):
    y,zf,zc,zs,zb,zbk,ax,wx=r
    return [Av(0,y,zf),Av(ax,y,zc),Av(wx,y,zs),Av(ax,y,zb),Av(0,y,zbk),Av(-ax,y,zb),Av(-wx,y,zs),Av(-ax,y,zc)]
V={
 'hair_c':(0,-64,64),'hair_o':(60,-52,32),
 'browC_c':(0,-5,95),'browC_r':(42,-5,89),'browC_o':(60,-2,60),
 'browU_c':(0,15,79),'browU_r':(38,15,75),'browU_o':(56,15,51),
 'skBot_r':(50,33,59),'skMedB_r':(22,35,71),
 'nRoot_c':(0,5,86),'nTip_c':(0,52,100),'nSide_r':(13,35,80),'nWing_r':(25,60,74),'nBase_c':(0,63,83),
 'zygo_r':(60,32,64),'cheekE_r':(67,30,22),'cheekL_r':(44,66,58),'mC_r':(30,82,66),
 'lipB_c':(0,94,80),'lipB_r':(22,93,70),
 'chT_c':(0,104,70),'chT_r':(18,104,60),'ch_c':(0,120,54),'ch_r':(13,118,48),
}
MASK=[
 ['hair_c','hair_o','browC_o','browC_c'],
 ['browC_c','browC_r','browU_r','browU_c'], ['browC_r','browC_o','browU_o','browU_r'],
 ['browU_c','browU_r','skMedB_r','nRoot_c'], ['browU_r','browU_o','skBot_r','skMedB_r'],
 ['nRoot_c','nTip_c','nSide_r'], ['nSide_r','nTip_c','nWing_r'], ['nTip_c','nWing_r','nBase_c'],
 ['nRoot_c','nSide_r','skMedB_r'], ['nSide_r','nWing_r','skMedB_r'],
 ['browU_o','cheekE_r','zygo_r'], ['browU_o','zygo_r','skBot_r'],
 ['skBot_r','zygo_r','cheekL_r'], ['skMedB_r','skBot_r','cheekL_r'],
 ['skMedB_r','cheekL_r','mC_r','nWing_r'], ['zygo_r','cheekE_r','cheekL_r'],
 ['nBase_c','nWing_r','mC_r','lipB_r'], ['nBase_c','lipB_r','lipB_c'],
 ['lipB_c','lipB_r','chT_r','chT_c'], ['chT_c','chT_r','ch_r','ch_c'],
 ['lipB_r','mC_r','cheekL_r','chT_r'], ['chT_r','cheekL_r','ch_r'],
]

def make_faces(ch):
    g=lambda k:ch.get(k,1.0)
    cran_h,cran_w,cran_back=g('cran_h'),g('cran_w'),g('cran_back')
    face_h,jaw_w,jaw_h=g('face_h'),g('jaw_w'),g('jaw_h')
    brow,nose_len,nose_proj,cheek=g('brow'),g('nose_len'),g('nose_proj'),g('cheek')
    def ty(y):
        if y<=-6: return y*cran_h
        yy=-6+(y+6)*face_h
        if y>80: yy+=(jaw_h-1.0)*(y-80)*face_h
        return yy
    def xs(y):
        if y<-6: return cran_w
        if y>60: return jaw_w
        if 25<=y<=45: return cheek
        return 1.0
    nR=ty(5)
    def warpV(name,x,y,z):
        nx=x*xs(y); ny=ty(y); nz=z
        if name.startswith('browC'): nz=z+(brow-1)*16
        if name.startswith('browU'): nz=z-(brow-1)*9; ny+= (brow-1)*4
        if name in ('nTip_c','nWing_r','nBase_c','nSide_r'):
            ny=nR+(ty(y)-nR)*nose_len; nz=z+(nose_proj-1)*18
        return (nx,ny,nz)
    def warpR(r):
        y,zf,zc,zs,zb,zbk,ax,wx=r; sc=xs(y); cb=cran_back if y<30 else 1.0
        return (ty(y),zf,zc,zs,zb*cb,zbk*cb,ax*sc,wx*sc)
    Rg=[ring_verts(warpR(r)) for r in RINGS]
    ap=Av(0,-130*cran_h,APEX[2]*cran_back); bs=Av(0,ty(128),BASE[2])
    Vw={n:Av(*warpV(n,*xyz)) for n,xyz in V.items()}
    F=[]
    for j in range(4): F.append(([ap,Rg[0][(2*j+2)%8],Rg[0][2*j+1],Rg[0][2*j]],True))
    for i in range(len(Rg)-1):
        t=Rg[i]; b=Rg[i+1]
        for j in range(8): F.append(([t[j],t[(j+1)%8],b[(j+1)%8],b[j]],True))
    for j in range(4): F.append(([bs,Rg[-1][2*j],Rg[-1][2*j+1],Rg[-1][(2*j+2)%8]],True))
    for keys in MASK:
        pts=[Vw[k] for k in keys]
        F.append((pts,False)); F.append(([mir(p) for p in reversed(pts)],False))
    return F

def newell(poly):
    n=np.zeros(3)
    for i in range(len(poly)):
        a=poly[i]; b=poly[(i+1)%len(poly)]
        n[0]+=(a[1]-b[1])*(a[2]+b[2]); n[1]+=(a[2]-b[2])*(a[0]+b[0]); n[2]+=(a[0]-b[0])*(a[1]+b[1])
    nn=np.linalg.norm(n); return n/nn if nn>1e-9 else n
def keep_long(mask,minpix):
    coords=set(map(tuple,np.argwhere(mask))); visited=set(); out=mask.copy()
    for start in coords:
        if start in visited: continue
        stack=[start]; comp=[]; visited.add(start)
        while stack:
            y,x=stack.pop(); comp.append((y,x))
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    n=(y+dy,x+dx)
                    if n in coords and n not in visited: visited.add(n); stack.append(n)
        if len(comp)<minpix:
            for y,x in comp: out[y,x]=False
    return out

CANVAS=np.full((H*SS,W*SS,3),PAPER,float)
def raster_head(faces_src,cx,cy,sc,yaw,pitch,roll=0,foc=FOC):
    Rm=Rz(rad(roll))@Ry(rad(yaw))@Rx(rad(pitch)); f=foc
    def proj(p): s=f/(f-p[2]); return (cx+p[0]*sc*s, cy+p[1]*sc*s)
    faces=[]; allx=[]; ally=[]
    for pts,cull in faces_src:
        rp=[Rm@p for p in pts]; nrm=newell(rp)
        if cull and nrm[2]<=0.02: continue
        nf=nrm if nrm[2]>=0 else -nrm
        sxy=[proj(p) for p in rp]; sx=[q[0] for q in sxy]; sy=[q[1] for q in sxy]
        allx+=sx; ally+=sy; faces.append((rp,nf,sx,sy))
    if not faces: return
    pad=4
    x0=max(0,int(min(allx))-pad); y0=max(0,int(min(ally))-pad)
    x1=min(W*SS,int(max(allx))+pad); y1=min(H*SS,int(max(ally))+pad)
    tw,th=x1-x0,y1-y0
    if tw<=0 or th<=0: return
    zbuf=np.full((th,tw),-1e18); fid=np.full((th,tw),-1,int)
    lx=np.arange(tw)[None,:]+x0; ly=np.arange(th)[:,None]+y0
    U=(lx-cx)/(sc*f); Vv=(ly-cy)/(sc*f)
    for k,(rp,nrm,sx,sy) in enumerate(faces):
        m=Image.new('L',(tw,th),0)
        ImageDraw.Draw(m).polygon([(sx[i]-x0,sy[i]-y0) for i in range(len(sx))],fill=255)
        mask=np.asarray(m)>0
        if not mask.any(): continue
        a,b,c=nrm; d=float(np.dot(nrm,rp[0]))
        G=a*U+b*Vv; den=np.where(np.abs(c-G)<1e-6,1e-6,c-G); z=(d-G*f)/den
        upd=mask&(z>zbuf); zbuf[upd]=z[upd]; fid[upd]=k
    fn=np.array([fc[1] for fc in faces]); fnrm=fn[np.clip(fid,0,len(faces)-1)]
    ct=math.cos(CREASE); e_int=np.zeros((th,tw),bool); e_sil=np.zeros((th,tw),bool)
    def mark(aF,bF,aN,bN,s0,s1):
        diff=aF!=bF; bg=(aF<0)|(bF<0); dot=np.sum(aN*bN,axis=-1)
        sil=diff&bg; inr=diff&(~bg)&(dot<ct)
        e_sil[s0]|=sil; e_sil[s1]|=sil; e_int[s0]|=inr; e_int[s1]|=inr
    mark(fid[:, :-1],fid[:,1:],fnrm[:, :-1],fnrm[:,1:],np.s_[:, :-1],np.s_[:,1:])
    mark(fid[:-1,:],fid[1:,:],fnrm[:-1,:],fnrm[1:,:],np.s_[:-1,:],np.s_[1:,:])
    e_int=keep_long(e_int,32)
    s=e_sil.copy()
    s[:, :-1]|=e_sil[:,1:]; s[:,1:]|=e_sil[:, :-1]; s[:-1,:]|=e_sil[1:,:]; s[1:,:]|=e_sil[:-1,:]
    reg=CANVAS[y0:y1,x0:x1]; reg[e_int]=np.array(INK,float); reg[s]=np.array(INK,float)

# ---- five people, built from the masses ----
PEOPLE=[
 ('the youth','open, looking up',
   dict(cran_h=1.04,cran_w=1.10,face_h=0.76,jaw_w=0.82,jaw_h=0.80,brow=0.45,nose_len=0.72,nose_proj=0.72,cheek=0.96),
   dict(yaw=-34,pitch=16,roll=0)),
 ('the elder','bowed, weighed',
   dict(cran_w=0.90,cran_back=1.12,face_h=1.18,jaw_w=0.86,jaw_h=1.04,brow=1.45,nose_len=1.22,nose_proj=1.28,cheek=0.90),
   dict(yaw=-40,pitch=-20,roll=0)),
 ('the bruiser','set, immovable',
   dict(cran_w=1.12,cran_h=0.92,face_h=0.96,jaw_w=1.28,jaw_h=1.0,brow=1.55,nose_len=0.94,nose_proj=1.12,cheek=1.14),
   dict(yaw=-24,pitch=-6,roll=0)),
 ('the aristocrat','aloof, chin up',
   dict(cran_w=0.86,cran_h=1.08,cran_back=1.05,face_h=1.06,jaw_w=0.80,jaw_h=0.90,brow=0.70,nose_len=1.12,nose_proj=1.18,cheek=1.0),
   dict(yaw=-76,pitch=12,roll=0)),
 ('the brooder','leaning, heavy',
   dict(cran_w=1.0,cran_h=0.95,face_h=1.0,jaw_w=1.10,jaw_h=1.0,brow=1.55,nose_len=1.0,nose_proj=1.05,cheek=1.06),
   dict(yaw=-28,pitch=-12,roll=30)),
]
cols=[168,396,624,852,1080]; cy=372; SCALE=1.0
for i,(name,att,ch,rot) in enumerate(PEOPLE):
    raster_head(make_faces(ch),cols[i]*SS,cy*SS,SCALE*SS,**rot)

img=Image.fromarray(np.clip(CANVAS,0,255).astype(np.uint8)); D=ImageDraw.Draw(img)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_IT=font(9); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'FIVE HEADS  ·  FROM IMAGINATION',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('no features — age, character and attitude from the masses alone'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1194*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,att,ch,rot) in enumerate(PEOPLE):
    D.text((cols[i]*SS-54*SS,(cy+162)*SS),caps(name),fill=LABEL,font=F_SM)
    D.text((cols[i]*SS-54*SS,(cy+184)*SS),att,fill=FAINT,font=F_IT)
D.line([(46*SS,724*SS),(1194*SS,724*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,740*SS),caps('same construction, five people — cranium, brow, nose, jaw, silhouette do all the talking'),fill=LABEL,font=F_CAP)
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/head_five_character.png'); print('done',out.size)
