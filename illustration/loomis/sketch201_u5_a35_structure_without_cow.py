"""A35 — The Structure Without The Cow. Keep only the carrying arc, the weight relationship, the
balance relationship, the directional flow. Remove all animal-specific marks (ears, dewlap,
muzzle, anatomy). Five versions, each stripping more animal information, to see how much of the
cow exists before the cow exists. Run the experiment; let the answer arrive."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140); WT=(176,172,164); FAINT=(200,196,188)
LM=dict(rumpground=(0.05,0.0), rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86),
 withers=(1.16,1.10), neckbase=(1.34,0.94), poll=(1.74,1.16), nose=(1.97,0.80),
 brisket=(1.13,0.10), bellymid=(0.80,0.13), bellyrear=(0.44,0.13), forehoof=(1.78,0.03))
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
def dot(d,c,r,col=INK): ell(d,c,r,r,col)
def arrow(d,a,b,col=INK,w=2.8):
    line(d,[a,b],col,w); v=np.array(b)-np.array(a); L=np.hypot(*v)+1e-9; u=v/L; n=np.array([-u[1],u[0]])
    tip=np.array(b)
    line(d,[tip,tip-(u*0.10-n*0.05)*100],col,w) if False else None
    h=0.07* s_for(d)
    line(d,[tip, tip-u*22+n*11],col,w); line(d,[tip, tip-u*22-n*11],col,w)
def s_for(d): return 1.0

def weight(d,P,sc):  # where the mass/load sits: a LOW mass on the ground, heavier toward the rear
    ell(d,P((0.62,0.24)),0.62*sc,0.22*sc,col=WT)   # low reclining body mass
    ell(d,P((0.28,0.30)),0.34*sc,0.28*sc,col=MID)  # denser at the rear = the load concentration
    line(d,[P('brisket'),P('bellyrear')],col=MID,w=3.0)  # ground bearing
def balance(d,P,sc):
    base=[P('forehoof'),P('rumpground')]; line(d,base,col=MID,w=2.0)
    for b in base: line(d,[b,(b[0],b[1]-0.05*sc)],col=MID,w=2.0)
    cog=(P('bellymid')[0]+0.06*sc,P('bellymid')[1]-0.30*sc); dot(d,cog,0.045*sc,INK)
    line(d,[cog,(cog[0],P('rumpground')[1])],col=MID,w=1.4)
def flow(d,P,sc,col=INK):
    a=cm([P('nose'),P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]); line(d,a,col,w=3.0)
    n=P('nose'); u=np.array(P('poll'))-np.array(n); u=u/ (np.hypot(*u)+1e-9)
    nn=np.array([-u[1],u[0]]); tip=np.array(n)
    line(d,[tip,tip-u*0.16*sc+nn*0.08*sc],col,3.0); line(d,[tip,tip-u*0.16*sc-nn*0.08*sc],col,3.0)
def arc_full(d,P,sc):   line(d,cm([P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')]),w=2.8)
def arc_nohump(d,P,sc): line(d,cm([P('poll'),(P('withers')[0],P('loin')[1]-0.04*sc),P('loin'),P('hip'),P('rumpback')]),w=2.8)
def arc_simple(d,P,sc): line(d,cm([(P('poll')[0],P('poll')[1]+0.04*sc),P('loin'),P('rumpback')]),w=2.8)

VERSIONS=[
 ("V1 · arc (calf contour) + weight + balance + flow", lambda d,P,sc:(weight(d,P,sc),balance(d,P,sc),arc_full(d,P,sc),flow(d,P,sc))),
 ("V2 · hump removed — generic resting topline",        lambda d,P,sc:(weight(d,P,sc),balance(d,P,sc),arc_nohump(d,P,sc))),
 ("V3 · topline simplified to one reclining sweep",     lambda d,P,sc:(weight(d,P,sc),balance(d,P,sc),arc_simple(d,P,sc))),
 ("V4 · flow + balance only",                            lambda d,P,sc:(balance(d,P,sc),flow(d,P,sc))),
 ("V5 · balance + a direction — pure structure",         lambda d,P,sc:(balance(d,P,sc), arrow_flow(d,P,sc))),
]
def arrow_flow(d,P,sc):
    a=(P('hip')[0],P('hip')[1]-0.45*sc); b=(P('poll')[0],P('poll')[1]-0.30*sc)
    line(d,[a,b],INK,3.0); u=np.array(b)-np.array(a); u=u/(np.hypot(*u)+1e-9); nn=np.array([-u[1],u[0]]); tip=np.array(b)
    line(d,[tip,tip-u*0.16*sc+nn*0.08*sc],INK,3.0); line(d,[tip,tip-u*0.16*sc-nn*0.08*sc],INK,3.0)

def render(path):
    cols=5; cw,ch=300,330; W,H=cols*cw,ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(9.5*SS))
    except: font=ImageFont.load_default()
    for i,(name,fn) in enumerate(VERSIONS):
        P=Cm(i*cw+cw*0.26, ch*0.62, 104); fn(d,P,104)
        # wrap label
        import textwrap
        for j,ln in enumerate(textwrap.wrap(name,28)):
            d.text((int((i*cw+10)*SS),int((ch-44+j*15)*SS)),ln,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a35_structure_without_cow.png")
