"""
STAGE 1 — construction & space.

The fundamental: everything in a frame shares ONE space. Forms are solids built
in three dimensions, standing on one ground plane, receding to one vanishing
point. This is what the "floating arch" was missing — the arch and the figure
were placed by eye in 2D with no shared space, so they didn't belong together.

Principle encoded as procedure: a real pinhole `Camera`. Every form — a wall, a
doorway, a blocked figure — is built from 3D points and projected through the
SAME camera. Shared space is then not a matter of taste; it's structural.

Check (run on the work): every standing form's base sits on the floor plane
(Y=0) and recedes to the camera's horizon/VP. `Camera.floor_tick()` drops a
contact mark to verify an object meets the ground. If two forms use one camera,
they share the room.

World: X right, Y up, Z into the screen (depth > 0). Floor at Y=0; camera at
height camH looking down +Z. Reconstruct, never copy.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS, INK
from linen import linen_ground

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1300, 950

class Camera:
    def __init__(self, w, h, eye_level=0.46, vpx=0.52, f=820.0, cam_h=1.45):
        self.w, self.h = w, h
        self.EY = h*eye_level          # horizon screen-y (where Z->inf projects)
        self.VPx = w*vpx               # vanishing point screen-x
        self.f = f                     # focal length
        self.camH = cam_h              # camera height above the floor
    def project(self, X, Y, Z):
        Z = max(float(Z), 1e-3)
        sx = self.VPx + self.f*X/Z
        sy = self.EY  - self.f*(Y - self.camH)/Z
        return (sx, sy)
    def scale(self, Z):
        return self.f/max(float(Z), 1e-3)

# ---- form builders: return lists of edges as [(p0,p1), ...] in world space ----
def cuboid(cx, cy, cz, hx, hy, hz):
    """Axis-aligned box centred (cx,cy,cz) with half-extents; cy is the BASE y
    offset so hy is full height sitting on cy. Returns 12 edges."""
    x0,x1 = cx-hx, cx+hx; y0,y1 = cy, cy+hy; z0,z1 = cz-hz, cz+hz
    c = [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1),
         (x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]
    E = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    return [(c[a],c[b]) for a,b in E]

def project_edges(cam, edges):
    return [(cam.project(*a), cam.project(*b)) for a,b in edges]

def edge_strokes(edges2d, w=5, smoothing=0.7, swell=0.25):
    out=[]
    for (p0,p1) in edges2d:
        out.append(dict(ctrl=[p0,p1], w=w, cap_start=True, cap_end=True,
                        swell=swell, smoothing=smoothing))
    return out

# ---------------------------------------------------------------- render
def render_construction(solid, faint, w, h, seed=0, tone=0.25):
    linen = linen_ground(w, h, seed=seed, tone=tone)
    def layer(strokes):
        im = Image.new("L",(w*SS,h*SS),0); d=ImageDraw.Draw(im)
        for s in strokes: stroke(d, **s)
        return np.asarray(im.resize((w,h),Image.LANCZOS),float)/255.0
    a_solid = layer(solid); a_faint = layer(faint)
    out = linen.copy()
    out = out*(1-(a_faint*0.30)[...,None]) + INK*(a_faint*0.30)[...,None]   # scaffold faint
    out = out*(1-a_solid[...,None]) + INK*a_solid[...,None]                  # forms full
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

# ---------------------------------------------------------------- the scene
def scene_room_figure_doorway():
    cam = Camera(W, H, eye_level=0.44, vpx=0.50, f=820, cam_h=1.45)
    faint, solid = [], []

    # --- scaffold: horizon + a floor grid receding to the VP (proves shared space)
    faint.append(dict(ctrl=[(0,cam.EY),(W,cam.EY)], w=2.5, cap_start=True, cap_end=True, swell=0, smoothing=0.95))
    for gx in (-3,-2,-1,0,1,2,3):                       # floor lines at constant X, receding
        faint += edge_strokes([(cam.project(gx,0,0.6), cam.project(gx,0,40))], w=2.2)
    for gz in (1,2,3,5,8,14):                           # floor cross-lines at depth
        faint += edge_strokes([(cam.project(-6,0,gz), cam.project(6,0,gz))], w=2.2)

    # --- the room: back wall at Z=9, a left wall, meeting the floor (real planes)
    Zback = 9.0
    solid += edge_strokes([(cam.project(-6,0,Zback), cam.project(6,0,Zback))], w=4)        # floor/back-wall seam
    solid += edge_strokes([(cam.project(-6,0,Zback), cam.project(-6,3.0,Zback))], w=4)     # back wall left edge
    solid += edge_strokes([(cam.project(6,0,Zback),  cam.project(6,3.0,Zback))], w=4)      # back wall right edge
    solid += edge_strokes([(cam.project(-6,3.0,Zback),cam.project(6,3.0,Zback))], w=4)     # back wall top
    solid += edge_strokes([(cam.project(-6,0,0.6),   cam.project(-6,0,Zback))], w=4)       # left floor/wall seam

    # --- the DOORWAY: a real opening with depth, cut into the back wall.
    # opening on the wall plane (Z=Zback) + an inner frame stepped back (Z+0.5)
    dx0,dx1, dh = 1.6, 3.0, 2.1
    front = cuboid_opening(cam, dx0,dx1,dh,Zback)
    inner = cuboid_opening(cam, dx0+0.12,dx1-0.12,dh-0.12,Zback+0.5)
    solid += edge_strokes(front, w=4.5)
    solid += edge_strokes(inner, w=3.2)
    # connect front to inner (jamb depth) so it reads as an opening, not a flat rectangle
    for (a,b) in zip(front, inner):
        solid += edge_strokes([(a[0], b[0])], w=2.6)

    # --- the FIGURE, blocked as solid masses, standing on the SAME floor at Z=5.5
    fx, fz = -2.2, 5.5
    solid += edge_strokes(project_edges(cam, cuboid(fx,0.0,fz, 0.28,0.95,0.18)), w=5)        # pelvis+legs block
    solid += edge_strokes(project_edges(cam, cuboid(fx,0.95,fz,0.34,0.85,0.22)), w=5)        # torso/ribcage block
    solid += edge_strokes(project_edges(cam, cuboid(fx,1.86,fz,0.16,0.26,0.16)), w=4.5)      # head block
    solid += edge_strokes(project_edges(cam, cuboid(fx-0.40,0.95,fz,0.10,0.78,0.10)), w=4)   # left arm
    solid += edge_strokes(project_edges(cam, cuboid(fx+0.40,0.95,fz,0.10,0.78,0.10)), w=4)   # right arm
    # ground-contact check: drop a tick where the figure base meets the floor
    solid += floor_tick(cam, fx, fz, hx=0.28)

    return solid, faint, cam

def cuboid_opening(cam, x0, x1, h, Z):
    """A rectangular opening on a wall plane at depth Z: 4 edges."""
    c=[(x0,0,Z),(x1,0,Z),(x1,h,Z),(x0,h,Z)]
    proj=[cam.project(*p) for p in c]
    return [(proj[0],proj[1]),(proj[1],proj[2]),(proj[2],proj[3]),(proj[3],proj[0])]

def floor_tick(cam, X, Z, hx=0.2):
    """A small mark on the floor under a form — verifies it meets the ground."""
    a=cam.project(X-hx,0,Z); b=cam.project(X+hx,0,Z)
    return [dict(ctrl=[a,b], w=4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9)]

if __name__ == "__main__":
    solid, faint, cam = scene_room_figure_doorway()
    render_construction(solid, faint, W, H, seed=2).save(f"{OUT}/stage1_space.png")
    print("done; horizon y=", round(cam.EY), "VPx=", round(cam.VPx))
