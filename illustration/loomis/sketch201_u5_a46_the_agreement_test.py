"""A46 — The Agreement Test. Tests the A45 lead (good marks create agreements) against accuracy.
2x2: right/meeting, right/missing, wrong/meeting, wrong/missing. Same ten marks per panel.
'Wrong' = distorted proportions (long low body, small head), all junctions still meet.
'Missing' = each junction stops short or overshoots; every mark individually plausible."""
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

def draw_calf(d,ox,oy,sc,wrong=False,missing=False):
    sx,sy=(1.30,0.74) if wrong else (1.0,1.0)
    hr=(0.10,0.094) if wrong else (0.15,0.14)          # head radii
    mr=(0.068,0.054) if wrong else (0.10,0.08)         # muzzle radii
    def Q(pt,k=None):
        x,y=LM[pt] if isinstance(pt,str) else pt
        x,y=x*sx,y*sy
        if missing and k:
            dx,dy=MISS[k]; x,y=x+dx,y+dy
        return (ox+x*sc, oy-y*sc)
    MISS=dict(top_s=(0.05,0.07), top_e=(-0.05,0.09), hoof_h=(0.0,0.06), belly_e=(-0.07,-0.03),
              throat_e=(0.07,0.09), fore_e=(-0.04,0.07), hump=(0.08,0.04), muz=(0.05,-0.035))
    hd=Q((1.90,1.0))                                    # head center (screen)
    hk=0.68 if wrong else 1.0                           # head-relative scale
    def R(dx,dy,k=None):                                # point relative to the actual head ball
        x,y=hd[0]+dx*sc*hk, hd[1]+dy*sc*hk
        if missing and k:
            mx,my=MISS[k]; x,y=x+mx*sc,y-my*sc
        return (x,y)
    # 1 topline head->rump (starts ON the head ball)
    line(d,cmr([R(-0.02,-0.10,'top_s'),Q('poll'),Q('withers'),Q('loin'),Q('hip'),Q('rumpback','top_e')]),w=3.0)
    # 2 hump
    w_=Q('withers','hump'); line(d,cmr([(w_[0]-0.16*sc,w_[1]-0.01*sc),(w_[0],w_[1]+0.15*sc),(w_[0]+0.16*sc,w_[1]-0.01*sc)]),w=2.6)
    # 3 rump->hind leg
    line(d,cmr([Q('rumpback'),Q((0.05,0.30)),Q((0.18,0.20)),Q((0.23,0.10)),Q((0.29,0.02),'hoof_h')]),w=2.8)
    # 4 belly (ends on hind leg)
    line(d,cmr([Q((1.24,0.24)),Q('brisket'),Q('bellymid'),Q((0.52,0.14)),Q((0.32,0.11),'belly_e')]),w=2.8)
    # 5 throat (starts at the jaw of the actual head, ends at chest)
    line(d,cmr([R(-0.12,0.20),Q((1.56,0.52)),Q((1.36,0.30)),Q((1.21,0.20),'throat_e')]),w=2.4)
    # 6 head ball  7 muzzle  8 eye
    ell(d,hd,hr[0]*sc,hr[1]*sc,INK)
    mz=R(0.16,0.06,'muz'); ell(d,mz,mr[0]*sc,mr[1]*sc,INK)
    ell(d,(hd[0]+0.02*sc*hk,hd[1]-0.02*sc*hk),0.026*sc*hk,0.026*sc*hk,PAPER)
    # 9 foreleg
    line(d,cmr([Q((1.20,0.20)),Q((1.46,0.07)),Q('forehoof','fore_e')]),w=2.8)
    # 10 ground
    gy=oy; line(d,[(ox-0.15*sc,gy),(ox+(2.15*sx+0.4)*sc,gy)],col=MID,w=1.8)

PANELS=[("Right marks, meeting",  dict(wrong=False,missing=False)),
        ("Right marks, missing",  dict(wrong=False,missing=True)),
        ("Wrong marks, meeting",  dict(wrong=True, missing=False)),
        ("Wrong marks, missing",  dict(wrong=True, missing=True))]
def render(path):
    cw,ch=520,330; W,H=2*cw,2*ch
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(13*SS))
    except: font=ImageFont.load_default()
    for i,(title,kw) in enumerate(PANELS):
        cxo=(i%2)*cw; cyo=(i//2)*ch
        draw_calf(d,cxo+cw*0.20,cyo+ch*0.66,118,**kw)
        tw=d.textlength(title,font=font)
        d.text((int(cxo*SS+(cw*SS-tw)//2),int((cyo+ch-38)*SS)),title,fill=INK,font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a46_the_agreement_test.png")
