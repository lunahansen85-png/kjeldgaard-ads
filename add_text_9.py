#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
QUOTE       = 'Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang'
NAME        = '- Ann Louise Haugaard'
OUTPUT_NAME = "kjeldgaard9_ann.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_9.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 976 x 1444

draw = ImageDraw.Draw(img)

WHITE = (255, 255, 255)

# Text zone — centered on stars (x≈480), stars end at y≈290
TEXT_CENTER = 662   # center of 5 stars (x=562-763)
TEXT_LEFT   = 490
TEXT_RIGHT  = 835
MAX_W       = TEXT_RIGHT - TEXT_LEFT
Y_QUOTE     = 320   # below stars
NAME_SIZE   = 26
Y_BOTTOM    = 600

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
font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h    = draw.textbbox((0, 0), NAME, font=font_name)[3]
available_h = Y_BOTTOM - Y_QUOTE - 50 - name_h

for size in range(30, 16, -1):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing = max(10, size // 3)
    wrapped = wrap_text(QUOTE, font_quote, MAX_W)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
    if (bbox[3] - bbox[1]) <= available_h:
        break

draw.multiline_text((TEXT_CENTER, Y_QUOTE), wrapped, font=font_quote,
                    fill=WHITE, spacing=spacing, anchor="ma", align="center",
                    stroke_width=1, stroke_fill=WHITE)

bbox = draw.multiline_textbbox((TEXT_CENTER, Y_QUOTE), wrapped,
                                font=font_quote, spacing=spacing, anchor="ma")
y_name = bbox[3] + 50

draw.text((TEXT_CENTER, y_name), NAME, font=font_name, fill=WHITE,
          anchor="ma", stroke_width=1, stroke_fill=WHITE)

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
