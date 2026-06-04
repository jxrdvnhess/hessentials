"""A32 — The One Cow, Ten Ways. One cow held constant (the zebu calf, studied from a single
Unsplash photo), drawn ten times through ten analytical lenses. Goal: depth, not variation —
one cow contains ten cows. The volume/flow/balance lenses answer the A31 note: see the animal
as continuous relationships, not assembled parts."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140); FAINT=(193,189,181)

# ---- the calf, in body units, facing RIGHT (x toward head, y up, ground y=0) ----
# landmarks studied from the photograph
LM=dict(
 rumpground=(0.05,0.0), rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86),
 withers=(1.16,1.04), neckbase=(1.34,0.94), poll=(1.74,1.16), foretop=(1.93,0.99),
 nose=(1.97,0.80), jaw=(1.66,0.64), throat=(1.48,0.60), dewlap=(1.42,0.28),
 chest=(1.34,0.44), brisket=(1.13,0.10), bellymid=(0.80,0.13), bellyrear=(0.44,0.13),
 # legs
 elbow=(1.30,0.34), carpus=(1.46,0.17), forehoof=(1.78,0.03),
 stifle=(0.56,0.50), hock=(0.52,0.17), hindhoof=(0.36,0.02),
)
SIL=['rumpground','rumpback','hip','loin','withers','neckbase','poll','foretop','nose',
     'jaw','throat','dewlap','chest','brisket','bellymid','bellyrear']
def cm(nodes,n=24,closed=True):
    P=[np.array(p,float) for p in nodes]
    P=([P[-1]]+P+[P[0],P[1]]) if closed else ([P[0]]+P+[P[-1]])
    out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    return out

class C:  # coordinate mapper for a panel
    def __init__(s,ox,oy,sc): s.ox,s.oy,s.sc=ox,oy,sc
    def __call__(s,k_or_xy):
        x,y = LM[k_or_xy] if isinstance(k_or_xy,str) else k_or_xy
        return (s.ox+x*s.sc, s.oy-y*s.sc)

def ipts(pts): return [(int(p[0]*SS),int(p[1]*SS)) for p in pts]
def poly(d,pts,col=INK): d.polygon(ipts(pts),fill=col)
def line(d,pts,col=INK,w=2,joint="curve"): d.line(ipts(pts),fill=col,width=max(1,int(w*SS)),joint=joint)
def ell(d,c,rx,ry,col=INK,outline=None,w=2):
    bb=[int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)]
    if outline: d.ellipse(bb,outline=outline,width=max(1,int(w*SS)))
    else: d.ellipse(bb,fill=col)
def cap(d,a,b,ra,rb,col=INK):
    a=np.array(a,float);b=np.array(b,float);v=b-a;L=np.hypot(*v)
    if L<1: ell(d,a,ra,ra,col); return
    n=np.array([-v[1],v[0]])/L
    poly(d,[a+n*ra,b+n*rb,b-n*rb,a-n*ra],col)
    ell(d,a,ra,ra,col); ell(d,b,rb,rb,col)
def dot(d,c,r,col=INK): ell(d,c,r,r,col)

def silhouette_path(P): return cm([P(k) for k in SIL],20)

def legs_fill(d,P,sc,col=INK):
    cap(d,P('chest'),P('carpus'),0.12*sc,0.075*sc,col); cap(d,P('carpus'),P('forehoof'),0.075*sc,0.05*sc,col)
    # tucked hind
    poly(d,[P('hindhoof'),P((0.20,0.0)),P((0.30,0.18))],col)
def ears(d,P,sc,col=INK):
    poll=P('poll')
    poly(d,[poll,(poll[0]-0.16*sc,poll[1]-0.05*sc),(poll[0]-0.10*sc,poll[1]+0.10*sc)],col)  # near ear back
    poly(d,[poll,(poll[0]+0.14*sc,poll[1]-0.02*sc),(poll[0]+0.06*sc,poll[1]+0.12*sc)],col)  # far ear
def hump(d,P,sc,col=INK):
    ell(d,(P('withers')[0],P('withers')[1]-0.02*sc),0.13*sc,0.10*sc,col)

# ============ THE TEN LENSES ============
def L1_mass(d,ox,oy,sc):
    P=C(ox,oy,sc); poly(d,silhouette_path(P)); hump(d,P,sc); legs_fill(d,P,sc); ears(d,P,sc)
def L2_outline(d,ox,oy,sc):
    P=C(ox,oy,sc); line(d,silhouette_path(P)+[silhouette_path(P)[0]],w=2.0)
    line(d,[P('chest'),P('carpus'),P('forehoof')],w=2.0); ears(d,P,sc,col=PAPER)  # no fill ears: draw as lines
    line(d,[P('poll'),(P('poll')[0]-0.14*sc,P('poll')[1]+0.06*sc)],w=2.0)
def L3_weight(d,ox,oy,sc):
    P=C(ox,oy,sc); line(d,silhouette_path(P)+[silhouette_path(P)[0]],col=FAINT,w=1.6)
    # heaviest mass (hindquarter) + ground contact rendered solid/dark = where weight goes
    ell(d,(P('hip')[0]-0.05*sc,P('hip')[1]-0.42*sc),0.40*sc,0.34*sc,col=INK)
    cap(d,P('brisket'),P('bellyrear'),0.10*sc,0.10*sc,col=INK)   # brisket/belly bearing on ground
    line(d,[P((-0.1,0.0)),P((2.0,0.0))],col=MID,w=1.4)            # ground
    # weight arrow at the centre of gravity, down into the base
    cog=(P('bellymid')[0]+0.05*sc, P('bellymid')[1]-0.35*sc)
    line(d,[cog,(cog[0],cog[1]+0.5*sc)],col=INK,w=2.4); poly(d,[(cog[0]-0.05*sc,cog[1]+0.42*sc),(cog[0]+0.05*sc,cog[1]+0.42*sc),(cog[0],cog[1]+0.55*sc)])
def L4_balance(d,ox,oy,sc):
    P=C(ox,oy,sc); line(d,silhouette_path(P)+[silhouette_path(P)[0]],col=FAINT,w=1.4)
    base=[P('forehoof'),P('rumpground')]                          # base of support along the ground
    line(d,base,col=INK,w=2.2)
    for b in base: line(d,[b,(b[0],b[1]-0.06*sc)],col=INK,w=2.2)   # base end-ticks
    cog=(P('bellymid')[0]+0.08*sc, P('bellymid')[1]-0.32*sc)
    dot(d,cog,0.05*sc,INK); line(d,[cog,(cog[0],oy)],col=INK,w=1.4) # plumb to ground, lands inside base
def L5_joints(d,ox,oy,sc):
    P=C(ox,oy,sc)
    spine=['hip','loin','withers','neckbase','poll']
    line(d,[P(k) for k in spine],col=INK,w=2.2)
    line(d,[P('poll'),P('nose')],col=INK,w=2.0)
    line(d,[P('withers'),P('elbow'),P('carpus'),P('forehoof')],col=INK,w=2.0)  # foreleg chain
    line(d,[P('hip'),P('stifle'),P('hock'),P('hindhoof')],col=INK,w=2.0)        # hind chain
    for k in ['hip','loin','withers','neckbase','poll','nose','elbow','carpus','forehoof','stifle','hock','hindhoof']:
        dot(d,P(k),0.035*sc,INK)
def L6_negative(d,ox,oy,sc):
    P=C(ox,oy,sc)
    d.rectangle([int((ox-0.5*sc)*SS),int((oy-1.5*sc)*SS),int((ox+2.3*sc)*SS),int((oy+0.35*sc)*SS)],fill=INK)
    poly(d,silhouette_path(P),col=PAPER); hump(d,P,sc,col=PAPER); legs_fill(d,P,sc,col=PAPER); ears(d,P,sc,col=PAPER)
    # the enclosed pockets the body makes with the ground stay dark (already dark) — mark the under-neck pocket
def L7_volumes(d,ox,oy,sc):
    P=C(ox,oy,sc)
    # construction solids, overlapping so they read as one connected chain
    ell(d,(P('hip')[0]+0.05*sc,P('hip')[1]-0.42*sc),0.42*sc,0.36*sc,outline=INK,w=2)     # hindquarter sphere
    ell(d,(P('bellymid')[0]+0.05*sc,P('bellymid')[1]-0.30*sc),0.52*sc,0.34*sc,outline=INK,w=2) # barrel ovoid
    ell(d,(P('withers')[0],P('withers')[1]-0.16*sc),0.24*sc,0.26*sc,outline=INK,w=2)     # shoulder+hump
    line(d,[P('neckbase'),(P('poll')[0]-0.04*sc,P('poll')[1]-0.02*sc)],col=INK,w=int(0.30*sc))  # neck cylinder (thick line as tube)
    ell(d,(P('foretop')[0]-0.06*sc,P('foretop')[1]-0.04*sc),0.20*sc,0.18*sc,outline=INK,w=2)    # head ovoid
    # leg tubes
    cap_outline(d,P('chest'),P('carpus'),0.10*sc); cap_outline(d,P('carpus'),P('forehoof'),0.06*sc)
    # a wrapping cross-contour on the barrel (shows it as a volume, not a flat shape)
    cx,cy=P('bellymid')[0]+0.05*sc,P('bellymid')[1]-0.30*sc
    d.arc([int((cx-0.20*sc)*SS),int((cy-0.30*sc)*SS),int((cx+0.20*sc)*SS),int((cy+0.30*sc)*SS)],-70,70,fill=INK,width=int(1.4*SS))
def cap_outline(d,a,b,r):
    a=np.array(a,float);b=np.array(b,float);v=b-a;L=np.hypot(*v)
    if L<1: return
    n=np.array([-v[1],v[0]])/L
    line(d,[a+n*r,b+n*r],w=1.6); line(d,[a-n*r,b-n*r],w=1.6)
def L8_flow(d,ox,oy,sc):
    P=C(ox,oy,sc)
    # the dominant arc: nose -> over poll -> down neck -> withers -> back -> hip -> rump
    arc=cm([P('nose'),P('poll'),P('withers'),P('loin'),P('hip'),P('rumpback')],26,closed=False)
    line(d,arc,col=INK,w=3.0)
    # secondary flows: the foreleg reach, the hind fold
    line(d,cm([P('chest'),P('carpus'),P('forehoof')],14,closed=False),col=MID,w=2.0)
    line(d,cm([P('hip'),P('stifle'),P('hindhoof')],14,closed=False),col=MID,w=2.0)
    # arrowhead on the main arc at the head
    n=P('nose'); line(d,[n,(n[0]-0.12*sc,n[1]-0.06*sc)],w=3.0); line(d,[n,(n[0]-0.12*sc,n[1]+0.08*sc)],w=3.0)
def L9_posture(d,ox,oy,sc):
    P=C(ox,oy,sc)
    # line of action: the lifted-head-to-settled-hip attitude in two strokes + ground
    line(d,cm([P('nose'),P('poll'),P('withers'),P('hip'),P('rumpground')],26,closed=False),col=INK,w=3.0)
    line(d,[P((0.0,0.0)),P('forehoof')],col=INK,w=2.4)   # the long ground contact = settled
    dot(d,P('foretop'),0.05*sc,INK)
def L10_fewest(d,ox,oy,sc):
    P=C(ox,oy,sc)
    line(d,cm([P('poll'),P('withers'),P('loin'),P('hip')],20,closed=False),w=3.0)   # the back
    line(d,[P('poll'),P('nose')],w=3.0)                                              # the head tilt
    line(d,[P('chest'),P('forehoof')],w=3.0)                                         # folded foreleg forward
    line(d,cm([P('hip'),P('rumpback'),P('rumpground')],14,closed=False),w=3.0)       # the hindquarter to ground
    line(d,[P('brisket'),P('bellyrear')],w=3.0)                                      # brisket on ground

LENSES=[("1 · mass",L1_mass),("2 · outline",L2_outline),("3 · weight",L3_weight),
        ("4 · balance",L4_balance),("5 · joints",L5_joints),("6 · negative space",L6_negative),
        ("7 · major volumes",L7_volumes),("8 · directional flow",L8_flow),
        ("9 · posture",L9_posture),("10 · fewest marks",L10_fewest)]

def render(path):
    cols,rows=5,2; cw,ch=300,300; W,H=cols*cw,rows*ch+10
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(11*SS))
    except: font=ImageFont.load_default()
    for i,(name,fn) in enumerate(LENSES):
        cxo=(i%cols)*cw; cyo=(i//cols)*ch
        ox=cxo+cw*0.30; oy=cyo+ch*0.66; sc=104
        fn(d,ox,oy,sc)
        d.text((int((cxo+12)*SS),int((cyo+ch-26)*SS)),name,fill=MID,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)

if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a32_one_cow.png")
