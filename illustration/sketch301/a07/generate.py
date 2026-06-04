# Sketch 301 — A7: can a static image promise improving information, wordlessly?
# Pair 1: a note with writing at threshold legibility (P1) vs fully legible (C1).
# Pair 2: still life with the background object withheld by defocus (P2) vs all sharp (C2).
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (32, 29, 26)
PAPER = (244, 239, 229)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"

LINES = ["Monday -", "buy lemons", "return the ladder", "call about the gate", "water the fig"]

def ground():
    base = np.full((H, W, 3), (226, 219, 207), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.5, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def note(size, blur):
    im = ground()
    sheet = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    d.polygon([(150, 130), (492, 142), (484, 520), (142, 508)], fill=(248, 244, 234, 255))
    d.line([(150, 130), (492, 142), (484, 520), (142, 508), (150, 130)],
           fill=(180, 172, 158, 255), width=2)
    sheet = sheet.rotate(2, resample=Image.BICUBIC, center=(320, 320))
    im.paste(sheet, (0, 0), sheet)
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dt = ImageDraw.Draw(txt)
    f = ImageFont.truetype(FONT, size)
    y = 185
    for line in LINES:
        dt.text((195, y), line, font=f, fill=(58, 52, 46, 255))
        y += int(size * 1.9)
    txt = txt.rotate(2, resample=Image.BICUBIC, center=(320, 320))
    if blur:
        txt = txt.filter(ImageFilter.GaussianBlur(blur))
    im.paste(txt, (0, 0), txt)
    # soft sheet shadow
    return im

def p1():  # threshold writing: small + slightly soft
    note(13, 1.1).save(f"{OUT}/p1_threshold_note.png")

def c1():  # fully legible
    note(30, 0).save(f"{OUT}/c1_legible_note.png")

def still(blur_bg):
    im = ground()
    # background layer: a jar with scissors handles rising out, on a hinted shelf line
    bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    d.line([(60, 420), (580, 420)], fill=(190, 182, 168, 255), width=3)
    d.polygon([(400, 290), (496, 290), (488, 420), (408, 420)], fill=(205, 196, 182, 255))  # jar
    d.ellipse([400, 278, 496, 302], fill=(214, 206, 192, 255), outline=(170, 162, 148, 255))
    d.ellipse([418, 196, 446, 242], outline=(60, 54, 48, 255), width=8)   # scissors handles
    d.ellipse([452, 192, 480, 238], outline=(60, 54, 48, 255), width=8)
    d.line([(432, 240), (444, 290)], fill=(60, 54, 48, 255), width=7)
    d.line([(466, 236), (452, 290)], fill=(60, 54, 48, 255), width=7)
    if blur_bg:
        bg = bg.filter(ImageFilter.GaussianBlur(9))
    im.paste(bg, (0, 0), bg)
    # foreground layer, always sharp: a small dark cup, low center-left
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    d.polygon([(160, 360), (320, 360), (304, 540), (176, 540)], fill=(52, 47, 42, 255))
    d.ellipse([160, 344, 320, 376], fill=(70, 63, 56, 255), outline=(40, 36, 32, 255))
    d.arc([300, 400, 380, 500], -85, 100, fill=(52, 47, 42, 255), width=14)
    d.ellipse([180, 540, 310, 562], fill=(180, 172, 158, 120))
    im.paste(fg, (0, 0), fg)
    return im

def p2():  # background withheld by defocus
    still(True).save(f"{OUT}/p2_defocus_still.png")

def c2():  # everything given
    still(False).save(f"{OUT}/c2_sharp_still.png")

if __name__ == "__main__":
    p1(); c1(); p2(); c2()
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["p1_threshold_note", "c1_legible_note", "p2_defocus_still", "c2_sharp_still"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
