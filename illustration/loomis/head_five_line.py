"""
FIVE HEADS · LINE ONLY  (Sketch 101, 2026-05-30)
Professor: "Value is currently helping you communicate structure — and that's what value is
for. But LINE-ONLY drawings reveal whether you truly understand hierarchy. If the form
survives with outline + five internal lines, you've internalised the lesson." Assignment:
take THIS exact head, five attitudes, NO shading, NO value grouping — line only.

So: the z-buffer/solid is unchanged, but the page renders bare paper + ink edges only. The
SILHOUETTE (outline) is drawn heavier; the few internal CREASE lines are thin and the crease
threshold is high, so only the lines the form cannot lose remain. Two fixes folded in:
 - the up/down labels were INVERTED (verified): +pitch = LOOKING UP (underside toward us),
   -pitch = looking down (cranium toward us). Labels corrected.
 - the up-view gets real COMPRESSION (high pitch + a CLOSER camera) so brow/nose/mouth/chin
   stack accordion-like, per the note that an extreme up-view rarely has room to breathe.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W,H,SS=1240,760,2
PAPER=(237,232,223); INK=(44,44,58); FAINT=(171,168,161); LABEL=(96,94,90)
CREASE=math.radians(54)        # line-only: only the indispensable internal turns
FOC=380.0

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
def build_faces():
    F=[]
    Rg=[ring_verts(r) for r in RINGS]; ap=Av(*APEX); bs=Av(*BASE)
    for j in range(4): F.append(([ap,Rg[0][(2*j+2)%8],Rg[0][2*j+1],Rg[0][2*j]],True))
    for i in range(len(Rg)-1):
        t=Rg[i]; b=Rg[i+1]
        for j in range(8): F.append(([t[j],t[(j+1)%8],b[(j+1)%8],b[j]],True))
    for j in range(4): F.append(([bs,Rg[-1][2*j],Rg[-1][2*j+1],Rg[-1][(2*j+2)%8]],True))
    for keys in MASK:
        pts=[Av(*V[k]) for k in keys]
        F.append((pts,False)); F.append(([mir(p) for p in reversed(pts)],False))
    return F
FACES=build_faces()

def newell(poly):
    n=np.zeros(3)
    for i in range(len(poly)):
        a=poly[i]; b=poly[(i+1)%len(poly)]
        n[0]+=(a[1]-b[1])*(a[2]+b[2]); n[1]+=(a[2]-b[2])*(a[0]+b[0]); n[2]+=(a[0]-b[0])*(a[1]+b[1])
    nn=np.linalg.norm(n); return n/nn if nn>1e-9 else n

def keep_long(mask,minpix):
    """remove 8-connected edge components smaller than minpix (kills floating tick fragments)."""
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
def raster_head(cx,cy,sc,yaw,pitch,roll=0,foc=FOC):
    Rm=Rz(rad(roll))@Ry(rad(yaw))@Rx(rad(pitch)); f=foc
    def proj(p): s=f/(f-p[2]); return (cx+p[0]*sc*s, cy+p[1]*sc*s)
    faces=[]; allx=[]; ally=[]
    for pts,cull in FACES:
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
        G=a*U+b*Vv; den=np.where(np.abs(c-G)<1e-6,1e-6,c-G)
        z=(d-G*f)/den
        upd=mask&(z>zbuf); zbuf[upd]=z[upd]; fid[upd]=k
    fn=np.array([fc[1] for fc in faces]); fnrm=fn[np.clip(fid,0,len(faces)-1)]
    ct=math.cos(CREASE); e_int=np.zeros((th,tw),bool); e_sil=np.zeros((th,tw),bool)
    def mark(aF,bF,aN,bN,s0,s1):
        diff=aF!=bF; bg=(aF<0)|(bF<0); dot=np.sum(aN*bN,axis=-1)
        sil=diff&bg; inr=diff&(~bg)&(dot<ct)
        e_sil[s0]|=sil; e_sil[s1]|=sil; e_int[s0]|=inr; e_int[s1]|=inr
    mark(fid[:, :-1],fid[:,1:],fnrm[:, :-1],fnrm[:,1:],np.s_[:, :-1],np.s_[:,1:])
    mark(fid[:-1,:],fid[1:,:],fnrm[:-1,:],fnrm[1:,:],np.s_[:-1,:],np.s_[1:,:])
    e_int=keep_long(e_int,22)   # drop stray tick fragments; keep the long structural lines
    # heavier outline: dilate silhouette by 1px (in SS space)
    s=e_sil.copy()
    s[:, :-1]|=e_sil[:,1:]; s[:,1:]|=e_sil[:, :-1]; s[:-1,:]|=e_sil[1:,:]; s[1:,:]|=e_sil[:-1,:]
    reg=CANVAS[y0:y1,x0:x1]
    reg[e_int]=np.array(INK,float)
    reg[s]=np.array(INK,float)

# ---- FIVE heads, line only (labels now CORRECT: up = underside) ----
HEADS=[
 ('extreme 3/4',        dict(yaw=-62,pitch=-4, roll=0)),
 ('profile',            dict(yaw=-90,pitch=0,  roll=0)),
 ('looking up · compressed', dict(yaw=-12,pitch=48,roll=0,foc=232)),
 ('tilt · three-quarter',dict(yaw=-46,pitch=6, roll=24)),
 ('extreme tilt',       dict(yaw=-20,pitch=-4, roll=33)),
]
cols=[168,396,624,852,1080]; cy=358; SCALE=1.0
for i,(name,rot) in enumerate(HEADS):
    raster_head(cols[i]*SS,cy*SS,SCALE*SS,**rot)

img=Image.fromarray(np.clip(CANVAS,0,255).astype(np.uint8)); D=ImageDraw.Draw(img)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())
D.text((46*SS,40*SS),'FIVE HEADS  ·  LINE ONLY',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('no value — only the lines the form cannot lose'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(1194*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,rot) in enumerate(HEADS):
    D.text((cols[i]*SS-58*SS,(cy+150)*SS),caps(name),fill=LABEL,font=F_SM)
D.line([(46*SS,672*SS),(1194*SS,672*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,688*SS),caps('outline carries the mass; a few internal lines carry the hierarchy'),fill=LABEL,font=F_CAP)
out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/head_five_line.png'); print('done',out.size)
