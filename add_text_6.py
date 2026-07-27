#!/usr/bin/env python3
"""
Adds text overlay to Kjeldgaard template 6 (face close-up, grey bg).
Layout: HEADLINE (white uppercase bold) top-left, then quote (white bold),
then name + gold stars bottom-left.
Edit HEADLINE, QUOTE, NAME, OUTPUT_NAME to create new variations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
HEADLINE    = '27% FÆRRE RYNKER\nPÅ 28 DAGE'
QUOTE       = '"Er forbavset over virkningen! Mine rynker ved øjnene, halsen og omkring munden er blevet formindsket"'
NAME        = '- Kate'
OUTPUT_NAME = "kjeldgaard6_kate.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_6.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1742 x 1600

draw = ImageDraw.Draw(img)

WHITE  = (255, 255, 255)
GOLD   = (230, 172, 40)
SHADOW = (0, 0, 0)

X_TEXT     = 75
Y_HEADLINE = 200
MAX_W      = 560
STAR_R     = 24
STAR_GAP   = 54
NUM_STARS  = 5

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines, current = [], ''
    for word in words:
        test = (current + ' ' + word).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return '\n'.join(lines)

def draw_star(cx, cy, r_outer, r_inner, fill):
    points = []
    for i in range(10):
        angle = math.pi / 5 * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

# Headline
font_headline = ImageFont.truetype(FONT_BOLD, size=88)
draw.multiline_text((X_TEXT, Y_HEADLINE), HEADLINE, font=font_headline,
                    fill=WHITE, spacing=12, stroke_width=3, stroke_fill=WHITE)
hl_bbox = draw.multiline_textbbox((X_TEXT, Y_HEADLINE), HEADLINE,
                                   font=font_headline, spacing=12)
y_quote = hl_bbox[3] + 130

# Quote — auto-size
NAME_SIZE  = 52
font_name  = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h     = draw.textbbox((0, 0), NAME, font=font_name)[3]
star_row_h = STAR_R * 2
Y_BOTTOM   = H - 150
available_h = Y_BOTTOM - y_quote - star_row_h - 100 - name_h

for size in range(62, 28, -2):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(14, size // 3)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

draw.multiline_text((X_TEXT, y_quote), wrapped, font=font_quote,
                    fill=WHITE, spacing=spacing, stroke_width=2, stroke_fill=WHITE)

bbox = draw.multiline_textbbox((X_TEXT, y_quote), wrapped, font=font_quote, spacing=spacing)
y_name = bbox[3] + 100

# Name + stars on same line
draw.text((X_TEXT, y_name), NAME, font=font_name, fill=WHITE, stroke_width=2, stroke_fill=WHITE)
name_w = draw.textlength(NAME, font=font_name)
x_stars = X_TEXT + int(name_w) + 18
for i in range(NUM_STARS):
    cx = x_stars + i * STAR_GAP + STAR_R
    cy = y_name + name_h // 2
    draw_star(cx, cy, STAR_R, STAR_R // 2, GOLD)

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
