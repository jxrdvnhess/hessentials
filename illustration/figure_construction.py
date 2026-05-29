"""
STAGE 3 — figure construction. Built on the reclined-gazing-up gesture (stage 2),
which is the exact pose the Merida notebook beat needs.

The fundamental (Loomis): a believable body is simple solid masses with
proportion and balance — a torso with volume, a real lap and back, limbs that
are tapered tubes with weight (never thin sticks), an arm that could actually
wrap or bear weight, and clean joins (no tangles where parts meet).

Second half of the gate: the believable body must STAY ALIVE. The masses hang on
the living action line; they don't replace it. So the head-cover test from stage
2 is run again, now on a real body: hide the head and the reclined-gazing-up
attitude must still hold. Believable AND alive, or it isn't a pass.
"""
import os
from line_figure import render

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1200, 950

def reclined_body(hide_head=False):
    """Reclined, weight settled back onto a propping arm, legs extended forward,
    head tipped back gazing up-and-out. Facing left; legs extend right (toward
    the light, in the beat). Torso = back contour (the action line) + front
    contour; limbs are tapered tubes with real width."""
    S = []
    # ===== TORSO — the action line lives in the back; front gives it volume =====
    S.append(dict(ctrl=[(398,378),(440,452),(508,556),(566,624)], w=13, lead=0.08, tail=0.14, swell=0.45, smoothing=0.7))  # BACK (action line)
    S.append(dict(ctrl=[(406,400),(452,486),(516,576),(576,618)], w=9, lead=0.12, tail=0.2, swell=0.35, phase=1.0, smoothing=0.7))  # front of torso -> lap
    # ===== HEAD — tipped back, gazing up, no face =====
    if not hide_head:
        S.append(dict(ctrl=[(398,378),(388,318),(356,298),(326,322),(330,358)], w=8, lead=0.10, tail=0.2, swell=0.35, smoothing=0.7))  # skull, tipped back
        S.append(dict(ctrl=[(330,358),(340,388),(364,392),(398,384)], w=6, lead=0.16, tail=0.3, swell=0.3, phase=0.6, smoothing=0.7))   # jaw/throat (chin up)
        S.append(dict(ctrl=[(356,298),(386,302),(398,330)], w=5, lead=0.22, tail=0.3, swell=0.5, smoothing=0.7))   # hair
    # ===== NEAR LEG — a tube with volume (top + underside), extended forward =====
    S.append(dict(ctrl=[(572,616),(656,634),(744,650)], w=12, lead=0.14, swell=0.3, smoothing=0.7))               # thigh top
    S.append(dict(ctrl=[(562,650),(652,668),(736,680)], w=9, lead=0.16, tail=0.2, swell=0.3, smoothing=0.7))      # thigh underside
    S.append(dict(ctrl=[(744,652),(812,676),(880,702)], w=10, lead=0.12, swell=0.3, smoothing=0.7))               # shin top
    S.append(dict(ctrl=[(736,682),(806,704),(872,720)], w=8, lead=0.14, tail=0.18, swell=0.3, smoothing=0.7))     # shin underside
    S.append(dict(ctrl=[(880,702),(910,708),(874,722)], w=7, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))  # foot
    # ===== FAR LEG — subordinate, slightly behind and lower =====
    S.append(dict(ctrl=[(556,634),(700,668),(848,718)], w=11, lead=0.16, tail=0.16, swell=0.32, smoothing=0.7))
    S.append(dict(ctrl=[(848,718),(878,724),(846,736)], w=6.5, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))  # far foot
    # ===== PROPPING ARM — bears the reclined weight: a tube to the planted hand =
    S.append(dict(ctrl=[(404,414),(360,500),(322,612),(312,648)], w=11, lead=0.12, tail=0.10, swell=0.4, smoothing=0.72))  # upper arm -> forearm -> wrist
    # the planted hand (fingers spread on the ground), full weight
    S.append(dict(ctrl=[(308,648),(296,672)], w=5, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))
    S.append(dict(ctrl=[(316,652),(308,684)], w=4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))
    S.append(dict(ctrl=[(326,650),(324,684)], w=4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))
    S.append(dict(ctrl=[(336,646),(342,680)], w=4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))
    # ===== NEAR ARM — rests forward onto the lap/thigh (a tube, welds to the hand)
    S.append(dict(ctrl=[(418,428),(476,544),(556,604)], w=10, lead=0.12, tail=0.08, swell=0.36, smoothing=0.72))
    # ===== seat / ground contact under the hips (weight) =====
    S.append(dict(ctrl=[(540,668),(606,674),(548,670)], w=6, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))
    return S, []

if __name__ == "__main__":
    S,_ = reclined_body(hide_head=False)
    render(S, [], W, H, render_on_linen=True,  seed=4).save(f"{OUT}/stage3_body_linen.png")
    render(S, [], W, H, render_on_linen=False, seed=4).save(f"{OUT}/stage3_body_bare.png")
    Sh,_ = reclined_body(hide_head=True)
    render(Sh, [], W, H, render_on_linen=False, seed=4).save(f"{OUT}/stage3_body_headless.png")
    print("done")
