#!/usr/bin/env python3
"""
Adds text overlay to Kjeldgaard template 5 (hand holding bottle, warm grey bg).
Edit QUOTE, NAME, and OUTPUT_NAME below to create new variations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE       = 'Mine mørke rander er faktisk væk – og bekymringsrynken i panden er blevet mindre synlig'
NAME        = '- Bettina Kirkegaard'
OUTPUT_NAME = "kjeldgaard5_bettina.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_5.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1396 x 1768

draw = ImageDraw.Draw(img)

WHITE = (255, 255, 255)
GOLD  = (230, 172, 40)

# Text area: starts well below the logo (logo ends ~y=165)
X_TEXT    = 70
Y_TEXT    = 295   # clear gap below logo
MAX_W     = 590
Y_MAX     = 900   # bottom of safe zone before product hand area
NAME_SIZE = 44
STAR_R    = 26    # star outer radius
STAR_GAP  = 62
NUM_STARS = 5

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

font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h    = draw.textbbox((0, 0), NAME, font=font_name)[3]
star_row_h = STAR_R * 2
available_h = Y_MAX - Y_TEXT - star_row_h - 30 - name_h - 25

for size in range(72, 30, -2):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(12, size // 4)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

sw = 2 if size >= 50 else (1 if size >= 36 else 0)
draw.multiline_text((X_TEXT, Y_TEXT), wrapped, font=font_quote,
                    fill=WHITE, spacing=spacing,
                    stroke_width=sw, stroke_fill=WHITE)

bbox = draw.multiline_textbbox((X_TEXT, Y_TEXT), wrapped, font=font_quote, spacing=spacing)

# Gold polygon stars
y_stars = bbox[3] + 40
for i in range(NUM_STARS):
    cx = X_TEXT + i * STAR_GAP + STAR_R
    cy = y_stars + STAR_R
    draw_star(cx, cy, STAR_R, STAR_R // 2, GOLD)

# Name in white
y_name = y_stars + star_row_h + 22
draw.text((X_TEXT, y_name), NAME, font=font_name, fill=WHITE,
          stroke_width=1, stroke_fill=WHITE)

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
