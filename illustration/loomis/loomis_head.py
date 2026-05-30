"""
LOOMIS HEAD — the 13 steps, then a clean pen-and-ink finish (target = the 4-faces
ink reference: confident contour, swept hair in flowing strokes, defined male
features, selective hatching on the shadow planes only).

Proportion scheme (front): top 160, hairline 280, brow 400, nose-base 520,
chin 640 -> three equal thirds (forehead/nose/mouth-chin) below a hairline placed
midway between brow and crown. Eyes just below the brow at the head's center,
one eye-width apart. Ears brow->nose. Light from the upper-left; shadow = right.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=1240,860
PAPER=np.array([237,232,223],float); FAINT=120
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d

# ---------- CONSTRUCTION (the 13 steps, faint) ----------
def construction(d, cx):
    def L(a,b,w=1.3,c=FAINT): d.line([(a[0]*SS,a[1]*SS),(b[0]*SS,b[1]*SS)],fill=c,width=int(w*SS))
    def C(c,r,w=1.3,col=FAINT): d.ellipse([(c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS],outline=col,width=int(w*SS))
    R=160; cyb=320
    C((cx,cyb),R)                                   # 1 ball (cranium)
    L((cx,cyb-R),(cx,640)); L((cx-R,cyb),(cx+R,cyb))# 2 middle + brow guideline (brow at ball center here)
    # 3 flattened side planes (~2/3 R) as vertical chords
    L((cx-int(R*0.78),cyb-120),(cx-int(R*0.78),cyb+120)); L((cx+int(R*0.78),cyb-120),(cx+int(R*0.78),cyb+120))
    # 4 the cross (brow line + middle), already crossed at (cx,320)... use brow=400
    L((cx-R,400),(cx+R,400)); L((cx,200),(cx,640))
    # 5 thirds: hairline / nose / chin
    for y in (280,400,520,640): L((cx-150,y),(cx+150,y),1.1)
    # 6 ears box (lower-back quadrant of side planes), brow->nose
    L((cx-150,400),(cx-150,520)); L((cx+150,400),(cx+150,520))
    # 7 jaw converging to chin
    L((cx-150,430),(cx-110,560)); L((cx-110,560),(cx,648)); L((cx+150,430),(cx+110,560)); L((cx+110,560),(cx,648))
    # 8 plane-break (rhythm) lines forehead/cheeks
    L((cx-96,300),(cx-104,470),1.1); L((cx+96,300),(cx+104,470),1.1)
    # eyes sockets + nose base marks (5)
    C((cx-56,420),34,1.1); C((cx+56,420),34,1.1)
    L((cx-28,520),(cx+28,520),1.1)

# ---------- FINISHED FACE (clean ink) ----------
def face_strokes(cx):
    S=[]
    def a(ctrl,w,lead=0.16,tail=0.22,swell=0.34,sm=0.6,cs=False,ce=False):
        S.append(dict(ctrl=[(x,y) for x,y in ctrl],w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # contour: temple -> cheekbone -> jaw -> chin (square male). lit-left a touch lighter.
    a([(cx-150,300),(cx-156,392),(cx-150,452),(cx-128,536),(cx-86,604),(cx-30,642),(cx,648)],3.0,lead=0.24,tail=0.18,swell=0.3)
    a([(cx,648),(cx+30,642),(cx+86,604),(cx+130,536),(cx+152,452),(cx+158,392),(cx+150,300)],3.8,swell=0.32)
    # hair: swept male cut — silhouette + flowing strokes, parted to our left
    a([(cx-150,300),(cx-160,232),(cx-120,184),(cx-40,160),(cx+40,158),(cx+126,184),(cx+162,250),(cx+150,300)],3.6,swell=0.4)
    a([(cx-110,300),(cx-86,236),(cx-30,210)],2.2,lead=0.3,tail=0.3,swell=0.2)        # hairline sweep
    a([(cx+8,206),(cx+70,214),(cx+120,256)],2.2,lead=0.3,tail=0.3,swell=0.2)
    for x0,x1,x2 in [(-118,-96,-84),(-86,-62,-48),(-52,-28,-16),(-14,6,14),(34,52,62),(70,90,98),(110,126,132)]:
        a([(cx+x0,190),(cx+x1,232),(cx+x2,292)],1.7,lead=0.34,tail=0.34,swell=0.18)   # flow strokes (fuller)
    a([(cx-150,300),(cx-150,250),(cx-110,206)],2.0,lead=0.3,tail=0.3,swell=0.18)       # extra mass left
    a([(cx+150,300),(cx+156,252),(cx+120,206)],2.0,lead=0.3,tail=0.3,swell=0.18)       # extra mass right
    # brows (heavy, masculine, slight asymmetry)
    a([(cx-90,392),(cx-50,380),(cx-16,392)],4.8,lead=0.12,tail=0.22,swell=0.44)
    a([(cx+14,390),(cx+52,379),(cx+92,393)],4.8,lead=0.12,tail=0.22,swell=0.44)
    # eyes: upper lid (strong), lower lid (light), iris, corners. one eye-width apart.
    for s in (-1,1):
        ex=cx+s*56
        a([(ex-30,418),(ex,426),(ex+30,417)],3.2,lead=0.16,tail=0.26,swell=0.3)       # upper lid
        a([(ex-26,432),(ex,436),(ex+24,431)],1.6,lead=0.32,tail=0.34,swell=0.16)      # lower lid
        a([(ex-9,424),(ex,432),(ex+9,424)],2.2,lead=0.3,tail=0.3,swell=0.18)          # iris top
        a([(ex-31,420),(ex-37,425)],1.5,cs=True,ce=True,swell=0.14)                   # tear duct
    # nose: bridge -> ball -> sides -> nostrils
    a([(cx-12,398),(cx-16,498),(cx-26,512)],2.0,lead=0.26,tail=0.36,swell=0.18)        # bridge (near edge)
    a([(cx-26,512),(cx,522),(cx+26,510)],2.4,lead=0.26,tail=0.3,swell=0.22)            # ball/base
    a([(cx-26,506),(cx-34,514),(cx-24,522)],2.2,lead=0.3,tail=0.34,swell=0.18)         # L nostril wing
    a([(cx+26,506),(cx+34,514),(cx+24,522)],2.2,lead=0.3,tail=0.34,swell=0.18)         # R nostril wing
    # mouth: lower third in thirds -> philtrum/lips/chin. seam strongest.
    a([(cx-42,582),(cx,590),(cx+42,580)],3.6,lead=0.14,tail=0.22,swell=0.36)           # seam
    a([(cx-30,572),(cx-12,566),(cx,572),(cx+12,566),(cx+30,572)],1.8,lead=0.3,tail=0.3,swell=0.16)  # upper lip (cupid)
    a([(cx-30,598),(cx,606),(cx+30,596)],2.2,lead=0.3,tail=0.3,swell=0.18)             # lower lip
    a([(cx-44,583),(cx-50,582)],1.8,cs=True,ce=True,swell=0.14); a([(cx+44,581),(cx+50,580)],1.8,cs=True,ce=True,swell=0.14)
    # ears (brow->nose), shadow-side fuller
    a([(cx-150,408),(cx-168,448),(cx-150,512),(cx-138,470)],2.4,lead=0.26,tail=0.3,swell=0.22)
    a([(cx+150,408),(cx+170,448),(cx+150,512),(cx+138,470)],2.6,lead=0.24,tail=0.3,swell=0.24)
    # neck + shoulders
    a([(cx-46,648),(cx-58,720),(cx-66,800)],2.6,lead=0.2,tail=0.34,swell=0.22)
    a([(cx+50,648),(cx+62,720),(cx+72,800)],2.8,lead=0.2,tail=0.34,swell=0.24)
    a([(cx-66,800),(cx-150,824)],2.4,lead=0.24,tail=0.3,swell=0.2); a([(cx+72,800),(cx+170,824)],2.6,lead=0.22,tail=0.3,swell=0.22)
    return S

def silhouette(cx):
    """filled head+hair+neck mask, to clip hatching inside the form."""
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.ellipse([cx-168,180,cx+168,540],fill=255)                    # head mass
    d.polygon([(cx-160,300),(cx-160,232),(cx-120,184),(cx-40,158),(cx+40,156),
               (cx+128,184),(cx+164,250),(cx+150,300)],fill=255)   # hair
    d.polygon([(cx-150,460),(cx-128,540),(cx-86,606),(cx,650),(cx+88,606),(cx+132,540),(cx+154,460)],fill=255) # jaw
    d.polygon([(cx-66,640),(cx+66,640),(cx+74,804),(cx+172,828),(cx-152,828),(cx-68,804)],fill=255)  # neck/shoulders
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def hatch_layer(cx, mask):
    sh  = g2(cx+118,468,36,140,0.9,0.12)        # right cheek / side plane
    sh += g2(cx+66,606,58,34,0.8)               # right jaw / under jaw
    sh += g2(cx+22,500,16,66,0.7,-0.05)         # right of nose
    sh += g2(cx,612,44,11,0.6)                  # under lower lip
    sh += g2(cx+66,296,56,40,0.5)               # under hair, shadow-side forehead
    sh += g2(cx+150,470,16,56,0.6)              # behind right ear
    sh += g2(cx+30,792,80,34,0.45)              # under jaw onto neck (shadow side)
    sh=soft(sh,5)*mask                          # CLIP to the silhouette
    ca,sa=np.cos(-0.5),np.sin(-0.5); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.8*soft(np.random.default_rng(1).normal(0,1,(H,W)),3)
    stripes=np.clip(1-np.abs(((vv/6.0+0.5)%1.0)-0.5)*6.0/1.5,0,1)
    return np.clip(sh,0,1)*stripes

def render():
    # construction panel
    cim=Image.new("L",(W*SS,H*SS),0); cd=ImageDraw.Draw(cim); construction(cd,310)
    cga=np.asarray(cim.resize((W,H),Image.LANCZOS),float)/255.0
    # finished face panel
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(900): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    hl=hatch_layer(900, silhouette(900))
    out=np.ones((H,W,3))*PAPER
    out=out*(1-(cga*0.55)[...,None]) + np.array([150,146,138],float)*(cga*0.55)[...,None]   # faint construction
    out=out*(1-(hl*0.5)[...,None]) + np.array(INK,float)*(hl*0.5)[...,None]                  # hatching
    out=out*(1-fa[...,None]) + np.array(INK,float)*fa[...,None]                              # ink line
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)); dd=ImageDraw.Draw(img)
    dd.text((70,36),"LOOMIS CONSTRUCTION — 13 steps",fill=(70,66,64))
    dd.text((760,36),"CLEAN INK FINISH",fill=(70,66,64))
    return img

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/loomis_head.png"); print("done")
