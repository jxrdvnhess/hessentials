import cv2, numpy as np, glob, os, sys, json
SRC="/sessions/wizardly-stoic-cerf/mnt/Sketch 201 Reference Library"
OUT="/sessions/wizardly-stoic-cerf/mnt/outputs/cut"
os.makedirs(OUT,exist_ok=True)
F=sorted(glob.glob(f"{SRC}/*.jpg"))

BOX={
1:(.44,.17,.69,.93),2:(.28,.20,.63,.96),3:(.42,.24,.64,.91),4:(.34,.10,.77,.97),
5:(.30,.11,.61,.99),6:(.22,.13,.86,.99),7:(.48,.07,.77,.99),8:(.28,.17,.73,.96),
9:(.43,.19,.71,.96),10:(.40,.14,.61,.96),11:(.30,.18,.80,.99),12:(.43,.28,.69,.96),
13:(.48,.10,.77,.99),14:(.30,.18,.96,.97),16:(.24,.10,.72,.99),18:(.18,.18,.82,.99),
19:(.28,.12,.82,.99),21:(.38,.28,.63,.93),22:(.32,.11,.67,.99),23:(.39,.19,.63,.98),
24:(.30,.18,.96,.99),26:(.43,.33,.80,.96),28:(.43,.24,.66,.96),29:(.33,.16,.64,.99),
30:(.30,.20,.72,.95),32:(.30,.10,.70,.96),33:(.28,.34,.92,.82),34:(.40,.18,.78,.96),
35:(.26,.24,.71,.96),36:(.28,.24,.86,.98),37:(.38,.18,.64,.99),38:(.38,.14,.63,.99),
39:(.44,.19,.63,.96),
}

def load(p,m=560):
    im=cv2.imread(p);h,w=im.shape[:2];s=m/max(h,w)
    return cv2.resize(im,(int(w*s),int(h*s)),interpolation=cv2.INTER_AREA) if s<1 else im
def gc(im,rect,it=5):
    mask=np.zeros(im.shape[:2],np.uint8);b=np.zeros((1,65),np.float64);f=np.zeros((1,65),np.float64)
    cv2.grabCut(im,mask,rect,b,f,it,cv2.GC_INIT_WITH_RECT)
    return np.where((mask==1)|(mask==3),255,0).astype(np.uint8)
def clean(m):
    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,k);m=cv2.morphologyEx(m,cv2.MORPH_OPEN,k)
    n,lab,st,_=cv2.connectedComponentsWithStats(m,8)
    if n<=1: return m
    return np.where(lab==1+int(np.argmax(st[1:,cv2.CC_STAT_AREA])),255,0).astype(np.uint8)

def process(idx):
    im=load(F[idx]);H,W=im.shape[:2]
    bx=BOX[idx]; rect=(int(W*bx[0]),int(H*bx[1]),int(W*(bx[2]-bx[0])),int(H*(bx[3]-bx[1])))
    m=clean(gc(im,rect))
    ys,xs=np.where(m>0)
    if len(xs)==0: return None,0,im
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    crop=m[y0:y1+1,x0:x1+1]
    return crop,m.mean()/255,im

if __name__=="__main__":
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    idxs=[i for i in sorted(BOX) if lo<=i<hi]
    log={}
    for i in idxs:
        crop,cov,im=process(i)
        if crop is None: print(i,"EMPTY"); continue
        # anti-aliased silhouette saved as grayscale alpha (255=figure)
        a=cv2.GaussianBlur(crop,(0,0),0.6)
        cv2.imwrite(f"{OUT}/sil_{i:02d}.png",a)
        log[i]=[round(cov,3),crop.shape[1],crop.shape[0]]
        print(i,os.path.basename(F[i])[:16],round(cov,3),crop.shape[::-1])
    # append to a json log
    pth=f"{OUT}/log.json"; d={}
    if os.path.exists(pth): d=json.load(open(pth))
    d.update({str(k):v for k,v in log.items()}); json.dump(d,open(pth,"w"))
    print("chunk done",idxs)
