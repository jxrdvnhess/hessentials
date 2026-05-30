"""
THE ASARO HEAD — SECONDARY MASSES  (Sketch 101, 2026-05-30)
Professor's assignment after the planed-skull page: stay in construction; advance from
MAJOR masses to SECONDARY masses — brow plane, temple plane, eye-socket plane, mouth
cylinder — and bring the nose up from a SYMBOL (a wedge) to a PLANE SYSTEM (bridge / side /
ball / under). Plus two structural fixes: more REAR CRANIAL MASS, and a DECISIVE zygomatic
corner (forehead -> face mask -> ZYGOMA -> side head as FOUR events). No features.

Key change from page I: the face is no longer a flat slab with cards on top. The FRONT is a
single CONNECTED plane-mask (shared vertices: forehead->brow->socket->nose->cheek->mouth->
chin) so the secondary masses ARE the surface. Behind it sits the watertight ring solid as
backing, so a gap or floating far-plane is impossible. Engine unchanged: per-pixel Z-BUFFER,
flat NOTAN value per plane, CREASE edges only where planes truly turn.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = "/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W, H, SS = 1000, 1440, 2
PAPER=(237,232,223); INK=(44,44,58); FAINT=(171,168,161); LABEL=(96,94,90)
V_LIGHT=np.array(PAPER,float); V_HALF=np.array((205,199,189),float)
V_UNDER=np.array((177,171,161),float); V_DEEP=np.array((150,144,135),float)
CREASE=math.radians(24)

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rad(d): return math.radians(d)
def A(*p): return np.array(p,float)
def mir(p): return np.array((-p[0],p[1],p[2]),float)

# ============================== MAJOR MASS: watertight ring solid (BACKING shell) ==========
# front z's pulled back so the connected face-mask always sits proud of this shell.
APEX=(0,-130,-30)
RINGS=[
 #  y     zf   zc   zs   zb    zbk   ax  wx
 (-108,  42,  28,   0, -64,  -94, 52, 66),   # cranium top   (rear mass)
 ( -60,  58,  60,   2, -72, -110, 58, 75),   # forehead      (deep rear cranium)
 (  -6,  74,  78,  10, -68, -114, 60, 78),   # brow line     (widest; rear)
 (  18,  60,  76,  14, -60, -104, 60, 78),   # eyes
 (  40,  64,  72,  12, -46,  -94, 64, 72),   # cheekbone level
 (  80,  62,  54,   6, -22,  -76, 47, 55),   # mouth
 ( 104,  54,  48,  10,  -8,  -60, 40, 44),   # jaw angle
 ( 120,  46,  42,  13,   2,  -46, 20, 22),   # chin
]
BASE=(0,128,20)
def ring_verts(r):
    y,zf,zc,zs,zb,zbk,ax,wx=r
    return [A(0,y,zf),A(ax,y,zc),A(wx,y,zs),A(ax,y,zb),A(0,y,zbk),A(-ax,y,zb),A(-wx,y,zs),A(-ax,y,zc)]

# ============================== SECONDARY MASSES: connected face-mask ======================
# named landmark vertices (right + centre); the left half is the x-mirror.
V = {
 'hair_c':(0,-64,64),'hair_r':(48,-60,46),'hair_o':(60,-52,32),
 'browC_c':(0,-4,90),'browC_r':(42,-4,84),'browC_o':(60,-2,58),    # brow crest (one continuous ridge)
 'browU_c':(0,12,84),'browU_r':(38,12,80),'browU_o':(56,12,56),    # brow under = roof of socket
 'skMed_r':(18,16,76),'skLat_r':(52,14,58),'skBot_r':(50,32,60),'skMedB_r':(22,34,72),  # socket
 'nRoot_c':(0,4,88),'nTip_c':(0,52,108),'nSide_r':(13,34,92),'nWing_r':(22,60,82),'nBase_c':(0,63,86),
 'zygo_r':(60,32,64),'cheekE_r':(67,30,22),'cheekL_r':(44,66,58),'mC_r':(30,82,66),
 'lipT_c':(0,70,82),'lipT_r':(20,71,73),
 'lipB_c':(0,94,80),'lipB_r':(22,93,70),
 'chT_c':(0,104,70),'chT_r':(18,104,60),'ch_c':(0,120,54),'ch_r':(13,118,48),
}
MASK = [
 # forehead: ONE plane per side, spanning centre to temple — only the centre line reads
 ['hair_c','hair_o','browC_o','browC_c'],
 # under-brow: the secondary mass that roofs the socket (goes to shadow under side light)
 ['browC_c','browC_r','browU_r','browU_c'], ['browC_r','browC_o','browU_o','browU_r'],
 # eye socket: one recessed plane per side, framed by brow / nose / cheek
 ['browU_c','browU_r','skMed_r','nRoot_c'], ['browU_r','browU_o','skLat_r','skMed_r'],
 ['skMed_r','skLat_r','skBot_r','skMedB_r'],
 # nose: big bridge/side slabs + under (a plane system, not a wedge symbol)
 ['nRoot_c','nTip_c','nSide_r'], ['nRoot_c','nSide_r','skMed_r'],
 ['nSide_r','nTip_c','nWing_r'], ['nSide_r','nWing_r','skMedB_r'], ['nTip_c','nWing_r','nBase_c'],
 # cheek + zygoma: the decisive front->side corner, as few big planes
 ['skLat_r','browU_o','cheekE_r','zygo_r'], ['skLat_r','zygo_r','skBot_r'],
 ['skBot_r','zygo_r','cheekL_r'], ['skMedB_r','skBot_r','cheekL_r'],
 ['skMedB_r','cheekL_r','mC_r','nWing_r'], ['zygo_r','cheekE_r','cheekL_r'],
 # mouth cylinder: barrel front (no lips)
 ['nBase_c','nWing_r','mC_r','lipT_r'], ['nBase_c','lipT_r','lipT_c'],
 ['lipT_c','lipT_r','lipB_r','lipB_c'], ['mC_r','lipB_r','lipT_r'],
 # chin
 ['lipB_c','lipB_r','chT_r','chT_c'], ['chT_c','chT_r','ch_r','ch_c'],
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
# light from the SIDE (upper-left), not head-on: each secondary mass then shows a lit plane
# AND a shadow plane, so the front reads as 3D masses (value grouping), not a flat mesh.
LIGHT=np.array([-0.68,-0.40,0.62]); LIGHT/=np.linalg.norm(LIGHT)

def newell(poly):
    n=np.zeros(3)
    for i in range(len(poly)):
        a=poly[i]; b=poly[(i+1)%len(poly)]
        n[0]+=(a[1]-b[1])*(a[2]+b[2]); n[1]+=(a[2]-b[2])*(a[0]+b[0]); n[2]+=(a[0]-b[0])*(a[1]+b[1])
    nn=np.linalg.norm(n); return n/nn if nn>1e-9 else n
def notan(s):
    if s> 0.30: return V_LIGHT
    if s> 0.00: return V_HALF
    if s>-0.30: return V_UNDER
    return V_DEEP

CANVAS=np.full((H*SS,W*SS,3),PAPER,float)
def raster_head(cx,cy,sc,yaw,pitch):
    Rm=Ry(rad(yaw))@Rx(rad(pitch))
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

# ============================== sheet =====================================================
MX,MY,MSC=300,330,1.66
yaws=[-4,-22,-44,-66,-90,18]
pitchs=[(-16,'chin up'),(0,'level'),(16,'chin down')]
gx0,gy0,dx,dy,gsc=120,748,150,224,0.66

raster_head(MX*SS,MY*SS,MSC*SS,yaw=-28,pitch=-6)
for r,(pt,_) in enumerate(pitchs):
    for c,yw in enumerate(yaws):
        raster_head((gx0+c*dx)*SS,(gy0+r*dy)*SS,gsc*SS,yaw=yw,pitch=pt)

img=Image.fromarray(np.clip(CANVAS,0,255).astype(np.uint8)); D=ImageDraw.Draw(img)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())

D.text((46*SS,40*SS),'THE ASARO HEAD  ·  SECONDARY MASSES',fill=INK,font=F_TTL)
D.text((46*SS,74*SS),caps('brow · temple · socket · zygoma · mouth — still no features'),fill=LABEL,font=F_CAP)
D.line([(46*SS,100*SS),(954*SS,100*SS)],fill=FAINT,width=max(1,int(1*SS)))

Rm0=Ry(rad(-28))@Rx(rad(-6))
def label(p3,txt,dx=0,dy=0):
    p=Rm0@A(*p3); D.text((MX*SS+p[0]*MSC*SS+dx,MY*SS+p[1]*MSC*SS+dy),caps(txt),fill=LABEL,font=F_SM)
label((6,-118,-30),'cranial mass',dx=-150,dy=-10)
label((20,-1,97),'brow',dx=-4,dy=-30)
label((58,-30,58),'temple',dx=12,dy=-12)
label((36,20,60),'socket',dx=-6,dy=-4)
label((60,34,40),'zygoma',dx=14,dy=8)
label((0,52,112),'nose',dx=18,dy=14)
label((0,86,84),'mouth cylinder',dx=16,dy=22)

D.text((560*SS,150*SS),caps('the four events'),fill=LABEL,font=F_CAP)
for i,t in enumerate([
   'forehead  →  the flat front of the brow.',
   'face mask  →  it turns down at the brow ridge.',
   'zygoma  →  the cheekbone: the decisive corner.',
   'side head  →  temple, ear, the angle of the jaw.',
   '',
   'the front is one continuous plane-mask now —',
   'the secondary masses ARE the surface, not cards:',
   'brow rolls to an under-plane roofing the socket;',
   'the socket recedes; the mouth is a barrel, not lips;',
   'the nose is planes — bridge, side, ball, under.',
   '',
   'no eyes. no lips. no hair.  stay in the solid.',
]):
    if t: D.text((560*SS,(184+i*25)*SS),t,fill=LABEL,font=F_CAP)
D.line([(46*SS,600*SS),(954*SS,600*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((46*SS,616*SS),caps('the same head, turned — the secondary masses must survive every angle'),fill=LABEL,font=F_CAP)
for r,(pt,plab) in enumerate(pitchs):
    D.text((40*SS,(gy0-22+r*dy)*SS),caps(plab),fill=LABEL,font=F_SM)

out=img.resize((W,H),Image.LANCZOS); os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/asaro_head.png'); print('done',out.size)
