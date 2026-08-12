#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/morten_base_7.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/morten_7")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

X_MARGIN   = 50
LINE_GAP   = 12
STROKE     = 7
Y_BOTTOM   = 1650   # bottom edge of the text block
Y_TOP_MAX  = 1230    # text block won't be allowed to start higher than this

REVIEWS = []
with open(Path(__file__).parent / "reviews_morten.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        REVIEWS.append({"text": _r["text"], "out": _r["out"]})

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
    return lines

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    width, height = img.size
    x_center = width // 2
    max_w = width - 2 * X_MARGIN

    for size in range(72, 20, -2):
        font = ImageFont.truetype(FONT_BOLD, size=size)
        lines = wrap_text(draw, r["text"], font, max_w - 2 * STROKE)
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
            line_heights.append(bbox[3] - bbox[1])
        total_h = sum(line_heights) + LINE_GAP * (len(lines) - 1)
        if total_h <= (Y_BOTTOM - Y_TOP_MAX):
            break

    y = Y_BOTTOM - total_h
    for line, line_h in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
        draw.text((x_center, y - bbox[1]), line, font=font,
                   fill=WHITE, anchor="ma", align="center",
                   stroke_width=STROKE, stroke_fill=BLACK)
        y += line_h + LINE_GAP

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
