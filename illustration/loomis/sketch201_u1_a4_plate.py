import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
from sketch201_u1_a4_rig import render
from sketch201_u1_a4_figures import FIGS
OUT="/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u1_a4_strangers.png"
PAPER=(237,232,223); INK=(33,31,29); LBL=(96,94,90); FAINT=(178,174,166); SS=2

TOP=[29,1,23,38,28,3,5,7,21,39]          # walking / standing
BOT=[16,2,4,8,34,14,30,35,33,32]          # seated / dynamic / reclining
ORDER=TOP+BOT

def alpha(idx):
    label,fn=FIGS[idx]; J,R=fn(); return render(J,R)

COLS=10; ROWS=2
cell_w, cell_h = 268, 560
top=170; left=70
W=left*2 + COLS*cell_w
H=top + ROWS*cell_h + 90
canvas=np.full((H*SS, W*SS, 3), PAPER[::-1], np.uint8)
maxh=int(cell_h*0.86)*SS; maxw=int(cell_w*0.82)*SS
for k,idx in enumerate(ORDER):
    a=alpha(idx); h,w=a.shape
    s=min(maxh/h, maxw/w); nw,nh=max(1,int(w*s)),max(1,int(h*s))
    a=cv2.resize(a,(nw,nh),interpolation=cv2.INTER_AREA)
    r=k//COLS; c=k%COLS
    cell_x=(left + c*cell_w)*SS; cell_y=(top + r*cell_h)*SS
    base=cell_y + int(cell_h*0.92)*SS
    ox=cell_x + (cell_w*SS - nw)//2; oy=base - nh
    reg=canvas[oy:oy+nh, ox:ox+nw].astype(np.float32)
    al=(a/255.0)[...,None]; ink=np.array(INK[::-1],np.float32)
    canvas[oy:oy+nh, ox:ox+nw]=(reg*(1-al)+ink*al).astype(np.uint8)

img=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB)); D=ImageDraw.Draw(img)
def font(px):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        try: return ImageFont.truetype(p,int(px*SS))
        except: pass
    return ImageFont.load_default()
def caps(s): return ' '.join(s.upper())
D.text((left*SS,52*SS),'TWENTY REAL STRANGERS',fill=INK,font=font(22))
D.text((left*SS,90*SS),caps('observed, then redrawn — one stranger per silhouette'),fill=LBL,font=font(10))
D.line([(left*SS,124*SS),((W-left)*SS,124*SS)],fill=FAINT,width=max(1,int(1*SS)))
D.text((left*SS,(H-52)*SS),caps('remove the face — is each still a person? do these read as twenty?'),fill=LBL,font=font(9.5))
img.resize((W,H),Image.LANCZOS).save(OUT); print('saved',OUT)
