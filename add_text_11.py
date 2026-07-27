#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── EDIT THESE FOR EACH NEW VERSION ──────────────────────────────────────────
HEADLINE    = '27% FÆRRE RYNKER\nPÅ 28 DAGE'  # forced 2-line break
QUOTE       = 'Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang'
NAME        = '- Ann Louise Haugaard'
OUTPUT_NAME = "kjeldgaard11_ann.jpg"
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_11.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

img = Image.open(BASE)
icc = img.info.get("icc_profile")
img = img.convert("RGB")
W, H = img.size  # 1110 x 1462

draw = ImageDraw.Draw(img)

DARK = (0, 0, 0)

X_TEXT           = 135   # aligned with KJELDGAARD text left edge
MAX_W_HEADLINE   = 880   # wide — headline fits in 2 lines
MAX_W_QUOTE      = 360   # left zone only, before bottle
Y_HEADLINE       = 60
HEADLINE_SIZE    = 80
QUOTE_SIZE       = 36    # auto-shrinks
NAME_SIZE        = 28

# ── Headline ──────────────────────────────────────────────────────────────────
def wrap_text(text, font, max_width):
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

font_headline = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE)
wrapped_headline = HEADLINE  # already has forced line break
spacing_h = 18

draw.multiline_text((X_TEXT, Y_HEADLINE), wrapped_headline, font=font_headline,
                    fill=DARK, spacing=spacing_h, stroke_width=1, stroke_fill=DARK)

# Find where headline ends
bbox_h = draw.multiline_textbbox((X_TEXT, Y_HEADLINE), wrapped_headline,
                                  font=font_headline, spacing=spacing_h)
y_after_headline = bbox_h[3] + 60  # gap below headline

# ── Quote ─────────────────────────────────────────────────────────────────────
font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
name_h    = draw.textbbox((0, 0), NAME, font=font_name)[3]
NAME_GAP  = 60
Y_BOTTOM  = 1167 - 40  # above logo top

available_h = Y_BOTTOM - y_after_headline - NAME_GAP - name_h

for size in range(QUOTE_SIZE, 28, -2):
    font_quote = ImageFont.truetype(FONT_BOLD, size=size)
    spacing_q  = max(12, size // 3)
    wrapped_q  = wrap_text(QUOTE, font_quote, MAX_W_QUOTE)
    bbox_q     = draw.multiline_textbbox((0, 0), wrapped_q, font=font_quote, spacing=spacing_q)
    if (bbox_q[3] - bbox_q[1]) <= available_h:
        break

draw.multiline_text((X_TEXT, y_after_headline), wrapped_q, font=font_quote,
                    fill=DARK, spacing=spacing_q, stroke_width=1, stroke_fill=DARK)

bbox_q2 = draw.multiline_textbbox((X_TEXT, y_after_headline), wrapped_q,
                                   font=font_quote, spacing=spacing_q)
y_name = bbox_q2[3] + NAME_GAP

draw.text((X_TEXT, y_name), NAME, font=font_name, fill=DARK)

# Save
out_path = OUT_DIR / OUTPUT_NAME
save_kwargs = {"quality": 100, "subsampling": 0}
if icc:
    save_kwargs["icc_profile"] = icc
img.save(out_path, **save_kwargs)
print(f"Saved: {out_path}")
