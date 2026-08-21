#!/usr/bin/env python3
import csv as _csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_4.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_4")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK  = (30, 30, 30)

IMG_W = 978

# Headline text highlight (per-line background)
BOX_PAD_X  = 18
BOX_PAD_Y  = 14
HL_TOP     = 130
BOX_RADIUS = 14
MAX_W_HL   = 680
HEADLINE_SIZE = 36

# Grey area text (below photo at y~951)
GREY_TOP    = 990
GREY_BOTTOM = 1220
TEXT_LEFT   = 50
TEXT_RIGHT  = 928
MAX_W_BODY  = TEXT_RIGHT - TEXT_LEFT
BODY_SIZE   = 30

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

def draw_rounded_rect(draw, x0, y0, x1, y1, radius, fill):
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + radius * 2, y0 + radius * 2], fill=fill)
    draw.ellipse([x1 - radius * 2, y0, x1, y0 + radius * 2], fill=fill)
    draw.ellipse([x0, y1 - radius * 2, x0 + radius * 2, y1], fill=fill)
    draw.ellipse([x1 - radius * 2, y1 - radius * 2, x1, y1], fill=fill)

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Combine headline + subheadline into one headline
    hl_parts = [p for p in [r["headline"], r["subheadline"]] if p.strip()]
    combined_hl = " ".join(hl_parts)

    font_hl = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE)
    wrapped_hl = wrap_text(draw, combined_hl, font_hl, MAX_W_HL)

    # Draw per-line highlight backgrounds then text on top
    lines = wrapped_hl.split('\n')
    LINE_SPACING = 10

    # Pre-calculate each line's metrics using anchor="lt" for accuracy
    line_metrics = []
    for line in lines:
        lbbox = draw.textbbox((0, 0), line, font=font_hl, anchor="lt")
        lw = lbbox[2] - lbbox[0]
        lh = lbbox[3] - lbbox[1]
        line_metrics.append((lw, lh))

    y = HL_TOP
    # First pass: draw all backgrounds
    for (lw, lh) in line_metrics:
        x0 = (IMG_W - lw) // 2 - BOX_PAD_X
        x1 = (IMG_W + lw) // 2 + BOX_PAD_X
        y0 = y - BOX_PAD_Y
        y1 = y + lh + BOX_PAD_Y
        draw_rounded_rect(draw, x0, y0, x1, y1, BOX_RADIUS, BLACK)
        y += lh + LINE_SPACING

    # Second pass: draw all text on top (centered horizontally, top-anchored)
    y = HL_TOP
    for i, line in enumerate(lines):
        lh = line_metrics[i][1]
        draw.text((IMG_W // 2, y), line, font=font_hl, fill=WHITE, anchor="mt")
        y += lh + LINE_SPACING

    # Body text in grey area
    if r["text"]:
        available_h = GREY_BOTTOM - GREY_TOP
        for size in range(BODY_SIZE, 14, -1):
            font_tx = ImageFont.truetype(FONT_BOLD, size=size)
            wrapped_tx = wrap_text(draw, r["text"], font_tx, MAX_W_BODY)
            bbox = draw.multiline_textbbox((TEXT_LEFT, GREY_TOP), wrapped_tx, font=font_tx, spacing=10)
            if (bbox[3] - bbox[1]) <= available_h:
                break
        draw.multiline_text((TEXT_LEFT, GREY_TOP), wrapped_tx, font=font_tx,
                            fill=DARK, spacing=10)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
