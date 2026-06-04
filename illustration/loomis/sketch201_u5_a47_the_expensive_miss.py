"""A47 — The Expensive Miss. The A46 right/meeting calf, five versions, each breaking exactly ONE
agreement. Break distance held constant (~0.09 body units) so location is the only variable.
Rank by damage to the statement: this is one animal."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
LM=dict(rumpback=(0.02,0.46), hip=(0.30,0.95), loin=(0.86,0.86), withers=(1.16,1.10),
 poll=(1.74,1.16), brisket=(1.13,0.10), bellymid=(0.80,0.13), forehoof=(1.78,0.03))
def cmr(nodes,n=26):
    P=[np.array(p,float) for p in nodes]; P=([P[0]]+P+[P[-1]]); out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(P[-2]); return out
def line(d,pts,col=INK,w=2.6): d.line([(int(p[0]*SS),int(p[1]*SS)) for p in pts],fill=col,width=max(1,int(w*SS)),joint="curve")
def ell(d,c,rx,ry,col): d.ellipse([int((c[0]-rx)*SS),int((c[1]-ry)*SS),int((c[0]+rx)*SS),int((c[1]+ry)*SS)],fill=col)

GAP=0.09  # uniform break distance, body units
def draw_calf(d,ox,oy,sc,brk=None):
    def Q(pt):
        x,y=LM[pt] if isinstance(pt,str) else pt
        return (ox+x*sc, oy-y*sc)
    hd=Q((1.90,1.0))
    def R(dx,dy): return (hd[0]+dx*sc, hd[1]+dy*sc)
    # 1 topline head->rump
    line(d,cmr([R(-0.02,-0.10),Q('poll'),Q('withers'),Q('loin'),Q('hip'),Q('rumpback')]),w=3.0)
    # 2 hump (brk: lifted off the back)
    w_=Q('withers')
    if brk=='hump': w_=(w_[0],w_[1]-GAP*sc)
    line(d,cmr([(w_[0]-0.16*sc,w_[1]-0.01*sc),(w_[0],w_[1]+0.15*sc),(w_[0]+0.16*sc,w_[1]-0.01*sc)]),w=2.6)
    # 3 rump->hind leg
    line(d,cmr([Q('rumpback'),Q((0.05,0.30)),Q((0.18,0.20)),Q((0.23,0.10)),Q((0.29,0.02))]),w=2.8)
    # 4 belly
    line(d,cmr([Q((1.24,0.24)),Q('brisket'),Q('bellymid'),Q((0.52,0.14)),Q((0.32,0.11))]),w=2.8)
    # 5 throat (brk: jaw end off the head)
    jaw=R(-0.12,0.20)
    if brk=='throat': jaw=(jaw[0]-0.035*sc,jaw[1]+0.083*sc)
    line(d,cmr([jaw,Q((1.56,0.52)),Q((1.36,0.30)),Q((1.21,0.20))]),w=2.4)
    # 6 head  7 muzzle (brk: off the head)  8 eye
    ell(d,hd,0.15*sc,0.14*sc,INK)
    mz=R(0.16,0.06)
    if brk=='muzzle': mz=(mz[0]+0.064*sc,mz[1]-0.064*sc)
    ell(d,mz,0.10*sc,0.08*sc,INK)
    ell(d,(hd[0]+0.02*sc,hd[1]-0.02*sc),0.026*sc,0.026*sc,PAPER)
    # 9 foreleg (brk 'leg': top off the body; brk 'hoof': end off the ground)
    s,m,e=Q((1.20,0.20)),Q((1.46,0.07)),Q('forehoof')
    if brk=='leg':  s=(s[0]+0.028*sc,s[1]+0.085*sc)
    if brk=='hoof': e=(e[0],e[1]-GAP*sc)
    line(d,cmr([s,m,e]),w=2.8)
    # 10 ground
    line(d,[(ox-0.15*sc,oy),(ox+2.55*sc,oy)],col=MID,w=1.8)

PANELS=[("unbroken",None),("hoof off the ground",'hoof'),("foreleg off the body",'leg'),
        ("throat off the head",'throat'),("muzzle off the head",'muzzle'),("hump off the back",'hump')]
def render(path):
    cols=3; rows=2; cw,ch=420,310; W,H=cols*cw,rows*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(12*SS))
    except: font=ImageFont.load_default()
    for i,(title,brk) in enumerate(PANELS):
        cxo=(i%cols)*cw; cyo=(i//cols)*ch
        draw_calf(d,cxo+cw*0.22,cyo+ch*0.64,118,brk=brk)
        tw=d.textlength(title,font=font)
        d.text((int(cxo*SS+(cw*SS-tw)//2),int((cyo+ch-32)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a47_the_expensive_miss.png")
