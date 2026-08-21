#!/usr/bin/env python3
import csv as _csv
import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/retinol_base_10.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/retinol_10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold-700.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

DARK  = (15, 15, 15)
WHITE = (255, 255, 255)

IMG_W = 838

BOX_PAD_X     = 18
BOX_PAD_Y     = 14
HL_TOP        = 55
BOX_RADIUS    = 14
MAX_W_HL      = 760
HEADLINE_SIZE = 40
LINE_SPACING  = 20

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
    for part in re.split(r'(\*\*.*?\*\*)', text):
        if part.startswith('**') and part.endswith('**'):
            for w in part[2:-2].split(' '):
                if w: segments.append((w, True))
        else:
            for w in part.split(' '):
                if w: segments.append((w, False))
    return segments

def wrap_segments(draw, segments, font_reg, font_bold, max_width):
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

def line_width(draw, line_segs, font_reg, font_bold):
    lw = sum(draw.textlength(w, font=(font_bold if b else font_reg)) for w, b in line_segs)
    lw += sum(draw.textlength(' ', font=(font_bold if b else font_reg))
              for j, (w, b) in enumerate(line_segs) if j < len(line_segs)-1)
    return lw

def line_height(draw, line_segs, font_reg, font_bold):
    return max((draw.textbbox((0,0), w, font=(font_bold if b else font_reg), anchor="lt")[3] -
                draw.textbbox((0,0), w, font=(font_bold if b else font_reg), anchor="lt")[1]
                for w, b in line_segs), default=0)

def draw_rounded_rect(draw, x0, y0, x1, y1, radius, fill):
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + radius*2, y0 + radius*2], fill=fill)
    draw.ellipse([x1 - radius*2, y0, x1, y0 + radius*2], fill=fill)
    draw.ellipse([x0, y1 - radius*2, x0 + radius*2, y1], fill=fill)
    draw.ellipse([x1 - radius*2, y1 - radius*2, x1, y1], fill=fill)

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    font_reg  = ImageFont.truetype(FONT_REG,  size=HEADLINE_SIZE)
    font_bold = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE)
    segments  = parse_segments(r["combined"])
    lines     = wrap_segments(draw, segments, font_reg, font_bold, MAX_W_HL)

    # First pass: per-line white backgrounds
    y = HL_TOP
    for line_segs in lines:
        lw = line_width(draw, line_segs, font_reg, font_bold)
        lh = line_height(draw, line_segs, font_reg, font_bold)
        x0 = (IMG_W - lw) // 2 - BOX_PAD_X
        x1 = (IMG_W + lw) // 2 + BOX_PAD_X
        draw_rounded_rect(draw, x0, y - BOX_PAD_Y, x1, y + lh + BOX_PAD_Y + 14, BOX_RADIUS, WHITE)
        y += lh + LINE_SPACING

    # Second pass: draw text
    y = HL_TOP
    for line_segs in lines:
        lh = line_height(draw, line_segs, font_reg, font_bold)
        lw = line_width(draw, line_segs, font_reg, font_bold)
        x = (IMG_W - lw) // 2
        for j, (word, bold) in enumerate(line_segs):
            font = font_bold if bold else font_reg
            draw.text((x, y), word, font=font, fill=DARK)
            word_w = draw.textlength(word, font=font)
            if j < len(line_segs) - 1:
                x += word_w + draw.textlength(' ', font=font)
        y += lh + LINE_SPACING

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
