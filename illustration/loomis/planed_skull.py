"""
THE PLANED SKULL  (Sketch 101, 2026-05-30)
Professor's note: face #3 reads FLAT because it's all front-contour with no skull
turning underneath. The cure is the planes-of-the-head drill — draw the head as a
SOLID of flat planes (Loomis / Asaro), skull not features, and TURN it. The "100 heads".

Build: construction-first / 3D-form-first. The head is ONE watertight solid — a stack of
octagonal cross-section rings (crown apex -> cranium -> brow -> cheekbone -> jaw -> chin
-> under-chin point), connected all the way around, so it can never leak a floating
far-side plane. The nose is a small wedge the z-buffer composites in front. Then that one
solid is rotated through yaw & pitch: the same object, every way it turns.
Crisp construction line (NOT the stroke engine — it tapers; wrong tool for geometry).
Flat per-plane NOTAN value (light plane = bare paper, then stepped halftone/under), which
is the planar value the Asaro head teaches — not gaussian mannequin-mush.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = "/sessions/nifty-keen-cerf/mnt/hessentials/illustration/loomis"
W, H, SS = 1000, 1380, 2
PAPER = (237,232,223)
INK   = (44,44,58)
FAINT = (171,168,161)
LABEL = (96,94,90)
# NOTAN steps (flat): light=bare paper, then stepping into shadow (steeper for plane read)
V_LIGHT=np.array(PAPER,float); V_HALF=np.array((205,199,189),float)
V_UNDER=np.array((180,174,164),float); V_DEEP=np.array((156,150,141),float)
CREASE=math.radians(24)   # only break an edge where planes turn more than this (kills latitude stripes)

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rad(d): return math.radians(d)

# ---------------------------------------------------------------- the solid
# coords: x right, y DOWN, z FORWARD (toward viewer). origin between the brows.
# each ring: (y, zf_front, zc_corner, zs_side, zb_backcorner, zbk_back, ax_cornerX, wx_sideX)
APEX = (0,-130,-10)
RINGS = [
 #  y     zf   zc   zs   zb    zbk  ax  wx     # carved profile -> reads as skull, not egg
 (-108,  46,  30,   4, -44,  -60, 50, 66),   # cranium top
 ( -60,  74,  64,   6, -54,  -82, 56, 74),   # forehead  (flat, wide front)
 (  -6,  90,  80,  12, -50,  -88, 60, 78),   # BROW RIDGE (widest, forward)
 (  18,  74,  78,  14, -44,  -84, 60, 77),   # eyes      (sockets recede; corners hold = cheekbone start)
 (  40,  80,  72,  14, -34,  -80, 62, 72),   # CHEEKBONE (forward + out)
 (  80,  78,  58,   8, -16,  -70, 48, 56),   # mouth / muzzle  (jaw narrowing)
 ( 104,  66,  50,  12,  -6,  -58, 40, 44),   # JAW ANGLE (gonion at back corner)
 ( 120,  54,  42,  14,   2,  -44, 20, 22),   # chin block
]
BASE = (0,128,26)

def ring_verts(r):
    y,zf,zc,zs,zb,zbk,ax,wx = r
    return [ (0,y,zf),(ax,y,zc),(wx,y,zs),(ax,y,zb),(0,y,zbk),(-ax,y,zb),(-wx,y,zs),(-ax,y,zc) ]

# family per around-direction index 0..7 (only affects nothing now; value is by light)
def build_faces():
    F=[]  # (list-of-3d-pts, is_nose)
    Rg=[ring_verts(r) for r in RINGS]
    A=[np.array(p,float) for p in [APEX]][0]
    B=np.array(BASE,float)
    # apex cap (top planes)
    for j in range(8):
        F.append(([A, np.array(Rg[0][(j+1)%8],float), np.array(Rg[0][j],float)], False))
    # bands
    for i in range(len(Rg)-1):
        top=Rg[i]; bot=Rg[i+1]
        for j in range(8):
            a=np.array(top[j],float); b=np.array(top[(j+1)%8],float)
            c=np.array(bot[(j+1)%8],float); d=np.array(bot[j],float)
            F.append(([a,b,c,d], False))
    # base cap (under planes)
    last=Rg[-1]
    for j in range(8):
        F.append(([B, np.array(last[j],float), np.array(last[(j+1)%8],float)], False))
    # ---- nose wedge (seated flush on the front plane; composited by the z-buffer)
    nroot=np.array((0,-6,90.)); nbr=np.array((0,28,100.)); ntip=np.array((0,54,112.))
    nwR=np.array((24,60,84.)); nwL=np.array((-24,60,84.)); nbase=np.array((0,62,86.))
    F += [([nroot,nbr,nwR],True),([nroot,nwL,nbr],True),          # ridge / front slabs (upper)
          ([nbr,ntip,nwR],True),([nbr,nwL,ntip],True),            # front slabs (lower)
          ([ntip,nwR,nbase],True),([ntip,nbase,nwL],True)]        # under-nose
    return F

FACES = build_faces()
LIGHT = np.array([-0.42,-0.52,0.74]); LIGHT/=np.linalg.norm(LIGHT)   # upper-left-front (y up = -y)

def newell(poly):
    n=np.zeros(3)
    for i in range(len(poly)):
        a=poly[i]; b=poly[(i+1)%len(poly)]
        n[0]+=(a[1]-b[1])*(a[2]+b[2]); n[1]+=(a[2]-b[2])*(a[0]+b[0]); n[2]+=(a[0]-b[0])*(a[1]+b[1])
    nn=np.linalg.norm(n); return n/nn if nn>1e-9 else n

def notan(s):                      # flat NOTAN steps from light dot
    if s >  0.30: return V_LIGHT
    if s >  0.00: return V_HALF
    if s > -0.30: return V_UNDER
    return V_DEEP

# ---------------------------------------------------------------- z-buffer raster
CANVAS = np.full((H*SS, W*SS, 3), PAPER, float)

def raster_head(cx, cy, sc, yaw, pitch):
    Rm = Ry(rad(yaw)) @ Rx(rad(pitch))
    faces=[]; allx=[]; ally=[]
    for pts,is_nose in FACES:
        rp=[Rm@p for p in pts]; nrm=newell(rp)
        front = nrm[2] > 0.02
        if not front and not is_nose: continue        # cull back (nose kept, then composited by z)
        nf = nrm if nrm[2] >= 0 else -nrm
        col=notan(float(np.dot(nf,LIGHT)))
        sx=[cx+p[0]*sc for p in rp]; sy=[cy+p[1]*sc for p in rp]
        allx+=sx; ally+=sy
        faces.append((rp,nf,col,sx,sy))
    if not faces: return
    pad=3
    x0=max(0,int(min(allx))-pad); y0=max(0,int(min(ally))-pad)
    x1=min(W*SS,int(max(allx))+pad); y1=min(H*SS,int(max(ally))+pad)
    tw,th=x1-x0,y1-y0
    if tw<=0 or th<=0: return
    zbuf=np.full((th,tw),-1e18); fid=np.full((th,tw),-1,int)
    lut=np.zeros((len(faces),3))
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
        upd=mask & (pz>zbuf); zbuf[upd]=pz[upd]; fid[upd]=k
    rgb=np.where(fid[...,None]>=0, lut[np.clip(fid,0,len(faces)-1)], np.array(PAPER,float))
    # CREASE EDGES: draw an edge only where the two planes turn (dihedral>CREASE) or at the
    # silhouette (plane vs background). Smoothly-continuing facet joins are suppressed ->
    # form reads as planes, not as an egg wrapped in latitude lines.
    fn=np.array([f[1] for f in faces]); fnrm=fn[np.clip(fid,0,len(faces)-1)]
    ct=math.cos(CREASE); ed=np.zeros((th,tw),bool)
    def mark(aF,bF,aN,bN,sl):
        diff=aF!=bF; bg=(aF<0)|(bF<0)
        dot=np.sum(aN*bN,axis=-1)
        cr=diff&(bg|(dot<ct)); ed[sl[0]]|=cr; ed[sl[1]]|=cr
    mark(fid[:, :-1],fid[:,1:],fnrm[:, :-1],fnrm[:,1:],(np.s_[:, :-1],np.s_[:,1:]))
    mark(fid[:-1,:],fid[1:,:],fnrm[:-1,:],fnrm[1:,:],(np.s_[:-1,:],np.s_[1:,:]))
    rgb[ed]=np.array(INK,float)
    paint=(fid>=0)|ed
    CANVAS[y0:y1,x0:x1][paint]=rgb[paint]

def label_master(D, cx, cy, sc, yaw, pitch, fsm):
    Rm = Ry(rad(yaw)) @ Rx(rad(pitch))
    def put(p3, txt, dx=0, dy=0):
        p=Rm@np.array(p3,float); D.text((cx+p[0]*sc+dx, cy+p[1]*sc+dy),
                                        ' '.join(txt.upper()), fill=LABEL, font=fsm)
    put((10,-120,-8),'top',  dx=-2,dy=-24)
    put((22,-30,82),'front', dx=8, dy=-34)
    put((76,-6,6),'side',    dx=16,dy=-6)
    put((62,34,40),'cheek',  dx=18,dy=10)
    put((10,128,18),'under', dx=-10,dy=26)

# ---------------------------------------------------------------- sheet
MX,MY,MSC = 300, 320, 1.55
yaws  = [-4,-22,-42,-64,-88, 18]
pitchs= [(-16,'chin up'),(0,'level'),(16,'chin down')]
gx0, gy0, dx, dy, gsc = 120, 700, 150, 218, 0.66

raster_head(MX*SS, MY*SS, MSC*SS, yaw=-26, pitch=-6)
for r,(pt,_) in enumerate(pitchs):
    for c,yw in enumerate(yaws):
        raster_head((gx0+c*dx)*SS, (gy0+r*dy)*SS, gsc*SS, yaw=yw, pitch=pt)

img=Image.fromarray(np.clip(CANVAS,0,255).astype(np.uint8)); D=ImageDraw.Draw(img)
def font(px):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(px*SS))
    except: return ImageFont.load_default()
F_TTL=font(20); F_SM=font(8.5); F_CAP=font(10)
def caps(s): return ' '.join(s.upper())

D.text((46*SS,40*SS), 'THE PLANES OF THE HEAD', fill=INK, font=F_TTL)
D.text((46*SS,74*SS), caps('skull, not features  —  one solid, turned'), fill=LABEL, font=F_CAP)
D.line([(46*SS,100*SS),(954*SS,100*SS)], fill=FAINT, width=max(1,int(1*SS)))

label_master(D, MX*SS, MY*SS, MSC*SS, -26, -6, F_SM)
D.text((560*SS,150*SS), caps('the master head'), fill=LABEL, font=F_CAP)
for i,t in enumerate([
   'top  — the roof of the cranium, rolling back.',
   'front — forehead, the face mask, the centre line.',
   'side  — temple, to ear, to the angle of the jaw.',
   'cheek — the zygomatic; the mask turning to the side.',
   'under — base of the nose, under-chin, under-jaw.',
   '',
   'build the planes first.  features sit ON them.',
]):
    if t: D.text((560*SS,(184+i*26)*SS), t, fill=LABEL, font=F_CAP)
D.line([(46*SS,556*SS),(954*SS,556*SS)], fill=FAINT, width=max(1,int(1*SS)))
D.text((46*SS,572*SS), caps('the hundred heads  —  the same skull, every way it turns'),
       fill=LABEL, font=F_CAP)
for r,(pt,plab) in enumerate(pitchs):
    D.text((40*SS,(gy0-22+r*dy)*SS), caps(plab), fill=LABEL, font=F_SM)

out=img.resize((W,H),Image.LANCZOS)
os.makedirs(OUT,exist_ok=True)
out.save(f'{OUT}/planed_skull.png'); print('done', out.size)
