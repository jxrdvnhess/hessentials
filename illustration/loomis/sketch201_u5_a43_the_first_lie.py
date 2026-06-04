"""A43 — The First Lie. Start from the coalition calf. Add five plausible, well-intentioned marks
that each secretly damage the drawing. Each panel shows the calf + ONE such mark in isolation; the
last panel shows all five at once. The question is not why each mark is bad — why it seemed good."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140); SH=(150,146,140)
LM=dict(rumpground=(0.05,0.0), rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86),
 withers=(1.16,1.10), neckbase=(1.34,0.94), poll=(1.74,1.16), nose=(1.97,0.80),
 brisket=(1.13,0.10), bellymid=(0.80,0.13), bellyrear=(0.44,0.13), chest=(1.34,0.44),
 carpus=(1.46,0.17), forehoof=(1.78,0.03))
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
# coalition calf
def backarc(d,P,sc): line(d,cm([P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=3.0)
def add_belly(d,P,sc): line(d,cm([P((1.24,0.24)),P('brisket'),P('bellymid'),P('bellyrear'),P('rumpground')]),w=2.8)
def add_head(d,P,sc):
    h=P((1.90,1.0)); ell(d,h,0.15*sc,0.14*sc,INK); line(d,[P('poll'),h],w=2.6)
    ell(d,(h[0]+0.16*sc,h[1]+0.06*sc),0.10*sc,0.08*sc,INK); ell(d,(h[0]+0.02*sc,h[1]-0.02*sc),0.028*sc,0.028*sc,PAPER)
    p=P('poll'); line(d,[(p[0]-0.02*sc,p[1]-0.02*sc),(p[0]-0.15*sc,p[1]+0.02*sc),(p[0]-0.08*sc,p[1]+0.13*sc)],w=2.4)
def add_foreleg(d,P,sc): line(d,cm([P((1.20,0.20)),P((1.46,0.07)),P('forehoof')]),w=2.8)
def add_ground(d,P,sc): line(d,[P((-0.15,0.0)),P((2.15,0.0))],col=MID,w=1.8)
def add_hump(d,P,sc): w=P('withers'); line(d,cm([(w[0]-0.16*sc,w[1]-0.01*sc),(w[0],w[1]+0.15*sc),(w[0]+0.16*sc,w[1]-0.01*sc)]),w=2.6)
def calf(d,P,sc):
    for m in (backarc,add_belly,add_head,add_foreleg,add_ground,add_hump): m(d,P,sc)
# the five lies
def lie_2ndground(d,P,sc): line(d,[P((-0.10,0.22)),P((2.05,0.22))],col=MID,w=1.6)          # "a far edge / depth"
def lie_spots(d,P,sc):
    for (x,y,rx,ry) in [(0.46,0.74,0.14,0.10),(0.78,0.78,0.10,0.075)]: ell(d,P((x,y)),rx*sc,ry*sc,INK)  # "hide / it's a cow"
def lie_fold(d,P,sc): line(d,cm([P((0.80,0.84)),P((0.82,0.48)),P((0.82,0.16))]),w=1.6)       # "a flank fold / anatomy"
def lie_shadow(d,P,sc): ell(d,P((0.95,-0.02)),0.62*sc,0.07*sc,SH)                              # "grounding shadow"
def lie_doubleback(d,P,sc): line(d,cm([(P('poll')[0],P('poll')[1]-0.12*sc),(P('withers')[0],P('withers')[1]-0.12*sc),(P('loin')[0],P('loin')[1]-0.10*sc),(P('hip')[0],P('hip')[1]-0.12*sc)]),col=MID,w=1.6)  # "soft/furry edge"

STAGES=[("+ second ground line",[lie_2ndground]),
        ("+ texture patch (spots)",[lie_spots]),
        ("+ interior fold",[lie_fold]),
        ("+ cast shadow",[lie_shadow]),
        ("+ doubled back-line",[lie_doubleback]),
        ("+ all five",[lie_shadow,lie_2ndground,lie_spots,lie_fold,lie_doubleback])]
def render(path):
    cols=3; rows=2; cw,ch=420,300; W,H=cols*cw,rows*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(11*SS))
    except: font=ImageFont.load_default()
    for i,(name,lies) in enumerate(STAGES):
        cxo=(i%cols)*cw; cyo=(i//cols)*ch
        P=Cm(cxo+cw*0.30, cyo+ch*0.62, 130)
        for m in lies:
            if m is lie_shadow: m(d,P,130)   # shadow under, draw first
        calf(d,P,130)
        for m in lies:
            if m is not lie_shadow: m(d,P,130)
        d.text((int((cxo+14)*SS),int((cyo+ch-28)*SS)),name,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a43_the_first_lie.png")
