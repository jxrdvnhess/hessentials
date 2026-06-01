"""A5 — SAME POSE, DIFFERENT HUMANS. Ten standers, one frozen pose, no gesture/costume/
face. Each built ONLY from observed landmarks. Validation compares each rendered silhouette
to its photo crop so the differences stay observed, not invented."""
import cv2, numpy as np, glob, os
from sketch201_u2_landmarks import build
from sketch201_u2_rig import render
SRC="/sessions/wizardly-stoic-cerf/mnt/Sketch 201 Reference Library"
OUTDIR="/sessions/wizardly-stoic-cerf/mnt/outputs/u2"
F=sorted(glob.glob(f"{SRC}/*.jpg"))
def g(n): return [x for x in F if n in os.path.basename(x)][0]

# observed landmark reads (relative differences grounded in the photos)
PEOPLE=[
 ('bruno',   'bruno-ngar',      (.30,.11,.61,.99), dict(sh_w=0.104,build=1.00,torso_len=0.310,neck_len=0.045,sh_drop=0.026,head_r=0.070,stance=0.070)),
 ('cemrecan','cemrecan',        (.46,.06,.78,.99), dict(sh_w=0.090,build=0.88,torso_len=0.265,neck_len=0.072,sh_drop=0.030,head_r=0.065)),
 ('cole',    'cole-keister',    (.41,.17,.73,.97), dict(sh_w=0.126,build=1.16,torso_len=0.335,waist=0.96,hip_w=0.085,sh_drop=0.016,stance=0.090,head_r=0.073)),
 ('jose',    'jose-nicdao',     (.36,.26,.65,.95), dict(sh_w=0.106,build=1.07,torso_len=0.320,waist=1.01,hip_w=0.082,sh_drop=0.046,neck_len=0.038,cog=0.07,head_r=0.071)),
 ('zachary', 'zachary',         (.42,.17,.65,.97), dict(sh_w=0.092,build=0.90,torso_len=0.300,sh_drop=0.030,neck_len=0.054)),
 ('omar',    'omar-tursic',     (.33,.16,.64,.99), dict(sh_w=0.118,build=1.00,torso_len=0.300,waist=0.80,hip_w=0.068,sh_drop=0.020)),
 ('linkedin','linkedin',        (.39,.19,.63,.98), dict(sh_w=0.128,build=1.12,torso_len=0.312,waist=0.90,sh_drop=0.016,stance=0.082,head_r=0.072)),
 ('nima',    'nima-mot',        (.43,.24,.66,.96), dict(sh_w=0.098,build=0.93,torso_len=0.305,sh_drop=0.026,neck_len=0.048)),
 ('talha',   'talha-khani',     (.38,.18,.64,.99), dict(sh_w=0.089,build=0.86,torso_len=0.262,neck_len=0.074,sh_drop=0.034,head_r=0.064)),
 ('wassim',  'wassim',          (.38,.14,.63,.99), dict(sh_w=0.096,build=0.91,torso_len=0.305,sh_drop=0.048,neck_len=0.050)),
]

def sil(ov):
    J,R=build(**ov); return render(J,R)

def validate():
    cells=[]
    for name,sub,bx,ov in PEOPLE:
        a=sil(ov); h,w=a.shape; s=360/h; a=cv2.resize(a,(int(w*s),360))
        sc=np.full((375,max(150,a.shape[1]+24)),236,np.uint8); ox=(sc.shape[1]-a.shape[1])//2
        sc[6:6+a.shape[0],ox:ox+a.shape[1]]=np.where(a>30,38,sc[6:6+a.shape[0],ox:ox+a.shape[1]])
        sc=cv2.cvtColor(sc,cv2.COLOR_GRAY2BGR)
        im=cv2.imread(g(sub));H,W=im.shape[:2]
        c=im[int(H*bx[1]):int(H*bx[3]),int(W*bx[0]):int(W*bx[2])]
        s2=360/c.shape[0]; c=cv2.resize(c,(int(c.shape[1]*s2),360)); c=cv2.convertScaleAbs(c,alpha=1.2,beta=15)
        c=cv2.copyMakeBorder(c,15,0,0,0,cv2.BORDER_CONSTANT,value=(0,0,0))
        cell=np.vstack([c, np.full((max(0,sc.shape[0]-0),0,3),0,np.uint8)]) if False else None
        pair=np.hstack([c, cv2.copyMakeBorder(sc,0,c.shape[0]-sc.shape[0] if c.shape[0]>sc.shape[0] else 0,0,0,cv2.BORDER_CONSTANT,value=(236,236,236))])
        cv2.putText(pair,name,(4,12),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,210),1)
        cells.append(pair)
    Hm=max(c.shape[0] for c in cells); Wm=max(c.shape[1] for c in cells)
    cells=[cv2.copyMakeBorder(c,0,Hm-c.shape[0],0,Wm-c.shape[1],cv2.BORDER_CONSTANT,value=(60,60,60)) for c in cells]
    rows=[np.hstack(cells[i:i+5]) for i in range(0,10,5)]
    cv2.imwrite(f"{OUTDIR}/_a5_validate.png",np.vstack(rows)); print("validate ok")

def plate(path, show_baseline=True):
    from PIL import Image, ImageDraw, ImageFont
    PAPER=(237,232,223); INK=(33,31,29); LBL=(96,94,90); FAINT=(178,174,166); SS=2
    COLS=10; cell_w=210; left=64; top=160
    W=left*2+COLS*cell_w; H=top+640+90
    canvas=np.full((H*SS,W*SS,3),PAPER[::-1],np.uint8)
    maxh=int(560*0.99)*SS; maxw=int(cell_w*0.84)*SS
    # common scale so heights are comparable (same pose, real proportion drives the read)
    sils=[sil(ov) for *_,ov in PEOPLE]
    Hmax=max(a.shape[0] for a in sils)
    for k,a in enumerate(sils):
        s=min(maxh/Hmax, maxw/max(x.shape[1] for x in sils))
        nw,nh=int(a.shape[1]*s),int(a.shape[0]*s)
        a=cv2.resize(a,(nw,nh),interpolation=cv2.INTER_AREA)
        cell_x=(left+k*cell_w)*SS; base=(top+580)*SS
        ox=cell_x+(cell_w*SS-nw)//2; oy=base-nh
        reg=canvas[oy:oy+nh,ox:ox+nw].astype(np.float32); al=(a/255.0)[...,None]
        canvas[oy:oy+nh,ox:ox+nw]=(reg*(1-al)+np.array(INK[::-1],np.float32)*al).astype(np.uint8)
    img=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB)); D=ImageDraw.Draw(img)
    def font(px):
        for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
            try: return ImageFont.truetype(p,int(px*SS))
            except: pass
        return ImageFont.load_default()
    caps=lambda s:' '.join(s.upper())
    D.text((left*SS,52*SS),'SAME POSE, DIFFERENT HUMANS',fill=INK,font=font(22))
    D.text((left*SS,90*SS),caps('ten standers — no gesture, no costume, no face. only what the body is.'),fill=LBL,font=font(10))
    D.line([(left*SS,124*SS),((W-left)*SS,124*SS)],fill=FAINT,width=max(1,int(SS)))
    D.text((left*SS,(H-52)*SS),caps('if everyone stands still — can you still tell them apart?'),fill=LBL,font=font(9.5))
    img.resize((W,H),Image.LANCZOS).save(path); print('saved',path)

if __name__=='__main__':
    validate()
    plate("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u2_a5_samepose.png")

