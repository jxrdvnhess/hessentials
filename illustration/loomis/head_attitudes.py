"""
THE HEAD IN ATTITUDE — FEWER DECISIONS  (Sketch 101, 2026-05-30)
Professor: "You've shown you can BUILD the structure. The next challenge is whether you can
COMMUNICATE it with fewer decisions." The danger now is OVER-FACETING — many small planes
where a few important ones would do. Assignment: take THIS EXACT head (same solid as
asaro_head.py — do not rebuild it), put it in six attitudes (up 30 / down 30 / extreme
profile / extreme 3/4 / slight tilt / severe tilt), and REMOVE lines wherever the form
survives without them. Editing, not adding. Keep the forehead architectural.

Implementation of "remove lines": the crease threshold is raised hard (24deg -> 36deg), so a
seam keeps its line ONLY where two planes genuinely turn; shallow joins drop the line but
keep the value step — the lost-and-found edge a master uses. The mouth's lip rows (tertiary)
are collapsed into one mass. Geometry is otherwise the same verified solid; subtraction is
done by threshold + value, not by re-carving. Adds Rz (head tilt / roll) for the tilts.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT="/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W,H,SS=1000,1240,2
PAPER=(237,232,223); INK=(44,44,58); FAINT=(171,168,161); LABEL=(96,94,90)
V_LIGHT=np.array(PAPER,float); V_HALF=np.array((206,200,190),float)
V_UNDER=np.array((178,172,162),float); V_DEEP=np.array((151,145,136),float)
CREASE=math.radians(36)        # SUBTRACTION: only break a line where planes truly turn

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def rad(d): return math.radians(d)
def A(*p): return np.array(p,float)
def mir(p): return np.array((-p[0],p[1],p[2]),float)

# ---- major mass: watertight ring solid (backing) ----
APEX=(0,-130,-30)
RINGS=[
 (-108,42,28,0,-64,-94,52,66),(-60,58,60,2,-72,-110,58,75),(-6,74,78,10,-68,-114,60,78),
 (18,60,76,14,-60,-104,60,78),(40,64,72,12,-46,-94,64,72),(80,62,54,6,-22,-76,47,55),
 (104,54,48,10,-8,-60,40,44),(120,46,42,13,2,-46,20,22)]
BASE=(0,128,20)
def ring_verts(r):
    y,zf,zc,zs,zb,zbk,ax,wx=r
    return [A(0,y,zf),A(ax,y,zc),A(wx,y,zs),A(ax,y,zb),A(0,y,zbk),A(-ax,y,zb),A(-wx,y,zs),A(-ax,y,zc)]

# ---- secondary masses: connected face-mask (same vertices; MOUTH collapsed to one mass) ----
V={
 'hair_c':(0,-64,64),'hair_o':(60,-52,32),
 'browC_c':(0,-4,90),'browC_r':(42,-4,84),'browC_o':(60,-2,58),
 'browU_c':(0,12,84),'browU_r':(38,12,80),'browU_o':(56,12,56),
 'skMed_r':(18,16,76),'skLat_r':(52,14,58),'skBot_r':(50,32,60),'skMedB_r':(22,34,72),
 'nRoot_c':(0,4,88),'nTip_c':(0,52,108),'nSide_r':(13,34,92),'nWing_r':(22,60,82),'nBase_c':(0,63,86),
 'zygo_r':(60,32,64),'cheekE_r':(67,30,22),'cheekL_r':(44,66,58),'mC_r':(30,82,66),
 'lipB_c':(0,94,80),'lipB_r':(22,93,70),
 'chT_c':(0,104,70),'chT_r':(18,104,60),'ch_c':(0,120,54),'ch_r':(13,118,48),
}
MASK=[
 ['hair_c','hair_o','browC_o','browC_c'],                                   # forehead (calm)
 ['browC_c','browC_r','browU_r','browU_c'], ['browC_r','browC_o','browU_o','browU_r'],  # brow
 ['browU_c','browU_r','skMed_r','nRoot_c'], ['browU_r','browU_o','skLat_r','skMed_r'],  # socket
 ['skMed_r','skLat_r','skBot_r','skMedB_r'],
 ['nRoot_c','nTip_c','nSide_r'], ['nRoot_c','nSide_r','skMed_r'],            # nose
 ['nSide_r','nTip_c','nWing_r'], ['nSide_r','nWing_r','skMedB_r'], ['nTip_c','nWing_r','nBase_c'],
 ['skLat_r','browU_o','cheekE_r','zygo_r'], ['skLat_r','zygo_r','skBot_r'],  # cheek + zygoma
 ['skBot_r','zygo_r','cheekL_r'], ['skMedB_r','skBot_r','cheekL_r'],
 ['skMedB_r','cheekL_r','mC_r','nWing_r'], ['zygo_r','cheekE_r','cheekL_r'],
 ['nBase_c','nWing_r','mC_r','lipB_r'], ['nBase_c','lipB_r','lipB_c'],       # mouth = ONE mass
 ['lipB_c','lipB_r','chT_r','chT_c'], ['chT_c','chT_r','ch_r','ch_c'],       # chin
 ['lipB_r','mC_r','cheekL_r','chT_r'], ['chT_r','cheekL_r','ch_r'],
]
def build_faces():
    F=[]
    Rg=[ring_verts(r) for r in RINGS]; ap=A(*APEX); bs=A(*BASE)
    for j in range(8): F.append(([ap,Rg[0][(j+1)%8],Rg[0][j]],True))
    for i in range(len(Rg)-1):
        t=Rg[i]; b=Rg[i+1]
        for j in range(8): F.append(([t[j],t[(j+1)%8],b[(j+1)%8],b[j]],True))
    for j in range(8): F.append(([bs,Rg[-1][j],Rg[-1][(j+1)%8]],True))
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
    Rm=Rz(rad(roll))@Ry(rad(yaw))@Rx(rad(pitch))
    faces=[]; allx=[]; ally=[]
    for pts,cull in FACES:
        rp=[Rm@p for p in pts]; nrm=newell(rp)
        if cull and nrm[2]<=0.02: continue
        nf=nrm if nrm[2]>=0 else -nrm
        col=notan(float(np.dot(nf,LIGHT)))
        sx=[cx+p[0]*sc for p in rp]; sy=[cy+p[1]*sc for p in rp]
        allx+=sx; ally+=sy; faces.append((rp,nf,col,sx,sy))
    if not faces: return
    pad=3
    x0=max(0,int(min(allx))-pad); y0=max(0,int(min(ally))-pad)
    x1=min(W*SS,int(max(allx))+pad); y1=min(H*SS,int(max(ally))+pad)
    tw,th=x1-x0,y1-y0
    if tw<=0 or th<=0: return
    zbuf=np.full((th,tw),-1e18); fid=np.full((th,tw),-1,int); lut=np.zeros((len(faces),3))
    lx=np.arange(tw)[None,:]+x0; ly=np.arange(th)[:,None]+y0
    pxg=(lx-cx)/sc; pyg=(ly-cy)/sc
    for k,(rp,nrm,col,sx,sy) in enumerate(faces):
        lut[k]=col
        m=Image.new('L',(tw,th),0)
        ImageDraw.Draw(m).polygon([(sx[i]-x0,sy[i]-y0) for i in range(len(sx))],fill=255)
        mask=np.asarray(m)>0
        if not mask.any(): continue
        a,b,c=nrm; P0=rp[0]
        if abs(c)<1e-6: continue
        pz=np.broadcast_to((np.dot(nrm,P0)-a*pxg-b*pyg)/c,(th,tw))
        upd=mask&(pz>zbuf); zbuf[upd]=pz[upd]; fid[upd]=k
    rgb=np.where(fid[...,None]>=0, lut[np.clip(fid,0,len(faces)-1)], np.array(PAPER,float))
    fn=np.array([f[1] for f in faces]); fnrm=fn[np.clip(fid,0,len(faces)-1)]
    ct=math.cos(CREASE); ed=np.zeros((th,tw),bool)
    def mark(aF,bF,aN,bN,sl):
        diff=aF!=bF; bg=(aF<0)|(bF<0); dot=np.sum(aN*bN,axis=-1)
        cr=diff&(bg|(dot<ct)); ed[sl[0]]|=cr; ed[sl[1]]|=cr
    mark(fid[:, :-1],fid[:,1:],fnrm[:, :-1],fnrm[:,1:],(np.s_[:, :-1],np.s_[:,1:]))
    mark(fid[:-1,:],fid[1:,:],fnrm[:-1,:],fnrm[1:,:],(np.s_[:-1,:],np.s_[1:,:]))
    rgb[ed]=np.array(INK,float)
    paint=(fid>=0)|ed
    CANVAS[y0:y1,x0:x1][paint]=rgb[paint]

# ---- sheet: the same head, six attitudes ----
ATT=[
 ('looking up · 30°',   dict(yaw=-12,pitch=-30,roll=0)),
 ('extreme 3/4',        dict(yaw=-54,pitch=-4, roll=0)),
 ('extreme profile',    dict(yaw=-88,pitch=0,  roll=0)),
 ('looking down · 30°', dict(yaw=-14,pitch=30, roll=0)),
 ('slight tilt',        dict(yaw=-22,pitch=-6, roll=12)),
 ('severe tilt',        dict(yaw=-34,pitch=8,  roll=28)),
]
cols=[206,500,794]; rows=[440,900]; SCALE=1.16
for i,(name,rot) in enumerate(ATT):
    cx=cols[i%3]; cy=rows[i//3]
    raster_head(cx*SS,cy*SS,SCALE*SS,**rot)

img=Image.fromarray(np.clip(CANVAS,0,255).astype(np.uint8)); D=ImageDraw.Draw(img)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(9); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())

D.text((46*SS,40*SS),'THE HEAD IN ATTITUDE',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('fewer decisions — a line only where the form needs it'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(954*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))
for i,(name,rot) in enumerate(ATT):
    cx=cols[i%3]; cy=rows[i//3]
    D.text((cx*SS-58*SS,(cy+150)*SS),caps(name),fill=LABEL,font=F_SM)
D.line([(46*SS,1150*SS),(954*SS,1150*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,1166*SS),caps('the test: erase half the lines and the head gets stronger — brow, zygoma, side, nose survive'),
       fill=LABEL,font=F_CAP)

out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/head_attitudes.png'); print('done',out.size)
