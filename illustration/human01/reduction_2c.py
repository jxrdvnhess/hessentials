"""
HUMAN STUDIES VOL. 1 — ASSIGNMENT 2C: THE REDUCTION TEST.
Five strongest 2B events, reduced A→B→C→D. Remove information each
step. Stop when the event dies; D is rendered AT or PAST death so
the kill is on the page, not guessed.

R1 cradle (i08) · R2 kiss (i01) · R3 greeting (i09)
R4 telling/receiving (i03) · R5 embrace (i02)

Pre-registered kill predictions (sealed before rendering):
R1 dies when the bowed head goes (attention is the hold).
R2 dies when lip-notch + closed eye go (attitude is the kiss).
R3 dies when the palms go (address is the second person).
R4 dies when the receiver's irises go (gaze is the BETWEEN).
R5 dies when the torso goes (an arm over nothing is a railing —
   already learned once in 2B; this reduction re-runs it as test).
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import render               # noqa: E402
from heads_batch01 import s                  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850

V = {}

# ---------- R1 CRADLE ----------
_cradle_arc   = s([(250,320),(252,420),(310,490),(420,508),(510,470),(540,408)], 3.6)
_cradle_close = s([(540,408),(536,360),(508,330)], 2.8)
_bowed_head   = s([(280,210),(296,150),(354,122),(416,134),(448,182),(440,242),(404,280)], 3.0)
_bow_jaw      = s([(404,280),(372,296),(338,290)], 2.4)
_infant_head  = s([(452,366),(448,332),(480,316),(508,334),(508,368),(482,384),(452,366)], 2.6)
_sprawl_arm   = s([(486,388),(540,432),(584,448)], 2.4)
_sprawl_hand  = s([(584,448),(598,442)], 1.6)
_dangle_leg   = s([(396,430),(386,470)], 1.8)
_infant_body  = s([(448,388),(404,418),(352,434)], 2.4)

V["r1a"] = [_cradle_arc, _cradle_close, _bowed_head, _bow_jaw,
            _infant_head, _infant_body, _sprawl_arm, _sprawl_hand]   # 8: eye line + leg removed
V["r1b"] = [_cradle_arc, _bowed_head, _infant_head, _sprawl_arm]     # 5→4: closing forearm, jaw, body, hand gone
V["r1c"] = [_cradle_arc, _bowed_head, _infant_head]                  # 3: THE SPRAWL GONE — trust dies, hold lives?
V["r1d"] = [_cradle_arc, _infant_head]                               # 2: the bow gone — predicted death

# ---------- R2 KISS ----------
_giver      = s([(170,330),(176,240),(228,186),(292,176),(330,206),(346,250),(342,282),(356,300)], 3.2)
_giver_lips = s([(356,300),(352,316),(340,322)], 2.6)
_giver_jaw  = s([(336,336),(310,386),(268,420)], 2.8)
_recv       = s([(360,296),(388,232),(452,206),(518,224),(548,288),(540,360),(508,428),(452,462)], 3.2)
_recv_cheek = s([(452,462),(414,448),(380,406),(362,350),(360,296)], 2.8)
_recv_eye1  = s([(416,310),(442,320),(468,312)], 2.4)
_recv_eye2  = s([(488,306),(512,314),(532,304)], 2.4)
_recv_smile = s([(432,396),(462,408),(496,396)], 2.5)
_recv_chin  = s([(424,452),(452,468),(484,456)], 2.2)

V["r2a"] = [_giver, _giver_lips, _giver_jaw, _recv, _recv_cheek,
            _recv_eye1, _recv_smile, _recv_chin]                     # 8: hair, eye2, throat removed
V["r2b"] = [_giver, _giver_lips, _recv, _recv_cheek, _recv_eye1,
            _recv_smile]                                             # 6: jaw + chin gone
V["r2c"] = [_giver, _giver_lips, _recv, _recv_eye1]                  # 4: smile + cheek gone — kiss + consent only
V["r2d"] = [_giver, _recv]                                           # 2: lip notch + eye gone — predicted death

# ---------- R3 GREETING ----------
_g_head  = s([(262,300),(274,218),(332,176),(396,178),(438,220),(442,300),(414,364),(356,392),(300,366),(268,326)], 3.0)
_g_eyeL  = s([(318,269),(326,276),(319,283),(312,276),(318,269)], 1.3)
_g_eyeR  = s([(380,266),(388,273),(381,280),(374,273),(380,266)], 1.3)
_g_grin  = s([(312,330),(336,344),(366,346),(394,332)], 2.6)
_g_grin2 = s([(320,344),(354,354),(388,338)], 1.6)
_g_palmL = s([(180,360),(172,290),(186,250),(214,244),(226,300),(222,358)], 2.8)
_g_palmR = s([(478,352),(486,284),(474,246),(448,242),(438,296),(444,352)], 2.8)
_g_fingL = s([(186,250),(184,228)], 1.8)
_g_fingR = s([(474,246),(478,222)], 1.8)

V["r3a"] = [_g_head, _g_eyeL, _g_eyeR, _g_grin, _g_grin2,
            _g_palmL, _g_palmR, _g_fingL, _g_fingR]                  # 9: brow lines + shoulders + 2 finger ticks gone
V["r3b"] = [_g_head, _g_eyeL, _g_eyeR, _g_grin, _g_palmL, _g_palmR]  # 6: finger ticks + grin depth gone
V["r3c"] = [_g_head, _g_grin, _g_palmL, _g_palmR]                    # 4: the EYES gone — aim lost, gesture left
V["r3d"] = [_g_head, _g_eyeL, _g_eyeR, _g_grin]                      # 4: the PALMS gone — predicted death

# ---------- R4 TELLING / RECEIVING ----------
_t_head   = s([(150,330),(160,248),(212,200),(276,196),(318,234),(326,304),(304,374),(252,406),(196,388),(160,352)], 3.0)
_t_mouth  = s([(216,352),(240,364),(266,352)], 2.6)
_t_mouth2 = s([(222,366),(244,372),(262,364)], 1.6)
_r_head   = s([(382,322),(394,240),(448,194),(514,192),(556,232),(562,304),(540,376),(486,408),(428,388),(392,348)], 3.0)
_r_browL  = s([(430,272),(456,262),(480,268)], 2.8)
_r_browR  = s([(498,266),(524,257),(546,264)], 2.8)
_r_irisL  = s([(438,302),(446,309),(439,315),(432,309),(438,302)], 1.2)
_r_irisR  = s([(503,299),(511,306),(504,312),(497,306),(503,299)], 1.2)
_r_smile  = s([(452,360),(484,370),(518,358)], 2.5)

V["r4a"] = [_t_head, _t_mouth, _t_mouth2, _r_head, _r_browL,
            _r_browR, _r_irisL, _r_irisR, _r_smile]                  # 9: teller eyes + lid lines gone
V["r4b"] = [_t_head, _t_mouth, _r_head, _r_browL, _r_irisL,
            _r_irisR, _r_smile]                                      # 7
V["r4c"] = [_t_head, _t_mouth, _r_head, _r_irisL, _r_irisR]          # 5: brows + smile gone — gaze alone
V["r4d"] = [_t_head, _t_mouth, _r_head]                              # 3: irises gone — predicted death

# ---------- R5 EMBRACE ----------
_e_head   = s([(280,310),(296,222),(356,176),(424,182),(468,238),(470,318),(440,396),(380,428),(322,400),(288,348)], 3.2)
_e_mouth  = s([(346,368),(372,376),(400,366)], 2.5)
_e_torsoL = s([(296,440),(266,500),(252,580)], 2.8)
_e_torsoR = s([(448,420),(478,484),(492,566)], 2.8)
_e_arm1   = s([(680,380),(596,388),(516,416),(470,448)], 3.6)
_e_arm2   = s([(688,428),(606,434),(532,460),(486,486)], 3.0)
_e_fore   = s([(470,448),(410,492),(340,520)], 3.2)
_e_hand   = s([(340,520),(316,540),(326,562),(354,556)], 2.6)

V["r5a"] = [_e_head, _e_mouth, _e_torsoL, _e_torsoR,
            _e_arm1, _e_arm2, _e_fore, _e_hand]                      # 8: eyes, chest line, arm underside detail gone
V["r5b"] = [_e_head, _e_torsoL, _e_torsoR, _e_arm1, _e_fore, _e_hand]# 6: mouth + one arm edge gone
V["r5c"] = [_e_head, _e_arm1, _e_fore, _e_hand]                      # 4: TORSO gone — predicted death (the railing)
V["r5d"] = [_e_arm1, _e_fore, _e_hand]                               # 3: head gone — past death, control

ORDER = ["r1a","r1b","r1c","r1d","r2a","r2b","r2c","r2d",
         "r3a","r3b","r3c","r3d","r4a","r4b","r4c","r4d",
         "r5a","r5b","r5c","r5d"]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = {}
    for name in ORDER:
        im = render(V[name], [], W, H, seed=hash(name) % 999)
        im.save(os.path.join(OUT, f"{name}.png"))
        imgs[name] = im
        print("wrote", name, len(V[name]), "strokes")
    tw, th = W // 3, H // 3
    sheet = Image.new("RGB", (4 * tw, 5 * th), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for n, name in enumerate(ORDER):
        x, y = (n % 4) * tw, (n // 4) * th
        sheet.paste(imgs[name].resize((tw, th)), (x, y))
        d.text((x + 8, y + 6), name, fill=(31, 29, 27))
    sheet.save(os.path.join(OUT, "_contact_2c.png"))
    print("contact ok")
