#!/usr/bin/env python3
"""
Adds text overlay to Kjeldgaard template 2 (light background).
Edit QUOTE, NAME, and OUTPUT_NAME below to create new variations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE = 'Jeg droppede natcremen og dagcremen — nu bruger jeg kun ét produkt'
NAME  = "- KARINA"
OUTPUT_NAME = "kjeldgaard2_karina.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_2.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

# Preserve ICC profile to avoid color shift
img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1496 x 1486

draw = ImageDraw.Draw(img)

DARK = (20, 20, 20)

# Text area: top-left, stays clear of product bottle and bottom elements
X_TEXT   = 95
Y_TEXT   = 85
MAX_W    = 690   # safe width before bottle overlaps
Y_MAX    = 660   # bottom of safe text zone (leaves clear gap above "18.000+")
NAME_SIZE = 52

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

# Auto-size: fit quote + name within Y_MAX
font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h = draw.textbbox((0, 0), NAME, font=font_name)[3]
available_h = Y_MAX - Y_TEXT - name_h - 55  # 55px gap before name

for size in range(72, 34, -2):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(10, size // 5)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

# Draw quote (stroke_width=2 simulates bold since the .ttf is actually Light weight)
draw.multiline_text((X_TEXT, Y_TEXT), wrapped, font=font_quote,
                    fill=DARK, spacing=spacing, stroke_width=2, stroke_fill=DARK)

# Draw name with generous gap
bbox = draw.multiline_textbbox((X_TEXT, Y_TEXT), wrapped, font=font_quote, spacing=spacing)
y_name = bbox[3] + 55
draw.text((X_TEXT, y_name), NAME, font=font_name, fill=DARK,
          stroke_width=1, stroke_fill=DARK)

# Save preserving ICC and full quality
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
