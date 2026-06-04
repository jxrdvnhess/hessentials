# Sketch 301 — A15: Specialization. Domain: musical notation.
# A lay / B locally damaged / C genuinely specialist / D apparent expertise
# (extended notation, unreadable to lay, plausible to an expert).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

SP = 14  # staff line spacing
X0, X1 = 100, 545

def staff(d, top):
    for i in range(5):
        d.line([(X0, top + i * SP), (X1, top + i * SP)], fill=INK, width=2)
    return top

def gclef(d, x, top):
    cy = top + 2 * SP
    d.ellipse([x - 11, cy - 4, x + 11, cy + 18], outline=INK, width=4)
    d.line([(x + 6, top - 16), (x + 6, top + 4 * SP + 8)], fill=INK, width=4)
    d.ellipse([x + 2, top + 4 * SP + 4, x + 12, top + 4 * SP + 14], fill=INK)
    d.arc([x - 14, top - 18, x + 18, top + 16], 200, 340, fill=INK, width=4)

def cclef(d, x, top):
    d.line([(x - 10, top), (x - 10, top + 4 * SP)], fill=INK, width=6)
    d.line([(x - 2, top), (x - 2, top + 4 * SP)], fill=INK, width=3)
    d.arc([x, top - 2, x + 26, top + 2 * SP + 2], 270, 90, fill=INK, width=5)
    d.arc([x, top + 2 * SP - 2, x + 26, top + 4 * SP + 2], 270, 90, fill=INK, width=5)

def note(d, x, line, top, open_head=False, stem="up", xhead=False, diamond=False):
    y = top + line * SP / 2
    if xhead:
        d.line([(x - 8, y - 7), (x + 8, y + 7)], fill=INK, width=3)
        d.line([(x - 8, y + 7), (x + 8, y - 7)], fill=INK, width=3)
    elif diamond:
        d.polygon([(x, y - 8), (x + 9, y), (x, y + 8), (x - 9, y)], outline=INK, width=3)
    elif open_head:
        d.ellipse([x - 9, y - 7, x + 9, y + 7], outline=INK, width=3)
    else:
        d.ellipse([x - 9, y - 7, x + 9, y + 7], fill=INK)
    if stem == "up":
        d.line([(x + 8, y), (x + 8, y - 3.2 * SP)], fill=INK, width=3)
    elif stem == "down":
        d.line([(x - 8, y), (x - 8, y + 3.2 * SP)], fill=INK, width=3)
    elif stem == "both":
        d.line([(x + 8, y), (x + 8, y - 3.2 * SP)], fill=INK, width=3)
        d.line([(x - 8, y), (x - 8, y + 3.2 * SP)], fill=INK, width=3)
    return x, y

def timesig(d, x, top, a="4", b="4"):
    f = ImageFont.truetype(FONT, 30)
    d.text((x, top + SP), a, font=f, fill=INK, anchor="mm")
    d.text((x, top + 3 * SP), b, font=f, fill=INK, anchor="mm")

def bar(d, x, top, h=1.0, double=False):
    d.line([(x, top), (x, top + 4 * SP * h)], fill=INK, width=3)
    if double:
        d.line([(x + 7, top), (x + 7, top + 4 * SP)], fill=INK, width=6)

MELODY = [(6, False), (5, False), (4, False), (5, False), (4, False), (3, False), (2, True)]

def sheet_a():
    im = ground(); d = ImageDraw.Draw(im)
    top = staff(d, 280)
    gclef(d, 130, top); timesig(d, 175, top)
    xs = [225, 275, 325, 415, 465, 515]
    for (ln, oh), x in zip(MELODY[:6], xs):
        note(d, x, ln, top, open_head=oh, stem="up" if ln >= 4 else "down")
    bar(d, 370, top); bar(d, 540, top, double=True)
    im.save(f"{OUT}/a_lay.png")

def sheet_b():
    im = ground(); d = ImageDraw.Draw(im)
    top = staff(d, 280)
    gclef(d, 130, top); timesig(d, 175, top, "4", "7")     # impossible denominator
    xs = [225, 275, 325, 415, 465, 515]
    for i, ((ln, oh), x) in enumerate(zip(MELODY[:6], xs)):
        stem = "both" if i == 2 else ("up" if ln >= 4 else "down")  # doubled stem
        note(d, x, ln, top, open_head=oh, stem=stem)
    bar(d, 370, top, h=0.5)                                 # half-height barline
    bar(d, 540, top, double=True)
    im.save(f"{OUT}/b_damaged.png")

def sheet_c():
    im = ground(); d = ImageDraw.Draw(im)
    f_it = ImageFont.truetype(FONTI, 20)
    f_sm = ImageFont.truetype(FONT, 16)
    top = staff(d, 280)
    cclef(d, 135, top); timesig(d, 185, top, "7", "8")
    # beamed eighth pair
    n1 = note(d, 230, 5, top, stem="up"); n2 = note(d, 262, 4, top, stem="up")
    d.line([(n1[0] + 8, n1[1] - 3.2 * SP), (n2[0] + 8, n2[1] - 3.2 * SP)], fill=INK, width=6)
    # 5:4 tuplet bracket over a group
    xs = [310, 338, 366, 394, 422]
    for k, x in enumerate(xs):
        note(d, x, 3 + (k % 2), top, stem="down")
    yb = top - 26
    d.line([(xs[0] - 10, yb), (xs[-1] + 10, yb)], fill=INK, width=2)
    d.line([(xs[0] - 10, yb), (xs[0] - 10, yb + 8)], fill=INK, width=2)
    d.line([(xs[-1] + 10, yb), (xs[-1] + 10, yb + 8)], fill=INK, width=2)
    d.text(((xs[0] + xs[-1]) / 2, yb - 10), "5:4", font=f_sm, fill=INK, anchor="mm")
    # fermata over a final open note
    nf = note(d, 490, 2, top, open_head=True, stem="down")
    d.arc([nf[0] - 14, nf[1] - SP * 4.4, nf[0] + 14, nf[1] - SP * 2.4], 180, 360, fill=INK, width=3)
    d.ellipse([nf[0] - 2, nf[1] - SP * 3.3, nf[0] + 2, nf[1] - SP * 3.3 + 4], fill=INK)
    # dynamics
    d.text((232, top + 4 * SP + 24), "pp", font=f_it, fill=INK, anchor="mm")
    d.text((420, top + 4 * SP + 24), "sfz", font=f_it, fill=INK, anchor="mm")
    # 8va dashed bracket
    for x in range(300, 440, 14):
        d.line([(x, top - 48), (x + 7, top - 48)], fill=INK, width=2)
    d.text((286, top - 48), "8va", font=f_sm, fill=INK, anchor="mm")
    bar(d, 295, top); bar(d, 455, top); bar(d, 540, top, double=True)
    im.save(f"{OUT}/c_specialist.png")

def sheet_d():
    im = ground(); d = ImageDraw.Draw(im)
    rng = random.Random(15)
    f_sm = ImageFont.truetype(FONT, 14)
    # asemic tempo marking
    x = 110
    for _ in range(9):
        h = rng.randint(9, 16)
        d.line([(x, 96), (x + rng.randint(-2, 3), 96 - h)], fill=INK, width=2)
        if rng.random() < 0.4:
            d.line([(x - 3, 90), (x + 5, 90)], fill=INK, width=1)
        x += rng.randint(8, 12)
    d.text((x + 18, 88), "= 63+", font=f_sm, fill=INK, anchor="lm")
    for top in (170, 400):
        staff(d, top)
        gclef(d, 126, top) if top == 170 else cclef(d, 130, top)
    top = 170
    # black cluster wedge spanning the staff
    d.polygon([(190, top), (230, top + 4 * SP), (190, top + 4 * SP)], fill=INK)
    d.line([(228, top + 4 * SP), (228, top - 30)], fill=INK, width=3)
    # x-heads with feathered beam (diverging)
    xs = [270, 300, 330, 360]
    pts = [note(d, x, 2 + (k % 3), top, xhead=True, stem="up") for k, x in enumerate(xs)]
    for b in range(3):
        d.line([(xs[0] + 8, top - 38 + b * 5), (xs[-1] + 8, top - 38 - b * 7)], fill=INK, width=3)
    # glissando sweep to a diamond harmonic
    nA = note(d, 408, 6, top, stem="down")
    nB = note(d, 505, 0, top, diamond=True, stem="down")
    d.line([(nA[0] + 12, nA[1] - 3), (nB[0] - 12, nB[1] + 3)], fill=INK, width=2)
    for t in range(1, 5):
        xx = nA[0] + 12 + (nB[0] - nA[0] - 24) * t / 5
        yy = nA[1] - 3 + (nB[1] - nA[1] + 6) * t / 5
        d.line([(xx - 3, yy + 3), (xx + 3, yy - 3)], fill=INK, width=2)
    top = 400
    # boxed aleatoric segment with asemic instruction
    d.rectangle([180, top - 24, 330, top + 4 * SP + 24], outline=INK, width=3)
    for k, x in enumerate([200, 230, 260, 290, 315]):
        note(d, x, rng.choice([1, 2, 4, 5, 6]), top, xhead=(k % 2 == 0),
             diamond=(k % 2 == 1), stem="up" if k % 2 else "down")
    xx = 184
    for _ in range(7):
        h = rng.randint(7, 12)
        d.line([(xx, top + 4 * SP + 44), (xx + rng.randint(-2, 2), top + 4 * SP + 44 - h)],
               fill=INK, width=2)
        xx += rng.randint(7, 10)
    d.line([(338, top + 2 * SP), (372, top + 2 * SP)], fill=INK, width=2)  # arrow
    d.polygon([(378, top + 2 * SP), (366, top + 2 * SP - 6), (366, top + 2 * SP + 6)], fill=INK)
    # half-flat-ish accidental (mirrored flat) + stacked cluster of seconds
    bx = 400
    d.line([(bx, top - 6), (bx, top + 2 * SP + 6)], fill=INK, width=3)
    d.arc([bx - 14, top + SP, bx + 2, top + 2 * SP + 4], 270, 90, fill=INK, width=3)  # mirrored bowl
    for k in range(4):
        d.ellipse([bx + 18 - 8, top + (3 + k) * SP / 2 - 6, bx + 18 + 8, top + (3 + k) * SP / 2 + 6],
                  outline=INK, width=3)
    # arrowed stem note (pitch bend)
    nC = note(d, 480, 3, top, stem="up")
    d.polygon([(nC[0] + 8, nC[1] - 3.2 * SP - 10), (nC[0] + 2, nC[1] - 3.2 * SP + 2),
               (nC[0] + 14, nC[1] - 3.2 * SP + 2)], fill=INK)
    bar(d, 540, 170, double=True); bar(d, 540, 400, double=True)
    im.save(f"{OUT}/d_boundary.png")

if __name__ == "__main__":
    sheet_a(); sheet_b(); sheet_c(); sheet_d()
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_lay", "b_damaged", "c_specialist", "d_boundary"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
