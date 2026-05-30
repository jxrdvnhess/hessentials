"""
FACE #3 (the favourite) — hair rebuilt with the LOOMIS male-hair construction:
build the hair as a DOME outward from the sphere (volume), wider & ANGULAR for a
man (extra volume at crown + side planes, receding at the temples), massed into
3D RIBBON-locks with overlapping strokes; shadow blocked UNDER the locks and at
the TEMPLES (where hair meets face), light kept on TOP of the dome.
"""
import face_generator as fg
import numpy as np
from PIL import Image, ImageDraw
g2,soft,stripes=fg.g2,fg.soft,fg.stripes
W,H,CX=fg.W,fg.H,fg.CX
PAPER,INK_SH=fg.PAPER,fg.INK_SH
stroke,SS,INK=fg.stroke,fg.SS,fg.INK
yy,xx=fg.yy,fg.xx
OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"

P={'seed':7,'ytop':156,'yhair':196,'ybrow':296,'yeye':321,'ynose':419,'ymouth':463,'ychin':533,
   'cheek':113,'jaw':114,'chin':39,'brow_w':5.4,'brow_slant':4,'brow_len':44,'eye_w':25,'eye_sp':51,
   'eye_open':9,'nose_w':33,'bridge':2.0,'mouth_w':34,'lip':6,'hair':2,'hair_h':60,'lw':3.6,'term':106,'shadow':0.16}

# FULLER dome whose sides come down at the temples; ARCED hairline that frames the forehead
_T=[(CX-117,190),(CX-126,140),(CX-92,112),(CX-44,96),(CX+10,90),(CX+62,102),(CX+104,124),(CX+122,150),(CX+114,192)]
DOME=_T+[(CX+86,196),(CX+40,203),(CX,200),(CX-40,203),(CX-86,196)]
# soft lock recesses (centre, angle) — used only as SHADOW between locks, never hard lines
REC=[(CX-46,148,-0.22),(CX+10,142,-0.10),(CX+60,148,0.02)]

def my_hair(a,P):
    cx=CX
    a(_T,2.2,lead=0.2,tail=0.22,swell=0.2)                                        # soft dome edge (light)
    a([(cx-86,196),(cx-40,203),(cx,200),(cx+40,203),(cx+86,196)],1.2,lead=0.3,tail=0.3,swell=0.1)  # arced hairline (light)
    for q in [((cx-44,184),(cx-30,134),(cx-4,104)),((cx-6,180),(cx+26,128),(cx+62,108)),
              ((cx+34,176),(cx+72,128),(cx+106,130)),((cx-74,182),(cx-52,140),(cx-18,110))]:
        a(list(q),1.1,lead=0.34,tail=0.36,swell=0.08)                            # soft swept flow on lock bodies
    a([(cx-113,184),(cx-121,150)],1.3,cs=True,ce=True,swell=0.1)                  # temple recession
    a([(cx+111,184),(cx+120,150)],1.3,cs=True,ce=True,swell=0.1)
    for q in [((cx+8,98),(cx+5,84)),((cx-44,104),(cx-49,92)),((cx+58,108),(cx+63,96))]:
        a(list(q),0.9,cs=True,ce=True,swell=0.06)                                # a few soft flyaways
    return DOME
fg.hair=my_hair

def poly(pts):
    im=Image.new("L",(W,H),0); ImageDraw.Draw(im).polygon([(float(x),float(y)) for x,y in pts],fill=255)
    return np.asarray(im,float)/255.0

def render():
    S,sil,hp=fg.D(P); cx=CX; ye=P['yeye']
    body=np.clip(poly(sil)+poly(hp)+poly([(cx-P['chin']-6,P['ychin']-4),(cx+P['chin']+6,P['ychin']-4),
        (cx+52,P['ychin']+150),(cx+250,P['ychin']+200),(cx-250,P['ychin']+200),(cx-52,P['ychin']+150)]),0,1)
    mask=(soft(body,2)>0.5).astype(float)
    # face light + under-plane accents
    xterm=(cx+P['term'])+(yy-ye)*0.12
    shadow=np.clip((xx-xterm)/28+0.5,0,1)*mask
    half=np.clip((shadow-0.16)/0.34,0,1)
    g=half*P['shadow']*stripes(-0.5,6,1.5,P['seed'])+np.clip(shadow-0.55,0,1)*0.30*stripes(0.6,7,1.5,P['seed']+1)
    g=np.clip(g+soft(g2(cx,P['ynose']+18,P['nose_w'],8,0.34)+g2(cx,P['ymouth']+22,P['mouth_w']*0.8,8,0.3)
        +g2(cx,P['ychin']+10,120,30,0.28)+g2(cx-P['eye_sp'],P['ybrow']+20,P['eye_w'],10,0.26)
        +g2(cx+P['eye_sp'],P['ybrow']+20,P['eye_w'],10,0.3),4)*mask*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)
    # HAIR VALUE — LAYERED locks: DARK in the recesses BETWEEN locks (drawn from DIV) +
    # temples + roots + shadow side; LIGHT on each lock's top (front + crown). Big contrast.
    hmask=soft(poly(hp),5)                                            # FEATHERED edges (soft hairline, no brim)
    rec=sum(g2(rx,ry,9,46,0.5,ra) for (rx,ry,ra) in REC)             # SOFT recesses between locks
    dark=np.clip(soft(rec + g2(cx-104,174,40,28,0.5)+g2(cx+106,172,40,32,0.55)  # + temples
                +g2(cx,190,120,14,0.4)+g2(cx+98,150,48,52,0.45),5),0,1)         # + roots + shadow side
    light=soft(g2(cx-16,110,86,22,1.0,-0.05)+g2(cx+46,116,46,16,0.6),5)         # lights on the lock tops (gloss)
    hairval=np.clip(0.40+dark-light*0.95,0,1)*hmask
    ghair=hairval*0.5*stripes(-0.66,5,1.6,3)+np.clip(hairval-0.52,0,1)*0.40*stripes(-1.2,5,1.5,4)
    g=np.clip(g+ghair,0,1)
    # ===== NECK & SHOULDERS (per the reference): SCM muscles -> sternal PIT, clavicles,
    #       Adam's apple; shadow in the pit, between/under the SCMs, under jaw + clavicles =====
    yc=P['ychin']
    def na(c,w,cs=False,ce=False): S.append(dict(ctrl=c,w=w,lead=0.2,tail=0.3,swell=0.2,smoothing=0.6,cap_start=cs,cap_end=ce))
    na([(cx-66,yc+4),(cx-42,yc+48),(cx-14,yc+98)],2.0)                                  # left SCM
    na([(cx+66,yc+4),(cx+42,yc+48),(cx+14,yc+98)],2.0)                                  # right SCM
    na([(cx-12,yc+96),(cx,yc+105),(cx+12,yc+96)],1.6)                                   # sternal pit (hollow)
    na([(cx-8,yc+38),(cx-6,yc+58)],1.1,cs=True,ce=True); na([(cx+8,yc+38),(cx+6,yc+58)],1.1,cs=True,ce=True)  # Adam's apple
    na([(cx-8,yc+100),(cx-72,yc+108),(cx-142,yc+120)],2.0)                              # left clavicle
    na([(cx+8,yc+100),(cx+72,yc+108),(cx+142,yc+120)],2.0)                              # right clavicle
    ncast=soft(g2(cx,yc+98,14,12,0.85)+g2(cx,yc+72,22,40,0.3)                            # pit + front hollow
              +g2(cx-50,yc+54,15,52,0.3)+g2(cx+52,yc+54,16,52,0.4)                       # sides of the SCMs (R deeper)
              +g2(cx-62,yc+130,74,16,0.34)+g2(cx+62,yc+130,74,16,0.36)                   # under the clavicles
              +g2(cx,yc+12,92,26,0.36),5)*mask                                          # under the jaw (cast)
    g=np.clip(g + ncast*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)
    # CHEEKBONE / JAW plane definition (handsome-masculine, reconstructed not copied)
    g=np.clip(g + soft(g2(cx+96,488,30,56,0.4,0.2)+g2(cx-96,488,26,56,0.26,-0.2)      # cheek hollow under the cheekbone (R deeper)
                       +g2(cx+118,540,30,40,0.3)+g2(cx-118,540,26,40,0.2),5)*mask*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)
    # STUBBLE — a five-o'clock shadow on jaw/chin/upper lip/sideburns (stippling), keeps the lips clear
    beard=soft(g2(cx,512,118,44,1.0)+g2(cx,472,40,11,0.8)+g2(cx-112,476,22,58,0.7)+g2(cx+112,476,22,58,0.7),4)
    beard=beard*(soft(np.asarray(Image.fromarray(((poly(sil))*255).astype(np.uint8)),float)/255.0,2))*(yy<548)
    beard=beard*(1-soft(g2(cx,500,58,18,1.0),3))               # leave the lips/mouth clearer
    stip=(np.random.default_rng(9).random((H,W))<np.clip(beard,0,1)*0.42).astype(float)
    g=np.clip(g + soft(stip,0.4)*0.42*np.clip(beard*1.7,0,1),0,1)
    out=np.ones((H,W,3))*PAPER
    out=out*(1-g[...,None])+INK_SH*g[...,None]
    im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
    for s in S: stroke(d,**s)
    fa=np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None])+INK*fa[...,None]
    cl=np.clip(soft(g2(cx-P['eye_sp']-3,ye-3,2,2.4,1)+g2(cx+P['eye_sp']-3,ye-3,2,2.4,1),0.4),0,1)
    out=out*(1-cl[...,None])+PAPER*cl[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__=="__main__":
    render().save(f"{OUT}/face03_loomis_hair.png"); print("done")
