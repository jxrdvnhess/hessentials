"""
STRAIGHT-ON MASCULINE LOOMIS HEAD — going for mastery.
Fixing the soft/abstract drift: SQUARE wide angular jaw (near cheekbone width,
broad chin), heavy STRAIGHT brows, deep-set eyes under a real brow ridge, a strong
nose with planes, a firm wide mouth, clear plane structure, BOLD confident line,
and light/form massing so it reads SOLID. Believable short cut (value-mass hair).
Light from the upper-left. Target = the reference male faces.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=940,1180
PAPER=np.array([237,232,223],float); INK_SH=np.array([52,52,66],float)
CX=470
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
    cx=CX; S=[]
    def a(c,w,lead=0.16,tail=0.22,swell=0.34,sm=0.56,cs=False,ce=False):
        S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # CONTOUR — WIDE square male jaw that stays near cheekbone width, then a BROAD flat chin
    a([(cx-118,316),(cx-152,374),(cx-156,456),(cx-154,528),(cx-140,594),(cx-104,652),(cx-60,694),(cx-38,712)],4.4,lead=0.18,tail=0.16,swell=0.3)
    a([(cx-38,712),(cx,720),(cx+38,712)],4.2,lead=0.22,tail=0.22,swell=0.26)                # broad flat chin
    a([(cx+38,712),(cx+60,694),(cx+104,652),(cx+140,594),(cx+154,528),(cx+156,456),(cx+152,374),(cx+118,316)],4.4,lead=0.16,tail=0.18,swell=0.3)
    # jaw-angle accents (the gonial corner — masculine, defined)
    a([(cx-156,520),(cx-148,580),(cx-114,646)],2.2,lead=0.34,tail=0.34,swell=0.14)
    a([(cx+156,520),(cx+148,580),(cx+114,646)],2.2,lead=0.34,tail=0.34,swell=0.14)
    # PLANE-BREAK down the side of the face (front-to-side) + cheekbone (zygomatic)
    a([(cx-108,336),(cx-116,452),(cx-96,520)],1.3,lead=0.4,tail=0.4,swell=0.1)
    a([(cx+108,336),(cx+116,452),(cx+96,520)],1.3,lead=0.4,tail=0.4,swell=0.1)
    a([(cx-118,470),(cx-86,492),(cx-58,500)],1.4,lead=0.36,tail=0.36,swell=0.12)
    a([(cx+118,470),(cx+86,492),(cx+58,500)],1.4,lead=0.36,tail=0.36,swell=0.12)
    # HAIR — MASSES + VALUE method (block dark/light in render). Here: a soft irregular
    #        top edge, the hairline, GROUPED flow strands following the sweep, a few flyaways.
    a([(cx-118,316),(cx-132,246),(cx-88,210),(cx-30,194),(cx+18,188),(cx+74,202),(cx+126,238),(cx+150,290),(cx+118,316)],2.2,lead=0.2,tail=0.24,swell=0.2)  # soft top edge (light)
    a([(cx-100,316),(cx-78,302),(cx-54,308)],1.6,lead=0.3,tail=0.34,swell=0.12)             # hairline temple L
    a([(cx-46,304),(cx,296),(cx+48,304)],1.6,lead=0.3,tail=0.3,swell=0.12)                  # hairline centre
    a([(cx+54,308),(cx+78,302),(cx+100,316)],1.6,lead=0.34,tail=0.3,swell=0.12)             # hairline temple R
    for q in [((cx-46,300),(cx-30,250),(cx-2,214)),((cx-30,250),(cx+26,228),(cx+88,210)),
              ((cx-8,236),(cx+44,222),(cx+108,212)),((cx-70,294),(cx-30,244),(cx+10,214)),
              ((cx+30,224),(cx+78,216),(cx+126,232))]:
        a(list(q),1.2,lead=0.34,tail=0.36,swell=0.1)                                        # grouped flow strands (sweep up & right)
    for q in [((cx-120,250),(cx-134,238)),((cx-40,192),(cx-44,180)),((cx+42,188),(cx+46,176)),((cx+128,236),(cx+140,228))]:
        a(list(q),1.0,cs=True,ce=True,swell=0.08)                                           # flyaways (broken, past the edge)
    # BROWS — heavy, straight, masculine, low (brow ridge)
    a([(cx-128,418),(cx-78,408),(cx-30,418)],5.6,lead=0.1,tail=0.18,swell=0.5)
    a([(cx+30,418),(cx+78,408),(cx+128,418)],5.6,lead=0.1,tail=0.18,swell=0.5)
    # EYES — OPEN, deep-set under the ridge; almond; iris disc with sclera; lid thickness
    for s in (-1,1):
        ex=cx+s*72
        a([(ex-34,446),(ex-4,438),(ex+32,444)],3.2,lead=0.14,tail=0.24,swell=0.34)          # upper lid (arched up = open)
        a([(ex+6,440),(ex+26,442),(ex+32,444)],1.5,lead=0.34,tail=0.3,swell=0.12)           # upper-lid thickness
        a([(ex-30,470),(ex+2,475),(ex+28,468)],1.6,lead=0.32,tail=0.34,swell=0.14)          # lower lid (dropped = open)
        a([(ex-11,447),(ex,441),(ex+11,447)],1.6,lead=0.3,tail=0.3,swell=0.12)              # iris top (tucked under lid)
        a([(ex-11,447),(ex,461),(ex+11,447)],1.8,lead=0.3,tail=0.3,swell=0.12)              # iris bottom (sclera shows beside it)
        a([(ex-4,451),(ex+4,451)],2.6,cs=True,ce=True,swell=0.1)                            # pupil
        a([(ex-35,449),(ex-44,455)],1.5,cs=True,ce=True,swell=0.12)                         # tear duct
    # NOSE — strong straight bridge + ball + wings + nostrils (set low)
    a([(cx-16,420),(cx-18,520),(cx-30,552)],2.2,lead=0.24,tail=0.36,swell=0.16)             # L bridge
    a([(cx+16,420),(cx+18,520),(cx+30,552)],1.8,lead=0.28,tail=0.38,swell=0.14)             # R bridge (lit, lighter)
    a([(cx-30,552),(cx-10,564),(cx+10,564),(cx+30,552)],2.2,lead=0.24,tail=0.24,swell=0.2)  # ball/base
    a([(cx-30,548),(cx-44,558),(cx-34,572),(cx-14,568)],2.0,lead=0.3,tail=0.32,swell=0.14)  # L wing
    a([(cx+30,548),(cx+44,558),(cx+34,572),(cx+14,568)],2.0,lead=0.3,tail=0.32,swell=0.14)  # R wing
    a([(cx-20,566),(cx-12,572)],2.2,cs=True,ce=True,swell=0.12); a([(cx+20,566),(cx+12,572)],2.2,cs=True,ce=True,swell=0.12)  # nostrils
    # MOUTH — firm, wide; philtrum; cupid's bow; lower lip + a shadow under
    a([(cx-8,580),(cx-9,604)],1.2,lead=0.36,tail=0.36,swell=0.1); a([(cx+8,580),(cx+9,604)],1.2,lead=0.36,tail=0.36,swell=0.1)  # philtrum
    a([(cx-40,616),(cx-18,608),(cx,616),(cx+18,608),(cx+40,616)],2.0,lead=0.3,tail=0.3,swell=0.16) # upper lip (cupid)
    a([(cx-56,628),(cx-20,636),(cx,635),(cx+20,636),(cx+56,626)],3.8,lead=0.1,tail=0.2,swell=0.4)  # seam (firm, wide)
    a([(cx-44,648),(cx,658),(cx+44,646)],2.4,lead=0.3,tail=0.3,swell=0.18)                  # lower lip
    a([(cx-58,629),(cx-66,628)],1.8,cs=True,ce=True,swell=0.12); a([(cx+58,627),(cx+66,626)],1.8,cs=True,ce=True,swell=0.12)   # corners
    # EARS (brow->nose), on the head sides
    a([(cx-150,452),(cx-172,492),(cx-156,548),(cx-142,512)],2.4,lead=0.26,tail=0.3,swell=0.2)
    a([(cx+150,452),(cx+172,492),(cx+156,548),(cx+142,512)],2.4,lead=0.26,tail=0.3,swell=0.2)
    # NECK (thick) + shoulders
    a([(cx-58,704),(cx-72,780),(cx-78,864)],3.0,lead=0.2,tail=0.34,swell=0.24)
    a([(cx+58,704),(cx+72,780),(cx+78,864)],3.0,lead=0.2,tail=0.34,swell=0.24)
    a([(cx-78,864),(cx-180,892),(cx-300,918)],3.2,lead=0.2,tail=0.3,swell=0.24)
    a([(cx+78,864),(cx+180,892),(cx+300,918)],3.2,lead=0.18,tail=0.3,swell=0.26)
    return S

def silhouette():
    cx=CX; im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    d.polygon([(cx-118,316),(cx-152,374),(cx-154,528),(cx-140,594),(cx-104,652),(cx-38,712),(cx,720),(cx+38,712),
               (cx+104,652),(cx+140,594),(cx+154,528),(cx+152,374),(cx+118,316),(cx+118,206),(cx-118,206)],fill=255)
    d.polygon([(cx-118,316),(cx-132,244),(cx-86,208),(cx-30,192),(cx+18,186),(cx+74,200),(cx+126,236),(cx+150,290),(cx+118,316)],fill=255) # hair
    d.polygon([(cx-58,700),(cx+58,700),(cx+78,864),(cx+300,918),(cx-300,918),(cx-78,864)],fill=255)
    return (soft(np.asarray(im,float)/255.0,2)>0.5).astype(float)

def head_shadow():
    cx=CX; ox,oy,a,b=cx,440,162,250
    he=( ((xx-ox)/a)**2 + ((yy-oy)/b)**2 <=1).astype(float); he=soft(he,6)
    # gentle front light from upper-left: terminator down the right-of-centre
    ys=np.array([300,360,420,480,540,610,680,712])
    xs=np.array([cx+98,cx+88,cx+88,cx+94,cx+106,cx+128,cx+150,cx+164])   # more frontal light: both eyes lit, only far cheek turns
    xterm=np.interp(np.arange(H),ys,xs)[:,None]
    shadow=np.clip((xx-xterm)/30.0+0.5,0,1)*he
    core=np.clip(1-np.abs(xx-(xterm+18))/22.0,0,1)*he*(shadow>0.5)
    # under-planes (brow ridge into sockets, nose, lip, jaw, cheek hollow), + temples
    cast=(g2(cx-72,452,22,12,0.4)+g2(cx+72,452,24,13,0.5)        # eye sockets under the ridge
          +g2(cx,500,150,14,0.3)                                # brow-ridge cast band
          +g2(cx+30,548,16,30,0.45,-0.05)                       # right of nose
          +g2(cx,572,26,9,0.5)                                  # under the nose
          +g2(cx,656,46,11,0.4)                                 # under the lower lip
          +g2(cx+96,560,34,80,0.34,0.12)                        # right cheek hollow
          +g2(cx,706,150,38,0.34))                              # under the jaw
    core=np.clip(core+soft(cast,4)*he,0,1)
    refl=soft((((xx-ox)/a)>0.70).astype(float)*he,4)
    return shadow,core,refl

def shade_to_ink(shadow,core,refl,mask,base=0.24):
    h1=stripes(-0.5,6,1.5,1); h2=stripes(0.62,7,1.5,2); h3=stripes(1.5,6,1.4,3)
    half=np.clip((shadow-0.14)/0.34,0,1)
    g=half*base*h1 + np.clip(shadow-0.5,0,1)*0.38*h2 + core*0.46*h3
    return np.clip(g*(1-refl*0.85),0,1)*mask

def render():
    cx=CX; out=np.ones((H,W,3))*PAPER
    mask=silhouette(); sh,co,re=head_shadow()
    g=shade_to_ink(sh,co,re,mask)
    # HAIR VALUE — block DARK & LIGHT for volume (the 7-step method): a mid base, DARK at
    # the roots & shadow side, a bright HIGHLIGHT band along the top sweep, big contrast,
    # hatched along the flow (cross-hatched in the darks). This is what kills the cap look.
    himg=Image.new("L",(W,H),0); ImageDraw.Draw(himg).polygon(
        [(cx-118,316),(cx-132,246),(cx-88,210),(cx-30,194),(cx+18,188),(cx+74,202),(cx+126,238),(cx+150,290),(cx+118,316)],fill=255)
    hmask=(soft(np.asarray(himg,float)/255.0,2)>0.5).astype(float)
    dark=soft(g2(cx-96,308,56,26,0.55)+g2(cx+96,306,56,30,0.6)+g2(cx+98,262,58,64,0.5)+g2(cx-40,302,84,16,0.4),5)  # roots + shadow side
    lightband=soft(g2(cx-18,214,118,20,1.0,-0.12),5)                                                              # gloss highlight (left bare)
    hairval=np.clip(0.42 + dark - lightband*0.95, 0, 1)*hmask
    ghair=hairval*0.5*stripes(-0.62,5,1.6,3) + np.clip(hairval-0.55,0,1)*0.42*stripes(-1.15,5,1.5,4)
    g=np.clip(g + ghair, 0, 1)
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    fim=Image.new("L",(W*SS,H*SS),0); fd=ImageDraw.Draw(fim)
    for s in face_strokes(): stroke(fd,**s)
    fa=np.asarray(fim.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None]) + INK*fa[...,None]
    cl=np.clip(soft(g2(cx-72-4,447,2.2,2.6,1.0)+g2(cx+72-4,447,2.2,2.6,1.0),0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); render().save(f"{OUT}/man_front_master.png"); print("done")
