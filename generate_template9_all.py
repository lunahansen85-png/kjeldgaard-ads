#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE     = Path("/Users/lunahansen/Desktop/Claude ads/template_base_9.jpg")
OUT_DIR  = Path("/Users/lunahansen/Desktop/Claude ads/output/template9")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"

DARK = (10, 27, 42)

SIDE_PAD    = 50
CARD_LEFT   = 136
CARD_RIGHT  = 542 - SIDE_PAD   # = 492
MAX_W       = CARD_RIGHT - CARD_LEFT  # = 356
CARD_BOTTOM = 800 - SIDE_PAD   # = 750
Y_STARS_END = 217
NAME_SIZE   = 28
NAME_GAP    = 35

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

    font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    Y_QUOTE   = Y_STARS_END + 25
    available_h = CARD_BOTTOM - Y_QUOTE - NAME_GAP - name_h

    for size in range(42, 20, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    y_quote = Y_QUOTE
    y_name  = CARD_BOTTOM - name_h

    draw.multiline_text((CARD_LEFT, y_quote), wrapped, font=font_quote,
                        fill=DARK, spacing=spacing, stroke_width=1, stroke_fill=DARK)
    draw.text((CARD_LEFT, y_name), r["name"], font=font_name,
              fill=DARK, stroke_width=1, stroke_fill=DARK)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
