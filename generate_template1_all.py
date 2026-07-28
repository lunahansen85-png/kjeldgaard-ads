#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_1.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/template1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

DARK      = (20, 20, 20)
X_TEXT    = 95
Y_TEXT    = 85
MAX_W     = 690
Y_MAX     = 660
NAME_SIZE = 52

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
    img = img.resize((1636, 1630), Image.LANCZOS)
    draw = ImageDraw.Draw(img)

    font_name   = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
    name_h      = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = Y_MAX - Y_TEXT - name_h - 55

    for size in range(72, 28, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 5)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    sw = 2 if size >= 50 else (1 if size >= 36 else 0)
    draw.multiline_text((X_TEXT, Y_TEXT), wrapped, font=font_quote,
                        fill=DARK, spacing=spacing,
                        stroke_width=sw, stroke_fill=DARK)

    bbox = draw.multiline_textbbox((X_TEXT, Y_TEXT), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 55
    draw.text((X_TEXT, y_name), r["name"], font=font_name, fill=DARK,
              stroke_width=1, stroke_fill=DARK)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
