"""A51 — The Strange Panel. Only the both-stems apple. Six panels, ONE variable changed per panel
from the A50 baseline (apple fixed at center, always two stems, always two boughs)."""
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

def boughL(d,o,tip,start=(34,52)):
    L(d,cmr([(o[0]+start[0],o[1]+start[1]),(o[0]+(start[0]+tip[0])//2+6,o[1]+(start[1]+tip[1])//2),(o[0]+tip[0],o[1]+tip[1])]),w=3.0)
def boughR(d,o,tip,start=(266,56)):
    L(d,cmr([(o[0]+start[0],o[1]+start[1]),(o[0]+(start[0]+tip[0])//2-6,o[1]+(start[1]+tip[1])//2),(o[0]+tip[0],o[1]+tip[1])]),w=3.0)
def appleball(d,o): E(d,(o[0]+150,o[1]+150),15,16,INK)

def p_length(d,o):   # shorter stems (boughs lowered, same spread)
    boughL(d,o,(118,128),start=(34,108)); boughR(d,o,(182,134),start=(266,112)); appleball(d,o)
    L(d,cmr([(o[0]+118,o[1]+128),(o[0]+132,o[1]+133),(o[0]+146,o[1]+138)]),w=1.5)
    L(d,cmr([(o[0]+182,o[1]+134),(o[0]+168,o[1]+138),(o[0]+154,o[1]+138)]),w=1.5)
def p_angle(d,o):    # stems arrive at the apple's sides
    boughL(d,o,(118,72)); boughR(d,o,(182,78)); appleball(d,o)
    L(d,cmr([(o[0]+118,o[1]+72),(o[0]+112,o[1]+110),(o[0]+126,o[1]+144),(o[0]+136,o[1]+151)]),w=1.5)
    L(d,cmr([(o[0]+182,o[1]+78),(o[0]+190,o[1]+112),(o[0]+174,o[1]+146),(o[0]+164,o[1]+151)]),w=1.5)
def p_thick(d,o):    # thick stems
    boughL(d,o,(118,72)); boughR(d,o,(182,78)); appleball(d,o)
    L(d,cmr([(o[0]+118,o[1]+72),(o[0]+132,o[1]+104),(o[0]+147,o[1]+135)]),w=3.2)
    L(d,cmr([(o[0]+182,o[1]+78),(o[0]+168,o[1]+108),(o[0]+153,o[1]+135)]),w=3.2)
def p_asym(d,o):     # one taut, one slack
    boughL(d,o,(118,72)); boughR(d,o,(182,78)); appleball(d,o)
    L(d,[(o[0]+118,o[1]+72),(o[0]+147,o[1]+135)],w=1.5)
    L(d,cmr([(o[0]+182,o[1]+78),(o[0]+188,o[1]+116),(o[0]+168,o[1]+132),(o[0]+153,o[1]+136)]),w=1.5)
def p_close(d,o):    # branches close together
    boughL(d,o,(138,70)); boughR(d,o,(162,74)); appleball(d,o)
    L(d,cmr([(o[0]+138,o[1]+70),(o[0]+142,o[1]+102),(o[0]+146,o[1]+134)]),w=1.5)
    L(d,cmr([(o[0]+162,o[1]+74),(o[0]+158,o[1]+104),(o[0]+154,o[1]+134)]),w=1.5)
def p_height(d,o):   # branches uneven (one high, one low)
    boughL(d,o,(112,46),start=(34,30)); boughR(d,o,(186,112),start=(266,96)); appleball(d,o)
    L(d,cmr([(o[0]+112,o[1]+46),(o[0]+128,o[1]+90),(o[0]+146,o[1]+134)]),w=1.5)
    L(d,cmr([(o[0]+186,o[1]+112),(o[0]+170,o[1]+124),(o[0]+155,o[1]+138)]),w=1.5)

PANELS=[("shorter stems",p_length),("stems to the sides",p_angle),("thick stems",p_thick),
        ("one taut, one slack",p_asym),("branches close",p_close),("branches uneven",p_height)]
def render(path):
    cw,ch=300,300; W,H=3*cw,2*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(12*SS))
    except: font=ImageFont.load_default()
    for i,(title,fn) in enumerate(PANELS):
        o=((i%3)*cw,(i//3)*ch)
        fn(d,o)
        tw=d.textlength(title,font=font)
        d.text((int(o[0]*SS+(cw*SS-tw)//2),int((o[1]+ch-30)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a51_the_strange_panel.png")
