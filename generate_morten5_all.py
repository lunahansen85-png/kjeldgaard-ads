#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/morten_base_5.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/morten_5")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"

BLUE  = (42, 71, 246)
WHITE = (255, 255, 255)

X_MARGIN     = 30
RIGHT_MARGIN = 30
PAD_X      = 22
PAD_TOP    = 12
PAD_BOTTOM = 7
LINE_GAP   = 0
STROKE     = 0
Y_BOTTOM   = 1100   # bottom edge of the text block (near photo bottom edge)
Y_TOP_MAX  = 800     # text block won't be allowed to start higher than this

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

    for size in range(40, 14, -2):
        font = ImageFont.truetype(FONT_BOLD, size=size)
        lines = wrap_text(draw, r["text"], font, max_w - 2 * PAD_X - 2 * STROKE)
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
            line_heights.append(bbox[3] - bbox[1])
        total_h = sum(h + PAD_TOP + PAD_BOTTOM for h in line_heights) + LINE_GAP * (len(lines) - 1)
        if total_h <= (Y_BOTTOM - Y_TOP_MAX):
            break

    line_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
        line_widths.append(bbox[2] - bbox[0])
    block_w = max(line_widths)
    x_left = (width - block_w) // 2

    y = Y_BOTTOM - total_h
    for line, line_h in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
        line_w = bbox[2] - bbox[0]
        box_left  = x_left - PAD_X
        box_right = x_left + line_w + PAD_X
        box_top   = y
        box_bot   = y + line_h + PAD_TOP + PAD_BOTTOM
        draw.rectangle([box_left, box_top, box_right, box_bot], fill=BLUE)
        draw.text((x_left, box_top + PAD_TOP - bbox[1]), line, font=font,
                   fill=WHITE, anchor="la", align="left",
                   stroke_width=STROKE, stroke_fill=WHITE)
        y = box_bot + LINE_GAP

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
