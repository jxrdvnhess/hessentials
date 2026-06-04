"""A37 — The Wrong Return. Begin at V5 (pure structure), then add the thing that FEELS most
promising — what a novice reaches for: the face, the spots, the horns, the tail, the surface
texture. Five wrong returns. Why do they feel convincing, and why do they fail? Run it."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
LM=dict(rumpground=(0.05,0.0), hip=(0.30,0.95), withers=(1.16,1.10), poll=(1.74,1.16),
 nose=(1.97,0.80), bellymid=(0.80,0.13), forehoof=(1.78,0.03))
class Cm:
    def __init__(s,ox,oy,sc): s.ox,s.oy,s.sc=ox,oy,sc
    def __call__(s,k):
        x,y=LM[k] if isinstance(k,str) else k; return (s.ox+x*s.sc, s.oy-y*s.sc)
def line(d,pts,col=INK,w=2.6): d.line([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def ell(d,c,rx,ry,col,fill=True,w=2):
    bb=[int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)]
    d.ellipse(bb,fill=col) if fill else d.ellipse(bb,outline=col,width=max(1,int(w*SS)))
def poly(d,pts,col=INK): d.polygon([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col)
def dot(d,c,r,col=INK): ell(d,c,r,r,col)

def base_V5(d,P,sc):
    b=[P('forehoof'),P('rumpground')]; line(d,b,col=MID,w=2.0)
    for e in b: line(d,[e,(e[0],e[1]-0.05*sc)],col=MID,w=2.0)
    cog=(P('bellymid')[0]+0.06*sc,P('bellymid')[1]-0.30*sc); dot(d,cog,0.045*sc,INK)
    line(d,[cog,(cog[0],P('rumpground')[1])],col=MID,w=1.4)
    a=(P('hip')[0],P('hip')[1]-0.46*sc); bb=(P('poll')[0],P('poll')[1]-0.30*sc)
    line(d,[a,bb],INK,2.6); u=np.array(bb)-np.array(a); u=u/(np.hypot(*u)+1e-9); nn=np.array([-u[1],u[0]]); tip=np.array(bb)
    line(d,[tip,tip-u*0.15*sc+nn*0.08*sc],INK,2.6); line(d,[tip,tip-u*0.15*sc-nn*0.08*sc],INK,2.6)

def add_face(d,P,sc):     # the most recognizable feature, in detail, floating
    h=P((1.78,0.98))
    ell(d,h,0.20*sc,0.17*sc,INK,fill=False,w=2.2)            # face outline
    dot(d,(h[0]-0.06*sc,h[1]-0.02*sc),0.025*sc)              # eye
    ell(d,(h[0]+0.10*sc,h[1]+0.06*sc),0.08*sc,0.06*sc,INK,fill=False,w=2.0)  # muzzle
    dot(d,(h[0]+0.07*sc,h[1]+0.07*sc),0.012*sc); dot(d,(h[0]+0.12*sc,h[1]+0.07*sc),0.012*sc)  # nostrils
    for dx in (-0.20,0.16): poly(d,[(h[0]+dx*sc,h[1]-0.10*sc),(h[0]+dx*sc-0.06*sc,h[1]-0.20*sc),(h[0]+dx*sc+0.04*sc,h[1]-0.16*sc)])  # ears
def add_spots(d,P,sc):    # Holstein patches — decorative identity, scattered where a body would be
    for (x,y,rx,ry) in [(0.55,0.34,0.20,0.13),(0.95,0.40,0.15,0.11),(0.35,0.28,0.12,0.10),(1.15,0.30,0.10,0.08)]:
        ell(d,P((x,y)),rx*sc,ry*sc,INK)
def add_horns(d,P,sc):    # the iconic part
    h=P((1.80,1.10))
    for s_ in (-1,1):
        line(d,[(h[0]+s_*0.04*sc,h[1]),(h[0]+s_*0.18*sc,h[1]-0.22*sc)],w=3.0)
def add_tail(d,P,sc):     # a distinctive recognizable part
    t=P('rumpground'); line(d,[(t[0]+0.02*sc,t[1]+0.05*sc),(t[0]-0.18*sc,t[1]-0.55*sc),(t[0]-0.30*sc,t[1]-0.20*sc)],w=2.4)
    poly(d,[P((-0.30,0.30)),P((-0.36,0.10)),P((-0.24,0.10))])  # tuft
def add_texture(d,P,sc):  # surface features: a field of short hair / cow-print marks
    rng=np.random.default_rng(5)
    for _ in range(40):
        x=rng.uniform(0.2,1.3); y=rng.uniform(0.18,0.55)
        a=P((x,y)); ang=rng.uniform(0,3.14)
        line(d,[a,(a[0]+np.cos(ang)*0.05*sc,a[1]+np.sin(ang)*0.05*sc)],col=MID,w=1.4)

VERSIONS=[
 ("V5 + a detailed face", add_face),
 ("V5 + spots (markings)", add_spots),
 ("V5 + horns", add_horns),
 ("V5 + tail", add_tail),
 ("V5 + surface texture / fur", add_texture),
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
            d.text((int((i*cw+10)*SS),int((ch-30+j*15)*SS)),ln,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a37_wrong_return.png")
