#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE    = Path("/Users/lunahansen/Desktop/Claude ads/template_base_3.jpg")
OUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output/template3")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Bold.ttf"
FONT_REG  = "/Users/lunahansen/Desktop/Claude ads/OpenSans-Regular.ttf"

WHITE      = (255, 255, 255)
TEAL_DARK  = (38, 76, 85)
TEAL_LIGHT = (117, 155, 179)

CARD_PAD      = 68
CARD_LEFT     = 199 + CARD_PAD
CARD_RIGHT    = 700 - CARD_PAD
CARD_TEXT_TOP = 970
CARD_BOTTOM   = 1454 - 80
MAX_W         = CARD_RIGHT - CARD_LEFT
NAME_SIZE     = 33

REVIEWS = [
    # PAGE 1
    {"headline": '"Produktet er virkelig\nfem stjerner værd."',        "quote": "Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra", "name": "- Bettina Kirkegaard", "out": "p1_bettina_1.jpg"},
    {"headline": '"Det glatter de fine linjer ud og\nmine mørke rander er faktisk væk."', "quote": "Selve produktet er virkelig fem stjerner værd. Det glatter de fine linjer ud og mine mørke rander under øjnene er faktisk væk. Selv min bekymringsrynke i panden er blevet mindre synlig. De varmeste anbefalinger herfra", "name": "- Bettina Kirkegaard", "out": "p1_bettina_2.jpg"},
    {"headline": '"Dejligt kun at bruge\net produkt."',                  "quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.", "name": "- Gitte Vedel", "out": "p1_gitte_1.jpg"},
    {"headline": '"Den er meget fugtgivende\nog giver glød."',           "quote": "Jeg har i mange år brugt forskellige cremer, som kun kunne købes på skønhedsklinikker. Nu har jeg prøvet Kjeldgaard serum i 2 mdr. Den er meget fugtgivende og giver glød. Dejligt kun at bruge et produkt.", "name": "- Gitte Vedel", "out": "p1_gitte_2.jpg"},
    {"headline": '"De synlige rynker er\nblevet meget mindre."',         "quote": "Var lidt skeptisk inden jeg købte mit første Kjeldgaard produkt, men efter 3 mdr. kan jeg kun anbefale produktet. Kan tydelig se en forskel i ansigtet og på halsen, de synlige rynker er blevet meget mindre og min hud er blevet pæn og glat.", "name": "- Nina Eben Jensen", "out": "p1_nina_1.jpg"},
    # PAGE 2
    {"headline": '"Fantastisk produkt!"',                                "quote": "Fantastisk produkt! Kan allerede efter at have brugt det i 14 dage se fremgang", "name": "- Ann Louise Haugaard", "out": "p2_ann_1.jpg"},
    {"headline": '"Mine rynker er\nblevet formindsket."',                "quote": "Er forbavset over virkningen - mine rynker ved øjnene, halsen og omkring munden er blevet formindsket", "name": "- Kate", "out": "p2_kate_1.jpg"},
    {"headline": '"Huden er glattere, blødere\nog mine solskader er forsvundet."', "quote": "Jeg har brugt Kjeldgaards Barrier defense siden den blev frigivet. Jeg kan kun anbefale det til alle andre. Huden er glattere, blødere og ikke mindst er mine solskader forsvundet!", "name": "- Sussie", "out": "p2_sussie_1.jpg"},
    {"headline": '"Ansigtshuden ser sund,\nmættet og ensartet ud."',    "quote": "Jeg er vildt begejstret for Barrier Defence Serum. Mine markeringer i ansigtet er blevet væsentlig formindsket, ansigtshuden ser sund, mættet og ensartet ud. Store anbefalinger herfra!", "name": "- Christel Møker", "out": "p2_christel_1.jpg"},
    {"headline": '"Min hud var grå og tør -\nnu er den silkeblød."',     "quote": "Før jeg begyndte at bruge cremen, var min hud grå at kigge på, og meget tør. Nu er min hud bare silkeblød og har fået sin glød tilbage igen. Samtidig har den udglattet de små fine linjer og rynker.", "name": "- Marianne", "out": "p2_marianne_1.jpg"},
    # PAGE 3
    {"headline": '"De fine linjer er udvisket\nog de dybe rynker er knap så dybe."', "quote": "Jeg har brugt Kjeldgaards serum, siden den kom frem. Tidligere syntes jeg mine rynker bare blev dybere og flere - men efter at jeg er begyndt at bruge Kjeldgaards serum, er de fine linjer udvisket, og de dybe rynker er knap så dybe.", "name": "- Karina", "out": "p3_karina_1.jpg"},
    {"headline": '"Jeg droppede natcremen\nog dagcremen."',              "quote": "Kjeldgaards Defense Serum har mindsket mine kragetæer ved øjnene og mine rynker under øjnene, og rynkerne rundt omkring munden. Det trænger hurtigt ind i huden og er nemt at bruge. Nu bruger jeg kun et produkt. Jeg vil varmt anbefale Kjeldgaards Defense Serum.", "name": "- Karina", "out": "p3_karina_2.jpg"},
    {"headline": '"Jeg er 60 - og mine fine\nlinjer er begyndt at forsvinde."', "quote": "Kjeldgaards Defense Serum har mindsket mine kragetæer ved øjnene og mine rynker. Det er nemt at bruge - for det er kun et produkt. Jeg vil varmt anbefale Kjeldgaards Defense Serum.", "name": "- Karina", "out": "p3_karina_3.jpg"},
    {"headline": '"Rigtig gode resultater\nblot efter et par ugers brug."', "quote": "Jeg vil virkelig anbefale denne serum! Rigtig gode resultater. Min hud er meget blødere og ser sundere ud. Blot efter et par ugers brug.", "name": "- Emma Kristine Eduardsen", "out": "p3_emma_1.jpg"},
    # PAGE 4
    {"headline": '"Kæmpe anbefaling\nherfra!"',                         "quote": "Lækker konsistens, fugter huden rigtig godt - og så hjælper den faktisk på at mindske og udglatte de fine linjer omkring øjne osv. Kæmpe anbefaling herfra!", "name": "- Gitte Gren", "out": "p4_gitte_gren_1.jpg"},
    {"headline": '"Jeg elsker den!"',                                    "quote": "Jeg har brugt Barrier defense serum i næsten 1 år. Min hud føles blød og glat uden brug af andre cremer. Det er et fantastisk produkt som sikrer at min hud altid føles frisk. Jeg elsker den!", "name": "- Kathrine Evers", "out": "p4_kathrine_1.jpg"},
    {"headline": '"Endelig en serum\nsom virkelig virker."',             "quote": "Endelig lykkes det mig at finde en serum som virkelig virker, er bare blevet mega afhængig af den så kun en varm anbefaling herfra", "name": "- Pia Anne Marie Hansen", "out": "p4_pia_1.jpg"},
    {"headline": '"Huden er mere glat og\nstrålende end mine veninders."', "quote": "Jeg får ros for min hud, min alder taget i betragtning. Den er meget mere glat og strålende end mine jævnaldrende veninders.", "name": "- Jane Lyngholm", "out": "p4_jane_1.jpg"},
    {"headline": '"Huden føles blod\nog dejligt fugtet."',               "quote": "Serummet er super lækkert. Konsistensen er blød, let at fordele, trænger hurtigt ind i huden og den strækker langt. Duften er mild og fin og huden føles blød og dejligt fugtet efter brug.", "name": "- Jane Lyngholm", "out": "p4_jane_2.jpg"},
    {"headline": '"Har aldrig haft\nså pæn en hud før."',              "quote": "Fantastisk produkt. Har aldrig haft så pæn en hud før.", "name": "- Katja Freiberg", "out": "p4_katja_1.jpg"},
    {"headline": '"Min hud er blevet\nsmidig og glansfuld."',            "quote": "Fantastisk produkt - har brugt det længe nu og min hud er blevet smidig og glansfuld.", "name": "- Ingrid Hedevang", "out": "p4_ingrid_1.jpg"},
    {"headline": '"Den har tydeligt\nmindsket rynker."',                 "quote": "Det er et fantastisk produkt. Fugter huden godt uden at give en fedtet hud, og den har tydeligt mindsket rynker. Det er min fjerde bestilling nu, så det kan klart anbefales.", "name": "- Mette Fisker", "out": "p4_mette_1.jpg"},
    # PAGE 5
    {"headline": '"Det bedste serum -\nklar forandring efter 14 dage."', "quote": "Jeg er nu på min tredje serum, og kan varmt anbefale den. Det bedste serum. Så en klar forandring efter ca 14 dage. Nu kan jeg ikke bruge andet!", "name": "- Kristina Johnson", "out": "p5_kristina_1.jpg"},
    {"headline": '"Mine brune pletter er\nforsvundet efter 2 måneder."', "quote": "Et super dejligt produkt, mine brune pletter efter solbadning er forsvundet efter 2 måneder.", "name": "- Jeanette", "out": "p5_jeanette_1.jpg"},
    {"headline": '"Den hjælper på mine mørke\nrande og min rosacea."',  "quote": "Er super glad for min serum. Den hjælper på mine mørke rande under øjnene. Den hjælper på min rosacea som jeg har haft på næse og kinder. Jeg kan kun anbefale denne serum.", "name": "- Lene Mønsted", "out": "p5_lene_m_1.jpg"},
    {"headline": '"Jeg kan kun\nanbefale produktet."',                   "quote": "Jeg er ovenud begejstret over produktet, som i den grad har formindsket mine rynker, uanset om det er panderynker, rynker ved mundvigene eller bekymringsrynker mellem øjnene. Jeg kan kun anbefale produktet.", "name": "- Lotte", "out": "p5_lotte_1.jpg"},
    {"headline": '"Den bedste serum\njeg har prøvet."',                  "quote": "Det er virkelig den bedste serum jeg har prøvet. Den virker, reducerer rynker og fine linjer, og min hud stråler og ser mere sund ud. En serum der virkelig lever 100% op til det de skriver.", "name": "- Tina", "out": "p5_tina_1.jpg"},
    {"headline": '"Virkelig alle\npengene værd."',                      "quote": "Har aldrig oplevet et produkt som rent faktisk hjælper og gør det det skal i forhold til min hud, acne ar, linjer mv. Virkelig alle pengene værd.", "name": "- Majken", "out": "p5_majken_1.jpg"},
    # PAGE 6
    {"headline": '"Mine rynker er tydeligt\nblevet mindre."',            "quote": "Super godt produkt. Jeg kan så tydeligt se forskel på min hud efter at have brugt serumen i 4 måneder, mine rynker er tydeligt blevet mindre og min hud er blevet meget mere glat og blød.", "name": "- Denice Zachariasen", "out": "p6_denice_1.jpg"},
    {"headline": '"Uuundværlig!"',                                       "quote": "Uuundværlig! Allerede efter 1 uge var min hud og glød helt anderledes end den plejer og efter 1 måneds brug har den synligt minimeret rynker og pigmenter. Jeg kan klart anbefale dette.", "name": "- Louise Jeppesen", "out": "p6_louise_1.jpg"},
    {"headline": '"I en alder på 68 er\nmin hud helt baby blød."',      "quote": "Dette er helt sikkert det bedste jeg har prøvet. I en alder på 68 er min hud helt baby blød og fine rynker er små. Min bedste anbefaling.", "name": "- Lone Kreipke", "out": "p6_lone_1.jpg"},
    {"headline": '"Den holder 100% i\nforhold til beskrivelsen."',       "quote": "En super skøn serum, som man ikke kan undvære, og som holder 100% i forhold til beskrivelsen af produktet. Jeg har brugt produktet de sidste 6 måneder, og jeg er kæmpe fan. De bedste anbefalinger herfra.", "name": "- Pernille", "out": "p6_pernille_1.jpg"},
    {"headline": '"Kan se en tydelig forskel\nefter et par måneder."',   "quote": "Virkelig lækker serum. Har brugt den hver dag i et par måneder nu og kan se en tydelig forskel. Den bliver en fast del af hudplejen!", "name": "- Line R W", "out": "p6_line_1.jpg"},
    {"headline": '"Mange hudplejeprodukter\ner blevet overflødige."',    "quote": "Super lækkert produkt som min hud nyder stor glæde af. Mange andre hudplejeprodukter er blevet helt overflødige efter jeg er gået over til denne serum.", "name": "- Jannie Andersen", "out": "p6_jannie_1.jpg"},
    # PAGE 7
    {"headline": '"Den første serum der\nhar gjort noget godt for mig."', "quote": "Den første serum, der har gjort noget godt for min hud og mig. Er utrolig nem at bruge og holder længe. Tak for et godt produkt.", "name": "- Ulla Tange", "out": "p7_ulla_1.jpg"},
    {"headline": '"Jeg er 63 - og huden\noprammer tydeligt."',           "quote": "Jeg er meget glad for Kjeldgaards Serum, jeg ser meget tydelige resultater. Jeg er 63 år, og med dette serum opstrammes huden tydeligt, bliver mere klar og levende.", "name": "- Annette Asmus", "out": "p7_annette_1.jpg"},
    {"headline": '"Endelig et produkt\nsom holder hvad det lover."',     "quote": "Endelig et produkt som holder hvad det lover. Jeg kan kun anbefale det!", "name": "- Trine Vilhelmsen", "out": "p7_trine_1.jpg"},
    {"headline": '"Rødmen fra Rosacea\nforsvandt efter 3-4 uger."',     "quote": "Jeg har brugt det siden nytår men allerede efter 3-4 uger forsvandt den rødmen jeg har haft omkring næsen i flere år. En rødmen som lægen mente var Rosacea, men som intet lægemiddel hjalp på.", "name": "- Jeanette Lauridsen", "out": "p7_jeanette_l_1.jpg"},
    # PAGE 8
    {"headline": '"Det føles som om produktet\ngår mere i dybden."',     "quote": "Min hud er mættet, og føles blød hele dagen. Det føles som om produktet går mere i dybden end andre produkter jeg har prøvet. Jeg fortsætter helt sikkert med at bruge serummet.", "name": "- Charlotte Snor", "out": "p8_charlotte_1.jpg"},
    {"headline": '"Det bedste produkt\njeg til dato har brugt."',        "quote": "Efter ganske få dage kunne jeg allerede se og mærke forskel ved brug af Kjeldgaard serum. Ansigtet føles dejligt hele dagen! Det bedste produkt, jeg til dato har brugt, tak!", "name": "- Lisbeth", "out": "p8_lisbeth_1.jpg"},
    {"headline": '"Den er for vild -\nholder 100% hvad den lover."',    "quote": "Den serum er for vild! Holder 100% hvad den lover, jeg er stor fan. Den er blevet et fast produkt i min morgen og aften rutine.", "name": "- Mia Sørensen", "out": "p8_mia_1.jpg"},
    {"headline": '"Huden ser friskere ud -\nog ja, yngre også."',       "quote": "Den bedste serum jeg til dato har prøvet. Huden bliver dejlig blød og ser friskere ud og tор jeg sige det - jo jeg gør - yngre ser den også ud. Jeg er mere end tilfreds og har allerede købt en mere.", "name": "- Hanne Weber", "out": "p8_hanne_1.jpg"},
    {"headline": '"Den har taget mange\naf mine rynker."',               "quote": "Den bedste creme bruger den hver dag, den har taget mange af mine rynker og min hud er blevet så blød. Kan varmt anbefales.", "name": "- Lis Pedersen", "out": "p8_lis_1.jpg"},
    {"headline": '"Man kan på ingen måde se,\nat jeg snart er 60 år."', "quote": "Giver huden et fantastisk løft og masser af glød. I mit lange liv har jeg prøvet alverdens cremer, men dette produkt slar simpelthen alt. Min hud føles fuldstændig silkeblød, og man kan på ingen måde se, at jeg snart er 60 år.", "name": "- Anita Malmstedt", "out": "p8_anita_1.jpg"},
    # PAGE 9
    {"headline": '"Jeg kan tydeligt se\nen forskel i mine rynker."',     "quote": "Jeg kan virkelig anbefale Kjeldgaards serum. Jeg begyndte at bruge det for et år siden, og jeg kan tydeligt se en forskel i mine rynker i ansigtet. Huden føles mere elastisk. En kæmpe anbefaling herfra!", "name": "- Signe Klint Buchbjerg", "out": "p9_signe_1.jpg"},
    {"headline": '"Den her er simpelthen\ni en klasse for sig."',        "quote": "Jeg har brugt Kjeldgaards Defense Serum igennem det sidste halve år. Jeg har brugt andre serummer i flere år, men den her er simpelthen i en klasse for sig.", "name": "- Dorte Wittrock", "out": "p9_dorte_1.jpg"},
    {"headline": '"Ingen serummer kan\nmåle sig med denne."',            "quote": "Denne serum fra Kjeldgaard har jeg brugt i tre måneder, og jeg er stor fan. Den er nem at smører på, huden bliver smidig og blød og ser sundere ud. Der er ingen serummer der kan måle sig med denne.", "name": "- Helle Madsen", "out": "p9_helle_1.jpg"},
    {"headline": '"Det bedste jeg\nnogensinde har gjort for mig selv."', "quote": "Jeg har nu brugt Kjeldgaards serum i to måneder, og det er det bedste, jeg nogensinde har gjort for mig selv. Jeg kan tydeligt se at der er blevet mindre her. Jeg har ikke så store poser under øjnene mere.", "name": "- Conny", "out": "p9_conny_1.jpg"},
    {"headline": '"Jeg er 71 år - og\nkan slet ikke undvære den."',    "quote": "Jeg er 71 år, og jeg har brugt Kjeldgaards Barrier Defense i omkring et år. Jeg kan bare anbefale den - jeg kan slet ikke undvære den. Det er simpelthen så lækkert at smøre ud.", "name": "- Maja Isaksen", "out": "p9_maja_1.jpg"},
    {"headline": '"Kjeldgaards er det\nbedste mærke på markedet."',    "quote": "Nu har jeg brugt Kjeldgaards igennem mange måneder, og det giver en helt utrolig fugt - på et niveau jeg ikke har prøvet for. Jeg behøver ikke lægge dagcreme ovenpå når jeg har brugt serum.", "name": "- Dorte Wittrock", "out": "p9_dorte_2.jpg"},
    # PAGE 10
    {"headline": '"Min hud er mega blod\nogså under øjnene og på halsen."', "quote": "Jeg er 68 år, og jeg har brugt Kjeldgaards Serum i cirka tre måneder. Min hud er mega blød. Det gælder også her under øjnene og ned på halsen. Det er virkelig nemt at bruge, og jeg kan varmt anbefale den.", "name": "- Jette Grønfeldt", "out": "p10_jette_1.jpg"},
    {"headline": '"Solskader er næsten væk\nog sorte rande er mindre."', "quote": "Allerede efter 14 dage kunne jeg mærke en tydelig forskel på solskader, jeg havde på mit ansigt. De er næsten væk. Desuden er de sorte rande under mine øjne blevet mindre, og mine pigmentpletter er afblegede.", "name": "- Inger Jensen", "out": "p10_inger_1.jpg"},
    {"headline": '"Mine folder i kinderne\ner ikke så dybe længere."',   "quote": "Jeg er 61 år gammel og har brugt Kjeldgaards Barrier Creme i 2 måneder. Jeg synes den har gjort meget ved min hud. Den er blevet lidt mere stram og mine folder i kinderne er ikke så dybe. Klar anbefaling!", "name": "- Lene Clemmensen", "out": "p10_lene_c_1.jpg"},
    {"headline": '"Mine linjer er meget fine\nog huden er mere smuk."',  "quote": "Jeg er 68 år og har brugt Kjeldgaards Serum i et halvt års tid. Mine linjer er blevet meget fine, og jeg er meget, meget glad for dem. Min hud er blevet blødere og mere smuk.", "name": "- Marianne Due", "out": "p10_marianne_d_1.jpg"},
    {"headline": '"Jeg bruger aldrig dagcreme\neller natcreme længere."', "quote": "Jeg har brugt Kjeldgaards Serum i cirka to år. Min hud er kommet i så fin en fugtbalance, så jeg faktisk aldrig bruger hverken dagcreme eller natcreme længere. Jeg har fået finere rynker rundt om øjnene og overlæben.", "name": "- Winie Moeslund", "out": "p10_winie_1.jpg"},
    # TP Kjeldgaards 2
    {"headline": '"Mine små rynker er nærmest\nforsvundet."', "quote": "Jeg er 68 år. Jeg har nu i fire måneder brugt Kjeldgaards Barrier Defense Serum. Det har bevirket, at min hud er blevet ekstremt blød, helt silkeagtig. Den har reduceret rigtig mange af mine små rynker, de er nærmest forsvundet.", "name": "- Birgitte Tronøe", "out": "tp2_birgitte_tronoe_1.jpg"},
    {"headline": '"Min hud har fået glans igen\nog jeg vil ikke undvære den."', "quote": "Det er det bedste, jeg nogensinde har gjort. Min hud har fået glans, og i dag vil jeg ikke undvære den, derfor de bedste anbefalinger herfra.", "name": "- Lilly Thorsen", "out": "tp2_lilly_1.jpg"},
    {"headline": '"På 5. måned og stadig\nsuper tilfreds."', "quote": "Hudpleje rutinen er blevet noget nemmere med kun jeres Barrier Defense Serum og nu er jeg på 5. måned og er stadig super godt tilfreds med resultatet og følelsen.", "name": "- Ann Boye-Hansen", "out": "tp2_ann_boye_1.jpg"},
    {"headline": '"Alt hvad de siger\ner RIGTIGT."', "quote": "Køb den, det er simpelthen så lækker og jeg har fået rigtig blød og frisk hud. Alt hvad de siger er RIGTIGT.", "name": "- Birgitte", "out": "tp2_birgitte_1.jpg"},
    {"headline": '"Kan se og mærke\nden store forskel."', "quote": "Køb det, alt hvad der bliver sagt passer. Jeg har selv købt og brugt det og kan se og mærke den store forskel, jeg er 61 år.", "name": "- Birgitte", "out": "tp2_birgitte_2.jpg"},
    {"headline": '"Jeg er 62 og har\nsynlige resultater allerede."', "quote": "Fantastisk lækkert produkt. Er ved min anden flaske og har allerede købt flere. Kan varmt anbefales. Jeg er 62 og har synlige resultater allerede.", "name": "- Charlotte Dam", "out": "tp2_charlotte_dam_1.jpg"},
    {"headline": '"Kunne hurtigt se en\nforandring i ansigtet."', "quote": "Er virkelig glad for min Serum. Kunne hurtigt se en forandring i ansigtet. Bruger den morgen og aften.", "name": "- Dorte Bruun Tronstrøm Lind", "out": "tp2_dorte_bruun_1.jpg"},
    {"headline": '"Anbefaler den til\nkvinder i alle aldre."', "quote": "Jeg vil stærkt anbefale Kjeldgaard serum til kvinder i alle aldre fordi den har så gode ingredienser som f.eks hyaluronsyre som er hudens vigtigste byggesten og den er nem at påføre, et par dråber er nok.", "name": "- Britt Bente Andreasen", "out": "tp2_britt_bente_1.jpg"},
    {"headline": '"Bare en fantastisk creme\nog fantastisk kundeservice."', "quote": "Jeg kan tilslutte mig de mange andre. Bare en fantastisk creme. Dertil kommer også fantastisk kundeservice.", "name": "- Ingrid Hedevang", "out": "tp2_ingrid_1.jpg"},
    {"headline": '"Har fået den smukkeste\nbløde og glatteste hud."', "quote": "Den blødgør, opstrammer, reducere linjer og rynker og huden føles dejlig glat og lækker. Jeg er selv på nr. 2 og har fået den smukkeste bløde og glatteste hud. Den er bare super effektiv.", "name": "- Ingrid Hedevang", "out": "tp2_ingrid_2.jpg"},
    {"headline": '"Kan virkelig se forskel\nefter en måned."', "quote": "Jeg har brugt den i en måned og kan virkelig se forskel. Før brugte jeg en del penge på alt det man skulle købe til ansigtet. Her bruger man kun en fantastisk serum.", "name": "- Britt Larsen", "out": "tp2_britt_larsen_1.jpg"},
    {"headline": '"Hjulpet på mine rynker\nog poser under øjnene."', "quote": "Jeg er også mega glad for cremen. Jeg ser forskel i mit ansigt og det har også hjulpet på mine rynker og poser under øjnene.", "name": "- Gauger1234", "out": "tp2_gauger_1.jpg"},
    {"headline": '"Denne er absolut\nmin favorit."', "quote": "Jeg har prøvet mange forskellige serummer, men denne er absolut min favorit, så den vil jeg fortsætte med. Mine bedste anbefalinger.", "name": "- Dorthe Albertsen", "out": "tp2_dorthe_albertsen_1.jpg"},
    {"headline": '"Jeg anbefaler den 100%."', "quote": "Jeg har brugt det i snart et år, og jeg bruger ikke andre serummer. Den er helt vildt lækker. Jeg anbefaler den 100%.", "name": "- Kirsten Søndervang", "out": "tp2_kirsten_1.jpg"},
    {"headline": '"Det er en ren fornøjelse\nhver eneste dag."', "quote": "Helt fantastisk serum! Har aldrig rigtig haft en rutine morgen og aften. Men efter jeg er startet med denne serum, er det en ren fornøjelse, og jeg gør det gerne hver dag.", "name": "- Lis Rauff Sørensen", "out": "tp2_lis_rauff_1.jpg"},
    {"headline": '"Den lever helt op til,\nhvad den lover."', "quote": "Når jeg læser anmeldelser, er det altid med en vis skepsis. Jeg tænkte dog, at denne serum lød til at være god, og købte den. Allerede efter kun at have prøvet den én gang, lever den helt op til, hvad den lover. Min hud har de sidste 2-3 mdr. været tør, grå og kedelig. Jeg brugte den i går aftes, og stadigvæk her til formiddag er der mere glød, end der har været de sidste mange mdr.", "name": "- Sanne Frank Sloth", "out": "tp2_sanne_frank_1.jpg"},
    {"headline": '"Min hud er meget blødere\nog ser sundere ud."', "quote": "Jeg vil virkelig anbefale denne serum! Rigtig gode resultater. Min hud er meget blødere og ser sundere ud. Blot efter et par ugers brug.", "name": "- Emma Kristine Eduardsen", "out": "tp2_emma_1.jpg"},
    {"headline": '"Kæmpe anbefaling\nherfra."', "quote": "Fantastisk produkt. Lækker konsistens, fugter huden rigtig godt - og så hjælper den faktisk på at mindske og udglatte de fine linjer omkring øjne osv. Kæmpe anbefaling herfra.", "name": "- Gitte Gren", "out": "tp2_gitte_gren_2.jpg"},
    {"headline": '"Hold nu op, det er\net skønt produkt."', "quote": "Har lige fået min for et par dage siden, hold nu op, det er et skønt produkt. Kan kun anbefales.", "name": "- Gitte Overgaard", "out": "tp2_gitte_overgaard_1.jpg"},
    {"headline": '"Jeg kan ikke\nundvære det."', "quote": "Som sagt tidligere - fantastisk produkt og jeg kan ikke undvære det. Jeg er imponeret over produkt og service. Varm anbefaling herfra.", "name": "- Helle Søby Germansen", "out": "tp2_helle_soeby_1.jpg"},
    {"headline": '"Den hjælper super godt\npå min eksem."', "quote": "Den er SÅ Fantastisk og har bestilt igen. Den hjælper super godt på min eksem og fugter godt.", "name": "- Helle", "out": "tp2_helle_1.jpg"},
    {"headline": '"Et super effektivt\nprodukt."', "quote": "Har brugt den siden den udkom, der er virkelig store stjerner herfra - et super effektivt produkt.", "name": "- Jeanette Quistgaard Steensen", "out": "tp2_jeanette_q_1.jpg"},
    {"headline": '"Den er fantastisk,\nbruger den morgen og aften."', "quote": "Jeg får min datter til at bestille den. Jeg er på nr. 2 flaske og den er fantastisk, bruger den morgen og aften. Har bestilt nr. 3 flaske. Kan kun anbefale den.", "name": "- Jytte Pedersen", "out": "tp2_jytte_1.jpg"},
    {"headline": '"Dejlig serum til\nsart og sensitiv hud."', "quote": "Dejlig konsistens og dejlig neutral duft der hurtigt forsvinder. I det hele taget en dejlig serum. Og jeg har prøvet mange i årenes løb, da jeg har sart og sensitiv hud. Så rigtig mange stjerner til jeres produkt.", "name": "- Karin", "out": "tp2_karin_1.jpg"},
    {"headline": '"Har fjernet mørke pletter\nog reduceret rynker."', "quote": "Jeg er SÅ tilfreds med Kjeldgaard's serum. Har benyttet den helt fra starten. Den har fjernet mine mørke pletter i ansigtet efter for meget soldyrkelse. Den trænger hurtigt ind i huden og har også reduceret nogen af de fine rynker omkring øjnene. Så den største anbefaling herfra.", "name": "- Karina", "out": "tp2_karina_1.jpg"},
    {"headline": '"Kan se tydelig forskel\nmed mine 74 år."', "quote": "Det er det bedste produkt jeg har brugt, kan se tydelig forskel og kan varmt anbefale det selv med mine 74 år.", "name": "- Kristina Johnson", "out": "tp2_kristina_j_1.jpg"},
    {"headline": '"Mine rynker er blevet\nglattet meget ud."', "quote": "Stor anbefaling herfra, det bedste produkt jeg har prøvet. Mine rynker er blevet glattet meget ud og det går bare fremad.", "name": "- Lis Pedersen", "out": "tp2_lis_pedersen_1.jpg"},
    {"headline": '"Efter Kjeldgaard har\njeg ikke brugt andet."', "quote": "Plejer at skifte og bruge flere forskellige cremer. Efter at jeg startede på Kjeldgaard, har jeg ikke brugt andet.", "name": "- Lisbeth Kobberup", "out": "tp2_lisbeth_kobberup_1.jpg"},
    {"headline": '"Mine hvide talgknopper\ner nu væk."', "quote": "Super produkt. Kan varmt anbefales. Havde nogle hvide talgknopper. De er nu væk.", "name": "- Lone", "out": "tp2_lone_1.jpg"},
    {"headline": '"Jeg har kun behov\nfor denne serum."', "quote": "Fantastisk serum! Jeg har kun behov for denne serum, og ingen dag eller natcreme, vil virkelig anbefale den til alle.", "name": "- Marianne Thurø", "out": "tp2_marianne_thuro_1.jpg"},
    {"headline": '"Reduceret mine rynker\nog bekymringsrynker."', "quote": "Jeg har brugt det siden det kom frem og kan varmt anbefale det. Det har reduceret mine rynker omkring øjnene og mine bekymringsrynker.", "name": "- Karina", "out": "tp2_karina_2.jpg"},
    {"headline": '"Min hud er blevet mere\nelastisk og fugtet."', "quote": "I overgangsalderen kan man godt mærke huden mangler fugt og elasticitet. Jeg har brugt serummet fra midt januar, og kan se og mærke at min hud er blevet mere elastisk og fugtet. Elsker den og anbefaler den til andre.", "name": "- Pernille Lützop Hansen", "out": "tp2_pernille_l_1.jpg"},
    {"headline": '"Det er blevet et fast\nritual morgen og aften."', "quote": "Det er blevet et fast ritual morgen og aften her hos mig. Det er et helt fantastisk produkt. Kæmpe anbefaling herfra.", "name": "- Suzette Kjellerup", "out": "tp2_suzette_1.jpg"},
    {"headline": '"Ser tydeligere, glattere\nog mere frisk hud."', "quote": "Jeg er også mega tilfreds med denne serum. I en alder af 60 år har jeg desværre stadig uren og fedtet hud, men denne serum har virkelig hjulpet på det. Efter kun 3 ugers brug, ser jeg tydeligere, glattere og mere frisk hud. Kan varmt anbefales.", "name": "- Lene", "out": "tp2_lene_1.jpg"},
    {"headline": '"Brugt den 1 dag og\nved den er den rigtige."', "quote": "Har brugt den 1 dag og kan mærke at det er den jeg skal bruge fremover.", "name": "- Birthe Klausen", "out": "tp2_birthe_1.jpg"},
    {"headline": '"Fantastisk serum med\nsynlige resultater."', "quote": "Virkelig et fantastisk serum med synlige resultater.", "name": "- Britt", "out": "tp2_britt_2.jpg"},
    {"headline": '"Synlig forskel efter\nkun 1,5 uger."', "quote": "Klart det bedste serum jeg nogensinde har prøvet! Synlig forskel efter kun 1,5 uger!", "name": "- Elisabeth Fossheim", "out": "tp2_elisabeth_1.jpg"},
    {"headline": '"Kæmpe anbefaling\nherfra."', "quote": "Fantastisk produkt, har brugt to flasker og nu bestilt tre. Kæmpe anbefaling herfra.", "name": "- Ferida Sahovic Bilalovic", "out": "tp2_ferida_1.jpg"},
    {"headline": '"Super lækkert produkt."', "quote": "Super lækkert produkt, de bedste anbefalinger herfra.", "name": "- Helle Nielsen", "out": "tp2_helle_nielsen_1.jpg"},
    {"headline": '"Den giver glød, fugt\nog reducerer rynker."', "quote": "Den Serum er bare helt fantastisk! Den giver mit ansigt en dejlig glød, masser af fugt, og reducerer rynker og et dejligt velvære. Jeg anvender den hver eneste morgen og den holder hele dagen. Den fedter ikke, men giver øjeblikkeligt fugt. Jeg kan kun anbefale den.", "name": "- Birgitte Larsen", "out": "tp2_birgitte_larsen_1.jpg"},
    {"headline": '"Min hud stråler."', "quote": "Min hud stråler efter jeg er begyndt at bruge den.", "name": "- Mia Klakstein", "out": "tp2_mia_klakstein_1.jpg"},
    {"headline": '"Jeg er fan\nog fortsætter."', "quote": "Jeg har brugt den i en uge nu og den er super god, kan varmt anbefales - jeg er fan og fortsætter.", "name": "- Lene Mogensen", "out": "tp2_lene_mogensen_1.jpg"},
    {"headline": '"Vil KLART ANBEFALE\ndet til enhver."', "quote": "Elsker dette produkt og vil KLART ANBEFALE det til enhver at prøve.", "name": "- Sanne Kosten-Mortilfire Munch", "out": "tp2_sanne_kosten_1.jpg"},
    {"headline": '"KÆMPE\nanbefaling."', "quote": "Den er så god, har lige bestilt igen i dag. KÆMPE anbefaling.", "name": "- Susanne Thora Nielsen", "out": "tp2_susanne_thora_1.jpg"},
    {"headline": '"Brugt den i 4 mdr.\nog kan kun anbefales."', "quote": "Fantastisk Serum, har brugt den i 4 mdr. nu. Kan kun anbefales.", "name": "- Lene Nielsen", "out": "tp2_lene_nielsen_1.jpg"},
    {"headline": '"Nu bruger jeg kun\ndenne serum."', "quote": "Før brugte jeg serum, natcreme og øjencreme, nu bruger jeg kun denne serum.", "name": "- Lone Mikkelsen", "out": "tp2_lone_mikkelsen_1.jpg"},
    {"headline": '"ELSKER den og vil\nikke undvære den."', "quote": "Virkelig lækker serum, jeg har brugt den i over et halvt år og jeg elsker den. Jeg har tit haft tør hud omkring næsen og i panden, det har jeg ikke mere og så hjælper den på de fine linjer omkring øjnene. ELSKER den og vil ikke undvære den.", "name": "- Lone", "out": "tp2_lone_2.jpg"},
    {"headline": '"Ændret min hud\ntil det bedre."', "quote": "Selv for en bedstemor på 65 år, har den ændret min hud til det bedre.", "name": "- Marina Fehrn", "out": "tp2_marina_1.jpg"},
    {"headline": '"Flot resultat\npå 30 dage."', "quote": "Har brugt den i 30 dage nu og med flot resultat.", "name": "- Tina Andreasen", "out": "tp2_tina_andreasen_1.jpg"},
    {"headline": '"En fuldstændig\nfantastisk ansigtscreme."', "quote": "Det er en fuldstændig fantastisk ansigtscreme.", "name": "- Tanja", "out": "tp2_tanja_1.jpg"},
    {"headline": '"Fin glød og frisk,\nglattere hud."', "quote": "Den giver en fin glød og en frisk og glattere hud.", "name": "- Trine", "out": "tp2_trine_1.jpg"},
    {"headline": '"Kan mærke og se\nforandring i ansigtet."', "quote": "Hvor er det lækkert, kan mærke og se forandring i mit ansigt.", "name": "- Malene Lundfort", "out": "tp2_malene_1.jpg"},
    {"headline": '"Et absolut\nmust have."', "quote": "Jeg har nørdet skønhedsprodukter siden jeg var 14 år - længe før det blev moderne - nu fylder jeg 64 år - og dette produkt er et absolut must have.", "name": "- Marianne Schmidt", "out": "tp2_marianne_schmidt_1.jpg"},
    {"headline": '"Udglatter, opstrammer og\ngør huden fast og blød."', "quote": "Er utrolig glad for min serum, den udglatter og opstrammer og gør huden dejlig fast og blød, rynkerne er meget mindre synlige. Det er fast inventar i min daglige hudpleje.", "name": "- Britt Bente Andreasen", "out": "tp2_britt_bente_2.jpg"},
    {"headline": '"Huden bliver mere blød\nog rynkerne minimeres."', "quote": "Den bedste jeg har prøvet, man kan både se og mærke forskellen. Huden bliver mere blød og glat og rynkerne minimeres.", "name": "- Britt Bente Andreasen", "out": "tp2_britt_bente_3.jpg"},
    {"headline": '"Den første serum jeg\nhar så god effekt med."', "quote": "Jeg har brugt Kjeldgaard nu i et år ca. og det er den første serum jeg har så god effekt med.", "name": "- Pia Kallmeyer", "out": "tp2_pia_kallmeyer_1.jpg"},
    {"headline": '"Super effektiv."', "quote": "Den får fem stjerner af mig. Den er super effektiv.", "name": "- Britt Bente Andreasen", "out": "tp2_britt_bente_4.jpg"},
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

    # Headline (white, top area)
    font_headline = ImageFont.truetype(FONT_BOLD, size=82)
    draw.multiline_text((199, 290), r["headline"], font=font_headline,
                        fill=WHITE, spacing=6, stroke_width=2, stroke_fill=WHITE)

    # Quote inside card (auto-size)
    font_name   = ImageFont.truetype(FONT_REG, size=NAME_SIZE)
    name_h      = draw.textbbox((0, 0), r["name"], font=font_name)[3]
    available_h = CARD_BOTTOM - CARD_TEXT_TOP - name_h - 40

    for size in range(48, 22, -1):
        font_quote = ImageFont.truetype(FONT_REG, size=size)
        spacing = max(8, size // 4)
        wrapped = wrap_text(draw, r["quote"], font_quote, MAX_W)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_quote, spacing=spacing)
        if (bbox[3] - bbox[1]) <= available_h:
            break

    draw.multiline_text((CARD_LEFT, CARD_TEXT_TOP), wrapped, font=font_quote,
                        fill=TEAL_DARK, spacing=spacing)

    bbox = draw.multiline_textbbox((CARD_LEFT, CARD_TEXT_TOP), wrapped,
                                    font=font_quote, spacing=spacing)
    y_name = bbox[3] + 30
    draw.text((CARD_LEFT, y_name), r["name"], font=font_name, fill=TEAL_LIGHT)

    out_path = OUT_DIR / r["out"]
    save_kwargs = {"quality": 100, "subsampling": 0}
    if icc:
        save_kwargs["icc_profile"] = icc
    img.save(out_path, **save_kwargs)
    print(f"Saved: {out_path}")

print(f"\nDone! {len(REVIEWS)} images saved to {OUT_DIR}")
