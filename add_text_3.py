#!/usr/bin/env python3
"""
Adds text overlay to Kjeldgaard template 3 (headline + white card).
Edit HEADLINE, QUOTE, NAME, and OUTPUT_NAME to create new variations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
HEADLINE    = 'Drømmer du om\nfærre rynker?'
QUOTE       = 'Den bedste jeg har prøvet, man kan både se og mærke forskellen. Huden bliver mere blød og glat og rynkerne minimeres.'
NAME        = '- Britt Bente Andreasen'
OUTPUT_NAME = "kjeldgaard3_britt.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_3.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img  = Image.open(BASE)
icc  = img.info.get("icc_profile")
img  = img.convert("RGB")
W, H = img.size  # 1496 x 1752

draw = ImageDraw.Draw(img)

WHITE      = (255, 255, 255)
TEAL_DARK  = (38, 76, 85)    # quote text color (from template stars)
TEAL_LIGHT = (117, 155, 179) # name color (from template quote marks)

# ── Headline (white, top-left) — aligns with card left edge x=199 ────────────
font_headline = ImageFont.truetype(FONT_BOLD, size=95)
draw.multiline_text((199, 290), HEADLINE, font=font_headline,
                    fill=WHITE, spacing=6,
                    stroke_width=2, stroke_fill=WHITE)

# ── Quote inside white card ───────────────────────────────────────────────────
# Card: left=199, right=700, stars end ~y=940, bottom=1454
CARD_PAD        = 68   # aligns text with stars
CARD_LEFT       = 199 + CARD_PAD
CARD_RIGHT      = 700 - CARD_PAD
CARD_TEXT_TOP   = 970
BOTTOM_PAD      = 80   # space under name
CARD_BOTTOM     = 1454 - BOTTOM_PAD
NAME_SIZE  = 33
MAX_W = CARD_RIGHT - CARD_LEFT

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

# Auto-size font to fit within available card height
font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
name_h = draw.textbbox((0,0), NAME, font=font_name)[3]
available_h = CARD_BOTTOM - CARD_TEXT_TOP - name_h - 40  # space for name + gap

for size in range(48, 22, -1):
    font_quote = ImageFont.truetype(FONT_REG, size=size)
    spacing = max(8, size // 4)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    text_h = bbox[3] - bbox[1]
    if text_h <= available_h:
        break

draw.multiline_text((CARD_LEFT, CARD_TEXT_TOP), wrapped, font=font_quote,
                    fill=TEAL_DARK, spacing=spacing)

bbox = draw.multiline_textbbox((CARD_LEFT, CARD_TEXT_TOP), wrapped,
                                font=font_quote, spacing=spacing)
y_name = bbox[3] + 30
draw.text((CARD_LEFT, y_name), NAME, font=font_name, fill=TEAL_LIGHT)

# ── Save ─────────────────────────────────────────────────────────────────────
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
