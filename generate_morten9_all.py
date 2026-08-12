#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/morten_base_9.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/morten_9")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"

BLACK = (0, 0, 0)

X_MARGIN     = 45
RIGHT_MARGIN = 45
LINE_GAP     = 18
STROKE       = 0
YELLOW_TOP    = 1032  # where the screenshot ends and the yellow area begins
YELLOW_BOTTOM = 1370  # bottom of the usable yellow area

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
    max_w = width - X_MARGIN - RIGHT_MARGIN

    for size in range(64, 18, -2):
        font = ImageFont.truetype(FONT_BOLD, size=size)
        lines = wrap_text(draw, r["text"], font, max_w)
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
            line_heights.append(bbox[3] - bbox[1])
        total_h = sum(line_heights) + LINE_GAP * (len(lines) - 1)
        if total_h <= (YELLOW_BOTTOM - YELLOW_TOP):
            break

    x_left = X_MARGIN
    leftover = YELLOW_BOTTOM - YELLOW_TOP - total_h
    y = YELLOW_TOP + int(leftover * 0.5)
    for line, line_h in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
        draw.text((x_left, y - bbox[1]), line, font=font,
                   fill=BLACK, anchor="la", align="left",
                   stroke_width=STROKE, stroke_fill=BLACK)
        y += line_h + LINE_GAP

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
