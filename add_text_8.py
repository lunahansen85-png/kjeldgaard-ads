#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE       = 'Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang'
NAME        = '- Ann Louise Haugaard'
OUTPUT_NAME = "kjeldgaard8_ann.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_8.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 988 x 1398

draw = ImageDraw.Draw(img)

DARK      = (10, 27, 42)
TEAL_NAME = (10, 27, 42)

# Text zone — right half, centered around x=673 (star center)
TEXT_LEFT   = 510
TEXT_RIGHT  = 930
TEXT_CENTER = 673   # aligned with star center
MAX_W       = TEXT_RIGHT - TEXT_LEFT
Y_QUOTE     = 370   # with gap below stars (end at y=327)
NAME_SIZE   = 26
Y_BOTTOM    = 720

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

# Quote — auto-size, centered
font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
name_h    = draw.textbbox((0, 0), NAME, font=font_name)[3]
available_h = Y_BOTTOM - Y_QUOTE - 40 - name_h

for size in range(36, 18, -1):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(10, size // 3)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

draw.multiline_text((TEXT_CENTER, Y_QUOTE), wrapped, font=font_quote,
                    fill=DARK, spacing=spacing, anchor="ma", align="center",
                    stroke_width=1, stroke_fill=DARK)

bbox = draw.multiline_textbbox((TEXT_CENTER, Y_QUOTE), wrapped,
                                font=font_quote, spacing=spacing, anchor="ma")
y_name = bbox[3] + 40

draw.text((TEXT_CENTER, y_name), NAME, font=font_name, fill=TEAL_NAME, anchor="ma")

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
