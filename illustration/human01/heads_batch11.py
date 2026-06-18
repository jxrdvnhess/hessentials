"""
HUMAN STUDIES VOL. 1 — Batch 11: RECOGNITION TEST 04 (the kill attempt).
INSTRUMENT A (modified, declared): no neutral Jennifer exists in the
expanded archive — the closest honest observation is IMG_2904: her
first PROFILE, smile at roughly half power. Drawn as observed; the
perturbation is therefore smile-REDUCED + view-rotated, two changes at
once, a weaker falsifier and labeled as such.
INSTRUMENT B: eye-region chimeras. h084 = Jensen's everything with
Jordan's brow-gaze transplanted. h085 = Jordan's everything with
Jensen's brow-gaze transplanted.
SEALED PREDICTIONS in ledger. Judge: who + confidence per position.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def h083_jennifer_profile():
    """Jennifer, IMG_2904: near-true profile left, smile ~half power.
    Offered channels: hair mass with the blue streak, the profile
    nose (slight lift at tip), red lip with teeth just showing, firm
    chin-to-neck line, chandelier earring. Crescents unavailable."""
    S = []
    # hair: long falls, crown sweep, the blue streak as one dark ribbon
    S += [s([(456,300),(440,212),(372,160),(290,156),(230,204),(208,290)], 3.4)]
    S += [s([(456,300),(470,396),(462,500),(478,600),(458,680)], 3.4)]
    S += [s([(208,290),(214,344),(238,376)], 2.6)]                 # fringe sweep
    S += [s([(300,170),(268,230),(258,290)], 1.6)]
    S += [s([(404,340),(412,440),(404,540),(416,620)], 2.8)]       # the streak
    S += [s([(372,360),(380,460),(372,560)], 1.4)]
    # PROFILE line: brow → straight nose, tip lifted → red lip → chin
    S += [s([(238,330),(228,360),(232,374)], 2.6)]                 # brow ridge
    S += [s([(232,374),(216,428),(214,442)], 2.6)]                 # the nose
    S += [s([(214,442),(228,452),(238,456)], 1.9)]                 # lifted base
    S += [s([(230,470),(252,478)], 2.6)]                           # upper lip (red)
    S += [s([(236,484),(246,488)], 1.5)]                           # teeth hint
    S += [s([(234,494),(256,502)], 2.2)]                           # lower lip
    S += [s([(252,514),(268,540),(292,560)], 2.6)]                 # firm chin
    S += [s([(292,560),(348,592),(412,604)], 2.8)]                 # jaw → ear
    # the visible eye in profile: lash line + brow, cheek lifted under
    S += [s([(246,338),(282,326),(310,330)], 2.4)]
    S += [s([(252,362),(278,356)], 2.2)]
    S += [s([(256,372),(276,370)], 1.2)]
    S += [s([(268,420),(290,452),(286,478)], 1.5)]                 # smile cheek, half
    # chandelier earring — the photo's one ornament
    S += [s([(386,400),(382,432)], 1.6)]
    S += [s([(370,436),(396,436),(398,462),(368,460),(370,436)], 1.8)]
    S += [s([(374,464),(376,482)], 1.1)]
    S += [s([(386,464),(388,484)], 1.1)]
    # neck, striped top hinted by two lines
    S += [s([(294,564),(286,640)], 2.6)]
    S += [s([(404,608),(412,668)], 2.6)]
    S += [s([(260,690),(330,712),(404,694)], 2.6)]
    S += [s([(272,716),(336,734),(398,718)], 1.2)]
    S = tilt(S, 2.0)
    return S, [s([(232,374),(412,380)], 1.0)]


def h084_chimera_jensen_body_jordan_eyes():
    """Jensen's everything — long face, forward quiff, longer nose,
    tucked-corner mouth, proud ears — with JORDAN'S brow-gaze unit
    transplanted (straight low 2.8 brows, outlined hooded eyes)."""
    S = []
    S += [s([(252,290),(258,202),(310,152),(376,142),(440,168),(464,244),(468,304)], 3.2)]
    S += [s([(296,210),(330,168),(378,150)], 2.2)]
    S += [s([(272,294),(304,258),(352,248),(402,262),(440,298)], 2.0)]
    S += [s([(258,310),(250,386),(258,456),(274,526),(304,578),(346,598)], 2.8)]
    S += [s([(462,316),(466,392),(456,462),(436,530),(402,582),(352,600)], 3.3)]
    S += [s([(310,584),(334,598),(368,598),(392,584)], 2.2)]
    # >>> JORDAN'S unit: straight LOW brows, short gap, hooded outlined eyes
    S += [s([(282,366),(314,360),(346,364)], 2.8)]
    S += [s([(378,363),(410,357),(440,363)], 2.8)]
    S += [s([(288,384),(314,378),(340,383)], 1.3)]
    S += [s([(286,396),(314,388),(338,394),(344,399)], 2.5)]
    S += [s([(306,390),(314,398),(307,405),(299,398),(306,390)], 1.3)]
    S += [s([(292,406),(316,410),(338,404)], 1.4)]
    S += [s([(380,394),(386,389),(410,382),(436,389)], 2.5)]
    S += [s([(400,386),(408,394),(401,401),(393,394),(400,386)], 1.3)]
    S += [s([(386,404),(410,408),(432,402)], 1.4)]
    # <<< back to Jensen: longer nose, tucked mouth, ears, long neck
    S += [s([(356,372),(352,448)], 1.9)]
    S += [s([(330,460),(354,470),(380,458)], 2.3)]
    S += [s([(310,512),(340,506),(358,509),(378,504),(408,511)], 2.7)]
    S += [s([(306,514),(298,508)], 1.5)]
    S += [s([(412,510),(418,504)], 1.5)]
    S += [s([(322,526),(358,533),(394,524)], 2.1)]
    S += [s([(252,368),(236,382),(242,420),(260,428)], 2.2)]
    S += [s([(466,364),(482,378),(476,416),(458,424)], 2.2)]
    S += [s([(312,600),(308,656)], 2.5)]
    S += [s([(392,600),(398,654)], 2.5)]
    S += [s([(296,662),(354,680),(410,660)], 2.6)]
    S = tilt(S, 2.0)
    return S, [s([(258,390),(462,390)], 1.0)]


def h085_chimera_jordan_body_jensen_eyes():
    """Jordan's everything — quiff vector, midface, nose, composed
    mouth — with JENSEN'S brow-gaze transplanted (heavy 3.4 brows,
    larger whole-iris steady eyes)."""
    S = []
    S += [s([(246,300),(256,212),(306,154),(370,142),(440,174),(466,256),(470,314)], 3.0)]
    S += [s([(290,238),(308,184),(354,154),(398,148)], 2.2)]
    S += [s([(268,302),(302,262),(352,274),(402,260),(444,306)], 2.0)]
    S += [s([(256,318),(250,390),(262,454),(280,518),(310,564),(352,584)], 2.8)]
    S += [s([(460,324),(464,396),(452,460),(432,522),(400,568),(356,586)], 3.3)]
    S += [s([(316,570),(338,584),(372,584),(396,570)], 2.3)]
    # >>> JENSEN'S unit: heavy straight brows, larger open whole irises
    S += [s([(280,358),(314,352),(346,357)], 3.4)]
    S += [s([(376,356),(410,350),(442,356)], 3.4)]
    S += [s([(286,390),(314,382),(340,389)], 2.5)]
    S += [s([(304,384),(312,392),(305,399),(297,391),(304,384)], 1.3)]
    S += [s([(290,400),(316,404),(338,398)], 1.4)]
    S += [s([(378,388),(406,380),(432,387)], 2.5)]
    S += [s([(398,382),(406,390),(399,397),(391,389),(398,382)], 1.3)]
    S += [s([(384,398),(408,402),(430,396)], 1.4)]
    # <<< back to Jordan: the nose, the composed mouth
    S += [s([(358,366),(354,442)], 2.0)]
    S += [s([(332,454),(354,464),(380,452)], 2.3)]
    S += [s([(318,504),(344,498),(360,501),(376,496),(400,503)], 2.7)]
    S += [s([(326,516),(358,524),(390,514)], 2.3)]
    S += [s([(314,586),(310,648)], 2.6)]
    S += [s([(394,586),(400,646)], 2.6)]
    S += [s([(296,652),(356,672),(414,650)], 2.6)]
    S = tilt(S, -2.5)
    return S, [s([(256,388),(460,390)], 1.0)]


SEQ = [("h083", h083_jennifer_profile),
       ("h084", h084_chimera_jensen_body_jordan_eyes),
       ("h085", h085_chimera_jordan_body_jensen_eyes)]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = {}
    for name, fn in SEQ:
        S, G = fn()
        imgs[name] = render(S, G, W, H, seed=hash(name) % 999)
        imgs[name].save(os.path.join(OUT, f"{name}.png"))
        print("wrote", name)
    order = ["h084", "h083", "h085"]   # key sealed in ledger
    sheet = Image.new("RGB", (3 * W, H), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for n, k in enumerate(order):
        sheet.paste(imgs[k], (n * W, 0))
        d.text((n * W + 20, 16), str(n + 1), fill=(31, 29, 27))
    sheet.resize((3 * W // 2, H // 2)).save(os.path.join(OUT, "_recognition_test_04.png"))
    print("sheet ok", order)
