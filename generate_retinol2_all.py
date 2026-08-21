#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_2.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

BLACK = (0, 0, 0)
DARK  = (40, 40, 40)

# White text area (left column)
WHITE_LEFT  = 54    # measured left edge of white area
WHITE_RIGHT = 569   # measured right edge of white area
PAD         = 45    # equal padding on all sides
TEXT_LEFT   = WHITE_LEFT  + PAD
TEXT_RIGHT  = WHITE_RIGHT - PAD
TEXT_TOP    = PAD
TEXT_BOTTOM = 1130 - PAD
MAX_W       = TEXT_RIGHT - TEXT_LEFT

HEADLINE_SIZE = 36
HEADLINE_MIN  = 24

REVIEWS = []
with open(Path(__file__).parent / "reviews_retinol.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        REVIEWS.append({
            "headline":    _r["headline"],
            "subheadline": _r["subheadline"],
            "text":        _r["text"],
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

    y = TEXT_TOP

    # Headline + subheadline combined as one block — auto-size to fit width & height
    hl_parts = [p for p in [r["headline"], r["subheadline"]] if p.strip()]
    combined_hl = " ".join(hl_parts)
    if combined_hl:
        available_hl_h = (TEXT_BOTTOM - TEXT_TOP) // 2  # at most half the column for headline
        for hl_size in range(HEADLINE_SIZE, HEADLINE_MIN - 1, -1):
            font_hl = ImageFont.truetype(FONT_BOLD, size=hl_size)
            wrapped_hl = wrap_text(draw, combined_hl, font_hl, MAX_W)
            bbox = draw.multiline_textbbox((TEXT_LEFT, y), wrapped_hl, font=font_hl, spacing=10)
            if (bbox[3] - bbox[1]) <= available_hl_h:
                break
        draw.multiline_text((TEXT_LEFT, y), wrapped_hl, font=font_hl,
                            fill=BLACK, spacing=10)
        bbox = draw.multiline_textbbox((TEXT_LEFT, y), wrapped_hl, font=font_hl, spacing=10)
        y = bbox[3] + 40


    # Body text — auto-size to always fit within text area
    if r["text"]:
        available_h = TEXT_BOTTOM - y
        for size in range(32, 10, -1):
            font_tx = ImageFont.truetype(FONT_REG, size=size)
            wrapped_tx = wrap_text(draw, r["text"], font_tx, MAX_W)
            bbox = draw.multiline_textbbox((TEXT_LEFT, y), wrapped_tx, font=font_tx, spacing=8)
            if (bbox[3] - bbox[1]) <= available_h:
                break
        draw.multiline_text((TEXT_LEFT, y), wrapped_tx, font=font_tx,
                            fill=DARK, spacing=8)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
