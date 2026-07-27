#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"
OUT_DIR   = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUT_DIR.mkdir(exist_ok=True)

VARIATIONS = [
    {
        "quote": "Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra",
        "name":  "- Bettina Kirkegaard",
        "out2":  "kjeldgaard2_bettina_1.jpg",
        "out4":  "kjeldgaard4_bettina_1.jpg",
    },
    {
        "quote": "Selve produktet er virkelig fem stjerner værd. Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra",
        "name":  "- Bettina Kirkegaard",
        "out2":  "kjeldgaard2_bettina_2.jpg",
        "out4":  "kjeldgaard4_bettina_2.jpg",
    },
    {
        "quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.",
        "name":  "- Gitte Vedel",
        "out2":  "kjeldgaard2_gitte_1.jpg",
        "out4":  "kjeldgaard4_gitte_1.jpg",
    },
    {
        "quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.",
        "name":  "- Gitte Vedel",
        "out2":  "kjeldgaard2_gitte_2.jpg",
        "out4":  "kjeldgaard4_gitte_2.jpg",
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

def render(base_path, v, out_name, card_left, card_right, card_text_top, card_bottom,
           name_size, name_font_path, name_color, quote_color, max_font, quote_font_path):
    img = Image.open(base_path)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    MAX_W = card_right - card_left
    font_name = ImageFont.truetype(name_font_path, size=name_size)
    name_h = draw.textbbox((0, 0), v["name"], font=font_name)[3]
    available_h = card_bottom - card_text_top - name_h - 45

    for size in range(max_font, 24, -1):
        font_quote = ImageFont.truetype(quote_font_path, size=size)
        spacing = max(8, size // 4)
        wrapped = wrap_text(draw, v["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    # Scale stroke with font size so small text stays readable
    sw = 2 if size >= 50 else (1 if size >= 36 else 0)
    draw.multiline_text((card_left, card_text_top), wrapped, font=font_quote,
                        fill=quote_color, spacing=spacing,
                        stroke_width=sw, stroke_fill=quote_color)

    bbox = draw.multiline_textbbox((card_left, card_text_top), wrapped,
                                    font=font_quote, spacing=spacing)
    y_name = bbox[3] + 40
    draw.text((card_left, y_name), v["name"], font=font_name, fill=name_color,
              stroke_width=1, stroke_fill=name_color)

    out_path = OUT_DIR / out_name
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

BASE2 = Path("/Users/lunahansen/Desktop/Claude ads/template_base_2.jpg")
BASE4 = Path("/Users/lunahansen/Desktop/Claude ads/template_base_4.jpg")

for v in VARIATIONS:
    # Template 2: light background, dark text, top-left text zone
    render(
        base_path      = BASE2,
        v              = v,
        out_name       = v["out2"],
        card_left      = 95,
        card_right     = 785,
        card_text_top  = 85,
        card_bottom    = 660,
        name_size      = 52,
        name_font_path = FONT_BOLD,
        name_color     = (20, 20, 20),
        quote_color    = (20, 20, 20),
        max_font       = 72,
        quote_font_path= FONT_BOLD,
    )
    # Template 4: portrait, teal bg, white card bottom-right
    render(
        base_path      = BASE4,
        v              = v,
        out_name       = v["out4"],
        card_left      = 634 + 55,
        card_right     = 1336 - 55,
        card_text_top  = 1105,
        card_bottom    = 1509 - 75,
        name_size      = 36,
        name_font_path = FONT_BOLD,
        name_color     = (91, 139, 162),
        quote_color    = (38, 76, 85),
        max_font       = 68,
        quote_font_path= FONT_BOLD,
    )
