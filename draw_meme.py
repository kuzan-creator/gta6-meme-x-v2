#!/usr/bin/env python3
"""Draw the v2 meme: LEONIDA EXPRESS parcel tracking notice for GTA VI.

1200x1200, vector-style with PIL so every word stays pixel-perfect and
readable when the judge shrinks it to 480x480. All text is drawn here;
no photo, no copied artwork.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (230, 0, 126)
DARK_MAGENTA = (200, 0, 105)
GREEN = (0, 150, 60)
DARK_GREEN = (0, 120, 45)
GRAY = (90, 90, 90)
LIGHT_GRAY = (210, 210, 210)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center(draw, x0, x1, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def star_points(cx, cy, r_outer, r_inner, rotation=-90):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.radians(rotation + i * 36)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Header: black bar -------------------------------------------
    d.rectangle([0, 0, W, 170], fill=BLACK)
    center(d, 0, W, 22, "LEONIDA EXPRESS", font(BOLD, 86), WHITE)
    center(d, 0, W, 118, "P A R C E L   T R A C K I N G", font(BOLD, 40), MAGENTA)

    # ---- Tracking number ----------------------------------------------
    d.text((60, 195), "TRACKING NO.", font=font(BOLD, 26), fill=GRAY)
    d.text((60, 225), "GTA-VI-2013-4811", font=font(BOLD, 58), fill=BLACK)
    d.line([(60, 292), (1140, 292)], fill=LIGHT_GRAY, width=3)

    # ---- From / To ------------------------------------------------------
    d.text((60, 312), "FROM", font=font(BOLD, 24), fill=GRAY)
    d.text((60, 340), "ROCKSTAR GAMES", font=font(BOLD, 42), fill=BLACK)
    d.text((60, 388), "Los Santos", font=font(REG, 30), fill=BLACK)
    d.text((640, 312), "TO", font=font(BOLD, 24), fill=GRAY)
    d.text((640, 340), "EVERY FAN", font=font(BOLD, 42), fill=BLACK)
    d.text((640, 388), "Vice City, Leonida", font=font(REG, 30), fill=BLACK)
    d.line([(60, 432), (1140, 432)], fill=LIGHT_GRAY, width=3)

    # ---- Tracking timeline ----------------------------------------------
    d.text((60, 452), "TRACKING HISTORY", font=font(BOLD, 26), fill=GRAY)
    rows = [
        ("ORDERED", "Sep 17, 2013", False),
        ("SHIPPED", "Sep 17, 2013", False),
        ("IN TRANSIT", "13 YEARS", False),
        ("OUT FOR DELIVERY", "Nov 19, 2026", False),
        ("DELIVERED", "Nov 19, 2026", True),
    ]
    top = 492
    step = 40
    # vertical connector line
    d.line([(76, top + 12), (76, top + step * 4 + 12)], fill=GREEN, width=4)
    for i, (label, date, done) in enumerate(rows):
        y = top + i * step
        # node circle
        d.ellipse([64, y, 88, y + 24], fill=GREEN)
        d.text((104, y - 4), label, font=font(BOLD, 30),
               fill=GREEN if done else BLACK)
        dw = d.textlength(date, font=font(REG, 30))
        d.text((780 - dw, y - 4), date, font=font(REG, 30),
               fill=GREEN if done else BLACK)

    # ---- Details box ------------------------------------------------------
    d.rounded_rectangle([60, 700, 1140, 872], radius=14, outline=BLACK, width=3)
    details = [
        ("CONTENTS:", "1x GRAND THEFT AUTO VI"),
        ("WEIGHT:", "13 YEARS OF PATIENCE"),
        ("STATUS:", "DELIVERED AFTER 4,811 DAYS"),
        ("SIGNED FOR BY:", "JASON & LUCIA"),
    ]
    for i, (label, value) in enumerate(details):
        y = 716 + i * 40
        d.text((84, y), label, font=font(BOLD, 28), fill=BLACK)
        lw = d.textlength(label, font=font(BOLD, 28))
        d.text((84 + lw + 14, y), value, font=font(REG, 28), fill=BLACK)

    # ---- Barcode ----------------------------------------------------------
    rng = random.Random(2013)
    x = 320
    while x < 880:
        bw = rng.choice([3, 4, 5, 7, 9])
        if rng.random() < 0.6:
            d.rectangle([x, 890, x + bw, 940], fill=BLACK)
        x += bw + rng.choice([2, 3, 4])
    center(d, 0, W, 946, "GTA-VI-2013-4811", font(REG, 24), BLACK)

    # ---- DELIVERED stamp (rotated, right of timeline, covers no text) ----
    stamp = Image.new("RGBA", (360, 130), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 356, 126], radius=12, outline=GREEN, width=7)
    sd.text((180, 34), "DELIVERED", font=font(BOLD, 58), fill=GREEN,
            anchor="ma")
    stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (800, 470), stamp)

    # ---- Footer: magenta bar ----------------------------------------------
    d.rectangle([0, 980, W, H], fill=MAGENTA)

    # Ghost (white, left)
    gx0, gx1 = 84, 224
    d.rectangle([gx0, 1072, gx1, 1152], fill=WHITE)
    d.pieslice([gx0, 1002, gx1, 1142], 180, 360, fill=WHITE)
    # wavy bottom: three white scallops hanging below the body rectangle;
    # the magenta footer behind them forms the wave gaps by itself.
    for cx in (107, 154, 201):
        d.ellipse([cx - 23, 1129, cx + 23, 1175], fill=WHITE)
    # eyes
    d.ellipse([118, 1082, 140, 1112], fill=BLACK)
    d.ellipse([170, 1082, 192, 1112], fill=BLACK)
    d.ellipse([124, 1088, 132, 1098], fill=WHITE)
    d.ellipse([176, 1088, 184, 1098], fill=WHITE)
    # star coin in the ghost's hand (white coin, magenta star)
    d.ellipse([222, 1112, 286, 1176], fill=WHITE)
    d.polygon(star_points(254, 1144, 24, 10), fill=MAGENTA)

    # Footer text (right of ghost)
    d.text((320, 1012), "PAID BY MY AI AGENT", font=font(BOLD, 52), fill=WHITE)
    d.text((320, 1080), "with a bounty payout it earned on",
           font=font(REG, 30), fill=WHITE)
    d.rounded_rectangle([320, 1124, 600, 1180], radius=28, fill=WHITE)
    center(d, 320, 600, 1134, "make.fun", font(BOLD, 40), MAGENTA)

    img.save("/home/hatch/workspace/gta6-meme-x-v2/meme.png")
    img.save("/home/hatch/workspace/gta6-meme-x-v2/meme.jpg", quality=92)
    print("saved meme.png / meme.jpg", img.size)


if __name__ == "__main__":
    main()
