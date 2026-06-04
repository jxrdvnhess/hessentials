"""A56 — The Final Cut. The A55 map edited again: three discoveries, not six. No new ideas; the old
middle (II–V) shown as one discovery at four scales. Labels and relationships only."""
from PIL import Image, ImageDraw, ImageFont
SS=3
PAPER=(237,232,223); INK=(43,43,53); MID=(150,146,140)
W,H=880,940
def F(path,size):
    try: return ImageFont.truetype(path,int(size*SS))
    except: return ImageFont.load_default()
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERI="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
f_title=F(SER,15); f_node=F(SER,21); f_sat=F(SER,13.5); f_open=F(SERI,13.5); f_was=F(SERI,12)

NODES=[
 ("1 · OBSERVATION BEATS SCHEMA","(was I)",
  ["the eye over the rig — A4 · A31",
   "one thing holds many structures — A32"]),
 ("2 · MEANING LIVES IN RELATIONSHIPS, NOT PARTS","(was II · III · IV · V — one discovery at four scales)",
  ["between marks — jobs, rivals, agreements — A35–45",
   "between marks and the figure — unity and identity, priced by routes — A45–48",
   "between the thing and the world — a thin relation rewrites meaning — A48–54",
   "the price of any relation — restraint is accounting — A41–42"]),
 ("3 · RELATIONS READ NATURAL OR INTENTIONAL","(was VI)",
  ["world-made vs only-for-the-object — A52",
   "two equal, separate claims read strange — A51",
   "held ≠ presented; the plinth assigns regard — A52",
   "unresolved conflict becomes story or address — A54"]),
]
OPEN=["attention or identification? entangled — A46–48",
      "where does the naming happen? object · relation · whole — A53",
      "is classification one thing? kinds · roles · statuses · functions — A54"]

def render(path):
    img=Image.new("RGB",(W*SS,H*SS),PAPER); d=ImageDraw.Draw(img)
    def text(x,y,s,font,col=INK): d.text((int(x*SS),int(y*SS)),s,fill=col,font=font)
    def line(pts,col=MID,w=1.6): d.line([(int(x*SS),int(y*SS)) for x,y in pts],fill=col,width=max(1,int(w*SS)))
    text(110,42,"S K E T C H  2 0 1  —  T H E  F I N A L  C U T   ·   T H R E E",f_title,INK)
    line([(110,70),(770,70)],MID,1.4)
    x_sp=84; y=108; centers=[]; blocks=[]
    for title,was,sats in NODES:
        y0=y
        text(110,y,title,f_node,INK); y+=32
        text(112,y,was,f_was,MID); y+=26
        line([(110,y),(770,y)],MID,1.2); y+=10
        for s in sats:
            text(128,y,s,f_sat,INK); y+=25
        centers.append(y0+15); blocks.append((y0,y)); y+=38
    line([(x_sp,centers[0]),(x_sp,centers[-1])],MID,1.8)
    for cy in centers:
        line([(x_sp,cy),(102,cy)],MID,1.8)
        line([(96,cy-4),(102,cy),(96,cy+4)],MID,1.8)
    yo=blocks[-1][1]+40
    text(110,yo,"O P E N",f_title,MID); yo+=26
    line([(110,yo),(770,yo)],MID,1.2); yo+=12
    for s in OPEN:
        line([(116,yo+10),(124,yo+10)],MID,1.5)
        text(134,yo,s,f_open,INK); yo+=26
    img=img.resize((W,H),Image.LANCZOS); img.save(path); print("saved",path)
if __name__=="__main__":
    render("/sessions/wizardly-stoic-cerf/mnt/hessentials/illustration/loomis/sketch201_u5_a56_the_final_cut.png")
