#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE     = Path("/Users/lunahansen/Desktop/Claude ads/template_base_3.jpg")
OUT_DIR  = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)
FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

WHITE      = (255, 255, 255)
TEAL_DARK  = (38, 76, 85)
TEAL_LIGHT = (117, 155, 179)

CARD_PAD      = 68
CARD_LEFT     = 199 + CARD_PAD
CARD_RIGHT    = 700 - CARD_PAD
CARD_TEXT_TOP = 970
BOTTOM_PAD    = 80
CARD_BOTTOM   = 1454 - BOTTOM_PAD
NAME_SIZE     = 33
MAX_W         = CARD_RIGHT - CARD_LEFT

VARIATIONS = [
    {
        "headline":    '"Produktet er virkelig\nfem stjerner værd."',
        "quote":       "Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra",
        "name":        "- Bettina Kirkegaard",
        "output_name": "kjeldgaard3_bettina_1.jpg",
    },
    {
        "headline":    '"Det glatter de fine linjer ud og mine\nmørke rander under øjnene er faktisk væk."',
        "quote":       "Selve produktet er virkelig fem stjerner værd. Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra",
        "name":        "- Bettina Kirkegaard",
        "output_name": "kjeldgaard3_bettina_2.jpg",
    },
    {
        "headline":    '"Dejligt kun at bruge\net produkt."',
        "quote":       "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.",
        "name":        "- Gitte Vedel",
        "output_name": "kjeldgaard3_gitte_1.jpg",
    },
    {
        "headline":    '"Den er meget fugtgivende\nog giver glød."',
        "quote":       "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.",
        "name":        "- Gitte Vedel",
        "output_name": "kjeldgaard3_gitte_2.jpg",
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

for v in VARIATIONS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Headline
    font_headline = ImageFont.truetype(FONT_BOLD, size=82)
    draw.multiline_text((199, 290), v["headline"], font=font_headline,
                        fill=WHITE, spacing=6, stroke_width=2, stroke_fill=WHITE)

    # Auto-size quote
    font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
    name_h = draw.textbbox((0, 0), v["name"], font=font_name)[3]
    available_h = CARD_BOTTOM - CARD_TEXT_TOP - name_h - 40

    for size in range(48, 22, -1):
        font_quote = ImageFont.truetype(FONT_REG, size=size)
        spacing = max(8, size // 4)
        wrapped = wrap_text(draw, v["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    draw.multiline_text((CARD_LEFT, CARD_TEXT_TOP), wrapped, font=font_quote,
                        fill=TEAL_DARK, spacing=spacing)

    bbox = draw.multiline_textbbox((CARD_LEFT, CARD_TEXT_TOP), wrapped,
                                    font=font_quote, spacing=spacing)
    y_name = bbox[3] + 30
    draw.text((CARD_LEFT, y_name), v["name"], font=font_name, fill=TEAL_LIGHT)

    out_path = OUT_DIR / v["output_name"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")
