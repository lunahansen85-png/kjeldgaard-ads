#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE     = Path("/Users/lunahansen/Desktop/Claude ads/template_base_8.jpg")
OUT_DIR  = Path("/Users/lunahansen/Desktop/Claude ads/output/template8")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

WHITE = (255, 255, 255)

TEXT_CENTER = 662
TEXT_LEFT   = 490
TEXT_RIGHT  = 835
MAX_W       = TEXT_RIGHT - TEXT_LEFT
Y_QUOTE     = 320
NAME_SIZE   = 26
Y_BOTTOM    = 600

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
    available_h = Y_BOTTOM - Y_QUOTE - 50 - name_h

    for size in range(30, 16, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    draw.multiline_text((TEXT_CENTER, Y_QUOTE), wrapped, font=font_quote,
                        fill=WHITE, spacing=spacing, anchor="ma", align="center",
                        stroke_width=1, stroke_fill=WHITE)

    bbox = draw.multiline_textbbox((TEXT_CENTER, Y_QUOTE), wrapped,
                                    font=font_quote, spacing=spacing, anchor="ma")
    y_name = bbox[3] + 50

    draw.text((TEXT_CENTER, y_name), r["name"], font=font_name,
              fill=WHITE, anchor="ma", stroke_width=1, stroke_fill=WHITE)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
