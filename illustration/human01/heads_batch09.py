"""
HUMAN STUDIES VOL. 1 — Batch 09 (h079–h082): THE MURDER ATTEMPT.
Doctrine under attack: the eye-region thesis.
Method: the four roster subjects drawn with the eye region WITHHELD —
sunglasses (Jordan, Jim, Jennifer) and distance (Jensen). Rendered
unlabeled as Recognition Test 02. If the judge still recognizes them,
the thesis weakens; if identity collapses, it strengthens.
Pre-registered prediction (logged before judging, ledger): Jennifer
most recognizable without eyes (smile structure is a strong secondary
climate), Jim next (the grin), Jordan third (nose + hair vector),
Jensen least (build alone).
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


# ---------------------------------------------------------------- h079
def h079():
    """Jordan — Spain street selfie, aviators. Withheld: brow-gaze.
    Offered: quiff vector, temple-notch hairline edge, the nose below
    the frames, composed level mouth, lean jaw, long neck."""
    S = []
    S += [s([(248,300),(258,212),(308,154),(372,142),(442,172),(468,254),(472,312)], 3.0)]
    S += [s([(292,236),(310,182),(356,152),(398,146)], 2.2)]
    S += [s([(338,242),(366,196),(408,174)], 1.6)]
    S += [s([(268,302),(302,262),(352,274),(402,260),(446,304)], 2.0)]
    S += [s([(258,318),(252,390),(264,452),(282,516),(312,562),(352,582)], 2.8)]
    S += [s([(460,324),(464,396),(452,458),(432,520),(400,566),(356,584)], 3.3)]
    S += [s([(316,568),(338,582),(372,582),(396,568)], 2.3)]
    # aviators: teardrop lenses + thin bridge + temple arms
    S += [s([(272,362),(308,354),(340,362),(346,398),(332,424),(300,428),(276,412),(268,382),(272,362)], 3.2)]
    S += [s([(372,360),(408,352),(440,360),(444,394),(430,420),(398,426),(376,410),(368,380),(372,360)], 3.2)]
    S += [s([(340,374),(372,372)], 2.4)]
    S += [s([(268,372),(252,366)], 2.0)]
    S += [s([(444,370),(460,364)], 2.0)]
    # the nose emerging below the frames — anchor 2 still on duty
    S += [s([(356,428),(354,446)], 1.9)]
    S += [s([(332,456),(354,466),(380,454)], 2.3)]
    # composed level mouth, fuller lower lip — anchor 5
    S += [s([(318,506),(344,500),(360,503),(376,498),(400,505)], 2.7)]
    S += [s([(326,518),(358,526),(390,516)], 2.3)]
    S += [s([(314,584),(310,646)], 2.6)]
    S += [s([(394,584),(400,644)], 2.6)]
    S += [s([(296,652),(356,672),(414,650)], 2.6)]
    S = tilt(S, -3.0)
    return S, [s([(258,390),(460,392)], 1.0)]


# ---------------------------------------------------------------- h080
def h080():
    """Jim — pickleball court, visor + wraparound shades. Withheld:
    the squint. Offered: the GRIN with its deep folds (left corner
    leading), lean weathered jaw, cords, the visor's sun posture."""
    S = []
    S += [s([(242,300),(252,222),(314,182),(384,178),(446,212),(468,286),(472,318)], 3.0)]
    S += [s([(234,316),(298,294),(376,290),(444,304),(480,320)], 3.2)]  # visor brim
    S += [s([(300,290),(296,250),(330,232)], 1.6)]                 # short hair above
    S += [s([(372,288),(390,246)], 1.4)]
    S += [s([(248,330),(242,394),(254,452),(274,510),(306,552),(350,572)], 2.8)]
    S += [s([(470,334),(474,398),(462,456),(440,514),(406,556),(356,574)], 3.4)]
    S += [s([(310,556),(336,570),(372,570),(398,556)], 2.3)]
    # wraparound shades: one dark band, no eyes offered
    S += [s([(268,362),(308,352),(356,356),(404,350),(444,360),(448,392),(406,404),(356,400),(306,406),(272,394),(268,362)], 3.6)]
    S += [s([(354,358),(356,398)], 1.8)]
    S += [s([(354,408),(350,438)], 1.7)]
    S += [s([(326,450),(350,461),(378,449)], 2.4)]
    # THE GRIN — his non-eye anchor, asymmetric, full folds
    S += [s([(292,486),(326,477),(356,482),(386,478),(418,489)], 2.9)]
    S += [s([(304,495),(338,493),(372,492),(404,492)], 1.6)]
    S += [s([(300,504),(334,522),(372,524),(410,506)], 2.9)]
    S += [s([(312,530),(352,540),(392,528)], 2.0)]
    S += [s([(322,446),(294,478),(288,498)], 2.2)]
    S += [s([(382,444),(412,474),(418,494)], 2.2)]
    # lean neck, cords, tee
    S += [s([(306,574),(300,632)], 2.6)]
    S += [s([(398,574),(406,630)], 2.6)]
    S += [s([(328,584),(326,626)], 1.1)]
    S += [s([(370,586),(372,628)], 1.1)]
    S += [s([(294,640),(354,660),(412,638)], 2.6)]
    S = tilt(S, -2.5)
    return S, [s([(248,384),(470,384)], 1.0)]


# ---------------------------------------------------------------- h081
def h081():
    """Jennifer — patio, big sunglasses. Withheld: the crescents.
    Offered: the SMILE structure entire (upper teeth, apples, folds),
    long blonde waves, slim chin — her secondary climate at full power."""
    S = []
    S += [s([(330,118),(256,140),(208,210),(192,318),(200,444),(214,560),(238,650)], 3.5)]
    S += [s([(330,118),(402,138),(450,206),(466,312),(456,440),(470,548),(444,644)], 3.5)]
    S += [s([(240,258),(222,360),(240,460),(222,552)], 1.6)]
    S += [s([(440,252),(456,354),(440,452),(458,544)], 1.6)]
    S += [s([(280,298),(316,272),(358,264),(400,278),(426,306)], 1.9)]
    S += [s([(264,332),(258,400),(270,460),(290,514),(322,550),(356,566)], 2.8)]
    S += [s([(438,336),(444,404),(432,464),(410,518),(384,552),(360,568)], 3.2)]
    S += [s([(318,556),(340,566),(366,566),(386,556)], 1.9)]
    # big rounded sunglasses
    S += [s([(274,366),(312,356),(344,366),(348,404),(334,424),(300,426),(276,410),(270,384),(274,366)], 3.6)]
    S += [s([(362,364),(400,354),(430,364),(434,400),(420,420),(388,424),(364,408),(358,382),(362,364)], 3.6)]
    S += [s([(348,380),(362,378)], 2.6)]
    S += [s([(354,426),(350,448)], 1.5)]
    S += [s([(330,458),(350,468),(374,457)], 2.1)]
    # THE SMILE at full power — teeth, apples, folds: can it carry her?
    S += [s([(298,488),(330,477),(358,481),(386,475),(418,486)], 2.9)]
    S += [s([(310,496),(342,494),(374,493),(406,491)], 1.5)]
    S += [s([(308,504),(340,518),(374,519),(410,500)], 2.7)]
    S += [s([(320,526),(356,535),(392,523)], 1.9)]
    S += [s([(324,442),(300,472),(294,490)], 1.8)]
    S += [s([(382,440),(408,468),(414,486)], 1.8)]
    S += [s([(280,446),(298,464)], 1.2)]
    S += [s([(432,442),(414,460)], 1.2)]
    S += [s([(318,568),(312,620)], 2.4)]
    S += [s([(386,568),(392,618)], 2.4)]
    S += [s([(256,662),(318,628),(358,622)], 2.8)]
    S += [s([(448,658),(396,626),(362,622)], 2.8)]
    S = tilt(S, 5.0)
    return S, [s([(264,388),(438,388)], 1.0)]


# ---------------------------------------------------------------- h082
def h082():
    """Jensen — lakeside at dusk, full figure at DISTANCE. The face is
    a few marks at this range; identity is asked of the long light
    frame, the stance, the dark crop, plaid shorts, the dog beside.
    The hardest condition: no face to speak of at all."""
    S = []
    # horizon + lake shimmer
    S += [s([(80,560),(360,552),(620,558)], 1.8)]
    S += [s([(120,580),(300,576)], 0.9)]
    S += [s([(380,578),(560,574)], 0.9)]
    # the figure: tall, light, weight on one leg — the family frame
    S += [s([(330,238),(322,260),(326,282)], 2.2)]                 # small head, dark crop
    S += [s([(322,244),(316,252)], 1.8)]                           # hair mass hint
    S += [s([(326,282),(322,300)], 1.6)]                           # neck
    S += [s([(300,308),(326,300),(352,306)], 2.2)]                 # shoulders square
    S += [s([(300,308),(292,360),(296,406)], 2.2)]                 # torso left
    S += [s([(352,306),(358,358),(352,404)], 2.2)]                 # torso right
    S += [s([(296,406),(290,418),(356,418),(352,404)], 2.0)]       # untucked tee hem
    # plaid shorts: block + two cross ticks
    S += [s([(292,418),(288,470),(296,474),(322,472),(324,420)], 2.2)]
    S += [s([(324,420),(326,470),(352,468),(356,418)], 2.2)]
    S += [s([(298,436),(318,434)], 0.9)]
    S += [s([(330,448),(350,446)], 0.9)]
    # legs: long, lean; weight on the left
    S += [s([(300,474),(298,520),(296,556)], 2.1)]
    S += [s([(340,470),(346,518),(350,554)], 2.1)]
    S += [s([(288,560),(304,562)], 1.9)]
    S += [s([(342,558),(360,560)], 1.9)]
    # arms: one loose, one toward the dog
    S += [s([(298,312),(284,352),(282,392)], 1.9)]
    S += [s([(354,312),(366,350),(382,378)], 1.9)]
    # the dog at his right knee, small dark mass + tail
    S += [s([(386,490),(420,478),(452,490),(458,524),(428,540),(396,532),(386,490)], 2.4)]
    S += [s([(418,476),(424,462),(434,470)], 1.7)]                 # head up at him
    S += [s([(458,512),(478,496)], 1.5)]                           # tail
    # dusk cloud bank, one line
    S += [s([(100,200),(300,180),(520,196)], 1.2)]
    S = tilt(S, 0.5)
    return S, [s([(80,560),(620,558)], 0.8)]


HEADS = [("h079", h079), ("h080", h080), ("h081", h081), ("h082", h082)]

if __name__ == "__main__":
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for name, fn in HEADS:
        if only and name not in only:
            continue
        S, G = fn()
        img = render(S, G, W, H, seed=hash(name) % 999)
        p = os.path.join(OUT, f"{name}.png")
        img.save(p)
        print("wrote", p)
