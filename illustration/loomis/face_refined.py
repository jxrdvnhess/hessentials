"""
LOOMIS FRONT FACE — features ADVANCED (study of the feature-detail sheets +
Loomis steps 9-11). Single, larger front face, clean ink.
  EYES: eyeball under lid, upper-lid THICKNESS, lid crease, tear duct, lower-lid
        catch, iris as a partial ellipse with pupil, lash weight, socket shadow.
  NOSE: nasal-bone bridge -> ball -> wings -> nostrils, with the under-plane in shadow.
  MOUTH: philtrum, cupid's-bow upper lip, the seam (overhang shadow), a fuller
        lower lip with a highlight gap and a shadow beneath; corners wider than the wings.
  EARS: helix, antihelix, tragus, lobe.
Light upper-left; shadow planes hatched and clipped to the form.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=940,1180
PAPER=np.array([237,232,223],float)
CX=470
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d

def face_strokes(cx):
    S=[]
    def a(ctrl,w,lead=0.16,tail=0.22,swell=0.34,sm=0.6,cs=False,ce=False):
        S.append(dict(ctrl=ctrl,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # ---- contour (broader, squarer male jaw + defined chin) ----
    a([(cx-150,300),(cx-158,392),(cx-152,456),(cx-138,540),(cx-104,602),(cx-52,640),(cx,650)],3.0,lead=0.24,tail=0.18,swell=0.3)
    a([(cx,650),(cx+52,640),(cx+104,602),(cx+140,540),(cx+154,456),(cx+160,392),(cx+150,300)],3.9,swell=0.32)
    # ---- cheekbone (zygomatic) + front-to-side plane break (subtle) ----
    a([(cx-100,452),(cx-78,474),(cx-58,486)],1.4,lead=0.34,tail=0.34,swell=0.14)
    a([(cx+100,452),(cx+78,474),(cx+58,486)],1.5,lead=0.34,tail=0.34,swell=0.14)
    a([(cx-104,330),(cx-110,440)],1.1,lead=0.4,tail=0.4,swell=0.1)            # L plane break down forehead/cheek
    a([(cx+104,330),(cx+112,440)],1.2,lead=0.4,tail=0.4,swell=0.1)            # R plane break
    # ---- hair as MASSES: parted on our left, swept across to the right; volume
    #      above the skull; clumps with CURVED flow; a bare gloss band kept on top ----
    a([(cx-150,300),(cx-166,224),(cx-110,174),(cx-8,156),(cx+98,176),(cx+166,246),(cx+150,300)],3.6,swell=0.4)  # silhouette (taller=volume)
    a([(cx-78,182),(cx-52,200),(cx-60,250),(cx-98,294)],2.2,lead=0.3,tail=0.3,swell=0.2)     # the part, short side over forehead-L
    a([(cx-72,180),(cx+6,190),(cx+86,206),(cx+150,250)],2.4,lead=0.28,tail=0.3,swell=0.2)    # big sweep clump edge
    a([(cx-58,200),(cx+24,214),(cx+104,240)],1.8,lead=0.32,tail=0.32,swell=0.16)             # mid clump
    a([(cx-44,220),(cx+44,236),(cx+118,270)],1.6,lead=0.34,tail=0.34,swell=0.14)             # lower clump
    a([(cx+40,178),(cx+96,194),(cx+140,234)],1.6,lead=0.34,tail=0.34,swell=0.14)             # upper clump (crown)
    a([(cx-150,300),(cx-128,250),(cx-104,208)],2.0,lead=0.3,tail=0.3,swell=0.16)             # left mass over temple
    a([(cx+150,300),(cx+160,250),(cx+128,212)],2.0,lead=0.3,tail=0.3,swell=0.16)             # right mass
    # ---- brows ----
    a([(cx-92,392),(cx-50,379),(cx-14,392)],4.8,lead=0.12,tail=0.22,swell=0.46)
    a([(cx+14,391),(cx+52,378),(cx+92,393)],4.8,lead=0.12,tail=0.22,swell=0.46)
    # ---- EYES (open, iris set between the lids, gaze present) ----
    for s in (-1,1):
        ex=cx+s*58
        a([(ex-32,414),(ex-2,422),(ex+31,412)],3.0,lead=0.16,tail=0.26,swell=0.32)           # upper lid (higher arch -> open)
        a([(ex+6,414),(ex+26,415),(ex+31,413)],1.6,lead=0.34,tail=0.3,swell=0.14)            # upper-lid THICKNESS
        a([(ex-30,402),(ex-2,408),(ex+28,400)],1.2,lead=0.36,tail=0.36,swell=0.12)           # brow-ridge/lid crease
        a([(ex-28,440),(ex+2,444),(ex+26,438)],1.6,lead=0.32,tail=0.34,swell=0.14)           # lower lid (dropped -> open)
        # iris: a near-circle sitting between the lids, top tucked under the upper lid
        a([(ex-10,420),(ex,415),(ex+10,420)],1.8,lead=0.3,tail=0.3,swell=0.16)               # iris top
        a([(ex-10,420),(ex,434),(ex+10,420)],2.0,lead=0.3,tail=0.3,swell=0.16)               # iris bottom
        a([(ex-4,425),(ex+4,425)],2.6,cs=True,ce=True,swell=0.1)                             # pupil
        a([(ex-33,418),(ex-40,424)],1.5,cs=True,ce=True,swell=0.12)                          # tear duct
    # ---- NOSE (advanced): bridge -> ball -> wings -> nostrils ----
    a([(cx-13,398),(cx-15,470),(cx-22,500)],1.8,lead=0.26,tail=0.36,swell=0.16)              # L nasal-bone side
    a([(cx+13,398),(cx+15,470),(cx+22,500)],1.4,lead=0.3,tail=0.38,swell=0.14)               # R bridge (lighter, lit)
    a([(cx-22,500),(cx-8,512),(cx+8,512),(cx+22,500)],2.0,lead=0.24,tail=0.24,swell=0.2)     # ball of the nose (under arc)
    a([(cx-22,498),(cx-34,508),(cx-26,520),(cx-10,516)],2.0,lead=0.3,tail=0.32,swell=0.16)   # L wing
    a([(cx+22,498),(cx+34,508),(cx+26,520),(cx+10,516)],2.0,lead=0.3,tail=0.32,swell=0.16)   # R wing
    a([(cx-16,514),(cx-10,520)],2.2,cs=True,ce=True,swell=0.14)                              # L nostril
    a([(cx+16,514),(cx+10,520)],2.2,cs=True,ce=True,swell=0.14)                              # R nostril
    # ---- MOUTH (advanced): philtrum, cupid's bow, seam w/ overhang, lower lip + corners ----
    a([(cx-7,524),(cx-8,560)],1.2,lead=0.36,tail=0.36,swell=0.12)                            # philtrum L
    a([(cx+7,524),(cx+8,560)],1.2,lead=0.36,tail=0.36,swell=0.12)                            # philtrum R
    a([(cx-30,572),(cx-14,565),(cx,572),(cx+14,565),(cx+30,572)],1.8,lead=0.3,tail=0.3,swell=0.16)  # upper lip (cupid's bow)
    a([(cx-42,582),(cx-16,589),(cx,588),(cx+16,589),(cx+42,580)],3.4,lead=0.12,tail=0.2,swell=0.36) # seam (slight wave)
    a([(cx-28,600),(cx,608),(cx+28,598)],2.2,lead=0.3,tail=0.3,swell=0.18)                   # lower lip (gap = highlight)
    a([(cx-44,583),(cx-51,582)],1.8,cs=True,ce=True,swell=0.12); a([(cx+44,581),(cx+51,580)],1.8,cs=True,ce=True,swell=0.12)  # corners
    # ---- EARS (advanced): helix, antihelix, tragus, lobe ----
    for s in (-1,1):
        exx=cx+s*150
        a([(exx,408),(exx+s*18,448),(exx,512),(exx-s*6,500)],2.4,lead=0.26,tail=0.3,swell=0.22)  # helix (outer rim)
        a([(exx-s*2,432),(exx+s*6,470),(exx-s*2,492)],1.4,lead=0.34,tail=0.34,swell=0.14)        # antihelix
        a([(exx-s*10,470),(exx-s*16,478)],1.6,cs=True,ce=True,swell=0.12)                        # tragus
        a([(exx+s*2,500),(exx-s*8,512),(exx-s*12,500)],1.6,lead=0.34,tail=0.34,swell=0.14)       # lobe
    # ---- neck + shoulders ----
    a([(cx-46,648),(cx-58,720),(cx-66,820)],2.6,lead=0.2,tail=0.34,swell=0.22)
    a([(cx+50,648),(cx+62,720),(cx+72,820)],2.8,lead=0.2,tail=0.34,swell=0.24)
    a([(cx-66,820),(cx-150,846)],2.4,lead=0.24,tail=0.3,swell=0.2); a([(cx+72,820),(cx+170,846)],2.6,lead=0.22,tail=0.3,swell=0.22)
    return S

def silhouette(cx):
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.ellipse([cx-168,180,cx+168,540],fill=255)
    d.polygon([(cx-160,300),(cx-160,232),(cx-120,184),(cx-40,158),(cx+40,156),(cx+128,184),(cx+164,250),(cx+150,300)],fill=255)
    d.polygon([(cx-150,460),(cx-128,540),(cx-86,606),(cx,650),(cx+88,606),(cx+132,540),(cx+154,460)],fill=255)
    d.polygon([(cx-66,640),(cx+66,640),(cx+74,824),(cx+172,848),(cx-152,848),(cx-68,824)],fill=255)
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def hatch_layer(cx, mask):
    sh  = g2(cx+118,468,36,140,0.85,0.12)       # right cheek / side plane
    sh += g2(cx+66,606,56,34,0.8)               # right jaw
    sh += g2(cx+24,506,14,30,0.7,-0.05)         # right of nose / under ball
    sh += g2(cx,520,26,9,0.6)                   # under the ball of the nose (under-plane)
    sh += g2(cx,604,40,9,0.55)                  # under the lower lip
    sh += g2(cx-44,420,16,14,0.4)+g2(cx+44,420,18,16,0.5)   # eye sockets (inner-upper)
    sh += g2(cx+66,296,52,38,0.45)              # shadow-side forehead under hair
    sh += g2(cx+150,470,15,52,0.55)             # behind right ear
    sh += g2(cx+30,800,76,32,0.45)              # under jaw onto neck
    sh += g2(cx+58,421,30,6,0.6)+g2(cx-58,421,30,6,0.5)    # cast shadow under each upper lid (across the iris)
    sh += g2(cx+82,250,72,84,0.5)+g2(cx-24,286,104,26,0.42) # hair: shadow side + roots under the sweep
    sh = np.clip(sh - g2(cx+12,196,88,18,0.8,-0.06), 0, 2)  # leave a bare GLOSS band on the sweep
    sh=soft(sh,4)*mask
    ca,sa=np.cos(-0.5),np.sin(-0.5); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.6*soft(np.random.default_rng(1).normal(0,1,(H,W)),3)
    stripes=np.clip(1-np.abs(((vv/5.6+0.5)%1.0)-0.5)*5.6/1.4,0,1)
    return np.clip(sh,0,1)*stripes

def render():
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(CX): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    hl=hatch_layer(CX, silhouette(CX))
    out=np.ones((H,W,3))*PAPER
    out=out*(1-(hl*0.5)[...,None]) + np.array(INK,float)*(hl*0.5)[...,None]
    out=out*(1-fa[...,None]) + np.array(INK,float)*fa[...,None]
    # catchlights: tiny paper-bright dots upper-left of each pupil (gaze comes alive)
    cl=g2(CX-58-3,422,2.0,2.4,1.0)+g2(CX+58-3,422,2.0,2.4,1.0)
    cl=np.clip(soft(cl,0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/face_refined.png"); print("done")
