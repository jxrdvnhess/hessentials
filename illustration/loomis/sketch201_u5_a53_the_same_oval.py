"""A53 — The Same Oval. Tests A52's banked claim: can a relationship change the KIND of thing the
viewer believes they are looking at? One identical filled oval (150,150 rx24 ry17) in six panels;
only the relationship differs. Blind pass: captionless + shuffled, name the object in each panel."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
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
CX,CY,RX,RY=150,150,24,17
def oval(d,o): E(d,(o[0]+CX,o[1]+CY),RX,RY,INK)

def p_bough(d,o):     # hanging by a stem from a bough
    L(d,cmr([(o[0]+30,o[1]+58),(o[0]+150,o[1]+70),(o[0]+270,o[1]+62)]),w=3.0)
    L(d,cmr([(o[0]+150,o[1]+69),(o[0]+147,o[1]+100),(o[0]+150,o[1]+134)]),w=1.5)
    oval(d,o)
def p_nest(d,o):      # in a nest of crossing sticks
    oval(d,o)
    L(d,cmr([(o[0]+108,o[1]+150),(o[0]+128,o[1]+174),(o[0]+170,o[1]+176),(o[0]+194,o[1]+154)]),w=1.8)
    L(d,cmr([(o[0]+116,o[1]+162),(o[0]+148,o[1]+182),(o[0]+186,o[1]+164)]),w=1.6)
    L(d,[(o[0]+104,o[1]+158),(o[0]+126,o[1]+150)],w=1.4)
    L(d,[(o[0]+176,o[1]+150),(o[0]+198,o[1]+160)],w=1.4)
def p_water(d,o):     # on a water line
    L(d,[(o[0]+20,o[1]+158),(o[0]+280,o[1]+158)],col=MID,w=1.8)
    L(d,cmr([(o[0]+60,o[1]+164),(o[0]+76,o[1]+160),(o[0]+92,o[1]+164)]),col=MID,w=1.4)
    L(d,cmr([(o[0]+208,o[1]+164),(o[0]+224,o[1]+160),(o[0]+240,o[1]+164)]),col=MID,w=1.4)
    oval(d,o)
def p_string(d,o):    # suspended from above
    L(d,[(o[0]+150,o[1]+18),(o[0]+150,o[1]+134)],w=1.5); oval(d,o)
def p_plinth(d,o):    # presented
    oval(d,o)
    L(d,[(o[0]+118,o[1]+168),(o[0]+182,o[1]+168)],w=2.6)
    L(d,[(o[0]+132,o[1]+169),(o[0]+128,o[1]+236)],w=2.4)
    L(d,[(o[0]+168,o[1]+169),(o[0]+172,o[1]+236)],w=2.4)
    L(d,[(o[0]+118,o[1]+238),(o[0]+182,o[1]+238)],w=2.6)
def p_ground(d,o):    # on the ground
    L(d,[(o[0]+20,o[1]+167),(o[0]+280,o[1]+167)],col=MID,w=1.8); oval(d,o)

CANON=[("by a stem, from a bough",p_bough),("in a nest",p_nest),("on water",p_water),
       ("by a string, from above",p_string),("on a plinth",p_plinth),("on the ground",p_ground)]
BLIND_ORDER=[4,2,0,5,3,1]
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
    render("/sessions/wizardly-stoic-cerf/mnt/outputs/_oval_blind.png",blind=True)
