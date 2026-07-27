#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE       = 'Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang'
NAME        = '- Ann Louise Haugaard'
OUTPUT_NAME = "kjeldgaard10_ann.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_10.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1114 x 1424

draw = ImageDraw.Draw(img)

DARK      = (10, 27, 42)
TEAL_NAME = (38, 76, 85)

# Stars at x=151-323, y≈194-213 — text left-aligned below stars
SIDE_PAD    = 50                        # = star left(136) - card left(86)
CARD_LEFT   = 136                       # aligned with star left edge
CARD_RIGHT  = 542 - SIDE_PAD           # = 492, equal right padding
MAX_W       = CARD_RIGHT - CARD_LEFT   # = 356
CARD_BOTTOM = 800 - SIDE_PAD           # = 750, equal bottom padding
Y_STARS_END = 217
NAME_SIZE   = 28

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

# Find font size that fits between stars and card bottom
font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h    = draw.textbbox((0, 0), NAME, font=font_name)[3]
Y_QUOTE   = Y_STARS_END + 25   # small gap after stars
NAME_GAP  = 35
available_h = CARD_BOTTOM - Y_QUOTE - NAME_GAP - name_h

for size in range(42, 20, -1):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(10, size // 3)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

# Text right after stars, name anchored to bottom
y_quote = Y_QUOTE
y_name  = CARD_BOTTOM - name_h   # anchored to bottom

draw.multiline_text((CARD_LEFT, y_quote), wrapped, font=font_quote,
                    fill=DARK, spacing=spacing, stroke_width=1, stroke_fill=DARK)
draw.text((CARD_LEFT, y_name), NAME, font=font_name, fill=DARK,
          stroke_width=1, stroke_fill=DARK)

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
