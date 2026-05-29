"""
STAGE 2 — gesture & line of action. Built on stage 1's construction.

The fundamental: a pose is carried by ONE line — the line of action — a single
sweeping curve holding the figure's weight and attitude. The blocked masses from
stage 1 don't stack vertically; they hang on that curve, leaning and flowing
along it. That is what turns a stack of boxes into a living, specific figure.

Principle as procedure: `line_of_action` is the primary structure. Masses
(pelvis, ribcage, head) are placed along it and tilted to its lean; limbs spring
off it as secondary gestures. The LOA is drawn heaviest — it is the spine of the
pose, not an afterthought.

Check (encoded): `render_pose(..., hide_head=True)` removes the head and we
confirm the body alone still carries the attitude. If it goes inert without the
head, the gesture isn't in the body yet.

Still blocking, not a finished body (that's stage 3). Reconstruct, never copy.
"""
import os
import numpy as np
from construction import Camera, edge_strokes, cuboid_opening, render_construction, OUT, W, H

def ellipse_poly(cx, cy, a, b, ang, n=26):
    t = np.linspace(0, 2*np.pi, n)
    x, y = a*np.cos(t), b*np.sin(t)
    ca, sa = np.cos(ang), np.sin(ang)
    X = cx + x*ca - y*sa; Y = cy + x*sa + y*ca
    return list(zip(X.tolist(), Y.tolist()))

def room(cam):
    """Stage 2 is figure-dominant: just a faint floor line to ground the pose
    (the full built room was stage 1's job)."""
    return [dict(ctrl=[(120,806),(1180,806)], w=2.4, cap_start=True, cap_end=True, swell=0, smoothing=0.95)]

def gesture_pose(hide_head=False):
    """A specific, legible gesture: seated and leaning forward, forearms on the
    knees, head lowered — the gathered, weary/contemplative lean. The LINE OF
    ACTION is the C-curve of the spine, hips up and forward to the head. Masses
    are PRESENT (a real torso), limbs read as limbs. Head-covered, the forward
    hunch still carries the whole attitude."""
    S = []
    # Rendered as a flowing, living gesture (not a rigid ellipse armature). The
    # construction is underneath — proportion, the seated masses — but the marks
    # are confident contour and the LINE OF ACTION dominates. Seated, leaning
    # forward, forearms to the knees, head bowed. Facing left.
    # --- LINE OF ACTION / curved back: seat up the spine to the bowed head ---
    S.append(dict(ctrl=[(648,648),(606,544),(566,430),(548,356),(520,316)], w=13, lead=0.08, tail=0.16, swell=0.5, smoothing=0.72))
    # --- head, bowed forward (no face) ---
    if not hide_head:
        S.append(dict(ctrl=[(520,316),(498,298),(474,316),(478,352),(508,360)], w=8, lead=0.12, tail=0.2, swell=0.35, smoothing=0.7))
        S.append(dict(ctrl=[(474,316),(486,300),(508,304)], w=5, lead=0.25, tail=0.3, swell=0.5, smoothing=0.7))   # hair
    # --- front of torso: chest curving down to the lap ---
    S.append(dict(ctrl=[(522,372),(566,500),(612,610)], w=8, lead=0.12, tail=0.24, swell=0.35, phase=1.0, smoothing=0.7))
    # --- near leg: thigh forward to the knee, shin down to the floor ---
    S.append(dict(ctrl=[(612,612),(720,632),(786,636)], w=10, lead=0.14, swell=0.36, smoothing=0.7))             # thigh
    S.append(dict(ctrl=[(786,636),(792,716),(806,802)], w=9, lead=0.12, swell=0.34, cap_end=True, smoothing=0.7))# shin/foot
    # --- far leg, a little behind ---
    S.append(dict(ctrl=[(600,620),(706,650),(764,656)], w=8.5, lead=0.16, swell=0.34, smoothing=0.7))
    S.append(dict(ctrl=[(764,656),(770,732),(782,812)], w=7.5, lead=0.14, swell=0.32, cap_end=True, smoothing=0.7))
    # --- arms: shoulder down to forearms resting on the knees (the lean) ---
    S.append(dict(ctrl=[(540,388),(636,520),(778,632)], w=8, lead=0.12, tail=0.16, swell=0.38, smoothing=0.7))   # near arm, welds to the knee
    S.append(dict(ctrl=[(556,398),(652,540),(758,652)], w=7, lead=0.16, tail=0.22, swell=0.32, smoothing=0.7))   # far arm
    # --- seat: a short ground-contact under the hips (weight) ---
    S.append(dict(ctrl=[(600,654),(672,662),(610,656)], w=6, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))
    return S

def render_pose(seed=2, hide_head=False, name="stage2_gesture"):
    cam = Camera(W, H, eye_level=0.44, vpx=0.50, f=820, cam_h=1.45)
    solid = gesture_pose(hide_head=hide_head)
    faint = room(cam)
    render_construction(solid, faint, W, H, seed=seed).save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render_pose(name="stage2_gesture")
    render_pose(name="stage2_gesture_headless", hide_head=True)   # the encoded check
    print("done")
