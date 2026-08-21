#!/usr/bin/env python3
import csv as _csv
import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_8.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_8")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

WHITE = (255, 255, 255)

IMG_W    = 920
IMG_H    = 920
TEXT_LEFT    = 50
TEXT_RIGHT   = 870
MAX_W        = TEXT_RIGHT - TEXT_LEFT
TEXT_Y_START = 618
TEXT_BOTTOM  = 880
TEXT_SIZE    = 44
LINE_SPACING = 12

REVIEWS = []
with open(Path(__file__).parent / "reviews_retinol.csv", newline='', encoding='utf-8') as _f:
    for _r in _csv.DictReader(_f):
        parts = [p for p in [_r["headline"], _r["subheadline"]] if p.strip()]
        REVIEWS.append({
            "text_t8": " ".join(parts),
            "out":     _r["out"],
        })

def parse_segments(text):
    """Split text into list of (word, is_bold) tuples."""
    segments = []
    # Split on **...** markers
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            words = part[2:-2].split(' ')
            for w in words:
                if w:
                    segments.append((w, True))
        else:
            words = part.split(' ')
            for w in words:
                if w:
                    segments.append((w, False))
    return segments

def layout_lines(draw, segments, font_reg, font_bold, max_width):
    """Wrap segments into lines, returning list of line-segment lists."""
    lines = []
    current_line = []
    current_w = 0

    for i, (word, bold) in enumerate(segments):
        font = font_bold if bold else font_reg
        word_w = draw.textlength(word, font=font)
        space_w = draw.textlength(' ', font=font)

        if current_line:
            needed = space_w + word_w
        else:
            needed = word_w

        if current_w + needed > max_width and current_line:
            lines.append(current_line)
            current_line = [(word, bold)]
            current_w = word_w
        else:
            current_line.append((word, bold))
            current_w += needed

    if current_line:
        lines.append(current_line)
    return lines

def line_height(draw, line_segs, font_reg, font_bold):
    max_h = 0
    for word, bold in line_segs:
        font = font_bold if bold else font_reg
        bbox = draw.textbbox((0, 0), word, font=font, anchor="lt")
        max_h = max(max_h, bbox[3] - bbox[1])
    return max_h

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    text = r["text_t8"]
    if not text.strip():
        img.save(OUT_DIR / r["out"], quality=100, subsampling=0)
        continue

    segments = parse_segments(text)

    # Auto-size to fit
    for size in range(TEXT_SIZE, 20, -1):
        font_reg  = ImageFont.truetype(FONT_REG,  size=size)
        font_bold = ImageFont.truetype(FONT_BOLD, size=size)
        lines = layout_lines(draw, segments, font_reg, font_bold, MAX_W)
        total_h = sum(line_height(draw, l, font_reg, font_bold) for l in lines)
        total_h += LINE_SPACING * (len(lines) - 1)
        if total_h <= (TEXT_BOTTOM - TEXT_Y_START):
            break

    # Position: fixed start point matching original layout
    text_y = TEXT_Y_START

    # Render line by line, word by word
    for line_segs in lines:
        lh = line_height(draw, line_segs, font_reg, font_bold)
        x = TEXT_LEFT
        for j, (word, bold) in enumerate(line_segs):
            font = font_bold if bold else font_reg
            draw.text((x, text_y), word, font=font, fill=WHITE)
            word_w = draw.textlength(word, font=font)
            if j < len(line_segs) - 1:
                space_w = draw.textlength(' ', font=font)
                x += word_w + space_w
        text_y += lh + LINE_SPACING

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
