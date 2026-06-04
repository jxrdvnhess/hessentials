"""A50 — The Two Boughs. Tests the pointed-at lead: is the thin mark's power belonging (membership
in a larger whole), or any contact? One apple, fixed dead center in every panel. Two boughs above,
left and right. Only the thin mark changes.
  1 bare           — no mark
  2 stem to left   — same apple, stem to the left bough
  3 stem to right  — same apple, stem to the right bough
  4 both stems     — held twice
  5 grazed         — an equally thin line touches the apple but ends nowhere and owns nothing"""
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

def scene(d,ox,oy,mode):
    # left bough, tip at (118,72); right bough, tip at (182,78); inset from panel edges
    L(d,cmr([(ox+34,oy+52),(ox+78,oy+63),(ox+118,oy+72)]),w=3.0)
    L(d,cmr([(ox+68,oy+60),(ox+56,oy+78),(ox+68,oy+88)]),w=1.6)                     # leaf, left
    L(d,cmr([(ox+266,oy+56),(ox+224,oy+68),(ox+182,oy+78)]),w=3.0)
    L(d,cmr([(ox+232,oy+66),(ox+246,oy+82),(ox+234,oy+92)]),w=1.6)                  # leaf, right
    E(d,(ox+150,oy+150),15,16,INK)                                                  # the apple, fixed
    if mode in ('left','both'):
        L(d,cmr([(ox+118,oy+72),(ox+132,oy+104),(ox+147,oy+135)]),w=1.5)            # stem to left
    if mode in ('right','both'):
        L(d,cmr([(ox+182,oy+78),(ox+168,oy+108),(ox+153,oy+135)]),w=1.5)            # stem to right
    if mode=='graze':
        L(d,[(ox+81,oy+240),(ox+261,oy+60)],w=1.5)                                  # touches, owns nothing
PANELS=[("bare",'bare'),("stem to the left bough",'left'),("stem to the right bough",'right'),
        ("both stems",'both'),("grazed by a line",'graze')]
def render(path):
    cw,ch=300,300; W,H=5*cw,ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(12*SS))
    except: font=ImageFont.load_default()
    for i,(title,mode) in enumerate(PANELS):
        scene(d,i*cw,0,mode)
        tw=d.textlength(title,font=font)
        d.text((int(i*cw*SS+(cw*SS-tw)//2),int((ch-30)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a50_the_two_boughs.png")
