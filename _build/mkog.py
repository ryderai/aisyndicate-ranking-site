#!/usr/bin/env python3
"""Social preview card. Same house style as the site: paper, ink, hairline rules,
one muted accent. No gradient, no agency brand marks."""
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (250, 248, 243)
INK = (25, 24, 20)
ACC = (31, 92, 77)
DIM = (107, 103, 92)
FAINT = (156, 150, 138)
RULE = (221, 215, 201)

# Font lookup: first file that exists wins. Covers this container, plain Linux and macOS.
SERIF = ["/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf",
         "/System/Library/Fonts/Supplemental/Georgia.ttf",
         "/Library/Fonts/Georgia.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
SERIF_B = ["/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf",
           "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
           "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
MONO = ["/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]


def f(sz, stack):
    for p in stack:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# top and bottom keylines
d.rectangle([0, 0, W, 5], fill=INK)
d.line([64, 566, W - 64, 566], fill=RULE, width=1)

# house mark: 3x3 grid, four filled
bx, by, s, g = 68, 60, 13, 21
d.rectangle([bx - 9, by - 9, bx + 2 * g + s + 9, by + 2 * g + s + 9], outline=INK, width=2)
filled = {(0, 0), (1, 1), (2, 0), (1, 2)}
for r in range(3):
    for c in range(3):
        x, y = bx + c * g, by + r * g
        if (r, c) in filled:
            d.rectangle([x, y, x + s, y + s], fill=INK)
        else:
            d.rectangle([x, y, x + s, y + s], outline=INK, width=2)

d.text((165, 66), "THE GEO AGENCY INDEX", font=f(24, MONO), fill=INK)
d.text((166, 100), "2026 EDITION  ·  MEASURED 14 AUGUST 2026", font=f(15, MONO), fill=FAINT)
d.line([64, 152, W - 64, 152], fill=RULE, width=1)

d.text((64, 196), "29 agencies sell", font=f(60, SERIF_B), fill=INK)
d.text((64, 268), "AI search visibility.", font=f(60, SERIF_B), fill=INK)
d.text((64, 356), "1 has done it on", font=f(60, SERIF_B), fill=ACC)
d.text((64, 428), "its own website.", font=f(60, SERIF_B), fill=ACC)

d.text((64, 512), "Seven public checks. Every score is a file you can open yourself.",
       font=f(24, SERIF), fill=DIM)
d.text((64, 584), "PUBLISHED BY AI SYNDICATE, WHICH IS RANKED IN IT", font=f(14, MONO), fill=FAINT)

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "og.png")
img.save(out)
print("og.png", img.size)
