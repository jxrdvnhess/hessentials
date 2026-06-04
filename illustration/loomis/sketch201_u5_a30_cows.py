"""A30 — The First Mark. Only this: a herd of cows lying down in a field.
No sky drama, no weather, no atmosphere, no cleverness. Plain filled silhouettes on warm
paper, one groundline. A drawing that declares itself made."""
import numpy as np
from PIL import Image, ImageDraw
SS=3
PAPER=(237,232,223); INK=(43,43,53); FAINT=(176,172,164)
W,H=1180,520

def catmull(nodes,n=24):
    P=[np.array(p,float) for p in nodes]; out=[]
    P=[P[0]]+P+[P[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for t in np.linspace(0,1,n,endpoint=False):
            t2=t*t;t3=t2*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(P[-2]); return out

def cow(draw, x, y, s, face=-1):
    """x,y = front-bottom anchor; s scale; a recumbent cow in profile, head up.
    body sits flat on the ground (no standing legs) = lying down."""
    L=2.05*s; Hb=0.82*s
    def P(dx,dy): return (x+face*dx*L, y-dy*Hb)   # dx along body (0=front), dy up (0=ground)
    # body outline, front(chest) -> shoulder hump -> back -> rump -> ground
    body=[P(0.02,0.50),P(0.10,0.74),P(0.26,0.98),P(0.46,0.86),P(0.66,0.90),
          P(0.86,0.78),P(0.99,0.46),P(1.00,0.10),P(0.93,0.0),P(0.06,0.0)]
    pts=[ (a,b) for a,b in catmull(body,22) ]
    draw.polygon([(int(a*SS),int(b*SS)) for a,b in pts], fill=INK)
    # neck + head, rising off the chest at the front
    nb_x,nb_y = P(0.06,0.62)
    head_cx,head_cy = (x+face*-0.16*L, y-1.04*Hb)
    neck=[P(0.02,0.50),P(0.10,0.74),(x+face*-0.02*L,y-0.92*Hb),(head_cx+face*0.07*L,head_cy+0.10*Hb),
          (head_cx+face*0.05*L,head_cy-0.10*Hb),(x+face*-0.06*L,y-0.74*Hb),P(0.10,0.55)]
    draw.polygon([(int(a*SS),int(b*SS)) for a,b in neck], fill=INK)
    # head (muzzle) — small rounded mass
    hw,hh=0.22*s,0.16*s
    draw.ellipse([int((head_cx-hw)*SS),int((head_cy-hh)*SS),int((head_cx+hw)*SS),int((head_cy+hh)*SS)],fill=INK)
    # ears — two small triangles atop the head
    er=0.10*s
    for o in (0.02,0.12):
        ex=head_cx+face*o*L*0.0+face*(0.02+o)*s*1.0
        ey=head_cy-hh*0.6
        draw.polygon([(int((ex)*SS),int((ey)*SS)),
                      (int((ex+face*er)*SS),int((ey-er*1.3)*SS)),
                      (int((ex+face*er*1.4)*SS),int((ey-er*0.2)*SS))],fill=INK)

def render(path):
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    # the field: one quiet far edge, above the herd so it never cuts a body
    far=int(H*0.45)
    d.line([(int(W*0.06*SS),far*SS),(int(W*0.94*SS),far*SS)],fill=FAINT,width=SS)
    # a herd lying down — varied size/position (nearer=lower&bigger), all settled the same way
    herd=[(170,386,82,-1),(362,372,70,-1),(560,394,90,-1),(770,376,74,-1),
          (250,326,52,-1),(620,322,50,-1),(940,388,80,-1)]
    # draw far (smaller, higher) first
    for (x,y,s,f) in sorted(herd,key=lambda c:c[1]):
        cow(d,x,y,s,f)
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)

if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a30_cows.png")
