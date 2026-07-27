#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_12.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/template12")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

DARK        = (10, 27, 42)
TEXT_LEFT   = 480
TEXT_RIGHT  = 980
TEXT_CENTER = 730
MAX_W       = TEXT_RIGHT - TEXT_LEFT
Y_QUOTE     = 440
NAME_SIZE   = 28
Y_BOTTOM    = 980

REVIEWS = [
    {"quote": "Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra.", "name": "– Bettina Kirkegaard", "out": "p1_bettina_1.jpg"},
    {"quote": "Selve produktet er virkelig fem stjerner værd. Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra.", "name": "– Bettina Kirkegaard", "out": "p1_bettina_2.jpg"},
    {"quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.", "name": "– Gitte Vedel", "out": "p1_gitte_1.jpg"},
    {"quote": "Den er meget fugtgivende og giver glød. Jeg har i mange år brugt forskellige cremer som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Dejligt kun at bruge et produkt.", "name": "– Gitte Vedel", "out": "p1_gitte_2.jpg"},
    {"quote": "Var lidt skeptisk inden jeg købte mit første Kjeldgaard produkt, men efter 3 mdr. kan jeg kun anbefale produktet. Kan tydelig se en forskel i ansigtet og på halsen, de synlige rynker er blevet meget mindre og min hud er blevet pæn og glat.", "name": "– Nina Eben Jensen", "out": "p1_nina_1.jpg"},
    {"quote": "Kan tydelig se en forskel i ansigtet og på halsen. Var lidt skeptisk inden jeg købte mit første Kjeldgaard produkt, men efter 3 mdr. kan jeg kun anbefale produktet. De synlige rynker er blevet meget mindre og min hud er blevet pæn og glat.", "name": "– Nina Eben Jensen", "out": "p1_nina_2.jpg"},
    {"quote": "Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang.", "name": "– Ann Louise Haugaard", "out": "p2_ann_1.jpg"},
    {"quote": "Er forbavset over virkningen – mine rynker ved øjnene, halsen og omkring munden er blevet formindsket.", "name": "– Kate", "out": "p2_kate_1.jpg"},
    {"quote": "Mine rynker er blevet formindsket. Er forbavset over virkningen ved øjnene, halsen og omkring munden.", "name": "– Kate", "out": "p2_kate_2.jpg"},
    {"quote": "Jeg har brugt Kjeldgaards Barrier defense siden den blev frigivet. Jeg kan kun anbefale det til alle andre. Huden er glattere, blødere og ikke mindst er mine solskader forsvundet.", "name": "– Sussie", "out": "p2_sussie_1.jpg"},
    {"quote": "Jeg er vildt begejstret for Barrier Defence Serum. Mine markeringer i ansigtet er blevet væsentlig formindsket, ansigtshuden ser sund, mættet og ensartet ud. Store anbefalinger herfra.", "name": "– Christel Møker", "out": "p2_christel_1.jpg"},
    {"quote": "Mine markeringer i ansigtet er blevet væsentlig formindsket, ansigtshuden ser sund, mættet og ensartet ud. Store anbefalinger herfra.", "name": "– Christel Møker", "out": "p2_christel_2.jpg"},
    {"quote": "Lækker konsistens, fugter huden rigtig godt - og så hjælper den faktisk på at mindske og udglatte de fine linjer omkring øjne osv. Kæmpe anbefaling herfra.", "name": "– Gitte Gren", "out": "p4_gitte_gren_1.jpg"},
    {"quote": "Jeg har brugt Barrier defense serum i næsten 1 år. Min hud føles blød og glat uden brug af andre cremer. Det er et fantastisk produkt som sikrer, at min hud altid føles frisk. Jeg elsker den.", "name": "– Kathrine Evers", "out": "p4_kathrine_1.jpg"},
    {"quote": "Endelig lykkedes det mig at finde en serum som virkelig virker - er bare blevet mega afhængig af den, så kun en varm anbefaling herfra.", "name": "– Pia Anne Marie Hansen", "out": "p4_pia_1.jpg"},
    {"quote": "Jeg er meget tilfreds. Jeg får ros for min hud, min alder taget i betragtning. Den er meget mere glat og strålende end mine jævnaldrende veninders.", "name": "– Jane Lyngholm", "out": "p4_jane_1.jpg"},
    {"quote": "Serummet er super lækkert. Konsistensen er blød, let at fordele, trænger hurtigt ind i huden og den strækker langt. Duften er mild og fin og huden føles blød og dejligt fugtet efter brug. Kan helt klart anbefales!", "name": "– Jane Lyngholm", "out": "p4_jane_2.jpg"},
    {"quote": "Fantastisk produkt. Har aldrig haft så pæn en hud før.", "name": "– Katja Freiberg", "out": "p4_katja_1.jpg"},
    {"quote": "Fantastisk produkt. Har brugt det længe nu og min hud er blevet smidig og glansfuld.", "name": "– Ingrid Hedevang", "out": "p4_ingrid_1.jpg"},
    {"quote": "Det er et fantastisk produkt. Fugter huden godt uden at give en fedtet hud, og den har tydeligt mindsket rynker. Det er min fjerde bestilling nu, så det kan klart anbefales.", "name": "– Mette Fisker", "out": "p4_mette_1.jpg"},
    {"quote": "Jeg er nu på min tredje serum, og kan varmt anbefale den. Den bedste serum. Så en klar forandring efter ca 14 dage. Nu kan jeg ikke bruge andet!", "name": "– Kristina Johnson", "out": "p5_kristina_1.jpg"},
    {"quote": "Et super dejligt produkt, mine brune pletter efter solbadning er forsvundet efter 2 måneder.", "name": "– Jeanette", "out": "p5_jeanette_1.jpg"},
    {"quote": "Er super glad for min serum. Den hjælper på mine mørke rande under øjnene og på min rosacea på næse og kinder. Jeg kan kun anbefale denne serum.", "name": "– Lene Mønsted", "out": "p5_lene_m_1.jpg"},
    {"quote": "Jeg er ovenud begejstret over produktet, som jeg kan se i den grad har formindsket mine rynker, uanset om det er panderynker, rynker ved mundvigene eller bekymringsrynker. Jeg kan kun anbefale produktet.", "name": "– Lotte", "out": "p5_lotte_1.jpg"},
    {"quote": "Det er virkelig den bedste serum jeg har prøvet. Den virker, reducerer rynker og fine linjer, og min hud stråler og ser mere sund ud. En serum der virkelig lever 100% op til det de skriver. Mine bedste anbefalinger.", "name": "– Tina", "out": "p5_tina_1.jpg"},
    {"quote": "Endelig en serum, der lever 100% op til det lovede. Min hud stråler og ser mere sund ud. Mine bedste anbefalinger!", "name": "– Tina", "out": "p5_tina_2.jpg"},
    {"quote": "Har aldrig oplevet et produkt som rent faktisk hjælper og gør det det skal i forhold til min hud, acne ar, linjer mv. Virkelig alle pengene værd.", "name": "– Majken", "out": "p5_majken_1.jpg"},
    {"quote": "Jeg kan så tydeligt se forskel på min hud efter at have brugt serumen i 4 måneder - mine rynker er tydeligt blevet mindre og min hud er blevet meget mere glat og blød. Kan kun anbefale serumen.", "name": "– Denice Zachariasen", "out": "p6_denice_1.jpg"},
    {"quote": "Uundværlig! Allerede efter 1 uge var min hud og glød helt anderledes end den plejer, og efter 1 måneds brug har den synligt minimeret rynker og pigmenter. Jeg kan klart anbefale dette.", "name": "– Louise Jeppesen", "out": "p6_louise_1.jpg"},
    {"quote": "Jeg var i tvivl - men den er SÅ meget pengene værd. Allerede efter 1 uge var min hud og glød helt anderledes end den plejer.", "name": "– Louise Jeppesen", "out": "p6_louise_2.jpg"},
    {"quote": "Dette er helt sikkert det bedste jeg har prøvet. I en alder på 68 er min hud helt baby blød og fine rynker er små. Jeg bruger det kun om aftenen, så det får lov til at virke natten over. Så min bedste anbefaling.", "name": "– Lone Kreipke", "out": "p6_lone_1.jpg"},
    {"quote": "En super skøn serum, som man ikke kan undvære, og som holder 100% i forhold til beskrivelsen af produktet. Jeg har brugt produktet de sidste 6 måneder, og jeg er kæmpe fan. De bedste anbefalinger herfra.", "name": "– Pernille", "out": "p6_pernille_1.jpg"},
    {"quote": "Virkelig lækker serum. Har brugt den hver dag i et par måneder nu og kan se en tydelig forskel. Den bliver en fast del af hudplejen!", "name": "– Line R W", "out": "p6_line_1.jpg"},
    {"quote": "Virkeligt et lækkert produkt, min hud elsker det! Kan varmt anbefales.", "name": "– Christina", "out": "p6_christina_1.jpg"},
    {"quote": "Super lækkert produkt som min hud nyder stor glæde af. Mange andre hudplejeprodukter er blevet helt overflødige efter jeg er gået over til denne serum. Er i gang med min anden flaske og har bestilt to mere.", "name": "– Jannie Andersen", "out": "p6_jannie_a_1.jpg"},
    {"quote": "Bare fantastisk - lever op til alt som beskrevet. Bestilt flere gange.", "name": "– Charlotte Marcher", "out": "p6_charlotte_m_1.jpg"},
    {"quote": "Den første serum, der har gjort noget godt for min hud og mig. Er utrolig nem at bruge og holder længe. Tak for et godt produkt.", "name": "– Ulla Tange", "out": "p7_ulla_1.jpg"},
    {"quote": "Kan beskrives med 1 ord: Mirakelmiddel.", "name": "– Mona", "out": "p7_mona_1.jpg"},
    {"quote": "Super godt produkt. Resultater allerede efter få dage.", "name": "– Pia Geisler Jensen", "out": "p7_pia_g_1.jpg"},
    {"quote": "Den er mega god, tror selv at jeg er blevet 10 år yngre. Ved godt at tro flytter bjerge, men jeg tror. Tak herfra.", "name": "– Lotte Boyer", "out": "p7_lotte_b_1.jpg"},
    {"quote": "Fantastisk produkt! Har prøvet en del, men dette er ud over al forventning.", "name": "– Izabella", "out": "p7_izabella_1.jpg"},
    {"quote": "Jeg er meget glad for Kjeldgaards Serum, jeg ser meget tydelige resultater. Jeg er 63 år, og med dette serum opstrammes huden tydeligt, bliver mere klar og levende. Og jeg har en MEGET sart hud og tåler det SÅ fint. Anbefales helt klart.", "name": "– Annette Asmus", "out": "p7_annette_1.jpg"},
    {"quote": "Virkelig god serum.", "name": "– Helle Nørgaard Petersen", "out": "p7_helle_n_1.jpg"},
    {"quote": "Endelig et produkt som holder hvad det lover. Jeg kan kun anbefale det.", "name": "– Trine Vilhelmsen", "out": "p7_trine_1.jpg"},
    {"quote": "Har været meget tilfreds med Kjeldgaard Barrier Defense og har derfor bestilt en mere. Kan tydelig mærke og se forskel på min hud i ansigtet.", "name": "– Jannie Lange Pedersen", "out": "p7_jannie_lp_1.jpg"},
    {"quote": "Fantastisk ansigtsspleje. Jeg er fuldstændig afhængig. Kan varmt anbefales.", "name": "– Tanja Pedersen", "out": "p7_tanja_p_1.jpg"},
    {"quote": "Jeg har brugt det siden nytår, men allerede efter 3-4 uger forsvandt den rødme jeg har haft omkring næsen i flere år. En rødmen som lægen mente var Rosacea, men som intet lægemiddel hjalp på. Jeg fortsætter med serumen og vil klart anbefale andre at bruge den.", "name": "– Jeanette Lauridsen", "out": "p7_jeanette_l_1.jpg"},
    {"quote": "Jeg vil helt klart anbefale serummet. Min hud er mættet, og føles blød hele dagen. Det føles som om produktet går mere i dybden end andre produkter jeg har prøvet. Jeg fortsætter helt sikkert med at bruge serummet.", "name": "– Charlotte Snor", "out": "p8_charlotte_s_1.jpg"},
    {"quote": "Jeg er ovenud tilfreds med produktet. Efter en måneds brug synes jeg min hud er kommet bedre i balance, den virker ikke så tør længere.", "name": "– Janne Fromberg Arvid", "out": "p8_janne_1.jpg"},
    {"quote": "Efter ganske få dage kunne jeg allerede se og mærke forskel. Ansigtet føles dejligt hele dagen! Det bedste produkt, jeg til dato har brugt.", "name": "– Lisbeth", "out": "p8_lisbeth_1.jpg"},
    {"quote": "Den serum er for vild! Holder 100% hvad den lover. Den er blevet et fast produkt i min morgen og aften rutine.", "name": "– Mia Sørensen", "out": "p8_mia_1.jpg"},
    {"quote": "Den bedste serum jeg til dato har prøvet. Huden bliver dejlig blød og ser friskere ud - og ja, yngre ser den også ud. Jeg er mere end tilfreds og har allerede købt en mere. Kæmpe anbefaling herfra.", "name": "– Hanne Weber", "out": "p8_hanne_1.jpg"},
    {"quote": "Kun godt. Har efterhånden prøvet en del serum uden synderlig positiv ændring. Men med Kjeldgaards mærker jeg virkelig en yderst positiv forandring. Kan på det varmeste anbefales.", "name": "– Lene Strate", "out": "p8_lene_strate_1.jpg"},
    {"quote": "Den bedste creme. Bruger den hver dag, den har taget mange af mine rynker og min hud er blevet så blød. Kan varmt anbefales.", "name": "– Lis Pedersen", "out": "p8_lis_1.jpg"},
    {"quote": "Kjeldgaards ansigtsserum er behageligt, let at påføre og trænger hurtigt ind uden at fedte. Jeg bliver desuden positivt overrasket hver gang over den lynhurtige levering. Et produkt og en service, der klart kan anbefales!", "name": "– Heidi", "out": "p8_heidi_1.jpg"},
    {"quote": "Jeg kan varmt anbefale denne serum. Ærgrer mig over at jeg ikke har taget et billede før jeg begyndte og så et nu - så ville man kunne se forskellen. Nemt at bruge. Det er bare super.", "name": "– Kunde", "out": "p8_kunde_1.jpg"},
    {"quote": "Giver huden et fantastisk løft og masser af glød. I mit lange liv har jeg prøvet alverdens cremer, men dette produkt slår simpelthen alt. Min hud føles fuldstændig silkeblød, og man kan på ingen måde se, at jeg snart er 60 år.", "name": "– Anita Malmstedt", "out": "p9_anita_1.jpg"},
    {"quote": "Jeg har prøvet alverdens cremer - men dette slår simpelthen alt. Min hud føles fuldstændig silkeblød, og man kan på ingen måde se, at jeg snart er 60 år. Det virker bare på alle parametre.", "name": "– Anita Malmstedt", "out": "p9_anita_2.jpg"},
    {"quote": "Min hud føles fuldstændig silkeblød, og man kan på ingen måde se, at jeg snart er 60 år. Jeg kan tydeligt se, at ansigtet har fået et friskere udseende og et flot løft. Hvis du overvejer at prøve det, så gør det - det er alle pengene værd!", "name": "– Anita Malmstedt", "out": "p9_anita_3.jpg"},
    {"quote": "Den Serum er bare helt fantastisk! Den giver mit ansigt en dejlig glød, masser af fugt, og reducerer rynker og et dejligt velvære. Jeg anvender den hver eneste morgen og den holder hele dagen. Den fedter ikke, men giver øjeblikkeligt fugt. Jeg kan kun anbefale den.", "name": "– Birgitte Larsen", "out": "p9_birgitte_l_1.jpg"},
    {"quote": "Den Serum er bare helt fantastisk! Den giver mit ansigt en dejlig glød, masser af fugt, og reducerer rynker. Den fedter ikke, men giver øjeblikkeligt fugt. Jeg kan kun anbefale den.", "name": "– Birgitte Larsen", "out": "p9_birgitte_l_2.jpg"},
    {"quote": "Den bedste jeg har prøvet, man kan både se og mærke forskellen. Huden bliver mere blød og glat og rynkerne minimeres.", "name": "– Britt Bente Andreasen", "out": "tp_britt_bente_1.jpg"},
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

for r in REVIEWS:
    img = Image.open(BASE)
    icc = img.info.get("icc_profile")
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    font_name   = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
    name_h      = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = Y_BOTTOM - Y_QUOTE - 40 - name_h

    for size in range(40, 18, -1):
        font_quote = ImageFont.truetype(FONT_BOLD, size=size)
        spacing = max(10, size // 3)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    draw.multiline_text((TEXT_CENTER, Y_QUOTE), wrapped, font=font_quote,
                        fill=DARK, spacing=spacing, anchor="ma", align="center",
                        stroke_width=1, stroke_fill=DARK)

    bbox = draw.multiline_textbbox((TEXT_CENTER, Y_QUOTE), wrapped,
                                    font=font_quote, spacing=spacing, anchor="ma")
    y_name = bbox[3] + 55

    draw.text((TEXT_CENTER, y_name), r["name"], font=font_name, fill=DARK, anchor="ma")

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
