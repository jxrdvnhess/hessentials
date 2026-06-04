"""A55 — The Map. One page. Every surviving finding from A30–A54, arranged: six discoveries on one
dependency spine, one cross-link, three open questions. No prose. No new ideas."""
from PIL import Image, ImageDraw, ImageFont
import math
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
W,H=880,1190
def F(path,size):
    try: return ImageFont.truetype(path,int(size*SS))
    except: return ImageFont.load_default()
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERI="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
f_title=F(SER,15); f_node=F(SER,20); f_sat=F(SER,13.5); f_open=F(SERI,13.5); f_link=F(SERI,12.5)

NODES=[
 ("I · OBSERVATION BEATS SCHEMA",
  ["the eye over the rig — A31",
   "one thing holds many structures — A32"]),
 ("II · MARKS HAVE JOBS",
  ["organize → recognize → name — A35–39",
   "reduction keeps the organizers — A33–34",
   "early jobs unlock later jobs — A40"]),
 ("III · A MARK'S VALUE IS RELATIONAL",
  ["reinforce or rival — A43–44",
   "good marks create agreements — A45",
   "every mark costs; restraint is accounting — A41–42"]),
 ("IV · UNITY AND IDENTITY ARE DIFFERENT CURRENCIES",
  ["meetings buy unity — is it one thing? — A45–46",
   "right marks buy identity — which thing is it? — A46",
   "a break is priced by remaining routes — A47–48"]),
 ("V · A THIN RELATION REWRITES MEANING",
  ["moves nothing, changes everything — A48–49",
   "destination does the work, not contact — A50",
   "carries no message, enables many — A49",
   "situation yields before identity — A53–54",
   "the relation's shape also names — A53"]),
 ("VI · THE INTENTIONAL REGISTER",
  ["two equal, separate claims read strange — A51",
   "a holder only for the object reads intended — A52",
   "held ≠ presented; the plinth assigns regard — A52",
   "unresolved conflict becomes story or address — A54"]),
]
OPEN=["attention or identification? entangled — A46–48",
      "where does the naming happen? object · relation · whole — A53",
      "is classification one thing? kinds · roles · statuses · functions — A54"]
LINK="one phenomenon in four costumes? rivals · agreements · claims — A43 · A45 · A51"

def render(path):
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    def text(x,y,s,font,col=INK): d.text((int(x*SS),int(y*SS)),s,fill=col,font=font)
    def line(pts,col=MID,w=1.6): d.line([(int(x*SS),int(y*SS)) for x,y in pts],fill=col,width=max(1,int(w*SS)))
    # header
    text(110,42,"S K E T C H  2 0 1  —  W H A T  S U R V I V E D   ·   A 3 0 – A 5 4",f_title,INK)
    line([(110,70),(770,70)],MID,1.4)
    # spine
    x_sp=84
    y=104; centers=[]
    blocks=[]
    for title,sats in NODES:
        y0=y
        text(110,y,title,f_node,INK); y+=34
        line([(110,y),(770,y)],MID,1.2); y+=10
        for s in sats:
            text(128,y,s,f_sat,INK); y+=24
        centers.append((y0+14))
        blocks.append((y0,y))
        y+=30
    # spine with arrowheads at each node title
    line([(x_sp,centers[0]),(x_sp,centers[-1])],MID,1.8)
    for cy in centers:
        line([(x_sp,cy),(102,cy)],MID,1.8)
        line([(96,cy-4),(102,cy),(96,cy+4)],MID,1.8)
    # cross-link: dashed arc on the right from node III to node VI
    c3=centers[2]; c6=centers[5]; x_arc=812
    n=46
    pts=[]
    for i in range(n+1):
        t=i/n
        yy=c3+(c6-c3)*t
        xx=778+ (x_arc-778)*math.sin(math.pi*t)
        pts.append((xx,yy))
    for i in range(0,n,2):
        line([pts[i],pts[i+1]],MID,1.5)
    line([(778,c3),(786,c3-4)],MID,1.5); line([(778,c6),(786,c6+4)],MID,1.5)
    # link label, stacked beside the arc
    mid_y=(c3+c6)//2
    for j,part in enumerate(["one phenomenon","in four costumes?","rivals · agreements","claims — A43 · A45 · A51"]):
        tw=d.textlength(part,font=f_link)/SS
        text(768-tw, mid_y-52+j*22, part, f_link, MID)
    # open questions
    yo=blocks[-1][1]+38
    text(110,yo,"O P E N",f_title,MID); yo+=26
    line([(110,yo),(770,yo)],MID,1.2); yo+=12
    for s in OPEN:
        # dashed bullet
        line([(116,yo+10),(124,yo+10)],MID,1.5)
        text(134,yo,s,f_open,INK); yo+=26
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a55_the_map.png")
