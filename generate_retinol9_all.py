#!/usr/bin/env python3
import csv as _csv
import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_9.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_9")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

DARK  = (20, 20, 20)
WHITE = (255, 255, 255)

IMG_W = 1142
IMG_H = 1144

# White box already on image — measured boundaries
BOX_LEFT   = 92
BOX_RIGHT  = 1087
BOX_TOP    = 649
BOX_BOTTOM = 949

# Text padding inside box
PAD_X = 55
PAD_Y = 45
TEXT_LEFT   = BOX_LEFT + PAD_X
TEXT_RIGHT  = BOX_RIGHT - PAD_X
MAX_W       = TEXT_RIGHT - TEXT_LEFT
TEXT_Y      = BOX_TOP + PAD_Y
TEXT_BOTTOM = BOX_BOTTOM - PAD_Y

TEXT_SIZE    = 46
LINE_SPACING = 14

REVIEWS = []
with open(Path(__file__).parent / "reviews_retinol.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        parts = [p for p in [_r["headline"], _r["subheadline"]] if p.strip()]
        REVIEWS.append({
            "combined": " ".join(parts),
            "out":      _r["out"],
        })

def parse_segments(text):
    segments = []
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            for w in part[2:-2].split(' '):
                if w: segments.append((w, True))
        else:
            for w in part.split(' '):
                if w: segments.append((w, False))
    return segments

def layout_lines(draw, segments, font_reg, font_bold, max_width):
    lines, current_line, current_w = [], [], 0
    for word, bold in segments:
        font = font_bold if bold else font_reg
        word_w = draw.textlength(word, font=font)
        space_w = draw.textlength(' ', font=font)
        needed = (space_w + word_w) if current_line else word_w
        if current_w + needed > max_width and current_line:
            lines.append(current_line)
            current_line, current_w = [(word, bold)], word_w
        else:
            current_line.append((word, bold))
            current_w += needed
    if current_line:
        lines.append(current_line)
    return lines

def line_height(draw, line_segs, font_reg, font_bold):
    return max((draw.textbbox((0,0), w, font=(font_bold if b else font_reg), anchor="lt")[3]
                for w, b in line_segs), default=0)

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    text = r["combined"]
    segments = parse_segments(text)

    # Auto-size to fit inside box
    available_h = TEXT_BOTTOM - TEXT_Y
    for size in range(TEXT_SIZE, 20, -1):
        font_reg  = ImageFont.truetype(FONT_REG,  size=size)
        font_bold = ImageFont.truetype(FONT_BOLD, size=size)
        lines = layout_lines(draw, segments, font_reg, font_bold, MAX_W)
        ref_lh = draw.textbbox((0, 0), "Ag", font=font_bold, anchor="lt")[3]
        total_h = ref_lh * len(lines) + LINE_SPACING * (len(lines) - 1)
        if total_h <= available_h:
            break

    # Use a fixed line height for consistent spacing
    fixed_lh = draw.textbbox((0, 0), "Ag", font=font_bold, anchor="lt")[3]
    total_h = fixed_lh * len(lines) + LINE_SPACING * (len(lines) - 1)

    # Vertically center in the white box, compensating for font's internal top leading
    FONT_LEADING = 15
    box_mid = (BOX_TOP + BOX_BOTTOM) // 2
    y = box_mid - total_h // 2 - FONT_LEADING
    for line_segs in lines:
        x = TEXT_LEFT
        for j, (word, bold) in enumerate(line_segs):
            font = font_bold if bold else font_reg
            draw.text((x, y), word, font=font, fill=DARK)
            word_w = draw.textlength(word, font=font)
            if j < len(line_segs) - 1:
                x += word_w + draw.textlength(' ', font=font)
        y += fixed_lh + LINE_SPACING

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
