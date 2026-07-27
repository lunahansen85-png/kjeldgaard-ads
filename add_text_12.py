#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

QUOTE       = 'Den bedste jeg har prøvet, man kan både se og mærke forskellen. Huden bliver mere blød og glat og rynkerne minimeres.'
NAME        = '– Britt Bente Andreasen'
OUTPUT_NAME = "test_template12.jpg"

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_12.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1078 x 1522
draw = ImageDraw.Draw(img)

DARK = (10, 27, 42)

TEXT_LEFT   = 480
TEXT_RIGHT  = 980
TEXT_CENTER = 730
MAX_W       = TEXT_RIGHT - TEXT_LEFT
Y_QUOTE     = 440
NAME_SIZE   = 28
Y_BOTTOM    = 980

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

font_name   = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
name_h      = draw.textbbox((0, 0), NAME, font=font_name)[3]
available_h = Y_BOTTOM - Y_QUOTE - 40 - name_h

for size in range(40, 18, -1):
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

draw.text((TEXT_CENTER, y_name), NAME, font=font_name, fill=DARK, anchor="ma")

out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
