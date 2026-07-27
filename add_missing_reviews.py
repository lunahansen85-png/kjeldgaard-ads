#!/usr/bin/env python3
"""Add missing reviews to each template so all templates have the same 121 images."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

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

# ── Review data for the missing reviews ─────────────────────────────────────

# Reviews that templates 2, 3, 4 are missing (from t5-t11)
NEW_FOR_2_3_4 = [
    {"quote": "Mine rynker er blevet formindsket - Er forbavset over virkningen ved øjnene, halsen og omkring munden", "name": "- Kate", "out": "p2_kate_2.jpg"},
    {"quote": "Min hud var grå og tør - nu er den silkeblød og har fået sin glød tilbage. Samtidig har den udglattet de små fine linjer og rynker.", "name": "- Marianne", "out": "p2_marianne_2.jpg"},
    {"quote": "Min hud er meget blødere og ser sundere ud - blot efter et par ugers brug.", "name": "- Emma Kristine Eduardsen", "out": "p3_emma_2.jpg"},
    {"quote": "Endelig en serum, der lever 100% op til det lovede. Min hud stråler og ser mere sund ud. Mine bedste anbefalinger!", "name": "- Tina", "out": "p5_tina_2.jpg"},
    {"quote": "Jeg var i tvivl - men den er SÅ meget pengene værd. Allerede efter 1 uge var min hud og glød helt anderledes end den plejer.", "name": "- Louise Jeppesen", "out": "p6_louise_2.jpg"},
    {"quote": "Har været meget tilfreds med Kjeldgaard Barrier Defense. Kan tydelig mærke og se forskel på min hud i ansigtet.", "name": "- Jannie Lange Pedersen", "out": "p7_jannie_lp_1.jpg"},
    {"quote": "Man kan på ingen måde se, at jeg snart er 60 år. Jeg har prøvet alverdens cremer, men dette slar simpelthen alt!", "name": "- Anita Malmstedt", "out": "p8_anita_2.jpg"},
    {"quote": "Min hud er mættet og føles blød hele dagen. Det føles som om produktet går mere i dybden end andre produkter jeg har prøvet.", "name": "- Charlotte Snor", "out": "p8_charlotte_s_1.jpg"},
    {"quote": "Super lækkert produkt som min hud nyder stor glæde af. Mange andre hudplejeprodukter er blevet helt overflødige efter jeg er gået over til denne serum.", "name": "- Jannie Andersen", "out": "p6_jannie_1.jpg"},
]

# p1_gitte_2 is also missing from template 4 only
GITTE_2 = {"quote": "Den er meget fugtgivende og giver glød. Jeg har i mange år brugt forskellige cremer som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Dejligt kun at bruge et produkt.", "name": "- Gitte Vedel", "out": "p1_gitte_2.jpg"}

# Reviews that templates 5-11 are missing (from t2-t4)
NEW_FOR_5_TO_11 = [
    {"quote": "Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra", "name": "- Bettina Kirkegaard", "out": "p1_bettina_1.jpg"},
    {"quote": "Selve produktet er virkelig fem stjerner værd. Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra", "name": "- Bettina Kirkegaard", "out": "p1_bettina_2.jpg"},
    {"quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.", "name": "- Gitte Vedel", "out": "p1_gitte_1.jpg"},
    {"quote": "Den er meget fugtgivende og giver glød. Jeg har i mange år brugt forskellige cremer som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Dejligt kun at bruge et produkt.", "name": "- Gitte Vedel", "out": "p1_gitte_2.jpg"},
    {"quote": "Var lidt skeptisk inden jeg købte mit første Kjeldgaard produkt, men efter 3 mdr. kan jeg kun anbefale produktet. Kan tydelig se en forskel i ansigtet og på halsen, de synlige rynker er blevet meget mindre og min hud er blevet pæn og glat.", "name": "- Nina Eben Jensen", "out": "p1_nina_1.jpg"},
    {"quote": "Super lækkert produkt som min hud nyder stor glæde af. Mange andre hudplejeprodukter er blevet helt overflødige efter jeg er gået over til denne serum.", "name": "- Jannie Andersen", "out": "p6_jannie_1.jpg"},
    {"quote": "Min hud er mættet og føles blød hele dagen. Det føles som om produktet går mere i dybden end andre produkter jeg har prøvet.", "name": "- Charlotte Snor", "out": "p8_charlotte_1.jpg"},
]

# t3 needs p6_jannie_a_1 instead of p6_jannie_1, plus p8_charlotte_s_1
NEW_FOR_3_ONLY = [
    r for r in NEW_FOR_2_3_4 if r["out"] != "p6_jannie_1.jpg"
]
# t3 uses p6_jannie_a_1 filename (same content)
JANNIE_A_1 = {"quote": "Super lækkert produkt som min hud nyder stor glæde af. Mange andre hudplejeprodukter er blevet helt overflødige efter jeg er gået over til denne serum.", "name": "- Jannie Andersen", "out": "p6_jannie_a_1.jpg"}
NEW_FOR_3_ONLY.append(JANNIE_A_1)

# ── Template 2 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 2 ===")
BASE2    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_2_new2.jpg")
OUT_DIR2 = Path("/Users/lunahansen/Desktop/Claude ads/output/template2")
DARK2    = (20, 20, 20)
X2, Y2   = 95, 85
MAX_W2   = 690
Y_MAX2   = 660
NAME_SIZE2 = 52

for r in NEW_FOR_2_3_4:
    out_path = OUT_DIR2 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE2)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    img = img.resize((1636, 1630), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    font_name   = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE2)
    name_h      = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = Y_MAX2 - Y2 - name_h - 55
    for size in range(72, 28, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 5)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W2)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    sw = 2 if size >= 50 else (1 if size >= 36 else 0)
    draw.multiline_text((X2, Y2), wrapped, font=font_quote, fill=DARK2, spacing=spacing, stroke_width=sw, stroke_fill=DARK2)
    bbox = draw.multiline_textbbox((X2, Y2), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 55
    draw.text((X2, y_name), r["name"], font=font_name, fill=DARK2, stroke_width=1, stroke_fill=DARK2)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 3 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 3 ===")
BASE3    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_3.jpg")
OUT_DIR3 = Path("/Users/lunahansen/Desktop/Claude ads/output/template3")
WHITE3      = (255, 255, 255)
TEAL_DARK3  = (38, 76, 85)
TEAL_LIGHT3 = (117, 155, 179)
CARD_PAD3      = 68
CARD_LEFT3     = 199 + CARD_PAD3
CARD_RIGHT3    = 700 - CARD_PAD3
CARD_TEXT_TOP3 = 970
CARD_BOTTOM3   = 1454 - 80
MAX_W3         = CARD_RIGHT3 - CARD_LEFT3
NAME_SIZE3     = 33

# Headlines for t3 new reviews (quoted style like existing t3 entries)
T3_HEADLINES = {
    "p2_kate_2.jpg":       '"Er forbavset\nover virkningen."',
    "p2_marianne_2.jpg":   '"Glød og silkeblød\nhud tilbage."',
    "p3_emma_2.jpg":       '"Blødere hud\nefter få uger."',
    "p5_tina_2.jpg":       '"Lever 100% op\ntil det lovede."',
    "p6_louise_2.jpg":     '"SÅ meget\npengene værd."',
    "p7_jannie_lp_1.jpg":  '"Kan mærke og se\nforskel på huden."',
    "p8_anita_2.jpg":      '"Man kan ikke se\njeg snart er 60."',
    "p8_charlotte_s_1.jpg":'"Huden er mættet og\nføles blød hele dagen."',
    "p6_jannie_a_1.jpg":   '"Mange hudplejeprodukter\ner blevet overflødige."',
}

for r in NEW_FOR_3_ONLY:
    out_path = OUT_DIR3 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    headline = T3_HEADLINES.get(r["out"], '"" ')
    img = Image.open(BASE3)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_headline = ImageFont.truetype(FONT_BOLD, size=82)
    draw.multiline_text((199, 290), headline, font=font_headline, fill=WHITE3, spacing=6, stroke_width=2, stroke_fill=WHITE3)
    font_name   = ImageFont.truetype(FONT_REG, size=NAME_SIZE3)
    name_h      = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = CARD_BOTTOM3 - CARD_TEXT_TOP3 - name_h - 40
    for size in range(48, 22, -1):
        font_quote = ImageFont.truetype(FONT_REG, size=size)
        spacing = max(8, size // 4)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W3)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    draw.multiline_text((CARD_LEFT3, CARD_TEXT_TOP3), wrapped, font=font_quote, fill=TEAL_DARK3, spacing=spacing)
    bbox = draw.multiline_textbbox((CARD_LEFT3, CARD_TEXT_TOP3), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 30
    draw.text((CARD_LEFT3, y_name), r["name"], font=font_name, fill=TEAL_LIGHT3)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 4 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 4 ===")
BASE4    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_4_new.jpg")
OUT_DIR4 = Path("/Users/lunahansen/Desktop/Claude ads/output/template4")
TEAL_DARK4  = (38, 76, 85)
TEAL_LIGHT4 = (91, 139, 162)
CARD_PAD4      = 55
CARD_LEFT4     = 634 + CARD_PAD4
CARD_RIGHT4    = 1336 - CARD_PAD4
CARD_TEXT_TOP4 = 1105
CARD_BOTTOM4   = 1509 - 75
MAX_W4         = CARD_RIGHT4 - CARD_LEFT4
NAME_SIZE4     = 36

NEW_FOR_4 = NEW_FOR_2_3_4 + [GITTE_2]

for r in NEW_FOR_4:
    out_path = OUT_DIR4 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE4)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    img = img.resize((1408, 1608), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    font_name   = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE4)
    name_h      = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = CARD_BOTTOM4 - CARD_TEXT_TOP4 - name_h - 45
    for size in range(68, 24, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(8, size // 4)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W4)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    sw = 2 if size >= 48 else (1 if size >= 34 else 0)
    draw.multiline_text((CARD_LEFT4, CARD_TEXT_TOP4), wrapped, font=font_quote, fill=TEAL_DARK4, spacing=spacing, stroke_width=sw, stroke_fill=TEAL_DARK4)
    bbox = draw.multiline_textbbox((CARD_LEFT4, CARD_TEXT_TOP4), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 40
    draw.text((CARD_LEFT4, y_name), r["name"], font=font_name, fill=TEAL_LIGHT4, stroke_width=1, stroke_fill=TEAL_LIGHT4)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 5 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 5 ===")
BASE5    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_5.jpg")
OUT_DIR5 = Path("/Users/lunahansen/Desktop/Claude ads/output/template5")
WHITE5   = (255, 255, 255)
GOLD5    = (230, 172, 40)
X5, Y5   = 158, 295
MAX_W5   = 530
Y_MAX5   = 900
NAME_SIZE5 = 38
STAR_R5    = 22
STAR_GAP5  = 54

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR5 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE5)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_name  = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE5)
    name_h     = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    star_row_h = STAR_R5 * 2
    available_h = Y_MAX5 - Y5 - star_row_h - 35 - name_h - 25
    for size in range(62, 28, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 4)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W5)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    sw = 2 if size >= 48 else (1 if size >= 34 else 0)
    draw.multiline_text((X5, Y5), wrapped, font=font_quote, fill=WHITE5, spacing=spacing, stroke_width=sw, stroke_fill=WHITE5)
    bbox = draw.multiline_textbbox((X5, Y5), wrapped, font=font_quote, spacing=spacing)
    y_stars = bbox[3] + 38
    for i in range(5):
        cx = X5 + i * STAR_GAP5 + STAR_R5
        cy = y_stars + STAR_R5
        draw_star(draw, cx, cy, STAR_R5, STAR_R5 // 2, GOLD5)
    y_name = y_stars + star_row_h + 20
    draw.text((X5, y_name), r["name"], font=font_name, fill=WHITE5, stroke_width=1, stroke_fill=WHITE5)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 6 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 6 ===")
BASE6    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_6.jpg")
OUT_DIR6 = Path("/Users/lunahansen/Desktop/Claude ads/output/template6")
WHITE6   = (255, 255, 255)
GOLD6    = (230, 172, 40)
X6       = 75
Y_HL6    = 120
MAX_W6   = 560
STAR_R6  = 24
STAR_GAP6= 54
NAME_SIZE6 = 52

T6_HEADLINES = {
    "p1_bettina_1.jpg": "MØRKE RANDER\nER FAKTISK VÆK",
    "p1_bettina_2.jpg": "FEM STJERNER\nVÆRD",
    "p1_gitte_1.jpg":   "FRA KLINIK-CREME\nTIL ÉT PRODUKT",
    "p1_gitte_2.jpg":   "FUGTGIVENDE OG\nGIVER GLØD",
    "p1_nina_1.jpg":    "FRA SKEPTISK\nTIL OVERBEVIST",
    "p6_jannie_1.jpg":  "MANGE PRODUKTER\nER OVERFLØDIGE",
    "p8_charlotte_1.jpg":"HUDEN FØLES BLØD\nHELE DAGEN",
}

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR6 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    headline = T6_HEADLINES.get(r["out"], "")
    img = Image.open(BASE6)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img)
    font_headline = ImageFont.truetype(FONT_BOLD, size=88)
    draw.multiline_text((X6, Y_HL6), headline, font=font_headline, fill=WHITE6, spacing=12, stroke_width=3, stroke_fill=WHITE6)
    hl_bbox = draw.multiline_textbbox((X6, Y_HL6), headline, font=font_headline, spacing=12)
    y_quote = hl_bbox[3] + 130
    font_name  = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE6)
    name_h     = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    star_row_h = STAR_R6 * 2
    Y_BOTTOM6  = H - 150
    available_h = Y_BOTTOM6 - y_quote - star_row_h - 100 - name_h
    for size in range(62, 28, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(14, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W6)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    draw.multiline_text((X6, y_quote), wrapped, font=font_quote, fill=WHITE6, spacing=spacing, stroke_width=2, stroke_fill=WHITE6)
    bbox = draw.multiline_textbbox((X6, y_quote), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 100
    draw.text((X6, y_name), r["name"], font=font_name, fill=WHITE6, stroke_width=2, stroke_fill=WHITE6)
    name_w = draw.textlength(r["name"], font=font_name)
    x_stars = X6 + int(name_w) + 18
    for i in range(5):
        cx = x_stars + i * STAR_GAP6 + STAR_R6
        cy = y_name + name_h // 2
        draw_star(draw, cx, cy, STAR_R6, STAR_R6 // 2, GOLD6)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 7 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 7 ===")
BASE7    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_7.jpg")
OUT_DIR7 = Path("/Users/lunahansen/Desktop/Claude ads/output/template7")
DARK7      = (38, 76, 85)
TEAL_NAME7 = (51, 114, 139)
CARD_LEFT7  = 164
CARD_RIGHT7 = 471
MAX_W7      = CARD_RIGHT7 - CARD_LEFT7
Y_QUOTE7    = 510
NAME_SIZE7  = 26
CARD_BOTTOM7 = None  # need to check...

# Let me get the CARD_BOTTOM from t7
import re
t7_src = open('/Users/lunahansen/Desktop/Claude ads/generate_template7_all.py').read()
cb7_match = re.search(r'CARD_BOTTOM\s*=\s*(\d+)', t7_src)
CARD_BOTTOM7 = int(cb7_match.group(1)) if cb7_match else 900

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR7 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE7)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE7)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = CARD_BOTTOM7 - Y_QUOTE7 - 30 - name_h
    for size in range(62, 22, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W7)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    draw.multiline_text((CARD_LEFT7, Y_QUOTE7), wrapped, font=font_quote, fill=DARK7, spacing=spacing)
    bbox = draw.multiline_textbbox((CARD_LEFT7, Y_QUOTE7), wrapped, font=font_quote, spacing=spacing)
    y_name = bbox[3] + 30
    draw.text((CARD_LEFT7, y_name), r["name"], font=font_name, fill=TEAL_NAME7)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 8 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 8 ===")
BASE8    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_8.jpg")
OUT_DIR8 = Path("/Users/lunahansen/Desktop/Claude ads/output/template8")
DARK8       = (10, 27, 42)
TEXT_CENTER8= 673
TEXT_LEFT8  = 510
TEXT_RIGHT8 = 930
MAX_W8      = TEXT_RIGHT8 - TEXT_LEFT8
Y_QUOTE8    = 370
NAME_SIZE8  = 26
Y_BOTTOM8   = 720

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR8 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE8)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE8)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = Y_BOTTOM8 - Y_QUOTE8 - 40 - name_h
    for size in range(36, 18, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W8)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    draw.multiline_text((TEXT_CENTER8, Y_QUOTE8), wrapped, font=font_quote, fill=DARK8, spacing=spacing, anchor="ma", align="center", stroke_width=1, stroke_fill=DARK8)
    bbox = draw.multiline_textbbox((TEXT_CENTER8, Y_QUOTE8), wrapped, font=font_quote, spacing=spacing, anchor="ma")
    y_name = bbox[3] + 40
    draw.text((TEXT_CENTER8, y_name), r["name"], font=font_name, fill=DARK8, anchor="ma")
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 9 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 9 ===")
BASE9    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_9.jpg")
OUT_DIR9 = Path("/Users/lunahansen/Desktop/Claude ads/output/template9")
WHITE9      = (255, 255, 255)
TEXT_CENTER9= 662
TEXT_LEFT9  = 490
TEXT_RIGHT9 = 835
MAX_W9      = TEXT_RIGHT9 - TEXT_LEFT9
Y_QUOTE9    = 320
NAME_SIZE9  = 26
Y_BOTTOM9   = 600

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR9 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE9)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_name = ImageFont.truetype(FONT_REG, size=NAME_SIZE9)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = Y_BOTTOM9 - Y_QUOTE9 - 50 - name_h
    for size in range(30, 16, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W9)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    draw.multiline_text((TEXT_CENTER9, Y_QUOTE9), wrapped, font=font_quote, fill=WHITE9, spacing=spacing, anchor="ma", align="center", stroke_width=1, stroke_fill=WHITE9)
    bbox = draw.multiline_textbbox((TEXT_CENTER9, Y_QUOTE9), wrapped, font=font_quote, spacing=spacing, anchor="ma")
    y_name = bbox[3] + 50
    draw.text((TEXT_CENTER9, y_name), r["name"], font=font_name, fill=WHITE9, anchor="ma", stroke_width=1, stroke_fill=WHITE9)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 10 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 10 ===")
BASE10    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_10.jpg")
OUT_DIR10 = Path("/Users/lunahansen/Desktop/Claude ads/output/template10")
DARK10    = (10, 27, 42)
CARD_LEFT10  = 136
CARD_RIGHT10 = 492
MAX_W10      = CARD_RIGHT10 - CARD_LEFT10
CARD_BOTTOM10= 750
Y_STARS_END10= 217
NAME_SIZE10  = 28
NAME_GAP10   = 35

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR10 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    img = Image.open(BASE10)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE10)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    Y_QUOTE10 = Y_STARS_END10 + 25
    available_h = CARD_BOTTOM10 - Y_QUOTE10 - NAME_GAP10 - name_h
    for size in range(42, 20, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W10)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break
    y_quote10 = Y_QUOTE10
    y_name10  = CARD_BOTTOM10 - name_h
    draw.multiline_text((CARD_LEFT10, y_quote10), wrapped, font=font_quote, fill=DARK10, spacing=spacing, stroke_width=1, stroke_fill=DARK10)
    draw.text((CARD_LEFT10, y_name10), r["name"], font=font_name, fill=DARK10, stroke_width=1, stroke_fill=DARK10)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

# ── Template 11 ───────────────────────────────────────────────────────────────
print("\n=== TEMPLATE 11 ===")
BASE11    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_11.jpg")
OUT_DIR11 = Path("/Users/lunahansen/Desktop/Claude ads/output/template11")
DARK11         = (0, 0, 0)
X11            = 135
MAX_W_HL11     = 880
MAX_W_Q11      = 360
Y_HEADLINE11   = 60
HEADLINE_SIZE11= 80
NAME_SIZE11    = 28

T11_HEADLINES = {
    "p1_bettina_1.jpg": "MØRKE RANDER\nER FAKTISK VÆK",
    "p1_bettina_2.jpg": "FEM STJERNER\nVÆRD",
    "p1_gitte_1.jpg":   "FRA KLINIK-CREME\nTIL ÉT PRODUKT",
    "p1_gitte_2.jpg":   "FUGTGIVENDE OG\nGIVER GLØD",
    "p1_nina_1.jpg":    "FRA SKEPTISK\nTIL OVERBEVIST",
    "p6_jannie_1.jpg":  "MANGE PRODUKTER\nER OVERFLØDIGE",
    "p8_charlotte_1.jpg":"HUDEN FØLES BLØD\nHELE DAGEN",
}

for r in NEW_FOR_5_TO_11:
    out_path = OUT_DIR11 / r["out"]
    if out_path.exists():
        print(f"Skip (exists): {out_path.name}")
        continue
    headline = T11_HEADLINES.get(r["out"], "")
    img = Image.open(BASE11)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font_headline = ImageFont.truetype(FONT_BOLD, size=HEADLINE_SIZE11)
    spacing_h = 18
    draw.multiline_text((X11, Y_HEADLINE11), headline, font=font_headline, fill=DARK11, spacing=spacing_h, stroke_width=1, stroke_fill=DARK11)
    bbox_h = draw.multiline_textbbox((X11, Y_HEADLINE11), headline, font=font_headline, spacing=spacing_h)
    y_after_headline = bbox_h[3] + 60
    font_name = ImageFont.truetype(FONT_BOLD, size=NAME_SIZE11)
    name_h    = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    NAME_GAP11 = 60
    Y_BOTTOM11 = 1127
    available_h = Y_BOTTOM11 - y_after_headline - NAME_GAP11 - name_h
    QUOTE_SIZE11 = 36
    for size in range(QUOTE_SIZE11, 20, -2):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing_q  = max(12, size // 3)
        wrapped_q  = wrap_text(draw, r["quote"], font_quote, MAX_W_Q11)
        bbox_q     = draw.multiline_textbbox((0, 0), wrapped_q, font=font_quote, spacing=spacing_q)
        if (bbox_q[3] - bbox_q[1]) <= available_h:
            break
    draw.multiline_text((X11, y_after_headline), wrapped_q, font=font_quote, fill=DARK11, spacing=spacing_q, stroke_width=1, stroke_fill=DARK11)
    bbox_q2 = draw.multiline_textbbox((X11, y_after_headline), wrapped_q, font=font_quote, spacing=spacing_q)
    y_name = bbox_q2[3] + NAME_GAP11
    draw.text((X11, y_name), r["name"], font=font_name, fill=DARK11, stroke_width=1, stroke_fill=DARK11)
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path.name}")

print("\n\nAll done!")
