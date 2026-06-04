"""A36 — The Structure That Returns. Begin at V5 (pure structure: a base, a centre of gravity, a
direction). Add exactly ONE thing back, five different ways, and watch what starts the calf
returning. Run it; do not predict."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140); WT=(176,172,164)
LM=dict(rumpground=(0.05,0.0), rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86),
 withers=(1.16,1.10), neckbase=(1.34,0.94), poll=(1.74,1.16), nose=(1.97,0.80),
 brisket=(1.13,0.10), bellymid=(0.80,0.13), bellyrear=(0.44,0.13), forehoof=(1.78,0.03),
 chest=(1.34,0.44), carpus=(1.46,0.17))
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
def ell(d,c,rx,ry,col,fill=True,w=2):
    bb=[int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)]
    d.ellipse(bb,fill=col) if fill else d.ellipse(bb,outline=col,width=max(1,int(w*SS)))
def dot(d,c,r,col=INK): ell(d,c,r,r,col)

def base_V5(d,P,sc):  # pure structure: base of support, centre of gravity, a direction
    b=[P('forehoof'),P('rumpground')]; line(d,b,col=MID,w=2.0)
    for e in b: line(d,[e,(e[0],e[1]-0.05*sc)],col=MID,w=2.0)
    cog=(P('bellymid')[0]+0.06*sc,P('bellymid')[1]-0.30*sc); dot(d,cog,0.045*sc,INK)
    line(d,[cog,(cog[0],P('rumpground')[1])],col=MID,w=1.4)
    a=(P('hip')[0],P('hip')[1]-0.46*sc); bb=(P('poll')[0],P('poll')[1]-0.30*sc)
    line(d,[a,bb],INK,2.6); u=np.array(bb)-np.array(a); u=u/(np.hypot(*u)+1e-9); nn=np.array([-u[1],u[0]]); tip=np.array(bb)
    line(d,[tip,tip-u*0.15*sc+nn*0.08*sc],INK,2.6); line(d,[tip,tip-u*0.15*sc-nn*0.08*sc],INK,2.6)

def add_backarc(d,P,sc):
    line(d,cm([P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=3.0)
def add_hump(d,P,sc):     # one deviation, alone (a bump where the withers would be, on nothing)
    w=P('withers'); line(d,cm([(w[0]-0.28*sc,w[1]+0.05*sc),(w[0],w[1]-0.12*sc),(w[0]+0.28*sc,w[1]+0.05*sc)]),w=3.0)
def add_proportion(d,P,sc):  # one proportion: a long, low mass (cattle barrel) on the base
    ell(d,P((0.70,0.30)),0.78*sc,0.30*sc,WT)
def add_foreleg(d,P,sc):
    line(d,cm([P('chest'),P('carpus'),P('forehoof')]),w=3.0)
def add_head(d,P,sc):     # one relationship: the head at the front of the direction
    h=P((1.85,1.0)); ell(d,h,0.16*sc,0.15*sc,INK)
    p=P('poll'); line(d,[(p[0]-0.02*sc,p[1]-0.02*sc),(p[0]-0.16*sc,p[1]+0.02*sc),(p[0]-0.09*sc,p[1]+0.14*sc)],w=2.6)  # ear

VERSIONS=[
 ("V5 + back-arc (one contour)", add_backarc),
 ("V5 + hump (one deviation)",   add_hump),
 ("V5 + long-low mass (one proportion)", add_proportion),
 ("V5 + folded foreleg (one contour)", add_foreleg),
 ("V5 + head & ear (one relationship)", add_head),
]
def render(path):
    cols=5; cw,ch=300,330; W,H=cols*cw,ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(9.5*SS))
    except: font=ImageFont.load_default()
    for i,(name,fn) in enumerate(VERSIONS):
        P=Cm(i*cw+cw*0.26, ch*0.62, 104)
        base_V5(d,P,104); fn(d,P,104)
        for j,ln in enumerate(textwrap.wrap(name,30)):
            d.text((int((i*cw+10)*SS),int((ch-44+j*15)*SS)),ln,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a36_structure_returns.png")
