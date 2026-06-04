"""A44 — The Honest Expert. Start from the coalition calf. Add five marks that each solve a REAL
weakness the calf already has (not a generic virtue, not a hypothetical). Before/after panels."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
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
# ---- coalition calf (carries A42 eye) ----
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
# ---- the five expert marks (each solves a real existing weakness) ----
def ex_hindleg(d,P,sc):   # WEAKNESS: legless rear — quadruped stands on the front only
    line(d,cm([P((0.30,0.74)),P((0.40,0.44)),P((0.22,0.18)),P((0.29,0.02))]),w=2.6)
def ex_throat(d,P,sc):    # WEAKNESS: head joins the body only along the top; neck has no underside
    line(d,cm([P((1.78,0.80)),P((1.56,0.52)),P((1.36,0.30)),P((1.21,0.20))]),w=2.4)  # ends at foreleg-top → continuous front edge
def ex_farforeleg(d,P,sc):# WEAKNESS: one front leg reads as a thin tripod; profile wants the far leg
    line(d,cm([P((1.08,0.18)),P((1.30,0.05)),P((1.56,0.015))]),col=(112,108,102),w=1.8)
def ex_hooves(d,P,sc):    # WEAKNESS: legs taper to points; no weight at the ground
    for k in ('forehoof',(1.56,0.015),(0.29,0.02)):
        c=P(k); ell(d,(c[0],c[1]+0.012*sc),0.034*sc,0.028*sc,INK)
def ex_muzzle(d,P,sc):    # WEAKNESS: head is two stacked dark balls with no front plane
    h=P((1.90,1.0)); m=(h[0]+0.16*sc,h[1]+0.06*sc)
    ell(d,(m[0]+0.05*sc,m[1]-0.018*sc),0.018*sc,0.018*sc,PAPER)                       # nostril knockout
    line(d,[(m[0]-0.01*sc,m[1]+0.055*sc),(m[0]+0.085*sc,m[1]+0.035*sc)],col=PAPER,w=2.2)  # mouth slit
EXPERT=[ex_hindleg,ex_throat,ex_farforeleg,ex_hooves,ex_muzzle]
def render(path):
    cols=2; cw,ch=520,400; W,H=cols*cw,ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(13*SS))
    except: font=ImageFont.load_default()
    for i,(name,marks) in enumerate([("the coalition calf",[]),("+ five expert marks",EXPERT)]):
        cxo=i*cw; P=Cm(cxo+cw*0.30, ch*0.66, 165)
        calf(d,P,165)
        for m in marks: m(d,P,165)
        d.text((int((cxo+18)*SS),int((ch-34)*SS)),name,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a44_the_honest_expert.png")
