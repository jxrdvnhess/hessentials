"""
Hessentials — ABOUT, three rooms (true reset).

Not an object. Not a symbol. Three real moments a discerning person lives inside,
re-rendered from owned interiors as made graphite drawings on cream — the same
photoreal -> honest-fiction move the homepage rooms were made with. The room is
the subject; the meal, the cup, the dishes are simply in it. Meaning is left to
emerge from observation.

  dinner   — a long table winding down, wine and a candle, light off the garden
  morning  — coffee at the table, the day not yet started
  cleanup  — the kitchen after, washing up in low light

Programmatic synthesis only (no diffusion). Warm graphite on warm cream.
"""
import os
from PIL import Image
from about_backdrop import scratch_on_cream

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "public", "home")
OUT = os.path.join(HERE, "..", "public", "about")

JOBS = [
    ("hacienda-01-dinner.jpg", "about-room-dinner.jpg"),
    ("hacienda-03-morning.jpg", "about-room-morning.jpg"),
    ("hacienda-04-cleanup.jpg", "about-room-cleanup.jpg"),
]


def size_for(path, long=1600):
    aw, ah = Image.open(path).size
    if aw >= ah:
        return long, round(long * ah / aw)
    return round(long * aw / ah), long


if __name__ == "__main__":
    for src, out in JOBS:
        sp = os.path.join(SRC, src)
        W, H = size_for(sp)
        img = scratch_on_cream(
            sp, W, H, seed=4, n_strokes=120000, ss=2, gamma=1.5,
            edge_gain=1.3, follow=0.88, floor_cut=0.24,
            hi_protect=0.6, hi_strength=0.88, glow=0.6, sat=6.5,
        )
        img.save(os.path.join(OUT, out), quality=92)
        print("saved", out, f"{W}x{H}")
