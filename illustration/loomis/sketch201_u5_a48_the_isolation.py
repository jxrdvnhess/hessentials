"""A48 — The Isolation. A47 left six explanations unseparated. This page isolates three, one pair
at a time, everything else held fixed. Same gap (~0.09) everywhere.
  ROUTES:    muzzle off, no route  vs  muzzle off, tethered by an added jaw line (one route left)
  OBJECTHOOD: muzzle off, filled   vs  muzzle off, outline only (same size, place, gap)
  LOCATION:  muzzle off at the head vs an equal filled single-route tuft off at the rump
Baselines included (unbroken; tuft attached)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
LM=dict(rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86), withers=(1.16,1.10),
 poll=(1.74,1.16), brisket=(1.13,0.10), bellymid=(0.80,0.13), forehoof=(1.78,0.03))
def cmr(nodes,n=26):
    P=[np.array(p,float) for p in nodes]; P=([P[0]]+P+[P[-1]]); out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(P[-2]); return out
def line(d,pts,col=INK,w=2.6): d.line([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def ell(d,c,rx,ry,col): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],fill=col)
def ello(d,c,rx,ry,col,w=2.4): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],outline=col,width=int(w*SS))

GAP=0.09
def draw_calf(d,ox,oy,sc,mode='plain'):
    def Q(pt):
        x,y=LM[pt] if isinstance(pt,str) else pt
        return (ox+x*sc, oy-y*sc)
    hd=Q((1.90,1.0))
    def R(dx,dy): return (hd[0]+dx*sc, hd[1]+dy*sc)
    line(d,cmr([R(-0.02,-0.10),Q('poll'),Q('withers'),Q('loin'),Q('hip'),Q('rumpback')]),w=3.0)
    w_=Q('withers'); line(d,cmr([(w_[0]-0.16*sc,w_[1]-0.01*sc),(w_[0],w_[1]+0.15*sc),(w_[0]+0.16*sc,w_[1]-0.01*sc)]),w=2.6)
    line(d,cmr([Q('rumpback'),Q((0.05,0.30)),Q((0.18,0.20)),Q((0.23,0.10)),Q((0.29,0.02))]),w=2.8)
    line(d,cmr([Q((1.24,0.24)),Q('brisket'),Q('bellymid'),Q((0.52,0.14)),Q((0.32,0.11))]),w=2.8)
    line(d,cmr([R(-0.12,0.20),Q((1.56,0.52)),Q((1.36,0.30)),Q((1.21,0.20))]),w=2.4)
    ell(d,hd,0.15*sc,0.14*sc,INK)
    ell(d,(hd[0]+0.02*sc,hd[1]-0.02*sc),0.026*sc,0.026*sc,PAPER)
    line(d,cmr([Q((1.20,0.20)),Q((1.46,0.07)),Q('forehoof')]),w=2.8)
    line(d,[(ox-0.25*sc,oy),(ox+2.55*sc,oy)],col=MID,w=1.8)
    # muzzle: attached or detached, filled or outline, tethered or not
    mz=R(0.16,0.06); mzd=(mz[0]+0.064*sc,mz[1]-0.064*sc)
    if mode in ('plain','tuft_on','tuft_off'):
        ell(d,mz,0.10*sc,0.08*sc,INK)
    elif mode=='mz_off':
        ell(d,mzd,0.10*sc,0.08*sc,INK)
    elif mode=='mz_tether':
        ell(d,mzd,0.10*sc,0.08*sc,INK)
        line(d,[(hd[0]+0.08*sc,hd[1]+0.11*sc),(mzd[0]-0.05*sc,mzd[1]+0.06*sc)],w=2.4)  # jaw tether
    elif mode=='mz_outline':
        ello(d,mzd,0.10*sc,0.08*sc,INK)
    # tuft: equal filled mass at the rump, single route to the rump line
    if mode in ('tuft_on','tuft_off'):
        rb=Q('rumpback'); base=(rb[0]-0.075*sc,rb[1]+0.10*sc)            # tangent to the rump curve
        c=base if mode=='tuft_on' else (base[0]-0.064*sc,base[1]-0.064*sc)
        ell(d,c,0.10*sc,0.08*sc,INK)

PANELS=[("unbroken",'plain'),("muzzle off — no route",'mz_off'),("muzzle off — tethered",'mz_tether'),
        ("muzzle off — outline",'mz_outline'),("tuft at the rump",'tuft_on'),("tuft off — no route",'tuft_off')]
def render(path):
    cols=3; rows=2; cw,ch=440,310; W,H=cols*cw,rows*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(12*SS))
    except: font=ImageFont.load_default()
    for i,(title,mode) in enumerate(PANELS):
        cxo=(i%cols)*cw; cyo=(i//cols)*ch
        draw_calf(d,cxo+cw*0.24,cyo+ch*0.64,118,mode=mode)
        tw=d.textlength(title,font=font)
        d.text((int(cxo*SS+(cw*SS-tw)//2),int((cyo+ch-32)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a48_the_isolation.png")
