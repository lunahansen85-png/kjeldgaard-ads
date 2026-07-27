#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_5.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

WHITE = (255, 255, 255)
GOLD  = (230, 172, 40)

# Layout — aligned with the KJELDGAARD logo left edge (x=158)
X_TEXT  = 158
Y_TEXT  = 295
MAX_W   = 530   # conservative to stay clear of bottle
Y_MAX   = 900
NAME_SIZE = 38
STAR_R    = 22
STAR_GAP  = 54
NUM_STARS = 5

REVIEWS = [
    {
        "quote": "Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra",
        "name":  "- Bettina Kirkegaard",
        "out":   "kjeldgaard5_bettina_1.jpg",
    },
    {
        "quote": "Selve produktet er virkelig fem stjerner værd. Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra",
        "name":  "- Bettina Kirkegaard",
        "out":   "kjeldgaard5_bettina_2.jpg",
    },
    {
        "quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.",
        "name":  "- Gitte Vedel",
        "out":   "kjeldgaard5_gitte_1.jpg",
    },
    {
        "quote": "Den er meget fugtgivende og giver glød. Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Dejligt kun at bruge et produkt.",
        "name":  "- Gitte Vedel",
        "out":   "kjeldgaard5_gitte_2.jpg",
    },
    {
        "quote": 'Var lidt skeptisk inden jeg købte min første Kjeldgaard produkt, men efter 3 mdr. kan jeg kun anbefale det. Kan tydelig se en forskel i ansigtet og på halsen, de synlige "rynker" er blevet meget mindre og min hud er blevet pæn og glat.',
        "name":  "- Nina Eben Jensen",
        "out":   "kjeldgaard5_nina_1.jpg",
    },
]

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

def draw_star(draw, cx, cy, r_outer, r_inner, fill):
    points = []
    for i in range(10):
        angle = math.pi / 5 * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    star_row_h = STAR_R * 2
    available_h = Y_MAX - Y_TEXT - star_row_h - 35 - name_h - 25

    for size in range(62, 28, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 4)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    sw = 2 if size >= 48 else (1 if size >= 34 else 0)
    draw.multiline_text((X_TEXT, Y_TEXT), wrapped, font=font_quote,
                        fill=WHITE, spacing=spacing,
                        stroke_width=sw, stroke_fill=WHITE)

    bbox = draw.multiline_textbbox((X_TEXT, Y_TEXT), wrapped, font=font_quote, spacing=spacing)

    y_stars = bbox[3] + 38
    for i in range(NUM_STARS):
        cx = X_TEXT + i * STAR_GAP + STAR_R
        cy = y_stars + STAR_R
        draw_star(draw, cx, cy, STAR_R, STAR_R // 2, GOLD)

    y_name = y_stars + star_row_h + 20
    draw.text((X_TEXT, y_name), r["name"], font=font_name, fill=WHITE,
              stroke_width=1, stroke_fill=WHITE)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")
