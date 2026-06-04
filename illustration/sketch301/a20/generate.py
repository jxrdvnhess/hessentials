# Sketch 301 — A20: The Arrow. The bare channel, measured.
# A single / B competing / C interrupted / D ambiguous-in-the-form.
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def arrow_shape(d, x0, y, length=300, w=26, head=64):
    """Solid arrow pointing right, baseline centered at y."""
    d.rectangle([x0, y - w // 2, x0 + length - head, y + w // 2], fill=INK)
    d.polygon([(x0 + length - head, y - head // 2),
               (x0 + length, y),
               (x0 + length - head, y + head // 2)], fill=INK)

def a_single():
    im = ground(); d = ImageDraw.Draw(im)
    arrow_shape(d, 170, 320)
    im.save(f"{OUT}/a_single.png")

def b_competing():
    im = ground(); d = ImageDraw.Draw(im)
    arrow_shape(d, 170, 240)                       # rightward
    # leftward, equal weight
    x0, y, length, w, head = 170, 400, 300, 26, 64
    d.rectangle([x0 + head, y - w // 2, x0 + length, y + w // 2], fill=INK)
    d.polygon([(x0 + head, y - head // 2), (x0, y), (x0 + head, y + head // 2)], fill=INK)
    im.save(f"{OUT}/b_competing.png")

def c_interrupted():
    im = ground(); d = ImageDraw.Draw(im)
    arrow_shape(d, 170, 320)
    # occluder: a soft grey rounded bar across the shaft's middle
    d.rounded_rectangle([265, 250, 365, 390], 16, fill=(205, 197, 183),
                        outline=(170, 162, 148), width=2)
    im.save(f"{OUT}/c_interrupted.png")

def d_ambiguous():
    im = ground(); d = ImageDraw.Draw(im)
    x0, y, length, w, head = 170, 320, 300, 26, 64
    # shaft
    d.rectangle([x0 + head, y - w // 2, x0 + length - head, y + w // 2], fill=INK)
    # solid head on the right
    d.polygon([(x0 + length - head, y - head // 2),
               (x0 + length, y),
               (x0 + length - head, y + head // 2)], fill=INK)
    # notched (concave) end on the left: a V cut INTO a block — reads as fletching
    # (pointing right) or as an open arrowhead (pointing left)
    d.polygon([(x0, y - head // 2), (x0 + head, y - head // 2),
               (x0 + head, y + head // 2), (x0, y + head // 2),
               (x0 + head * 0.62, y)], fill=INK)
    im.save(f"{OUT}/d_ambiguous.png")

if __name__ == "__main__":
    a_single(); b_competing(); c_interrupted(); d_ambiguous()
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_single", "b_competing", "c_interrupted", "d_ambiguous"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
