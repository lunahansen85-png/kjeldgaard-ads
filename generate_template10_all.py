#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE     = Path("/Users/lunahansen/Desktop/Claude ads/template_base_10.jpg")
OUT_DIR  = Path("/Users/lunahansen/Desktop/Claude ads/output/template10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"

DARK = (0, 0, 0)

X_TEXT         = 135
MAX_W_HEADLINE = 880
MAX_W_QUOTE    = 360
Y_HEADLINE     = 60
HEADLINE_SIZE  = 80
QUOTE_SIZE     = 36
NAME_SIZE      = 28

REVIEWS = []
with open(Path(__file__).parent / "reviews.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        REVIEWS.append({"headline": _r["headline_t10"], "quote": _r["quote"], "name": _r["name"], "out": _r["out"]})

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

    font_headline = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE)
    wrapped_h = r["headline"]  # pre-formatted with \n
    spacing_h = 18

    draw.multiline_text((X_TEXT, Y_HEADLINE), wrapped_h, font=font_headline,
                        fill=DARK, spacing=spacing_h, stroke_width=1, stroke_fill=DARK)

    bbox_h = draw.multiline_textbbox((X_TEXT, Y_HEADLINE), wrapped_h,
                                      font=font_headline, spacing=spacing_h)
    y_after_headline = bbox_h[3] + 60

    font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    NAME_GAP  = 60
    Y_BOTTOM  = 1127

    available_h = Y_BOTTOM - y_after_headline - NAME_GAP - name_h

    for size in range(QUOTE_SIZE, 20, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing_q  = max(12, size // 3)
        wrapped_q  = wrap_text(draw, r["quote"], font_quote, MAX_W_QUOTE)
        bbox_q     = draw.multiline_textbbox((0, 0), wrapped_q, font=font_quote, spacing=spacing_q)
        if (bbox_q[3] - bbox_q[1]) <= available_h:
            break

    draw.multiline_text((X_TEXT, y_after_headline), wrapped_q, font=font_quote,
                        fill=DARK, spacing=spacing_q, stroke_width=1, stroke_fill=DARK)

    bbox_q2 = draw.multiline_textbbox((X_TEXT, y_after_headline), wrapped_q,
                                       font=font_quote, spacing=spacing_q)
    y_name = bbox_q2[3] + NAME_GAP

    draw.text((X_TEXT, y_name), r["name"], font=font_name, fill=DARK)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
