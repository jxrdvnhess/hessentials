"""A31 — The Same Cow, Ten Times. From ten real resting-cow photographs (Unsplash, observed
via browser). Each cow is a single observed outline tracing the recumbent structure I saw:
nose/poll, low forward neck with dewlap, withers, a loin dip, the HIGH HIP, rump to ground,
the hind hoof tucked forward, the belly resting, the near foreleg folded forward to a hoof,
big side ear. No field, no herd, no atmosphere. Reconstructed, not traced. Ten configurations."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); LBL=(120,116,110)

def cm(nodes,n=22,closed=True):
    P=[np.array(p,float) for p in nodes]
    P=([P[-1]]+P+[P[0],P[1]]) if closed else ([P[0]]+P+[P[-1]])
    out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    return out

def _ell(draw,cx,cy,rx,ry):
    draw.ellipse([int((cx-rx)*SS),int((cy-ry)*SS),int((cx+rx)*SS),int((cy+ry)*SS)],fill=INK)
def _cap(draw,a,b,ra,rb):
    a=np.array(a,float);b=np.array(b,float);d=b-a;L=np.hypot(*d)
    if L<1: _ell(draw,a[0],a[1],ra,ra); return
    n=np.array([-d[1],d[0]])/L
    draw.polygon([(int(p[0]*SS),int(p[1]*SS)) for p in [a+n*ra,b+n*rb,b-n*rb,a-n*ra]],fill=INK)
    _ell(draw,a[0],a[1],ra,ra); _ell(draw,b[0],b[1],rb,rb)

def cow(draw, ox, oy, s, P, f=-1):
    g=lambda k,d: P.get(k,d)
    nu=g('head_u',1.18); na=g('head_fwd',1.08)          # nose height / forward distance
    hiph=g('hiph',1.12); loin=g('loin',0.95); wth=g('withers',1.06)
    fe=g('foreleg_ext',0.55); hump=g('hump',0.0)
    def pt(a,u): return (ox + f*a*s, oy - u*s)
    # ---- TORSO outline (shorter, bulkier barrel); foreleg drawn separately to avoid notches ----
    O=[
      pt(0.16,0.62),                     # chest-front top (neck attaches here)
      pt(-0.03, wth+hump+0.02),          # withers (+hump)
      pt(0.48, wth),                     # behind withers
      pt(0.95, loin),                    # loin dip
      pt(1.36, hiph),                    # HIP (high point)
      pt(1.62, hiph-0.12),               # tailhead
      pt(1.80, 0.55),                    # rump back
      pt(1.66, 0.0),                     # rump to ground (rear)
      pt(1.18, 0.11),                    # belly resting (rear)
      pt(0.66, 0.18),                    # belly mid (rounded, higher barrel)
      pt(0.30, 0.12),                    # brisket bottom
      pt(0.16, 0.40),                    # chest-front bottom
    ]
    if g('shaggy',False):
        rng=np.random.default_rng(g('seed',1))
        O=[(x+f*rng.uniform(-0.05,0.05)*s, y+rng.uniform(-0.05,0.05)*s) for (x,y) in O]
    draw.polygon([(int(p[0]*SS),int(p[1]*SS)) for p in cm(O,20)], fill=INK)
    # near foreleg: folded forward to a hoof on the ground (separate capsules)
    _cap(draw, pt(0.22,0.44), pt(-0.05,0.18), 0.13*s, 0.085*s)
    _cap(draw, pt(-0.05,0.18), pt(-(0.30+fe),0.03), 0.085*s, 0.055*s)
    # tucked hind hoof wedge, forward of the rump
    hh=[pt(1.18,0.0),pt(0.90,0.0),pt(1.06,0.16)]
    draw.polygon([(int(p[0]*SS),int(p[1]*SS)) for p in hh],fill=INK)
    # ---- NECK (thick) from the crest to the head ----
    crest=pt(0.26,1.0); head=pt(-na,nu)
    _cap(draw,crest,head, 0.32*s, 0.18*s)
    # ---- HEAD: forehead + a distinct projecting muzzle (two lobes, not a knob) ----
    hx,hy=head
    _ell(draw,hx,hy,0.21*s,0.20*s)                       # forehead/skull
    mz=(hx+f*0.30*s, hy+0.07*s)                           # muzzle clearly forward
    _ell(draw,mz[0],mz[1],0.16*s,0.115*s)
    _cap(draw,(hx,hy),mz,0.15*s,0.12*s)                   # bridge of the face
    # ---- ears: big, off the back of the skull, out & slightly down ----
    er=g('ear',0.30)
    eb=(hx-f*0.02*s, hy-0.08*s)
    draw.polygon([(int(eb[0]*SS),int(eb[1]*SS)),
                  (int((eb[0]-f*er*1.2*s)*SS),int((eb[1]-er*0.25*s)*SS)),
                  (int((eb[0]-f*er*0.9*s)*SS),int((eb[1]+er*0.6*s)*SS))],fill=INK)
    # ---- dewlap: skin hanging under the neck/throat ----
    if g('dewlap',0.0)>0:
        dn=[pt(0.16,0.58),(hx+f*0.04*s,hy-0.12*s),pt(-0.18,0.05),pt(0.10,0.08)]
        draw.polygon([(int(p[0]*SS),int(p[1]*SS)) for p in dn],fill=INK)
    # ---- horns optional, off the top of the skull ----
    if g('horns',False):
        ho=g('horn',0.20)
        for dx in (-0.06,0.06):
            bx,by=hx+f*dx*s, hy-0.16*s
            draw.line([(int(bx*SS),int(by*SS)),(int((bx+f*(dx>0 and ho or -ho*0.2)*s)*SS),int((by-ho*0.9*s)*SS))],fill=INK,width=int(0.085*s*SS))

COWS=[
 dict(label="1 zebu calf",   head_u=1.24,head_fwd=0.86,hump=0.20,ear=0.40,dewlap=0.6,hiph=0.92,loin=0.80,withers=0.92,foreleg_ext=0.60),
 dict(label="2 highland low", head_u=0.70,head_fwd=0.96,horns=True,shaggy=True,seed=3,ear=0.24,dewlap=0.4,hiph=1.0,loin=0.86,withers=1.04),
 dict(label="3 highland prof",head_u=1.06,head_fwd=0.82,horns=True,shaggy=True,seed=7,ear=0.26,hiph=1.04,loin=0.92),
 dict(label="4 slope cow",    head_u=1.14,head_fwd=0.80,ear=0.32,dewlap=0.55,hiph=1.05,loin=0.95),
 dict(label="5 holstein",     head_u=1.16,head_fwd=0.78,hiph=1.26,loin=0.82,withers=1.02,ear=0.30,foreleg_ext=0.44),
 dict(label="6 black calf",   head_u=1.20,head_fwd=0.82,hiph=0.88,loin=0.80,withers=0.94,ear=0.34,foreleg_ext=0.56),
 dict(label="7 grazing rest", head_u=0.52,head_fwd=1.04,ear=0.30,dewlap=0.38,hiph=1.04,loin=0.92),
 dict(label="8 head low horns",head_u=0.64,head_fwd=0.94,horns=True,ear=0.28,dewlap=0.55,hiph=1.02,loin=0.9),
 dict(label="9 limousin",     head_u=1.18,head_fwd=0.78,horns=True,ear=0.34,dewlap=0.6,hiph=1.12,loin=0.96,foreleg_ext=0.60),
 dict(label="10 meadow cow",  head_u=1.08,head_fwd=0.80,ear=0.31,hiph=1.05,loin=0.94,foreleg_ext=0.50),
]

def render(path):
    W,H=1540,740
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(10*SS))
    except: font=ImageFont.load_default()
    cols=5; cw=W/cols; rh=H/2
    for i,P in enumerate(COWS):
        cx=(i%cols)*cw + cw*0.56; cy=(i//cols)*rh + rh*0.60
        f=-1 if i%2==0 else 1
        cow(d, cx, cy, 80, P, f)
        d.text((int(((i%cols)*cw+14)*SS), int(((i//cols)*rh+rh-24)*SS)), P['label'], fill=LBL, font=font)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)

if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a31_cow_studies.png")
