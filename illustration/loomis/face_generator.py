"""
Parameterized straight-on MALE FACE generator (Loomis-based). Varies face shape,
jaw/chin, length, brow, eyes, nose, mouth, hair style, line weight, light.
Renders 25 distinct men into a contact sheet + individual files.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/sessions/lucid-charming-babbage/mnt/hessentials/illustration")
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis/faces25"
W,H=600,760; CX=300
PAPER=np.array([237,232,223],float); INK_SH=np.array([52,52,66],float)
yy,xx=np.mgrid[0:H,0:W].astype(float)
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.3*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)

def D(P):
    """Return (strokes, silhouette polygon pts, hair polygon pts) for one face."""
    cx=CX
    chk=P['cheek']; jw=P['jaw']; cw=P['chin']
    yb=P['ybrow']; ye=P['yeye']; yn=P['ynose']; ym=P['ymouth']; yc=P['ychin']; yt=P['ytop']; yh=P['yhair']
    lw=P['lw']; S=[]
    def a(c,w,lead=0.16,tail=0.22,swell=0.34,sm=0.56,cs=False,ce=False):
        S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
    # contour: temple->cheek->jaw->chin (square-ness from jw vs cw)
    jm=(ye+yc)//2
    a([(cx-chk+8,yt+40),(cx-chk-6,yb-30),(cx-chk-8,ye+18),(cx-chk+2,jm),(cx-jw,jm+44),(cx-jw+10,yc-44),(cx-cw-14,yc-10),(cx-cw,yc)],lw,lead=0.18,tail=0.16,swell=0.3)
    a([(cx-cw,yc),(cx,yc+8),(cx+cw,yc)],lw*0.95,lead=0.22,tail=0.22,swell=0.26)
    a([(cx+cw,yc),(cx+cw+14,yc-10),(cx+jw-10,yc-44),(cx+jw,jm+44),(cx-2+chk,jm),(cx+chk-2,ye+18),(cx+chk+6,yb-30),(cx+chk-8,yt+40)],lw,lead=0.16,tail=0.18,swell=0.3)
    # jaw-angle accents
    a([(cx-chk+2,ye+40),(cx-jw+4,jm+40),(cx-jw+24,yc-50)],1.6,lead=0.34,tail=0.34,swell=0.12)
    a([(cx+chk-2,ye+40),(cx+jw-4,jm+40),(cx+jw-24,yc-50)],1.6,lead=0.34,tail=0.34,swell=0.12)
    # brows (weight + slant: outer end drops by slant)
    bw=P['brow_w']; sl=P['brow_slant']; bl=P['brow_len']
    a([(cx-bl-18,yb-2+sl),(cx-bl+30,yb-8),(cx-22,yb+2)],bw,lead=0.1,tail=0.18,swell=0.5)
    a([(cx+22,yb+2),(cx+bl-30,yb-8),(cx+bl+18,yb-2+sl)],bw,lead=0.1,tail=0.18,swell=0.5)
    # eyes
    ew=P['eye_w']; es=P['eye_sp']; eo=P['eye_open']
    for s2 in (-1,1):
        ex=cx+s2*es
        a([(ex-ew,ye-eo),(ex-2,ye-eo-6),(ex+ew-2,ye-eo+1)],2.6,lead=0.14,tail=0.24,swell=0.34)   # upper lid
        a([(ex-ew+4,ye+eo),(ex+2,ye+eo+4),(ex+ew-4,ye+eo-2)],1.4,lead=0.32,tail=0.34,swell=0.14) # lower lid
        a([(ex-7,ye-3),(ex,ye-7),(ex+7,ye-3)],1.4,lead=0.3,tail=0.3,swell=0.12)                  # iris top
        a([(ex-7,ye-3),(ex,ye+7),(ex+7,ye-3)],1.5,lead=0.3,tail=0.3,swell=0.12)                  # iris bottom
        a([(ex-3,ye),(ex+3,ye)],2.0,cs=True,ce=True,swell=0.1)                                   # pupil
        a([(ex-ew-1,ye+1),(ex-ew-7,ye+5)],1.3,cs=True,ce=True,swell=0.12)                        # tear duct
    # nose
    nw=P['nose_w']; nl=yn; br=P['bridge']
    a([(cx-10,yb+6),(cx-12,nl-30),(cx-nw+6,nl)],br,lead=0.24,tail=0.36,swell=0.16)
    a([(cx+10,yb+6),(cx+12,nl-30),(cx+nw-6,nl)],br*0.8,lead=0.28,tail=0.38,swell=0.14)
    a([(cx-nw+6,nl),(cx-6,nl+8),(cx+6,nl+8),(cx+nw-6,nl)],1.8,lead=0.24,tail=0.24,swell=0.2)      # base
    a([(cx-nw+6,nl-4),(cx-nw-6,nl+6),(cx-nw+2,nl+16),(cx-8,nl+12)],1.7,lead=0.3,tail=0.32,swell=0.12) # L wing
    a([(cx+nw-6,nl-4),(cx+nw+6,nl+6),(cx+nw-2,nl+16),(cx+8,nl+12)],1.7,lead=0.3,tail=0.32,swell=0.12) # R wing
    a([(cx-12,nl+10),(cx-6,nl+15)],1.8,cs=True,ce=True,swell=0.12); a([(cx+12,nl+10),(cx+6,nl+15)],1.8,cs=True,ce=True,swell=0.12)
    # mouth
    mw=P['mouth_w']; lf=P['lip']
    a([(cx-mw,ym+2),(cx-12,ym+6),(cx,ym+6),(cx+12,ym+6),(cx+mw,ym)],2.6,lead=0.1,tail=0.2,swell=0.4)     # seam
    a([(cx-mw+8,ym-8),(cx-10,ym-12-lf),(cx,ym-6),(cx+10,ym-12-lf),(cx+mw-8,ym-8)],1.5,lead=0.3,tail=0.3,swell=0.16) # upper lip
    a([(cx-mw+10,ym+14),(cx,ym+18+lf),(cx+mw-10,ym+12)],1.8,lead=0.3,tail=0.3,swell=0.18)                # lower lip
    # ears
    a([(cx-chk-2,ye-6),(cx-chk-18,ye+26),(cx-chk-6,ye+70),(cx-chk+4,ye+40)],1.8,lead=0.26,tail=0.3,swell=0.18)
    a([(cx+chk+2,ye-6),(cx+chk+18,ye+26),(cx+chk+6,ye+70),(cx+chk-4,ye+40)],1.8,lead=0.26,tail=0.3,swell=0.18)
    # neck + shoulders
    a([(cx-cw-6,yc-4),(cx-48,yc+60),(cx-52,yc+150)],lw*0.7,lead=0.2,tail=0.34,swell=0.22)
    a([(cx+cw+6,yc-4),(cx+48,yc+60),(cx+52,yc+150)],lw*0.7,lead=0.2,tail=0.34,swell=0.22)
    a([(cx-52,yc+150),(cx-150,yc+178),(cx-250,yc+200)],lw*0.7,lead=0.2,tail=0.3,swell=0.22)
    a([(cx+52,yc+150),(cx+150,yc+178),(cx+250,yc+200)],lw*0.7,lead=0.2,tail=0.3,swell=0.22)
    # hair (by style) -> also returns hair silhouette pts
    hp=hair(a,P)
    sil=[(cx-chk+8,yt+40),(cx-chk-6,yb-30),(cx-chk+2,jm),(cx-jw,jm+44),(cx-jw+10,yc-44),(cx-cw,yc),
         (cx+cw,yc),(cx+jw-10,yc-44),(cx+jw,jm+44),(cx+chk-2,ye+18),(cx+chk+6,yb-30),(cx+chk-8,yt+40)]
    return S,sil,hp

def hair(a,P):
    cx=CX; yt=P['ytop']; yh=P['yhair']; chk=P['cheek']; hh=P['hair_h']; st=P['hair']
    top=yt-hh
    if st==0:  # short crop, neat, low
        pts=[(cx-chk+6,yt+30),(cx-chk-2,yt-10),(cx-60,yt-30),(cx+40,yt-34),(cx+chk-4,yt-6),(cx+chk-2,yt+30)]
        a([(cx-chk+6,yt+30),(cx-chk-2,yt-10),(cx-60,yt-30),(cx+40,yt-34),(cx+chk-4,yt-6),(cx+chk-2,yt+30)],3.0,lead=0.16,tail=0.2,swell=0.32)
        a([(cx-70,yt+2),(cx,yt-12),(cx+70,yt+4)],1.5,lead=0.3,tail=0.3,swell=0.12)
    elif st==1:  # side part, swept
        pts=[(cx-chk+4,yt+28),(cx-chk-6,yt-30),(cx-70,top+6),(cx+10,top-8),(cx+80,top+18),(cx+chk-2,yt-8),(cx+chk-2,yt+28)]
        a(pts+[pts[0]],3.0,lead=0.16,tail=0.2,swell=0.34)
        a([(cx-30,yt-6),(cx-16,top+20),(cx+4,top)],1.7,lead=0.3,tail=0.3,swell=0.14)              # part
        for q in [((cx-18,top+18),(cx+40,top+30),(cx+96,yt-6)),((cx-2,top),(cx+50,top+14),(cx+100,yt-12))]:
            a(list(q),1.3,lead=0.34,tail=0.36,swell=0.12)
    elif st==2:  # fuller wavy (volume)
        pts=[(cx-chk,yt+24),(cx-chk-16,top+20),(cx-78,top-14),(cx-20,top-30),(cx+44,top-22),(cx+96,top+8),(cx+chk+6,yt-2),(cx+chk-2,yt+26)]
        a(pts,3.0,lead=0.16,tail=0.2,swell=0.36)
        for q in [((cx-60,yt-6),(cx-40,top+10),(cx-6,top-12)),((cx-6,yt-8),(cx+18,top+6),(cx+50,top-16)),((cx+40,yt-4),(cx+70,top+16),(cx+96,top+2))]:
            a(list(q),1.4,lead=0.34,tail=0.34,swell=0.14)
    elif st==3:  # slicked back, higher
        pts=[(cx-chk+2,yt+26),(cx-chk-4,yt-26),(cx-50,top),(cx+50,top-2),(cx+chk-2,yt-22),(cx+chk-4,yt+26)]
        a(pts,3.0,lead=0.16,tail=0.2,swell=0.34)
        for q in [((cx-60,yt-4),(cx-20,top+14),(cx+20,top+6)),((cx-20,yt-8),(cx+24,top+8),(cx+64,top+2))]:
            a(list(q),1.3,lead=0.34,tail=0.34,swell=0.12)
    elif st==4:  # receding / widow's peak, shorter
        pts=[(cx-chk+8,yt+34),(cx-chk,yt-4),(cx-70,yt-20),(cx+50,yt-22),(cx+chk-6,yt-2),(cx+chk-2,yt+34)]
        a(pts,2.8,lead=0.16,tail=0.2,swell=0.3)
        a([(cx-86,yt+6),(cx-50,yt-4),(cx-30,yt+10)],1.5,lead=0.3,tail=0.32,swell=0.12)            # M temple L
        a([(cx-26,yt+18),(cx,yt+6),(cx+26,yt+18)],1.5,lead=0.3,tail=0.3,swell=0.12)               # peak
        a([(cx+30,yt+10),(cx+50,yt-4),(cx+86,yt+6)],1.5,lead=0.32,tail=0.3,swell=0.12)            # M temple R
    else:  # st==5 textured/messy tufts
        pts=[(cx-chk-2,yt+26),(cx-chk-14,top+24),(cx-84,top-6),(cx-30,top-26),(cx+10,top-10),(cx+50,top-28),(cx+92,top+6),(cx+chk+4,yt-2),(cx+chk-2,yt+26)]
        a(pts,2.8,lead=0.16,tail=0.2,swell=0.32)
        for q in [((cx-50,yt-8),(cx-44,top+8),(cx-20,top-10)),((cx-10,yt-10),(cx+6,top+4),(cx+30,top-12)),((cx+34,yt-6),(cx+58,top+10),(cx+82,top-6))]:
            a(list(q),1.2,lead=0.34,tail=0.36,swell=0.1)
    return pts

def poly_mask(pts):
    im=Image.new("L",(W,H),0); ImageDraw.Draw(im).polygon([(float(x),float(y)) for x,y in pts],fill=255)
    return np.asarray(im,float)/255.0

def render_face(P):
    S,sil,hp=D(P)
    body=np.clip(poly_mask(sil)+poly_mask(hp),0,1)
    body=np.clip(body+poly_mask([(CX-P['chin']-6,P['ychin']-4),(CX+P['chin']+6,P['ychin']-4),(CX+52,P['ychin']+150),(CX+250,P['ychin']+200),(CX-250,P['ychin']+200),(CX-52,P['ychin']+150)]),0,1)
    mask=(soft(body,2)>0.5).astype(float)
    # light: terminator x at eye level offset by P['term']; frontal=large
    cx=CX; ye=P['yeye']; t=P['term']
    xterm=(cx+t)+ (yy-ye)*0.12
    shadow=np.clip((xx-xterm)/28.0+0.5,0,1)*mask
    half=np.clip((shadow-0.16)/0.34,0,1)
    g=half*P['shadow']*stripes(-0.5,6,1.5,P['seed']) + np.clip(shadow-0.55,0,1)*0.30*stripes(0.6,7,1.5,P['seed']+1)
    # under-plane accents
    g=np.clip(g + soft(g2(cx,P['ynose']+18,P['nose_w'],8,0.34)+g2(cx,P['ymouth']+22,P['mouth_w']*0.8,8,0.3)+g2(cx,P['ychin']+10,120,30,0.28)+g2(cx-P['eye_sp'],P['ybrow']+20,P['eye_w'],10,0.26)+g2(cx+P['eye_sp'],P['ybrow']+20,P['eye_w'],10,0.3),4)*mask*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)
    out=np.ones((H,W,3))*PAPER
    out=out*(1-g[...,None]) + INK_SH*g[...,None]
    im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
    for s in S: stroke(d,**s)
    fa=np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    out=out*(1-fa[...,None]) + INK*fa[...,None]
    # catchlights
    cl=np.clip(soft(g2(cx-P['eye_sp']-3,P['yeye']-3,2.0,2.4,1.0)+g2(cx+P['eye_sp']-3,P['yeye']-3,2.0,2.4,1.0),0.4),0,1)
    out=out*(1-cl[...,None]) + PAPER*cl[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

def make_params():
    rng=np.random.default_rng(7); P=[]
    for i in range(25):
        chin_y=int(rng.integers(528,566))
        p=dict(seed=i*3+1, ytop=156, yhair=196,
            ybrow=296, yeye=int(rng.integers(316,326)), ynose=int(rng.integers(400,420)),
            ymouth=int(rng.integers(456,472)), ychin=chin_y,
            cheek=int(rng.integers(104,116)), jaw=int(rng.integers(92,116)), chin=int(rng.integers(26,42)),
            brow_w=round(float(rng.uniform(4.4,6.4)),1), brow_slant=int(rng.integers(-2,9)), brow_len=int(rng.integers(40,56)),
            eye_w=int(rng.integers(22,30)), eye_sp=int(rng.integers(48,58)), eye_open=int(rng.integers(8,13)),
            nose_w=int(rng.integers(24,34)), bridge=round(float(rng.uniform(1.8,2.6)),1),
            mouth_w=int(rng.integers(34,46)), lip=int(rng.integers(2,7)),
            hair=int(i%6), hair_h=int(rng.integers(34,72)),
            lw=round(float(rng.uniform(3.4,4.6)),1),
            term=int(rng.integers(70,120)), shadow=round(float(rng.uniform(0.16,0.26)),2))
        P.append(p)
    return P

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    P=make_params(); thumbs=[]
    for i,p in enumerate(P):
        img=render_face(p); img.save(f"{OUT}/face_{i+1:02d}.png"); thumbs.append(img)
        print("face",i+1,"done")
    # 5x5 contact sheet
    cw,ch=300,380; pad=10; cols=5; rows=5
    sheet=Image.new("RGB",(cols*cw+pad*(cols+1), rows*ch+pad*(rows+1)+30),(228,224,215))
    dd=ImageDraw.Draw(sheet); dd.text((pad,8),"25 MALE FRONT FACES",fill=(60,56,58))
    for i,img in enumerate(thumbs):
        t=img.resize((cw,ch)); r,c=divmod(i,cols)
        x=pad+c*(cw+pad); y=30+pad+r*(ch+pad); sheet.paste(t,(x,y))
        dd.text((x+4,y+4),str(i+1),fill=(90,86,88))
    sheet.save(f"{OUT}/contact_sheet.png"); print("sheet done")
