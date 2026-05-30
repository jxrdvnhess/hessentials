"""
THE MAN — 3/4 VIEW. Full synthesis on construction: Loomis ball+jaw with the
centerline & feature-lines wrapping the form per the turn; front profile edge
with a projecting nose; cranium/jaw bulk receding back-right; near eye fuller,
far eye compressed; near ear; swept hair mass; mouth shifted toward the front.
Mastered eyes (lid thickness, lid cast shadow, iris+catchlight, tear duct) and
light & form (lit front-left, shadow massed on the far/right + under-planes off
one clean terminator, reflected light, cast falloff, cool shadow).
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=940,1180
PAPER=np.array([237,232,223],float); INK_SH=np.array([50,50,64],float)
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.4*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)

def face_strokes():
    S=[]
    def a(c,w,lead=0.16,tail=0.22,swell=0.32,sm=0.6,cs=False,ce=False):
        S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # FRONT profile edge (left): forehead->brow->bridge->nose TIP->under-nose->lips->chin
    a([(396,162),(360,250),(346,346),(352,388),(336,452),(318,514),(304,556),
       (330,572),(342,590),(338,610),(350,628),(340,652),(354,676),(392,712)],3.4,lead=0.12,tail=0.16,swell=0.32)
    a([(304,556),(330,566),(352,556)],2.2,lead=0.3,tail=0.32,swell=0.18)         # near nostril/base
    a([(322,560),(316,572),(328,580)],1.8,lead=0.34,tail=0.34,swell=0.14)        # near nostril
    # BACK contour: crown -> back of skull -> near cheek/jaw -> chin
    a([(396,162),(482,138),(576,152),(646,218),(672,322),(670,432),(646,520),
       (598,600),(536,668),(456,706),(392,712)],3.9,lead=0.1,tail=0.2,swell=0.36)
    a([(456,706),(420,716),(392,712)],2.4,lead=0.32,tail=0.3,swell=0.2)          # jaw/chin underplane
    # HAIR — swept mass over the cranium (volume above the skull), parted front-left
    a([(396,162),(380,108),(470,84),(580,96),(648,160),(672,250)],3.4,lead=0.2,tail=0.24,swell=0.4)  # hair top silhouette
    a([(360,250),(372,180),(440,150),(520,150)],2.2,lead=0.3,tail=0.3,swell=0.2)        # hairline front
    a([(396,168),(470,150),(560,168),(636,214)],2.0,lead=0.3,tail=0.3,swell=0.18)       # part/crown sweep
    for p in [((404,176),(470,196),(560,214)),((420,200),(500,224),(600,256)),((448,156),(540,168),(626,210))]:
        a(list(p),1.5,lead=0.34,tail=0.34,swell=0.14)                                   # flow clumps curving right
    # BROWS (near fuller, far compressed & a touch higher)
    a([(338,360),(384,348),(424,360)],4.8,lead=0.12,tail=0.22,swell=0.46)               # near brow
    a([(470,356),(508,350),(540,360)],3.8,lead=0.18,tail=0.26,swell=0.4)                # far brow
    # EYES — near (left) fuller, far (right) compressed. lids w/ thickness, iris, duct
    # near eye
    a([(346,392),(386,400),(424,388)],3.0,lead=0.16,tail=0.26,swell=0.32)               # upper lid
    a([(392,390),(414,391),(424,389)],1.5,lead=0.34,tail=0.3,swell=0.14)                # lid thickness
    a([(352,408),(388,414),(420,406)],1.6,lead=0.32,tail=0.34,swell=0.14)               # lower lid
    a([(360,398),(370,392),(382,398)],1.7,lead=0.3,tail=0.3,swell=0.14)                 # iris top
    a([(360,398),(370,408),(382,398)],1.9,lead=0.3,tail=0.3,swell=0.14)                 # iris bottom
    a([(367,402),(373,402)],2.4,cs=True,ce=True,swell=0.1)                              # pupil
    a([(344,394),(336,400)],1.5,cs=True,ce=True,swell=0.12)                             # tear duct
    # far eye (compressed)
    a([(468,388),(500,396),(534,386)],2.6,lead=0.18,tail=0.28,swell=0.3)                # upper lid
    a([(474,402),(500,407),(528,400)],1.4,lead=0.34,tail=0.34,swell=0.12)               # lower lid
    a([(492,394),(500,389),(510,394)],1.5,lead=0.3,tail=0.3,swell=0.12)                 # far iris top
    a([(492,394),(500,402),(510,394)],1.6,lead=0.3,tail=0.3,swell=0.12)                 # far iris bottom
    a([(497,397),(503,397)],2.0,cs=True,ce=True,swell=0.1)                              # far pupil
    # NOSE ridge (front plane edge) from brow to tip
    a([(360,366),(346,460),(312,520)],2.0,lead=0.26,tail=0.36,swell=0.16)
    a([(352,556),(372,566),(388,556)],1.8,lead=0.32,tail=0.34,swell=0.14)               # far wing/base
    # MOUTH — shifted toward the front; far corner recedes up-right
    a([(320,632),(366,640),(432,628)],3.4,lead=0.14,tail=0.22,swell=0.36)               # seam
    a([(330,624),(360,618),(400,622),(428,620)],1.8,lead=0.3,tail=0.3,swell=0.14)       # upper lip
    a([(332,650),(368,658),(420,646)],2.0,lead=0.3,tail=0.3,swell=0.16)                 # lower lip
    a([(318,633),(312,632)],1.8,cs=True,ce=True,swell=0.12)                             # near corner
    # NEAR EAR (right side, on the receding plane)
    a([(602,408),(628,442),(618,500),(600,508)],2.6,lead=0.24,tail=0.3,swell=0.22)      # helix
    a([(606,430),(600,466),(610,488)],1.4,lead=0.34,tail=0.34,swell=0.12)               # antihelix
    # NECK + shoulders (3/4: front of neck from chin, back from nape)
    a([(392,712),(372,784),(386,864)],2.8,lead=0.2,tail=0.34,swell=0.24)                # front neck
    a([(540,668),(560,760),(566,864)],3.0,lead=0.18,tail=0.34,swell=0.26)               # back neck (trapezius)
    a([(386,864),(300,892),(212,918)],3.0,lead=0.2,tail=0.3,swell=0.24)                 # near shoulder
    a([(566,864),(648,892),(740,918)],3.2,lead=0.18,tail=0.3,swell=0.26)                # back shoulder
    a([(212,918),(208,1010)],2.6,lead=0.26,tail=0.34,swell=0.2); a([(740,918),(744,1010)],2.8,lead=0.24,tail=0.34,swell=0.22)
    return S

def silhouette():
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.polygon([(396,162),(360,250),(346,346),(336,452),(304,556),(338,610),(354,676),(392,712),
               (456,706),(536,668),(598,600),(646,520),(670,432),(672,322),(646,218),(576,152),(482,138)],fill=255)
    d.polygon([(396,162),(380,108),(470,84),(580,96),(648,160),(672,250),(648,218),(576,152),(482,138)],fill=255) # hair
    d.polygon([(392,706),(540,668),(566,864),(740,918),(744,1040),(204,1040),(208,918),(386,864)],fill=255)       # neck+shoulders
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def head_shadow():
    # head ovoid for the form, terminator down the centre-right (lit front-left)
    ox,oy,a,b=505,400,180,250
    he=( ((xx-ox)/a)**2 + ((yy-oy)/b)**2 <=1).astype(float); he=soft(he,6)
    ys=np.array([300,360,410,460,520,580,640,700])
    xs=np.array([462,448,442,448,466,498,540,584])   # terminator x per row
    xterm=np.interp(np.arange(H),ys,xs)[:,None]
    shadow=np.clip((xx-xterm)/30.0+0.5,0,1)*he
    core=np.clip(1-np.abs(xx-(xterm+20))/24.0,0,1)*he*(shadow>0.45)
    cast=(g2(352,572,20,7,0.8)+g2(380,650,30,6,0.6)        # under near nostril, under lip
          +g2(370,398,16,10,0.45)+g2(500,400,16,9,0.5)     # eye sockets
          +g2(560,640,60,30,0.6)+g2(520,210,150,16,0.4))   # under far jaw, under hair
    core=np.clip(core+soft(cast,2)*he,0,1)
    refl=soft((((xx-ox)/a)>0.66).astype(float)*he,4)
    return shadow,core,refl

def shade_to_ink(shadow,core,refl,mask,base=0.34):
    h1=stripes(-0.5,6,1.5,1); h2=stripes(0.62,7,1.5,2); h3=stripes(1.5,6,1.4,3)
    half=np.clip((shadow-0.12)/0.33,0,1)
    g=half*base*h1 + np.clip(shadow-0.45,0,1)*0.5*h2 + core*0.55*h3
    g=g*(1-refl*0.85)
    return np.clip(g,0,1)*mask

def render():
    mask=silhouette()
    sh,co,re=head_shadow()
    g=shade_to_ink(sh,co,re,mask)
    # hair shadow (roots/shadow side) + gloss band bare; neck cast crisp-near
    g=np.clip(g + soft(g2(560,200,80,90,0.5)+g2(420,150,120,24,0.4),5)*mask*0.5*stripes(-1.0,5,1.6,5)
              - soft(g2(470,150,110,22,0.8),4), 0,1)
    neck_cast=np.clip(1-(yy-714)/150,0,1)*(yy>714)*g2(480,756,110,80,1.0)
    g=np.clip(g + soft(neck_cast,3)*mask*0.4*stripes(-0.5,6,1.5,7),0,1)
    out=np.ones((H,W,3))*PAPER
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None]) + INK*fa[...,None]
    cl=np.clip(soft(g2(364,400,2.2,2.6,1.0)+g2(495,396,1.8,2.2,1.0),0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/man_threequarter.png"); print("done")
