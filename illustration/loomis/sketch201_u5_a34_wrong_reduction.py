"""A34 — The Wrong Reduction. Same zebu calf, same marks as A33, but removed in the WRONG order:
the carrying STRUCTURE (back-arc, foreleg, belly-ground, rump, neck) destroyed first; the small
DETAILS (ear, dewlap, muzzle, far ear, hind hoof) protected to the end. Tests A33's leverage:
what dies when the wrong thing survives. Compared by information, not aesthetics."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
LM=dict(
 rumpground=(0.05,0.0), rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86),
 withers=(1.16,1.10), neckbase=(1.34,0.94), poll=(1.74,1.16), nose=(1.97,0.80),
 jaw=(1.66,0.64), throat=(1.48,0.60), dewlap=(1.42,0.28), chest=(1.34,0.44),
 brisket=(1.13,0.10), bellymid=(0.80,0.13), bellyrear=(0.44,0.13),
 carpus=(1.46,0.17), forehoof=(1.78,0.03), hock=(0.52,0.17), hindhoof=(0.36,0.02),
)
def cm(nodes,n=24):
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
def line(d,pts,col=INK,w=2.4): d.line([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def ell(d,c,rx,ry,col=INK): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],fill=col)

def m_backarc(d,P,sc):   line(d,cm([P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=2.6)
def m_ear(d,P,sc):       p=P('poll'); line(d,[(p[0]-0.02*sc,p[1]-0.02*sc),(p[0]-0.18*sc,p[1]+0.02*sc),(p[0]-0.10*sc,p[1]+0.16*sc)],w=2.4)
def m_headtilt(d,P,sc):  line(d,[P('poll'),P('nose')],w=2.4)
def m_foreleg(d,P,sc):   line(d,cm([P('chest'),P('carpus'),P('forehoof')]),w=2.4)
def m_hindrear(d,P,sc):  line(d,[P('rumpback'),P('rumpground')],w=2.4)
def m_brisket(d,P,sc):   line(d,cm([P('brisket'),P('bellymid'),P('bellyrear'),P('rumpground')]),w=2.4)
def m_neckunder(d,P,sc): line(d,cm([P('neckbase'),P('throat'),P('chest')]),w=2.2)
def m_dewlap(d,P,sc):    line(d,cm([P('throat'),P('dewlap'),P('chest')]),w=2.0)
def m_farear(d,P,sc):    p=P('poll'); line(d,[(p[0]+0.04*sc,p[1]),(p[0]+0.16*sc,p[1]-0.02*sc),(p[0]+0.08*sc,p[1]+0.12*sc)],w=2.0)
def m_muzzle(d,P,sc):    ell(d,(P('nose')[0]-0.02*sc,P('nose')[1]+0.02*sc),0.06*sc,0.05*sc)
def m_hindtuck(d,P,sc):  line(d,[P('hock'),P('hindhoof')],w=2.2)
def m_ground(d,P,sc):    line(d,[P((-0.2,0.0)),P((2.1,0.0))],col=MID,w=1.4)
MARKS={1:m_backarc,2:m_ear,3:m_headtilt,4:m_foreleg,5:m_hindrear,6:m_brisket,
       7:m_neckunder,8:m_dewlap,9:m_farear,10:m_muzzle,11:m_hindtuck,12:m_ground}
# WRONG order: destroy structure first (back_arc, brisket, hindrear, foreleg, neckunder, head_tilt),
# protect details (ear, dewlap, far_ear, muzzle, hind_tuck, ground) to the end.
STAGES=[
 [1,2,3,4,5,6,7,8,9,10,11,12],
 [2,3,4,5,6,7,8,9,10,11,12],   # -back_arc (the carrying spine, gone first)
 [2,3,4,5,7,8,9,10,11,12],     # -brisket/belly-ground
 [2,3,4,7,8,9,10,11,12],       # -hind rear
 [2,3,7,8,9,10,11,12],         # -foreleg
 [2,3,8,9,10,11,12],           # -neck under
 [2,8,9,10,11,12],             # -head tilt  (now: details only)
 [2,8,9,10,11],                # -ground
 [2,8,9,10],                   # -hind tuck
 [2,8,10],                     # -far ear  -> ear + dewlap + muzzle
]
def render(path):
    cols,rows=5,2; cw,ch=300,300; W,H=cols*cw,rows*ch+10
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(11*SS))
    except: font=ImageFont.load_default()
    for i,marks in enumerate(STAGES):
        cxo=(i%cols)*cw; cyo=(i//cols)*ch
        P=Cm(cxo+cw*0.28, cyo+ch*0.60, 104)
        for mid in marks: MARKS[mid](d,P,104)
        d.text((int((cxo+12)*SS),int((cyo+ch-26)*SS)), f"{len(marks)} marks", fill=MID, font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a34_wrong_reduction.png")
