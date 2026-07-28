#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

BASE     = Path("/Users/lunahansen/Desktop/Claude ads/template_base_6.jpg")
OUT_DIR  = Path("/Users/lunahansen/Desktop/Claude ads/output/template6")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

DARK      = (38, 76, 85)
TEAL_NAME = (51, 114, 139)

CARD_LEFT   = 164
CARD_RIGHT  = 471
MAX_W       = CARD_RIGHT - CARD_LEFT
Y_QUOTE     = 510
NAME_SIZE   = 26
CARD_BOTTOM = 875

REVIEWS = []
with open(Path(__file__).parent / "reviews.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        REVIEWS.append({"quote": _r["quote"], "name": _r["name"], "out": _r["out"]})

def wrap_text(draw, text, font, max_width):
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

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = CARD_BOTTOM - Y_QUOTE - 30 - name_h

    for size in range(62, 22, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    draw.multiline_text((CARD_LEFT, Y_QUOTE), wrapped, font=font_quote,
                        fill=DARK, spacing=spacing)

    bbox = draw.multiline_textbbox((CARD_LEFT, Y_QUOTE), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 30

    draw.text((CARD_LEFT, y_name), r["name"], font=font_name, fill=TEAL_NAME)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
