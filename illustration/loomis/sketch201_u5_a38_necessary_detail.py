"""A38 — The Necessary Detail. Base = the back-arc ALONE (A36's strongest structure). Add ONE
detail at a time, not to identify the calf but to help the structure do its job (read as a
reclining body). Five attempts. Which detail contributes most once structure already exists?"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
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
def line(d,pts,col=INK,w=2.8): d.line([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def ell(d,c,rx,ry,col): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],fill=col)

def backarc(d,P,sc): line(d,cm([P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=3.0)

def add_ground(d,P,sc):  line(d,[P((-0.15,0.0)),P((2.05,0.0))],col=MID,w=1.8)
def add_belly(d,P,sc):   line(d,cm([P('chest'),P('brisket'),P('bellymid'),P('bellyrear'),P('rumpground')]),w=2.8)
def add_head(d,P,sc):
    h=P((1.88,1.0)); ell(d,h,0.15*sc,0.14*sc,INK); line(d,[P('poll'),h],w=2.6)
    p=P('poll'); line(d,[(p[0]-0.02*sc,p[1]-0.02*sc),(p[0]-0.15*sc,p[1]+0.02*sc),(p[0]-0.08*sc,p[1]+0.13*sc)],w=2.4)
def add_foreleg(d,P,sc): line(d,cm([P('chest'),P('carpus'),P('forehoof')]),w=2.8)
def add_hump(d,P,sc):    w=P('withers'); line(d,cm([(w[0]-0.18*sc,w[1]-0.02*sc),(w[0],w[1]+0.16*sc),(w[0]+0.18*sc,w[1]-0.02*sc)]),w=2.8)

VERSIONS=[
 ("arc + ground", add_ground),
 ("arc + belly (close the body)", add_belly),
 ("arc + head & ear", add_head),
 ("arc + folded foreleg", add_foreleg),
 ("arc + hump", add_hump),
]
def render(path):
    cols=5; cw,ch=300,330; W,H=cols*cw,ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(9.5*SS))
    except: font=ImageFont.load_default()
    for i,(name,fn) in enumerate(VERSIONS):
        P=Cm(i*cw+cw*0.26, ch*0.60, 104)
        backarc(d,P,104); fn(d,P,104)
        for j,ln in enumerate(textwrap.wrap(name,28)):
            d.text((int((i*cw+10)*SS),int((ch-30+j*15)*SS)),ln,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a38_necessary_detail.png")
