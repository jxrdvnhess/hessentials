"""A52 — The Intentional Object. One stone, identical in every panel (center 150,150, rx27 ry19).
Six relationships: alone / naturally supported / gently held / suspended / presented / constrained.
Blind pass renders captionless + shuffled; final pass captioned in canonical order."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, math
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
def L(d,pts,col=INK,w=2.6):
    d.line([(int(x*SS),int(y*SS)) for x,y in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def E(d,c,rx,ry,col): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],fill=col)
def cmr(nodes,n=22):
    P=[np.array(p,float) for p in nodes]; P=([P[0]]+P+[P[-1]]); out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(tuple(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3)))
    out.append(tuple(P[-2])); return out
CX,CY,RX,RY=150,150,27,19
def stone(d,o): E(d,(o[0]+CX,o[1]+CY),RX,RY,INK)

def p_alone(d,o): stone(d,o)
def p_supported(d,o):
    L(d,[(o[0]+20,o[1]+169),(o[0]+280,o[1]+169)],col=MID,w=1.8); stone(d,o)
def p_held(d,o):
    stone(d,o)
    L(d,cmr([(o[0]+112,o[1]+138),(o[0]+122,o[1]+168),(o[0]+150,o[1]+177),(o[0]+178,o[1]+168),(o[0]+188,o[1]+138)]),w=1.8)
def p_suspended(d,o):
    L(d,[(o[0]+150,o[1]+18),(o[0]+150,o[1]+132)],w=1.5); stone(d,o)
def p_presented(d,o):
    stone(d,o)
    L(d,[(o[0]+118,o[1]+170),(o[0]+182,o[1]+170)],w=2.6)                       # slab
    L(d,[(o[0]+132,o[1]+171),(o[0]+128,o[1]+238)],w=2.4)                       # plinth sides
    L(d,[(o[0]+168,o[1]+171),(o[0]+172,o[1]+238)],w=2.4)
    L(d,[(o[0]+118,o[1]+240),(o[0]+182,o[1]+240)],w=2.6)                       # base
def p_constrained(d,o):
    stone(d,o)
    L(d,[(o[0]+110,o[1]+118),(o[0]+190,o[1]+118)],w=2.4)                       # cage frame
    L(d,[(o[0]+110,o[1]+182),(o[0]+190,o[1]+182)],w=2.4)
    L(d,[(o[0]+110,o[1]+118),(o[0]+110,o[1]+182)],w=2.4)
    L(d,[(o[0]+190,o[1]+118),(o[0]+190,o[1]+182)],w=2.4)
    for x in (126,142,158,174):                                                # bars, in front of the stone
        dx=x-CX
        if abs(dx)<RX:
            dy=RY*math.sqrt(1-(dx/RX)**2)
            L(d,[(o[0]+x,o[1]+118),(o[0]+x,o[1]+CY-dy)],w=2.0)
            L(d,[(o[0]+x,o[1]+CY-dy),(o[0]+x,o[1]+CY+dy)],col=PAPER,w=2.0)
            L(d,[(o[0]+x,o[1]+CY+dy),(o[0]+x,o[1]+182)],w=2.0)
        else:
            L(d,[(o[0]+x,o[1]+118),(o[0]+x,o[1]+182)],w=2.0)

CANON=[("alone",p_alone),("naturally supported",p_supported),("gently held",p_held),
       ("suspended",p_suspended),("presented",p_presented),("constrained",p_constrained)]
BLIND_ORDER=[3,0,4,5,1,2]   # shuffled
def render(path,blind=False):
    cw,ch=300,300; W,H=3*cw,2*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(12*SS))
    except: font=ImageFont.load_default()
    seq=[CANON[i] for i in BLIND_ORDER] if blind else CANON
    for i,(title,fn) in enumerate(seq):
        o=((i%3)*cw,(i//3)*ch)
        fn(d,o)
        if not blind:
            tw=d.textlength(title,font=font)
            d.text((int(o[0]*SS+(cw*SS-tw)//2),int((o[1]+ch-30)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/outputs/_intent_blind.png",blind=True)
