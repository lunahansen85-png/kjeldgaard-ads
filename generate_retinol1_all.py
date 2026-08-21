#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_1.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

BLACK = (0, 0, 0)
DARK  = (40, 40, 40)

# Card boundaries
CARD_EDGE_LEFT   = 170
CARD_EDGE_RIGHT  = 745
CARD_EDGE_TOP    = 215
CARD_EDGE_BOTTOM = 870

# Equal padding on all sides (same as space above the logo)
PAD = 50

CARD_LEFT   = CARD_EDGE_LEFT  + PAD
CARD_RIGHT  = CARD_EDGE_RIGHT - PAD
CARD_TOP    = 308   # below the logo
CARD_BOTTOM = CARD_EDGE_BOTTOM - PAD
MAX_W       = CARD_RIGHT - CARD_LEFT

HEADLINE_SIZE    = 38
SUBHEADLINE_SIZE = 22

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

    y = CARD_TOP

    # Headline (bold, larger)
    if r["headline"]:
        font_hl = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE)
        wrapped_hl = wrap_text(draw, r["headline"], font_hl, MAX_W)
        draw.multiline_text((CARD_LEFT, y), wrapped_hl, font=font_hl,
                            fill=BLACK, spacing=8)
        bbox = draw.multiline_textbbox((CARD_LEFT, y), wrapped_hl, font=font_hl, spacing=8)
        y = bbox[3] + 12

    # Subheadline (bold, smaller)
    if r["subheadline"]:
        font_sh = ImageFont.truetype(FONT_BOLD, size=SUBHEADLINE_SIZE)
        wrapped_sh = wrap_text(draw, r["subheadline"], font_sh, MAX_W)
        draw.multiline_text((CARD_LEFT, y), wrapped_sh, font=font_sh,
                            fill=BLACK, spacing=4)
        bbox = draw.multiline_textbbox((CARD_LEFT, y), wrapped_sh, font=font_sh, spacing=4)
        y = bbox[3] + 24

    # Body text — auto-size to always fit within card
    if r["text"]:
        available_h = CARD_BOTTOM - y - 10
        for size in range(24, 10, -1):
            font_tx = ImageFont.truetype(FONT_REG, size=size)
            wrapped_tx = wrap_text(draw, r["text"], font_tx, MAX_W)
            bbox = draw.multiline_textbbox((CARD_LEFT, y), wrapped_tx, font=font_tx, spacing=6)
            if (bbox[3] - bbox[1]) <= available_h:
                break
        draw.multiline_text((CARD_LEFT, y), wrapped_tx, font=font_tx,
                            fill=DARK, spacing=6)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
