"""A45 — The Silent Proof. Three versions of the coalition calf, exactly 10 marks each.
A: the coalition calf. B: improved (same budget, spent on closure). C: damaged (same budget,
spent on rivals). One page, three titles, no analysis."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
LM=dict(rumpground=(0.05,0.0), rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86),
 withers=(1.16,1.10), poll=(1.74,1.16), brisket=(1.13,0.10), bellymid=(0.80,0.13),
 bellyrear=(0.44,0.13), forehoof=(1.78,0.03))
def cm(nodes,n=26):
    P=[np.array(p,float) for p in nodes]; P=([P[0]]+P+[P[-1]]); out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(P[-2]); return out
class Cm:
    def __init__(s,ox,oy,sc): s.ox,s.oy,s.sc=ox,oy,sc
    def __call__(s,k):
        x,y=LM[k] if isinstance(k,str) else k; return (s.ox+x*s.sc, s.oy-y*s.sc)
def line(d,pts,col=INK,w=2.6): d.line([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def ell(d,c,rx,ry,col): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],fill=col)

# ---- marks (each function = one mark) ----
def m_backarc(d,P,sc): line(d,cm([P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=3.0)
def m_topline_b(d,P,sc):       # B: one stroke from head-top over the back to the rump (absorbs neckline)
    line(d,cm([P((1.88,1.10)),P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=3.0)
def m_rear_hindleg(d,P,sc):    # B: rump curve flowing into the hind leg, one stroke (closes the rear)
    line(d,cm([P('rumpback'),P((0.05,0.30)),P((0.18,0.20)),P((0.23,0.10)),P((0.29,0.02))]),w=2.8)
def m_belly(d,P,sc): line(d,cm([P((1.24,0.24)),P('brisket'),P('bellymid'),P('bellyrear'),P('rumpground')]),w=2.8)
def m_belly_b(d,P,sc): line(d,cm([P((1.24,0.24)),P('brisket'),P('bellymid'),P((0.52,0.14)),P((0.32,0.11))]),w=2.8)  # B: ends on the hind leg
def m_neckline(d,P,sc): line(d,[P('poll'),P((1.90,1.0))],w=2.6)
def m_headball(d,P,sc): ell(d,P((1.90,1.0)),0.15*sc,0.14*sc,INK)
def m_muzzle(d,P,sc): h=P((1.90,1.0)); ell(d,(h[0]+0.16*sc,h[1]+0.06*sc),0.10*sc,0.08*sc,INK)
def m_ear(d,P,sc): p=P('poll'); line(d,[(p[0]-0.02*sc,p[1]-0.02*sc),(p[0]-0.15*sc,p[1]+0.02*sc),(p[0]-0.08*sc,p[1]+0.13*sc)],w=2.4)
def m_eye(d,P,sc): h=P((1.90,1.0)); ell(d,(h[0]+0.02*sc,h[1]-0.02*sc),0.028*sc,0.028*sc,PAPER)
def m_foreleg(d,P,sc): line(d,cm([P((1.20,0.20)),P((1.46,0.07)),P('forehoof')]),w=2.8)
def m_hindleg(d,P,sc): line(d,cm([P((0.30,0.74)),P((0.40,0.44)),P((0.22,0.18)),P((0.29,0.02))]),w=2.6)
def m_throat(d,P,sc): line(d,cm([P((1.78,0.80)),P((1.56,0.52)),P((1.36,0.30)),P((1.21,0.20))]),w=2.4)
def m_ground(d,P,sc): line(d,[P((-0.15,0.0)),P((2.15,0.0))],col=MID,w=1.8)
def m_hump(d,P,sc): w=P('withers'); line(d,cm([(w[0]-0.16*sc,w[1]-0.01*sc),(w[0],w[1]+0.15*sc),(w[0]+0.16*sc,w[1]-0.01*sc)]),w=2.6)
def m_doubleback(d,P,sc): line(d,cm([(P('poll')[0],P('poll')[1]-0.12*sc),(P('withers')[0],P('withers')[1]-0.12*sc),(P('loin')[0],P('loin')[1]-0.10*sc),(P('hip')[0],P('hip')[1]-0.12*sc)]),col=MID,w=1.6)
def m_2ndground(d,P,sc): line(d,[P((-0.10,0.22)),P((2.05,0.22))],col=MID,w=1.6)
def m_fold(d,P,sc): line(d,cm([P((0.80,0.84)),P((0.82,0.48)),P((0.82,0.16))]),w=1.6)

VERSIONS=[
 ("Ten marks",
  [m_backarc,m_belly,m_neckline,m_headball,m_muzzle,m_ear,m_eye,m_foreleg,m_ground,m_hump]),
 ("Ten marks, closed",
  [m_topline_b,m_hump,m_rear_hindleg,m_belly_b,m_throat,m_headball,m_muzzle,m_eye,m_foreleg,m_ground]),
 ("Ten marks, divided",
  [m_backarc,m_doubleback,m_neckline,m_headball,m_muzzle,m_eye,m_foreleg,m_ground,m_2ndground,m_fold]),
]
def render(path):
    cols=3; cw,ch=420,330; W,H=cols*cw,ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(13*SS))
    except: font=ImageFont.load_default()
    for i,(title,marks) in enumerate(VERSIONS):
        cxo=i*cw; P=Cm(cxo+cw*0.27, ch*0.62, 132)
        for m in marks: m(d,P,132)
        tw=d.textlength(title,font=font)
        d.text((int(cxo*SS+(cw*SS-tw)//2),int((ch-40)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a45_the_silent_proof.png")
