#!/usr/bin/env python3
"""
Adds text overlay to Kjeldgaard template 4 (portrait, teal background, white card bottom-right).
Edit QUOTE, NAME, and OUTPUT_NAME below to create new variations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE       = 'Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang'
NAME        = '- Ann Louise Haugaard'
OUTPUT_NAME = "kjeldgaard4_ann.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_4.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1408 x 1608

draw = ImageDraw.Draw(img)

TEAL_DARK  = (38, 76, 85)
TEAL_LIGHT = (91, 139, 162)

# Card boundaries (found by pixel scan)
# left=634, right=1336, top=972, bottom=1509, stars at y=1055
CARD_PAD      = 55
CARD_LEFT     = 634 + CARD_PAD
CARD_RIGHT    = 1336 - CARD_PAD
CARD_TEXT_TOP = 1105   # below stars at y=1055
BOTTOM_PAD    = 75
CARD_BOTTOM   = 1509 - BOTTOM_PAD
NAME_SIZE     = 36
MAX_W         = CARD_RIGHT - CARD_LEFT

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

# Auto-size quote to fill card with equal padding
font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h = draw.textbbox((0, 0), NAME, font=font_name)[3]
available_h = CARD_BOTTOM - CARD_TEXT_TOP - name_h - 45

for size in range(68, 24, -1):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(8, size // 4)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

# Draw quote (stroke simulates bold since font file is Light weight)
draw.multiline_text((CARD_LEFT, CARD_TEXT_TOP), wrapped, font=font_quote,
                    fill=TEAL_DARK, spacing=spacing,
                    stroke_width=2, stroke_fill=TEAL_DARK)

# Draw name
bbox = draw.multiline_textbbox((CARD_LEFT, CARD_TEXT_TOP), wrapped,
                                font=font_quote, spacing=spacing)
y_name = bbox[3] + 40
draw.text((CARD_LEFT, y_name), NAME, font=font_name, fill=TEAL_LIGHT,
          stroke_width=1, stroke_fill=TEAL_LIGHT)

# Save preserving ICC and full quality
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
