"""
THE MAN — head + neck + TORSO, rebuilt on MASS construction (per the references):
ribcage BARREL + pelvis BOX + deltoid SPHERES + limb cylinders are blocked first
(faint), then the surface anatomy is hung on them. Broad chest, defined waist,
a real pelvis. Construction/sketch phase, light upper-left.
"""
import face03_loomis_hair as f3
fg=f3.fg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS, INK

OUT="/sessions/lucid-charming-babbage/mnt/outputs/loomis"
W,H=620,1500; CX=300
PAPER=np.array([237,232,223],float); INK_SH=np.array([52,52,66],float); GREY=np.array([150,146,138],float)
yy,xx=np.mgrid[0:H,0:W].astype(float)
P=f3.P; DOME=f3.DOME; REC=f3.REC; cx=CX; yc=P['ychin']; ye=P['yeye']
def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def g2(cx,cy,sx,sy,d,ang=0.0):
    ca,sa=np.cos(ang),np.sin(ang); u=((xx-cx)*ca+(yy-cy)*sa)/sx; v=(-(xx-cx)*sa+(yy-cy)*ca)/sy
    return np.exp(-(u*u+v*v))*d
def stripes(angle,gap,lw,seed=1):
    ca,sa=np.cos(angle),np.sin(angle); u=xx*ca+yy*sa; v=-xx*sa+yy*ca
    vv=v+1.3*soft(np.random.default_rng(seed).normal(0,1,(H,W)),3)
    return np.clip(1-np.abs(((vv/gap+0.5)%1.0)-0.5)*gap/lw,0,1)
def poly(pts):
    im=Image.new("L",(W,H),0); ImageDraw.Draw(im).polygon([(float(x),float(y)) for x,y in pts],fill=255)
    return np.asarray(im,float)/255.0

S,sil,hp=fg.D(P)
def na(c,w,cs=False,ce=False,sw=0.2): S.append(dict(ctrl=c,w=w,lead=0.2,tail=0.3,swell=sw,smoothing=0.6,cap_start=cs,cap_end=ce))
na([(cx-66,yc+4),(cx-42,yc+48),(cx-14,yc+98)],2.0); na([(cx+66,yc+4),(cx+42,yc+48),(cx+14,yc+98)],2.0)  # SCMs
na([(cx-12,yc+96),(cx,yc+105),(cx+12,yc+96)],1.6)                                                       # pit
na([(cx-8,yc+38),(cx-6,yc+58)],1.1,cs=True,ce=True); na([(cx+8,yc+38),(cx+6,yc+58)],1.1,cs=True,ce=True)# Adam's apple
na([(cx-8,yc+100),(cx-72,yc+108),(cx-142,yc+120)],2.0); na([(cx+8,yc+100),(cx+72,yc+108),(cx+142,yc+120)],2.0)  # clavicles

# ---- SURFACE anatomy hung on the masses ----
def a(c,w,lead=0.18,tail=0.24,swell=0.3,sm=0.58,cs=False,ce=False): S.append(dict(ctrl=c,w=w,lead=lead,tail=tail,swell=swell,smoothing=sm,cap_start=cs,cap_end=ce))
a([(cx,yc+100),(cx-2,776),(cx+2,884),(cx,1012),(cx-2,1100),(cx,1170)],1.0,lead=0.4,tail=0.4,swell=0.08)   # centre line
# ARMS — cylinders with sphere joints + muscle forms + blocked hands (hang from deltoids)
def arm(s):
    # outer: deltoid -> upper arm -> elbow -> forearm mass (bulge near elbow) -> wrist
    a([(cx+s*150,744),(cx+s*244,792),(cx+s*254,900),(cx+s*246,1010),(cx+s*242,1062),
       (cx+s*254,1124),(cx+s*234,1228),(cx+s*220,1286)],3.0,lead=0.14,tail=0.18,swell=0.28)
    # inner: armpit -> inner upper arm -> elbow -> inner forearm -> wrist
    a([(cx+s*182,824),(cx+s*210,922),(cx+s*214,1012),(cx+s*214,1064),
       (cx+s*216,1144),(cx+s*206,1238),(cx+s*200,1286)],2.2,lead=0.22,tail=0.24,swell=0.2)
    a([(cx+s*214,864),(cx+s*222,952),(cx+s*214,1024)],1.3,lead=0.32,tail=0.34,swell=0.12)        # biceps mass
    a([(cx+s*240,1080),(cx+s*230,1164),(cx+s*214,1236)],1.3,lead=0.32,tail=0.34,swell=0.12)      # forearm muscle mass
    a([(cx+s*214,1058),(cx+s*238,1062)],1.2,cs=True,ce=True,swell=0.1)                           # elbow crease
    # HAND (blocked): back/palm -> fingers + thumb
    a([(cx+s*220,1286),(cx+s*230,1330),(cx+s*224,1380),(cx+s*204,1388)],2.0,lead=0.2,tail=0.26,swell=0.16)  # outer hand
    a([(cx+s*200,1286),(cx+s*196,1332),(cx+s*200,1374),(cx+s*204,1388)],1.8,lead=0.24,tail=0.26,swell=0.14) # inner hand
    for fx in (0,1,2):
        a([(cx+s*(202+fx*8),1346),(cx+s*(202+fx*8),1382)],0.9,cs=True,ce=True,swell=0.06)        # finger divisions
    a([(cx+s*197,1296),(cx+s*186,1314),(cx+s*194,1334)],1.4,lead=0.3,tail=0.32,swell=0.1)        # thumb (inner)
arm(-1); arm(1)
# faint upper-thigh hint (so the hands have context at the sides)
a([(cx-118,1196),(cx-128,1320),(cx-120,1440)],1.4,lead=0.4,tail=0.4,swell=0.1)
a([(cx+118,1196),(cx+128,1320),(cx+120,1440)],1.4,lead=0.4,tail=0.4,swell=0.1)
a([(cx-12,1180),(cx-16,1320),(cx-12,1440)],1.1,lead=0.42,tail=0.42,swell=0.08)
a([(cx+12,1180),(cx+16,1320),(cx+12,1440)],1.1,lead=0.42,tail=0.42,swell=0.08)
# torso sides: armpit -> broad ribcage -> waist -> hip (inverted trapezoid)
a([(cx-182,824),(cx-166,902),(cx-104,1006),(cx-116,1078),(cx-128,1166),(cx-112,1216)],2.6,lead=0.2,tail=0.22,swell=0.24)
a([(cx+182,824),(cx+166,902),(cx+104,1006),(cx+116,1078),(cx+128,1166),(cx+112,1216)],2.6,lead=0.2,tail=0.22,swell=0.24)
# clavicle/pec top + sternum
a([(cx-150,744),(cx-70,758),(cx-8,764)],1.8,lead=0.3,tail=0.3,swell=0.14); a([(cx+150,744),(cx+70,758),(cx+8,764)],1.8,lead=0.3,tail=0.3,swell=0.14)
a([(cx,764),(cx,842)],1.4,lead=0.34,tail=0.34,swell=0.1)
# PECS — broad slabs, lifted; underline sternum->armpit + nipple
a([(cx-10,842),(cx-82,850),(cx-152,822),(cx-182,792)],2.4,lead=0.2,tail=0.28,swell=0.18)
a([(cx+10,842),(cx+82,850),(cx+152,822),(cx+182,792)],2.4,lead=0.2,tail=0.28,swell=0.18)
a([(cx-96,822),(cx-88,834)],1.4,cs=True,ce=True,swell=0.1); a([(cx+96,822),(cx+88,834)],1.4,cs=True,ce=True,swell=0.1)
# rib arch (solar plexus V)
a([(cx-50,860),(cx,880),(cx+50,860)],1.5,lead=0.3,tail=0.3,swell=0.12)
# RECTUS ABDOMINIS: linea alba + side borders + 3 division rows; navel
a([(cx,880),(cx,1096)],1.4,lead=0.34,tail=0.34,swell=0.1)
for ylev in (916,956,996): a([(cx-48,ylev),(cx,ylev+4),(cx+48,ylev)],1.2,lead=0.34,tail=0.34,swell=0.1)
a([(cx-52,888),(cx-56,1064)],1.3,lead=0.32,tail=0.34,swell=0.12); a([(cx+52,888),(cx+56,1064)],1.3,lead=0.32,tail=0.34,swell=0.12)
a([(cx-6,1028),(cx+6,1028)],1.6,cs=True,ce=True,swell=0.1)                                  # navel
# obliques + inguinal V (pelvis) + iliac-crest dimples
a([(cx-56,1064),(cx-98,1106),(cx-30,1156),(cx,1162)],1.4,lead=0.3,tail=0.32,swell=0.12)
a([(cx+56,1064),(cx+98,1106),(cx+30,1156),(cx,1162)],1.4,lead=0.3,tail=0.32,swell=0.12)
a([(cx-116,1080),(cx-92,1116)],1.3,cs=True,ce=True,swell=0.1); a([(cx+116,1080),(cx+92,1116)],1.3,cs=True,ce=True,swell=0.1)

# ---- VALUE / light ----
BODY=[(cx-150,740),(cx-256,860),(cx-244,1130),(cx-210,1392),(cx-118,1450),(cx,1454),(cx+118,1450),(cx+210,1392),(cx+244,1130),(cx+256,860),(cx+150,740)]
mask=(soft(np.clip(poly(sil)+poly(DOME)+poly(BODY),0,1),2)>0.5).astype(float)
xterm=(cx+P['term'])+(yy-ye)*0.12
shadow=np.clip((xx-xterm)/28+0.5,0,1)*mask
half=np.clip((shadow-0.16)/0.34,0,1)
g=half*P['shadow']*stripes(-0.5,6,1.5,P['seed'])+np.clip(shadow-0.55,0,1)*0.30*stripes(0.6,7,1.5,P['seed']+1)
g=np.clip(g+soft(g2(cx,P['ynose']+18,P['nose_w'],8,0.34)+g2(cx,P['ymouth']+22,P['mouth_w']*0.8,8,0.3)
    +g2(cx,yc+10,120,30,0.28)+g2(cx-P['eye_sp'],P['ybrow']+20,P['eye_w'],10,0.26)+g2(cx+P['eye_sp'],P['ybrow']+20,P['eye_w'],10,0.3),4)*mask*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)
hmask=soft(poly(DOME),5)
rec=sum(g2(rx,ry,9,46,0.5,ra) for (rx,ry,ra) in REC)
dark=np.clip(soft(rec+g2(cx-104,174,40,28,0.5)+g2(cx+106,172,40,32,0.55)+g2(cx,190,120,14,0.4)+g2(cx+98,150,48,52,0.45),5),0,1)
lightb=soft(g2(cx-16,110,86,22,1.0,-0.05)+g2(cx+46,116,46,16,0.6),5)
hairval=np.clip(0.40+dark-lightb*0.95,0,1)*hmask
g=np.clip(g+hairval*0.5*stripes(-0.66,5,1.6,3)+np.clip(hairval-0.52,0,1)*0.40*stripes(-1.2,5,1.5,4),0,1)
g=np.clip(g+soft(g2(cx,yc+98,14,12,0.85)+g2(cx,yc+72,22,40,0.3)+g2(cx-50,yc+54,15,52,0.3)+g2(cx+52,yc+54,16,52,0.4)
    +g2(cx-62,yc+130,74,16,0.34)+g2(cx+62,yc+130,74,16,0.36)+g2(cx,yc+12,92,26,0.36),5)*mask*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)
tor=(g2(cx-78,852,64,16,0.5)+g2(cx+78,852,64,16,0.55)            # under the pecs
    +g2(cx,866,40,12,0.3)                                        # solar plexus
    +g2(cx-58,948,10,86,0.32)+g2(cx+58,948,10,86,0.36)          # ab side borders
    +g2(cx,936,46,8,0.25)+g2(cx,976,46,8,0.25)                  # ab divisions
    +g2(cx-182,802,22,40,0.5)+g2(cx+182,802,22,40,0.55)        # armpits
    +g2(cx+150,980,42,170,0.34)+g2(cx-150,980,30,170,0.22)     # torso form sides (R deeper)
    +g2(cx-96,1110,34,30,0.3)+g2(cx+96,1110,34,30,0.34)        # inguinal/hip
    +g2(cx+250,1010,26,190,0.4)+g2(cx-250,1010,22,190,0.26)    # upper-arm form shadow
    +g2(cx+222,1200,20,120,0.36)+g2(cx-222,1200,18,120,0.24)   # forearm form shadow
    +g2(cx+210,1346,24,34,0.4)+g2(cx-210,1346,22,34,0.3))      # hands
g=np.clip(g+soft(tor,5)*mask*0.5*stripes(-0.5,6,1.5,P['seed']),0,1)

out=np.ones((H,W,3))*PAPER
# faint CONSTRUCTION masses (ribcage barrel, pelvis box, deltoid spheres, waist) under it all
cim=Image.new("L",(W*2,H*2),0); cd=ImageDraw.Draw(cim); s2=2
def ce_(c,a_,b,w=1): cd.ellipse([(c[0]-a_)*s2,(c[1]-b)*s2,(c[0]+a_)*s2,(c[1]+b)*s2],outline=255,width=int(w*s2))
def cl_(p,q,w=1): cd.line([(p[0]*s2,p[1]*s2),(q[0]*s2,q[1]*s2)],fill=255,width=int(w*s2))
ce_((cx,858),150,118)                                   # ribcage barrel
ce_((cx-198,786),58,58); ce_((cx+198,786),58,58)        # deltoid spheres
cl_((cx-112,1006),(cx+112,1006)); cl_((cx-128,1170),(cx+128,1170))                # pelvis box top/bottom
cl_((cx-112,1006),(cx-128,1170)); cl_((cx+112,1006),(cx+128,1170))               # pelvis box sides
ce_((cx,1006),104,16)                                   # waist ellipse
ce_((cx-238,1064),25,25); ce_((cx+238,1064),25,25)      # elbow spheres
ce_((cx-210,1288),17,17); ce_((cx+210,1288),17,17)      # wrist spheres
cl_((cx-228,850),(cx-234,1052)); cl_((cx+228,850),(cx+234,1052))   # upper-arm cylinder axis
cl_((cx-236,1080),(cx-212,1280)); cl_((cx+236,1080),(cx+212,1280)) # forearm cylinder axis
cd.rectangle([(cx-228)*s2,1288*s2,(cx-196)*s2,1352*s2],outline=255,width=int(1*s2))   # left hand box
cd.rectangle([(cx+196)*s2,1288*s2,(cx+228)*s2,1352*s2],outline=255,width=int(1*s2))   # right hand box
ca=np.asarray(cim.resize((W,H),Image.LANCZOS),float)/255.0
out=out*(1-(ca*0.32)[...,None]) + GREY*(ca*0.32)[...,None]
out=out*(1-g[...,None])+INK_SH*g[...,None]
im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
for s in S: stroke(d,**s)
fa=np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
out=out*(1-fa[...,None])+INK*fa[...,None]
clt=np.clip(soft(g2(cx-P['eye_sp']-3,ye-3,2,2.4,1)+g2(cx+P['eye_sp']-3,ye-3,2,2.4,1),0.4),0,1)
out=out*(1-clt[...,None])+PAPER*clt[...,None]
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(f"{OUT}/the_man.png"); print("done")
