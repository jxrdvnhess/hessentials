"""
HUMAN STUDIES VOL. 1 — Batch 10: RECOGNITION TEST 03 (degradation).
Subject: Jordan. Removal order DECLARED, weakest predicted anchor
first, so the final survivable image isolates the claimed dominant:
  A  all channels (baseline, h034 geometry)
  B  minus mouth            (scarf low)
  C  minus mouth+hair       (+ beanie)
  D  minus mouth+hair+nose  (scarf raised: ONLY brow-gaze visible)
  E  minus everything       (+ sunglasses: contour and wraps alone)
  F  DECOY — Nicolas Knuth at D-level degradation (his heavy low
     brows + pale eyes in the same wrap). If the judge calls F
     "Jordan," a style tell is exposed.
Presentation shuffled; key and predictions sealed in the ledger.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def jordan_base(eyes=True, nose=True, mouth=True, hair=True,
                beanie=False, scarf_low=False, scarf_high=False,
                shades=False):
    S = []
    S += [s([(246,300),(256,212),(306,154),(370,142),(440,174),(466,256),(470,314)], 3.0)]
    if hair:
        S += [s([(290,238),(308,184),(352,154),(396,148)], 2.2)]
        S += [s([(336,244),(364,198),(406,176)], 1.6)]
        S += [s([(268,304),(302,264),(352,276),(402,262),(444,306)], 2.0)]
    if beanie:
        S += [s([(238,310),(250,238),(306,196),(372,186),(436,212),(462,272),(466,316)], 3.6)]
        S += [s([(244,316),(304,292),(372,288),(434,302),(468,322)], 2.6)]
        S += [s([(300,294),(306,266)], 1.2)]
        S += [s([(366,290),(370,262)], 1.2)]
    S += [s([(256,318),(250,390),(262,454),(280,518),(310,564),(352,584)], 2.8)]
    S += [s([(460,324),(464,396),(452,460),(432,522),(400,568),(356,586)], 3.3)]
    if eyes and not shades:
        S += [s([(280,360),(312,354),(342,358)], 2.8)]
        S += [s([(378,357),(410,351),(440,357)], 2.8)]
        S += [s([(286,392),(312,384),(338,391)], 2.5)]
        S += [s([(306,386),(314,394),(307,401),(299,394),(306,386)], 1.3)]
        S += [s([(292,402),(314,406),(336,400)], 1.4)]
        S += [s([(380,390),(406,382),(432,389)], 2.5)]
        S += [s([(400,384),(408,392),(401,399),(393,392),(400,384)], 1.3)]
        S += [s([(386,400),(408,404),(430,398)], 1.4)]
    if shades:
        S += [s([(272,362),(308,354),(340,362),(346,398),(332,424),(300,428),(276,412),(268,382),(272,362)], 3.2)]
        S += [s([(372,360),(408,352),(440,360),(444,394),(430,420),(398,426),(376,410),(368,380),(372,360)], 3.2)]
        S += [s([(340,374),(372,372)], 2.4)]
    if nose and not scarf_high:
        S += [s([(358,366),(354,442)], 2.0)]
        S += [s([(332,454),(354,464),(380,452)], 2.3)]
    if mouth and not (scarf_low or scarf_high):
        S += [s([(318,504),(344,498),(360,501),(376,496),(400,503)], 2.7)]
        S += [s([(326,516),(358,524),(390,514)], 2.3)]
        S += [s([(316,570),(338,584),(372,584),(396,570)], 2.3)]
    if scarf_low or scarf_high:
        top = 470 if scarf_high else 520
        S += [s([(252,(top+8)),(300,top),(360,(top-6)),(420,top),(462,(top+10))], 3.4)]
        S += [s([(248,(top+44)),(310,(top+34)),(372,(top+30)),(432,(top+38),),(464,(top+48))], 2.6)]
        S += [s([(256,(top+80)),(320,(top+70)),(390,(top+68)),(452,(top+78))], 2.2)]
    S += [s([(314,586),(310,648)], 2.6)]
    S += [s([(394,586),(400,646)], 2.6)]
    S += [s([(296,652),(356,672),(414,650)], 2.6)]
    return tilt(S, -2.5), [s([(256,390),(460,392)], 1.0)]


def A(): return jordan_base()
def B(): return jordan_base(scarf_low=True, mouth=False)
def C(): return jordan_base(scarf_low=True, mouth=False, hair=False, beanie=True)
def D(): return jordan_base(scarf_high=True, mouth=False, nose=False, hair=False, beanie=True)
def E(): return jordan_base(scarf_high=True, mouth=False, nose=False, hair=False, beanie=True, eyes=False, shades=True)


def F():
    """Decoy: Nicolas Knuth at D-level wrap — HIS brows (heavier,
    closer to the eyes), HIS larger rounder eye, same beanie+scarf."""
    S = []
    S += [s([(250,312),(244,206),(296,150),(372,130),(442,154),(472,216),(476,310)], 3.0)]
    S += [s([(242,322),(254,250),(310,208),(376,198),(440,224),(466,284),(470,328)], 3.6)]
    S += [s([(248,328),(308,304),(376,300),(438,314),(472,334)], 2.6)]
    S += [s([(250,326),(244,388),(254,452),(272,514),(304,558),(348,578)], 2.8)]
    S += [s([(474,322),(478,394),(466,456),(444,518),(408,562),(354,580)], 3.2)]
    # HIS brows: heavier, lower, nearly touching the lids
    S += [s([(276,376),(312,372),(344,376)], 3.8)]
    S += [s([(376,375),(410,370),(442,375)], 3.8)]
    # HIS eyes: larger, rounder openings, pale irises
    S += [s([(284,394),(312,386),(340,393)], 2.5)]
    S += [s([(304,388),(313,397),(305,404),(296,396),(304,388)], 1.3)]
    S += [s([(288,406),(314,410),(338,403)], 1.5)]
    S += [s([(378,392),(406,384),(432,391)], 2.5)]
    S += [s([(398,386),(407,395),(399,402),(390,394),(398,386)], 1.3)]
    S += [s([(382,404),(408,408),(430,401)], 1.5)]
    # same wrap as D
    S += [s([(252,478),(300,470),(360,464),(420,470),(462,480)], 3.4)]
    S += [s([(248,514),(310,504),(372,500),(432,508),(464,518)], 2.6)]
    S += [s([(256,550),(320,540),(390,538),(452,548)], 2.2)]
    S += [s([(312,584),(308,646)], 2.6)]
    S += [s([(392,584),(398,644)], 2.6)]
    S += [s([(294,650),(354,670),(412,648)], 2.6)]
    return tilt(S, -2.0), [s([(250,390),(474,392)], 1.0)]


SEQ = [("A", A), ("B", B), ("C", C), ("D", D), ("E", E), ("F", F)]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = {}
    for name, fn in SEQ:
        S, G = fn()
        imgs[name] = render(S, G, W, H, seed=hash(name) % 999)
        imgs[name].save(os.path.join(OUT, f"rt03_{name}.png"))
        print("wrote", name)
    # shuffled sheet: positions 1-6, letters withheld from filenames
    order = ["D", "B", "F", "A", "E", "C"]          # key sealed in ledger
    sheet = Image.new("RGB", (3 * W, 2 * H), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for n, k in enumerate(order):
        x, y = (n % 3) * W, (n // 3) * H
        sheet.paste(imgs[k], (x, y))
        d.text((x + 20, y + 16), str(n + 1), fill=(31, 29, 27))
    sheet = sheet.resize((3 * W * 2 // 5, 2 * H * 2 // 5))
    sheet.save(os.path.join(OUT, "_recognition_test_03.png"))
    print("sheet ok", order)
