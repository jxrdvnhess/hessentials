"""SKETCH 201 · A4 REBUILD — observed figure rig.
A posable 2D mannequin filled to a clean human-reading silhouette. The pose and
proportions are READ from each real photograph (observe, then rebuild); the marks
are ours. Not extraction — selection. Every figure must read as a human with the
face removed."""
import cv2, numpy as np

UNIT=720  # px per body-height unit
def _x(v): return int((v[0]+0.5)*UNIT)
def _y(v): return int(v[1]*UNIT)

def capsule(mask, a, b, ra, rb):
    A=np.array([_x(a),_y(a)],float); B=np.array([_x(b),_y(b)],float)
    ra*=UNIT; rb*=UNIT
    d=B-A; L=np.hypot(*d)
    if L<1:
        cv2.circle(mask,tuple(A.astype(int)),int(max(ra,rb)),255,-1); return
    n=np.array([-d[1],d[0]])/L
    poly=np.array([A+n*ra, B+n*rb, B-n*rb, A-n*ra]).astype(np.int32)
    cv2.fillConvexPoly(mask,poly,255)
    cv2.circle(mask,tuple(A.astype(int)),int(ra),255,-1)
    cv2.circle(mask,tuple(B.astype(int)),int(rb),255,-1)

def ellipse(mask, c, rx, ry, ang=0):
    cv2.ellipse(mask,(_x(c),_y(c)),(int(rx*UNIT),int(ry*UNIT)),ang,0,360,255,-1)

def torso(mask, shL,shR,hpL,hpR, waist=0.86, shround=0.055, neck=None):
    # smooth tapered trunk: shoulders -> waist pinch -> hips, as a filled curve
    midL=((shL[0]*0.5+hpL[0]*0.5)*waist,(shL[1]+hpL[1])/2)
    midR=((shR[0]*0.5+hpR[0]*0.5)*waist,(shR[1]+hpR[1])/2)
    pts=[shL,midL,hpL,hpR,midR,shR]
    poly=np.array([[_x(p),_y(p)] for p in pts],np.int32)
    cv2.fillPoly(mask,[poly],255)
    # trapezius: slope the neck base into the shoulders so the shoulder LINE reads (not a flat bar)
    if neck is not None:
        tri=np.array([[_x(neck),_y(neck)],[_x(shL),_y(shL)],[_x(shR),_y(shR)]],np.int32)
        cv2.fillPoly(mask,[tri],255)
    for p,r in [(shL,shround),(shR,shround),(hpL,0.07),(hpR,0.07)]:
        cv2.circle(mask,(_x(p),_y(p)),int(r*UNIT),255,-1)

def render(J, R, smooth=True):
    """J: joint dict, R: radii dict. Returns cropped grayscale alpha (255=figure)."""
    H=int(1.25*UNIT); W=int(1.0*UNIT)
    m=np.zeros((H,W),np.uint8)
    g=lambda k:J[k]
    # legs (draw first, behind)
    capsule(m,g('hpL'),g('knL'),R['thigh'],R['calf']); capsule(m,g('knL'),g('anL'),R['calf'],R['ankle'])
    capsule(m,g('hpR'),g('knR'),R['thigh'],R['calf']); capsule(m,g('knR'),g('anR'),R['calf'],R['ankle'])
    # feet
    for an,ft in [('anL','ftL'),('anR','ftR')]:
        capsule(m,g(an),g(ft),R['ankle'],R['ankle']*0.7)
    # arms
    capsule(m,g('shL'),g('elL'),R['uarm'],R['farm']); capsule(m,g('elL'),g('wrL'),R['farm'],R['wrist'])
    capsule(m,g('shR'),g('elR'),R['uarm'],R['farm']); capsule(m,g('elR'),g('wrR'),R['farm'],R['wrist'])
    for w in ('wrL','wrR'): cv2.circle(m,(_x(g(w)),_y(g(w))),int(R['hand']*UNIT),255,-1)
    # torso + neck + head
    torso(m,g('shL'),g('shR'),g('hpL'),g('hpR'),R.get('waist',0.86),R.get('shround',0.055),g('neck'))
    capsule(m,g('neck'),g('sh'),R['neck'],R['neck'])
    ellipse(m,g('head'),R['headx'],R['heady'],R.get('headang',0))
    # clean union -> single smooth silhouette
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
    cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c=max(cnts,key=cv2.contourArea)
    out=np.zeros_like(m); cv2.drawContours(out,[c],-1,255,cv2.FILLED)
    if smooth: out=cv2.GaussianBlur(out,(0,0),1.0)
    ys,xs=np.where(out>30)
    return out[ys.min():ys.max()+1, xs.min():xs.max()+1]

# default radii (body-height units)
def radii(**kw):
    d=dict(head_unused=0,neck=0.038,headx=0.072,heady=0.092,uarm=0.046,farm=0.034,
           wrist=0.026,hand=0.030,thigh=0.072,calf=0.050,ankle=0.030,waist=0.86)
    d.update(kw); return d

# standing default skeleton (x centered at 0, y: head-top 0 -> feet ~1.0)
def base():
    return dict(head=(0,0.075),neck=(0,0.155),sh=(0,0.20),
        shL=(-0.105,0.205),shR=(0.105,0.205),elL=(-0.135,0.345),elR=(0.135,0.345),
        wrL=(-0.15,0.475),wrR=(0.15,0.475),hip=(0,0.50),hpL=(-0.075,0.515),hpR=(0.075,0.515),
        knL=(-0.075,0.73),knR=(0.075,0.73),anL=(-0.075,0.965),anR=(0.075,0.965),
        ftL=(-0.115,0.995),ftR=(0.115,0.995))

def merge(d,**kw):
    e=dict(d); e.update(kw); return e

# ---- THREE TEST POSES, authored from observation ----
def omar_walker():
    J=base()
    # mid-stride, slight forward lean, arms swinging opposite legs
    J=merge(J, head=(0.01,0.075),neck=(0.01,0.155),sh=(0.0,0.20),
        shL=(-0.10,0.205),shR=(0.11,0.205),
        elL=(-0.115,0.34),elR=(0.145,0.345), wrL=(-0.085,0.46),wrR=(0.155,0.47),
        hpL=(-0.065,0.515),hpR=(0.075,0.515),
        knL=(-0.135,0.71),knR=(0.115,0.74),       # left knee forward(stride), right back
        anL=(-0.16,0.95),anR=(0.16,0.93),
        ftL=(-0.205,0.985),ftR=(0.115,0.965))
    return J, radii(thigh=0.066,calf=0.046)

def subhaan_seated():
    # seated, elbows on knees, leaning forward, head dropped. compressed height.
    J=dict(head=(0.0,0.18),neck=(0.0,0.27),sh=(0.0,0.31),
        shL=(-0.12,0.315),shR=(0.12,0.315),
        elL=(-0.165,0.55),elR=(0.165,0.55),          # elbows out on knees
        wrL=(-0.085,0.62),wrR=(0.085,0.62),           # forearms in toward center
        hip=(0,0.66),hpL=(-0.115,0.66),hpR=(0.115,0.66),
        knL=(-0.185,0.62),knR=(0.185,0.62),           # knees up, wide, near elbows
        anL=(-0.175,0.96),anR=(0.175,0.96),
        ftL=(-0.205,0.99),ftR=(0.205,0.99))
    return J, radii(thigh=0.082,calf=0.055,uarm=0.05,headx=0.078,heady=0.098,waist=0.95)

def dominic_dancer():
    # dynamic: torso upright-tilt, one leg planted, one extended/lifted, arms spread
    J=dict(head=(0.02,0.085),neck=(0.0,0.165),sh=(0.0,0.21),
        shL=(-0.11,0.205),shR=(0.11,0.215),
        elL=(-0.235,0.165),elR=(0.215,0.27),          # left arm up/out, right arm lower out
        wrL=(-0.33,0.11),wrR=(0.30,0.345),
        hip=(0,0.52),hpL=(-0.07,0.52),hpR=(0.075,0.52),
        knL=(-0.10,0.74),knR=(0.215,0.62),            # left leg planted, right leg lifted/extended out
        anL=(-0.105,0.97),anR=(0.36,0.69),
        ftL=(-0.145,0.995),ftR=(0.40,0.70))
    return J, radii(thigh=0.06,calf=0.043,uarm=0.04,farm=0.03)

if __name__=='__main__':
    import os
    OUT='/sessions/wizardly-stoic-cerf/mnt/outputs/reb'
    tests=[('omar',omar_walker()),('subhaan',subhaan_seated()),('dominic',dominic_dancer())]
    cells=[]
    for name,(J,R) in tests:
        a=render(J,R)
        h,w=a.shape; s=420/h; a=cv2.resize(a,(int(w*s),420))
        cv=np.full((440,max(220,a.shape[1]+40)),235,np.uint8)
        ox=(cv.shape[1]-a.shape[1])//2
        cv[10:10+a.shape[0],ox:ox+a.shape[1]]=np.where(a>30,40,cv[10:10+a.shape[0],ox:ox+a.shape[1]])
        cv=cv2.cvtColor(cv,cv2.COLOR_GRAY2BGR); cv2.putText(cv,name,(6,435),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,200),1)
        cells.append(cv)
    H=max(c.shape[0] for c in cells)
    cells=[cv2.copyMakeBorder(c,0,H-c.shape[0],0,10,cv2.BORDER_CONSTANT,value=(235,235,235)) for c in cells]
    cv2.imwrite(f'{OUT}/_rigtest.png',np.hstack(cells)); print('ok')
