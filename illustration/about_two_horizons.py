"""
Hessentials — About page, Study 05: two horizons.

One scene, two cameras. A table set for two, minutes before. The host's chair
angled, just risen from. Two glasses at the guest's place, one at the host's.
Late light from the right. Nothing else.

Sketch A — standing horizon (a step inside the room).
Sketch B — seated horizon (the guest's chair).

Pinhole camera (construction.py doctrine: one space, one floor, one VP) under a
wandering living line (linen.stroke_alpha). The tabletop is opaque: strokes
behind it are clipped against its projected silhouette, so the line stops where
the world does. Evaluation criterion is curiosity, not admiration:
"Who is about to sit down here?"
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from linen import stroke_alpha

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "samples")
os.makedirs(OUT, exist_ok=True)

CREAM = np.array([246, 241, 232], float)
INK = np.array([54, 49, 44], float)

TOP = 0.74          # table height
R = 0.525           # table radius


# ------------------------------------------------------------------ camera
class Cam:
    def __init__(self, w, h, eye_level, f, cam_h, vpx=0.5):
        self.w, self.h = w, h
        self.EY = h * eye_level
        self.VPx = w * vpx
        self.f = f
        self.camH = cam_h

    def project(self, p):
        x, y, z = p
        z = max(float(z), 0.12)
        return (self.VPx + self.f * x / z, self.EY - self.f * (y - self.camH) / z)

    def scale(self, z):
        return self.f / max(float(z), 0.12)


class Scene:
    """Scene coords: table center at origin, guest side -z, host side +z.
    yaw rotates the whole scene about Y; (dx,dz) places it in camera space."""

    def __init__(self, cam, yaw, dx, dz):
        self.cam = cam
        self.ca, self.sa = np.cos(yaw), np.sin(yaw)
        self.dx, self.dz = dx, dz
        self.strokes = []           # (pts2, w, alpha_key, occluded_flag)

    def T(self, p):
        x, y, z = p
        return (x * self.ca + z * self.sa + self.dx, y,
                -x * self.sa + z * self.ca + self.dz)

    def poly(self, pts3, w=2.0, layer="solid", occl=False, raw=False):
        pts2 = [self.cam.project(p if raw else self.T(p)) for p in pts3]
        self.strokes.append((pts2, w, layer, occl))

    def anchor(self, p):
        pw = self.T(p)
        sx, sy = self.cam.project(pw)
        return sx, sy, self.cam.scale(pw[2]), pw[2]

    def glyph(self, pts2_local, sx, sy, s, w=2.0, layer="solid"):
        pts = [(sx + x * s, sy + y * s) for x, y in pts2_local]
        self.strokes.append((pts, w, layer, False))

    def squash(self, y_top, z):
        """ellipse minor-axis ratio for a horizontal circle at height y_top
        seen from cam height at depth z."""
        return float(np.clip(0.95 * abs(self.cam.camH - y_top) / max(z, 0.2),
                             0.16, 0.55))

    def table_silhouette(self, dilate=1.045):
        pts = np.array([self.cam.project(self.T(p))
                        for p in circle3(0, TOP, 0, R, n=72)])
        c = pts.mean(0)
        return c + (pts - c) * dilate


def circle3(cx, cy, cz, r, n=56, a0=0.0, a1=2 * np.pi):
    aa = np.linspace(a0, a1, n)
    return [(cx + r * np.cos(a), cy, cz + r * np.sin(a)) for a in aa]


def ell(cx, cy, rx, ry, n=36, a0=0.0, a1=2 * np.pi):
    aa = np.linspace(a0, a1, n)
    return [(cx + rx * np.cos(a), cy + ry * np.sin(a)) for a in aa]


# ------------------------------------------------------------------ furniture
def table(S):
    S.poly(circle3(0, TOP, 0, R), w=2.4)                       # top rim
    S.poly(circle3(0, TOP - 0.028, 0, R * 0.995), w=1.7)       # edge thickness
    for a in (0.79, 2.36, 3.93, 5.50):                         # four legs
        lx, lz = 0.40 * np.cos(a), 0.40 * np.sin(a)
        S.poly([(lx, TOP - 0.03, lz), (lx * 1.10, 0, lz * 1.10)], w=2.2)


def chair(S, cx, cz, yaw, w=0.43, d=0.43, seat=0.45, back=0.93, occl=False):
    ca, sa = np.cos(yaw), np.sin(yaw)

    def L(x, z, y):
        return (cx + x * ca + z * sa, y, cz - x * sa + z * ca)

    hx, hz = w / 2, d / 2
    corners = [(-hx, -hz), (hx, -hz), (hx, hz), (-hx, hz)]
    for (x, z) in corners:
        S.poly([L(x, z, seat), L(x * 0.9, z * 0.9, 0)], w=2.2, occl=occl)
    S.poly([L(*c, seat) for c in corners] + [L(*corners[0], seat)], w=2.2, occl=occl)
    for (x, z) in [(-hx, hz), (hx, hz)]:
        S.poly([L(x, z, seat), L(x, z * 1.06, back)], w=2.2, occl=occl)
    S.poly([L(-hx, hz * 1.055, back - 0.045), L(hx, hz * 1.055, back - 0.045)],
           w=2.2, occl=occl)
    S.poly([L(-hx, hz * 1.045, back - 0.13), L(hx, hz * 1.045, back - 0.13)],
           w=2.0, occl=occl)
    S.poly([L(-hx, hz * 1.03, seat + 0.28), L(hx, hz * 1.03, seat + 0.28)],
           w=2.0, occl=occl)


# ------------------------------------------------------------------ tableware
def plate(S, x, z, r=0.135):
    S.poly(circle3(x, TOP + 0.005, z, r), w=2.0)
    S.poly(circle3(x, TOP + 0.007, z, r * 0.70), w=1.4)


def cutlery(S, x, z, side, toward=1.0):
    bx = x + side * 0.225
    z0, z1 = z + 0.115 * toward, z - 0.10 * toward
    S.poly([(bx, TOP + 0.007, z0), (bx, TOP + 0.007, z1)], w=1.8)
    if side < 0:
        for k in (-0.012, 0.0, 0.012):
            S.poly([(bx + k, TOP + 0.007, z1),
                    (bx + k, TOP + 0.007, z1 - 0.035 * toward)], w=1.3)


def napkin(S, x, z, s=0.082, ang=0.18):
    ca, sa = np.cos(ang), np.sin(ang)
    q = [(-s, -s), (s, -s), (s, s), (-s, s), (-s, -s)]
    S.poly([(x + a * ca - b * sa, TOP + 0.009, z + a * sa + b * ca) for a, b in q],
           w=1.6)
    S.poly([(x - s * 0.7 * ca, TOP + 0.011, z - s * 0.7 * sa),
            (x + s * 0.7 * ca, TOP + 0.011, z + s * 0.7 * sa)], w=1.2)


def tumbler(S, x, z, h=0.105, r=0.036):
    sx, sy, s, zc = S.anchor((x, TOP, z))
    sq = S.squash(TOP + h, zc)
    S.glyph([(-r, 0), (-r * 0.92, -h)], sx, sy, s, w=1.8)
    S.glyph([(r, 0), (r * 0.92, -h)], sx, sy, s, w=1.8)
    S.glyph(ell(0, -h, r * 0.92, r * 0.92 * sq), sx, sy, s, w=1.6)
    S.glyph(ell(0, 0, r, r * sq * 0.8, a0=0.15, a1=np.pi - 0.15), sx, sy, s, w=1.5)


def wineglass(S, x, z, h=0.205):
    sx, sy, s, zc = S.anchor((x, TOP, z))
    sq = S.squash(TOP + h, zc)
    rb, rf = 0.043, 0.036
    yb = -h + 0.005
    S.glyph(ell(0, 0, rf, rf * sq * 0.8, a0=0.1, a1=np.pi - 0.1), sx, sy, s, w=1.6)
    S.glyph([(0, -0.004), (0, -h + 0.085)], sx, sy, s, w=1.7)
    S.glyph([(-rb, yb + 0.012), (-rb * 0.96, yb + 0.052), (-rb * 0.30, yb + 0.085),
             (0, yb + 0.086)], sx, sy, s, w=1.7)
    S.glyph([(rb, yb + 0.012), (rb * 0.96, yb + 0.052), (rb * 0.30, yb + 0.085),
             (0, yb + 0.086)], sx, sy, s, w=1.7)
    S.glyph(ell(0, yb + 0.012, rb, rb * sq), sx, sy, s, w=1.6)


def carafe(S, x, z, h=0.235):
    sx, sy, s, zc = S.anchor((x, TOP, z))
    sq = S.squash(TOP + h, zc)
    r0, rn = 0.062, 0.030
    prof = [(r0 * 0.85, 0), (r0, -0.045), (r0 * 0.96, -0.115), (rn, -0.165),
            (rn, -h + 0.012), (rn * 1.25, -h)]
    S.glyph(prof, sx, sy, s, w=1.8)
    S.glyph([(-a, b) for a, b in prof], sx, sy, s, w=1.8)
    S.glyph(ell(0, -h, rn * 1.25, rn * 1.25 * sq), sx, sy, s, w=1.5)
    S.glyph(ell(0, 0, r0 * 0.85, r0 * 0.85 * sq * 0.8, a0=0.2, a1=np.pi - 0.2),
            sx, sy, s, w=1.4)
    S.glyph(ell(0, -0.085, r0 * 0.97, r0 * 0.97 * sq, a0=0.5, a1=np.pi - 0.5),
            sx, sy, s, w=1.2)


# ------------------------------------------------------------------ light & room
def room_and_light(S, wall_z=5.0, span=5.0):
    S.poly([(-span * 0.6, 0, wall_z), (span, 0, wall_z)], w=1.8,
           layer="faint", occl=True)
def setting(S, side, wine):
    """side=-1 guest (near), +1 host (far)."""
    z = 0.335 * side
    plate(S, 0, z)
    napkin(S, 0, z)
    cutlery(S, 0, z, -1, toward=-side)
    cutlery(S, 0, z, +1, toward=-side)
    gz = z - 0.135 * side                         # glasses above the plate
    tumbler(S, 0.215 * -side, gz)
    if wine:
        wineglass(S, 0.215 * -side + (-side) * 0.090, gz - 0.065 * side)


# ------------------------------------------------------------------ rendering
def resample(pts, step=3.0):
    p = np.array(pts, float)
    if len(p) < 2:
        return p
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    if d[-1] < 1.5:
        return p
    n = int(np.clip(d[-1] / step, len(p), 1600))
    tt = np.linspace(0, d[-1], n)
    return np.stack([np.interp(tt, d, p[:, 0]), np.interp(tt, d, p[:, 1])], 1)


def inside(pts, poly):
    x, y = pts[:, 0], pts[:, 1]
    px, py = poly[:, 0], poly[:, 1]
    flag = np.zeros(len(pts), bool)
    j = len(poly) - 1
    for i in range(len(poly)):
        cond = ((py[i] > y) != (py[j] > y)) & \
               (x < (px[j] - px[i]) * (y - py[i]) / (py[j] - py[i] + 1e-12) + px[i])
        flag ^= cond
        j = i
    return flag


def split_runs(pts, hidden):
    runs, cur = [], []
    for p, h in zip(pts, hidden):
        if h:
            if len(cur) > 2:
                runs.append(np.array(cur))
            cur = []
        else:
            cur.append(p)
    if len(cur) > 2:
        runs.append(np.array(cur))
    return runs


def add_noise(q, rng, amp):
    n = len(q)
    if n < 3:
        return q

    def sm(k):
        k = max(1, min(k, n))
        return np.convolve(rng.normal(0, 1, n), np.ones(k) / k, mode="same")

    L = np.sum(np.linalg.norm(np.diff(q, axis=0), axis=1))
    sc = amp * np.clip(L / 90.0, 0.5, 1.6)
    out = q.copy()
    out[:, 0] += sm(9) * sc + sm(3) * sc * 0.35
    out[:, 1] += sm(9) * sc + sm(3) * sc * 0.35
    return out


def render(S, W, H, fname, seed=3):
    rng = np.random.default_rng(seed)
    sil = S.table_silhouette()
    solid, faint = [], []
    for pts2, w, layer, occl in S.strokes:
        q = resample(pts2)
        if len(q) < 2:
            continue
        runs = split_runs(q, inside(q, sil)) if occl else [q]
        for run in runs:
            run = add_noise(run, rng, amp=1.5 if layer == "solid" else 2.0)
            (solid if layer == "solid" else faint).append(
                (list(map(tuple, run)), w))
    img = np.ones((H, W, 3)) * CREAM
    af = stroke_alpha(W, H, faint, width=2.0, jitterblur=0.7, supersample=3) * 0.23
    a = stroke_alpha(W, H, solid, width=2.0, jitterblur=0.55, supersample=3)
    a = np.clip(np.maximum(a, af), 0, 1)
    img = img * (1 - a[..., None]) + INK * a[..., None]
    g = rng.normal(0, 1, (H, W))
    g = np.asarray(Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-6) * 255)
                                   .astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float)
    img += (g / 255.0 - 0.5)[..., None] * 6.0
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)) \
        .filter(ImageFilter.GaussianBlur(0.3)).save(os.path.join(OUT, fname), quality=94)
    print("saved", fname, "-", len(solid), "solid /", len(faint), "faint strokes")


# ------------------------------------------------------------------ sketches
def sketch_a():
    """Standing horizon — a step inside the room. Near-profile view: the two
    chairs read as silhouettes, one tucked, one angled and pushed back."""
    W, H = 1500, 1900
    cam = Cam(W, H, eye_level=0.40, f=1300, cam_h=1.52, vpx=0.5)
    S = Scene(cam, yaw=1.30, dx=-0.10, dz=2.45)
    # wall junction + late light, in camera space (raw)
    S.poly([(-6.0, 0, 9.0), (6.5, 0, 9.0)], w=1.8, layer="faint", raw=True)
    S.poly([(0.55, 0, 2.0), (3.0, 0, 2.9), (2.6, 0, 3.6), (0.35, 0, 2.5),
            (0.55, 0, 2.0)], w=1.8, layer="faint", occl=True, raw=True)
    # light chords on the tabletop (scene coords, avoid the settings)
    a = np.arctan2(1.0, -0.52)
    ux, uz = np.cos(a), np.sin(a)
    for c in (-0.34, 0.36):
        px, pz = c * -uz, c * ux
        d = np.sqrt(max(R * R - c * c, 0)) * 0.96
        S.poly([(px - ux * d, TOP + 0.004, pz - uz * d),
                (px + ux * d, TOP + 0.004, pz + uz * d)], w=1.5, layer="faint")
    table(S)
    chair(S, 0.0, -0.55, yaw=np.pi)                        # guest chair, tucked
    chair(S, 0.10, 0.97, yaw=0.46, occl=True)              # host chair: angled, risen-from
    setting(S, -1, wine=True)
    setting(S, +1, wine=False)
    carafe(S, -0.165, 0.02)
    render(S, W, H, "about-two-horizons-A-standing.png", seed=21)


def sketch_b():
    """Seated horizon — the guest's chair."""
    W, H = 1500, 1900
    cam = Cam(W, H, eye_level=0.42, f=1050, cam_h=1.16)
    S = Scene(cam, yaw=0.05, dx=0.02, dz=1.08)
    room_and_light(S, wall_z=4.5, span=6.0)
    # late light from behind the viewer's right shoulder, falling past the
    # table onto the far floor (camera space, clipped by the tabletop)
    S.poly([(-2.2, 0, 3.2), (-0.75, 0, 1.6), (-1.6, 0, 1.35), (-3.2, 0, 2.5),
            (-2.2, 0, 3.2)], w=1.8, layer="faint", occl=True, raw=True)
    table(S)
    chair(S, -0.62, 0.98, yaw=-0.50, back=0.97, occl=True)  # host chair: angled, risen-from
    setting(S, -1, wine=True)                              # your place, foreground
    setting(S, +1, wine=False)                             # the host's, opposite
    carafe(S, -0.36, -0.18)
    render(S, W, H, "about-two-horizons-B-seated.png", seed=22)


if __name__ == "__main__":
    sketch_a()
    sketch_b()
