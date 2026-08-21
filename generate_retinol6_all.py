#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_6.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_6")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"

DARK = (20, 20, 20)

IMG_W = 1098

# Yellow text area
GREY_TOP    = 1058
GREY_BOTTOM = 1360
TEXT_LEFT   = 55
TEXT_RIGHT  = 1043
MAX_W       = TEXT_RIGHT - TEXT_LEFT
TEXT_SIZE   = 54

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

    # Combine headline + subheadline
    parts = [p for p in [r["headline"], r["subheadline"]] if p.strip()]
    combined = " ".join(parts)

    grey_h = GREY_BOTTOM - GREY_TOP
    for size in range(TEXT_SIZE, 20, -1):
        font_tx = ImageFont.truetype(FONT_BOLD, size=size)
        wrapped = wrap_text(draw, combined, font_tx, MAX_W)
        bbox = draw.multiline_textbbox((TEXT_LEFT, 0), wrapped, font=font_tx, spacing=14)
        text_h = bbox[3] - bbox[1]
        if text_h <= grey_h:
            break

    # Vertically center text in yellow area with slight upward nudge
    text_y = GREY_TOP + (grey_h - text_h) // 2 - 18
    draw.multiline_text((TEXT_LEFT, text_y), wrapped, font=font_tx,
                        fill=DARK, spacing=14)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
