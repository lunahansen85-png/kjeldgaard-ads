#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_3n.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_3")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD   = "/System/Library/Fonts/Times.ttc"

WHITE = (255, 255, 255)

IMG_W       = 1294
CENTER_X    = IMG_W // 2
MAX_W       = 1150  # equal margins left and right

Y_HEADLINE    = 210  # start below KJELDGAARD logo
HEADLINE_SIZE = 80
SUB_SIZE      = 62

REVIEWS = []
with open(Path(__file__).parent / "reviews_retinol.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        REVIEWS.append({
            "headline":    _r["headline"],
            "subheadline": _r["subheadline"],
            "out":         _r["out"],
        })

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

    # Headline — bold, centered
    HL_SPACING = 20
    if r["headline"]:
        font_hl = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE, index=1)
        wrapped_hl = wrap_text(draw, r["headline"], font_hl, MAX_W)
        num_hl_lines = len(wrapped_hl.split('\n'))
        y = Y_HEADLINE - (20 if num_hl_lines > 2 else 0)
        draw.multiline_text((CENTER_X, y), wrapped_hl, font=font_hl,
                            fill=WHITE, spacing=HL_SPACING, anchor="ma", align="center")
        bbox = draw.multiline_textbbox((CENTER_X, y), wrapped_hl, font=font_hl,
                                       spacing=HL_SPACING, anchor="ma")
        y = bbox[3] + 60
    else:
        y = Y_HEADLINE

    # Subheadline — bold, centered, white
    if r["subheadline"]:
        font_sh = ImageFont.truetype(FONT_BOLD, size=SUB_SIZE, index=1)
        wrapped_sh = wrap_text(draw, r["subheadline"], font_sh, MAX_W)
        draw.multiline_text((CENTER_X, y), wrapped_sh, font=font_sh,
                            fill=WHITE, spacing=18, anchor="ma", align="center")

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
