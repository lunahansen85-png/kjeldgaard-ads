#!/usr/bin/env python3
"""
Adds text overlay to Kjeldgaard template image.
Edit QUOTE, NAME, and OUTPUT_NAME below to create new variations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE = '"Jeg droppede natcremen og dagcremen — nu bruger jeg kun ét produkt"'
NAME  = "- KARINA"
OUTPUT_NAME = "kjeldgaard_karina.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE      = Path("/Users/lunahansen/Desktop/Claude ads/template_base.jpg")
OUT_DIR   = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD   = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_REG    = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_EMOJI  = "/System/Library/Fonts/Apple Color Emoji.ttc"

img  = Image.open(BASE).convert("RGBA")
W, H = img.size   # 1762 x 1850

draw = ImageDraw.Draw(img)

WHITE  = (255, 255, 255, 255)
GOLD   = (255, 184, 0, 255)
SHADOW = (0, 0, 0, 130)

# Max width for text (left side only, away from product)
MAX_W = 950
x_text = 150
y_text = 340

# ── Wrap quote text to fit MAX_W ─────────────────────────────────────────────
font_quote = ImageFont.truetype(FONT_BOLD, size=80)

def wrap_text(text, font, max_width):
    """Wrap text so each line fits within max_width pixels."""
    words = text.replace('\n', ' \n ').split(' ')
    lines = []
    current = ''
    for word in words:
        if word == '\n':
            lines.append(current.strip())
            current = ''
            continue
        test = (current + ' ' + word).strip()
        w = draw.textlength(test, font=font)
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return '\n'.join(lines)

quote_clean = QUOTE.replace('"', '“').replace('"', '”')
wrapped = wrap_text(quote_clean, font_quote, MAX_W)

# Shadow then text
draw.multiline_text((x_text+3, y_text+3), wrapped, font=font_quote,
                    fill=SHADOW, spacing=14)
draw.multiline_text((x_text, y_text), wrapped, font=font_quote,
                    fill=WHITE, spacing=14)

# ── Stars (draw gold circles as stars manually) ───────────────────────────────
bbox = draw.multiline_textbbox((x_text, y_text), wrapped,
                                font=font_quote, spacing=14)
y_stars = bbox[3] + 50
star_size = 52
star_gap  = 62
for i in range(5):
    cx = x_text + i * star_gap + star_size // 2
    cy = y_stars + star_size // 2
    # Draw a simple filled star using polygon
    import math
    points = []
    for j in range(10):
        angle = math.pi / 5 * j - math.pi / 2
        r = star_size // 2 if j % 2 == 0 else star_size // 4
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=GOLD)

# ── Name ─────────────────────────────────────────────────────────────────────
font_name = ImageFont.truetype(FONT_REG, size=56)
y_name = y_stars + star_size + 36
draw.text((x_text+3, y_name+3), NAME, font=font_name, fill=SHADOW)
draw.text((x_text, y_name), NAME, font=font_name, fill=WHITE)

# ── Save ─────────────────────────────────────────────────────────────────────
out = img.convert("RGB")
out_path = OUT_DIR / OUTPUT_NAME
out.save(out_path, quality=95)
print(f"Saved: {out_path}")
