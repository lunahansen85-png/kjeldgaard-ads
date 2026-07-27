#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE       = '"Den bedste jeg har prøvet, man kan både se og mærke forskellen. Huden bliver mere blød og glat og rynkerne minimeres."'
NAME        = '– Britt Bente Andreasen'
OUTPUT_NAME = "kjeldgaard7_britt.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_7.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1094 x 1672

draw = ImageDraw.Draw(img)

DARK       = (38, 76, 85)
TEAL_NAME  = (51, 114, 139)
STAR_COLOR = (38, 76, 85)

# Card text zone (stars already on template at y=457-484, x=164)
CARD_LEFT   = 164   # 53px from card left edge (111)
CARD_RIGHT  = 471   # 53px from card right edge (524) — equal padding
MAX_W       = CARD_RIGHT - CARD_LEFT
Y_QUOTE     = 510   # just below existing stars
NAME_SIZE   = 26
CARD_BOTTOM = 875   # 56px above card bottom (931) — equal to top padding

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

y_quote = Y_QUOTE

# Quote — auto-size
font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
name_h    = draw.textbbox((0, 0), NAME, font=font_name)[3]
available_h = CARD_BOTTOM - y_quote - 40 - name_h

for size in range(62, 22, -1):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(10, size // 3)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

draw.multiline_text((CARD_LEFT, y_quote), wrapped, font=font_quote,
                    fill=DARK, spacing=spacing)

bbox = draw.multiline_textbbox((CARD_LEFT, y_quote), wrapped, font=font_quote, spacing=spacing)
y_name = bbox[3] + 30

# Name
draw.text((CARD_LEFT, y_name), NAME, font=font_name, fill=TEAL_NAME)

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
