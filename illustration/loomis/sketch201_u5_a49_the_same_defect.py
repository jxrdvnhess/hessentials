"""A49 — The Same Defect. Five pairs, no cow. Top row: the piece sits apart, nothing holds it.
Bottom row: identical position, one thin mark holds it. Only that mark differs."""
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

def branch(d,ox,oy,held):
    L(d,cmr([(ox+55,oy+255),(ox+62,oy+150),(ox+58,oy+45)]),w=4.2)                  # trunk
    L(d,cmr([(ox+60,oy+115),(ox+95,oy+125),(ox+128,oy+140)]),w=2.8)                # bough stub
    L(d,cmr([(ox+152,oy+152),(ox+195,oy+163),(ox+238,oy+178)]),w=2.8)              # broken piece
    L(d,[(ox+195,oy+163),(ox+212,oy+148)],w=2.0)                                   # its twiglet
    if held: L(d,cmr([(ox+128,oy+140),(ox+139,oy+143),(ox+152,oy+152)]),w=1.5)     # the one twig
def apple(d,ox,oy,held):
    L(d,cmr([(ox+15,oy+62),(ox+150,oy+74),(ox+285,oy+66)]),w=3.0)                  # bough
    L(d,cmr([(ox+95,oy+70),(ox+82,oy+88),(ox+95,oy+98)]),w=1.8)                    # leaf
    L(d,cmr([(ox+205,oy+70),(ox+220,oy+86),(ox+208,oy+96)]),w=1.8)                 # leaf
    E(d,(ox+150,oy+142),15,16,INK)                                                 # apple
    if held: L(d,cmr([(ox+150,oy+73),(ox+147,oy+100),(ox+150,oy+127)]),w=1.5)      # stem
def button(d,ox,oy,held):
    L(d,cmr([(ox+138,oy+45),(ox+134,oy+150),(ox+138,oy+252)]),w=2.6)               # placket edge
    L(d,cmr([(ox+172,oy+45),(ox+176,oy+150),(ox+172,oy+252)]),w=2.6)               # placket edge
    L(d,[(ox+138,oy+45),(ox+112,oy+25)],w=2.6); L(d,[(ox+172,oy+45),(ox+198,oy+25)],w=2.6)  # collar
    for y in (95,140): E(d,(ox+155,oy+y),7,7,INK)                                  # buttons on
    L(d,[(ox+149,oy+185),(ox+161,oy+185)],w=2.0)                                   # empty buttonhole
    E(d,(ox+190,oy+222),7,7,INK)                                                   # the loose button
    if held: L(d,cmr([(ox+155,oy+186),(ox+168,oy+200),(ox+184,oy+217)]),w=1.3)     # thread
def tile(d,ox,oy,held):
    L(d,[(ox+25,oy+118),(ox+275,oy+96)],w=3.0)                                     # eave line
    xs=[40,95,150,205]                                                             # tile row, one slot empty
    for i,x in enumerate(xs):
        if i==2: continue
        p=[(ox+x,oy+112-x*0.06),(ox+x+44,oy+108-x*0.06),(ox+x+38,oy+78-x*0.06),(ox+x-6,oy+82-x*0.06)]
        L(d,p+[p[0]],w=2.2)
    p=[(ox+150,oy+175),(ox+194,oy+171),(ox+188,oy+141),(ox+144,oy+145)]            # slid tile, below
    L(d,p+[p[0]],w=2.2)
    if held: L(d,[(ox+152,oy+101),(ox+146,oy+146)],w=1.5)                          # corner still caught
def boat(d,ox,oy,held):
    L(d,[(ox+10,oy+205),(ox+290,oy+205)],col=MID,w=1.8)                            # water
    L(d,[(ox+18,oy+148),(ox+105,oy+148)],w=3.0)                                    # dock
    for x in (30,68,100): L(d,[(ox+x,oy+148),(ox+x,oy+203)],w=2.4)                 # posts
    L(d,cmr([(ox+178,oy+186),(ox+196,oy+202),(ox+248,oy+202),(ox+262,oy+186)]),w=2.8)  # hull
    L(d,[(ox+178,oy+186),(ox+262,oy+186)],w=2.2)                                   # gunwale
    L(d,[(ox+218,oy+186),(ox+218,oy+152)],w=2.0)                                   # mast
    if held: L(d,cmr([(ox+100,oy+150),(ox+138,oy+176),(ox+180,oy+188)]),w=1.3)     # rope
PAIRS=[("branch off","branch by a twig",branch),("apple off","apple by its stem",apple),
       ("button off","button by a thread",button),("tile off","tile by a corner",tile),
       ("boat off","boat by a rope",boat)]
def render(path):
    cw,ch=300,300; W,H=5*cw,2*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(12*SS))
    except: font=ImageFont.load_default()
    for i,(ta,tb,fn) in enumerate(PAIRS):
        for r,(title,held) in enumerate([(ta,False),(tb,True)]):
            ox,oy=i*cw,r*ch
            fn(d,ox,oy,held)
            tw=d.textlength(title,font=font)
            d.text((int(ox*SS+(cw*SS-tw)//2),int((oy+ch-30)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a49_the_same_defect.png")
