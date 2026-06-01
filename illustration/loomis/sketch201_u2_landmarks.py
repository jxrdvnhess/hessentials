"""SKETCH 201 · UNIT 2 — A5: SAME POSE, DIFFERENT HUMANS.
Ten ordinary standers, same direction, FROZEN identical pose. Forbidden to separate
them by gesture / action / costume / props / face. Identity must come ONLY from observed
body landmarks: proportion, weight distribution, shoulder slope, neck length, torso shape,
hip structure, leg relationship, stance. The accent-killer: same pose, so only the real
measurements can do the work."""
import cv2, numpy as np
from sketch201_u2_rig import render, radii

# --- landmark standing figure: pose is FIXED; only these measurements vary ---
LD=dict(head_r=0.070, neck_len=0.045, sh_y=0.205, sh_w=0.105, sh_drop=0.022,
        torso_len=0.31, waist=0.86, hip_w=0.075, stance=0.075, cog=0.0,
        ankle_y=0.965, build=1.0)

def build(**ov):
    L=dict(LD); L.update(ov)
    hr=L['head_r']; hry=hr*1.28
    head_cy=L['sh_y']-L['neck_len']-hry
    sh_y=L['sh_y']; sw=L['sh_w']; dr=L['sh_drop']
    hip_y=sh_y+L['torso_len']; hx=L['cog']*0.5
    ak=L['ankle_y']; kn=hip_y+(ak-hip_y)*0.5; st=L['stance']
    J=dict(
        head=(0.0,head_cy), neck=(0.0, head_cy+hry*0.55), sh=(0.0,sh_y),
        shL=(-sw, sh_y+dr), shR=(sw, sh_y+dr),
        elL=(-sw-0.012, sh_y+0.145), elR=(sw+0.012, sh_y+0.145),
        wrL=(-sw-0.006, sh_y+0.275), wrR=(sw+0.006, sh_y+0.275),
        hip=(hx,hip_y), hpL=(-L['hip_w']+hx, hip_y), hpR=(L['hip_w']+hx, hip_y),
        knL=(-st*0.9+hx*0.5, kn), knR=(st*0.9+hx*0.5, kn),
        anL=(-st, ak), anR=(st, ak),
        ftL=(-st-0.035, 0.995), ftR=(st+0.035, 0.995))
    b=L['build']
    R=radii(thigh=0.060*b, calf=0.042*b, uarm=0.044*b, farm=0.031*b, wrist=0.024*b,
            hand=0.027*b, neck=0.032*b, headx=hr, heady=hry, waist=L['waist'])
    R['shround']=0.036
    return J,R

# render() needs to pass shround + neck into torso(); patch via wrapper
from sketch201_u2_rig import _x,_y,capsule,ellipse
import sketch201_u2_rig as skel
def render_lm(J,R):
    return render(J,R)

if __name__=='__main__':
    OUT='/sessions/wizardly-stoic-cerf/mnt/outputs/u2'
    import os; os.makedirs(OUT,exist_ok=True)
    tests=[('neutral',{}),
           ('long neck',dict(neck_len=0.085)),
           ('broad+heavy',dict(sh_w=0.135,build=1.28,waist=1.0,torso_len=0.30)),
           ('narrow+steep shoulders',dict(sh_w=0.088,sh_drop=0.05,build=0.9)),
           ('short legs / long torso',dict(torso_len=0.37)),
           ('long legs / short torso',dict(torso_len=0.25))]
    cells=[]
    for name,ov in tests:
        J,R=build(**ov); a=render(J,R)
        h,w=a.shape; s=440/h; a=cv2.resize(a,(int(w*s),440))
        cv=np.full((470,max(200,a.shape[1]+30)),236,np.uint8); ox=(cv.shape[1]-a.shape[1])//2
        cv[8:8+a.shape[0],ox:ox+a.shape[1]]=np.where(a>30,38,cv[8:8+a.shape[0],ox:ox+a.shape[1]])
        cv=cv2.cvtColor(cv,cv2.COLOR_GRAY2BGR); cv2.putText(cv,name,(4,463),cv2.FONT_HERSHEY_SIMPLEX,0.42,(0,0,200),1)
        cells.append(cv)
    Hm=max(c.shape[0] for c in cells)
    cells=[cv2.copyMakeBorder(c,0,Hm-c.shape[0],0,8,cv2.BORDER_CONSTANT,value=(235,235,235)) for c in cells]
    cv2.imwrite(f'{OUT}/_rigtest.png',np.hstack(cells)); print('ok')
