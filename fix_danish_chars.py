#!/usr/bin/env python3
"""Fix missing Danish characters (æ, ø, å) in all template generator scripts."""
import re
from pathlib import Path

FILES = [
    "generate_template2_all.py",
    "generate_template3_all.py",
    "generate_template4_all.py",
    "generate_template5_all.py",
    "generate_template6_all.py",
    "generate_template7_all.py",
]

# Order matters — longer/more specific replacements first
REPLACEMENTS = [
    # Names
    ("Christel Moker",          "Christel Møker"),
    ("Lene Monsted",            "Lene Mønsted"),
    ("Mia Sorensen",            "Mia Sørensen"),
    ("Jette Gronfeldt",         "Jette Grønfeldt"),

    # Specific words (longest first to avoid partial matches)
    ("skonhedsklinikker",       "skønhedsklinikker"),
    ("laegemiddel",             "lægemiddel"),
    ("jaevnaldrende",           "jævnaldrende"),
    ("fuldstaendig",            "fuldstændig"),
    ("forsaetter",              "fortsætter"),
    ("bekymringsrynker",        "bekymringsrynker"),  # already correct
    ("overflodige",             "overflødige"),
    ("undvaerlig",              "uundværlig"),
    ("Uundvaerlig",             "Uundværlig"),
    ("undvaere",                "undvære"),
    ("afhaengig",               "afhængig"),
    ("vasentlig",               "væsentlig"),
    ("stralende",               "strålende"),
    ("laengere",                "længere"),
    ("naesten",                 "næsten"),
    ("maneder",                 "måneder"),
    ("maerke",                  "mærke"),
    ("maettet",                 "mættet"),
    ("laekkert",                "lækkert"),
    ("Laekkert",                "Lækkert"),
    ("Laekker",                 "Lækker"),
    ("laekker",                 "lækker"),
    ("hjaelper",                "hjælper"),
    ("Hjaelper",                "Hjælper"),
    ("hjaelp",                  "hjælp"),
    ("kragetaer",               "kragetæer"),
    ("kragetær",                "kragetæer"),  # keep correct
    ("overlaben",               "overlæben"),
    ("overflodige",             "overflødige"),
    ("kaempe",                  "kæmpe"),
    ("Kaempe",                  "Kæmpe"),
    ("glaede",                  "glæde"),
    ("silkeblod",               "silkeblød"),
    ("silkeblød",               "silkeblød"),  # keep correct
    ("bladere",                 "blødere"),
    ("blødere",                 "blødere"),    # keep correct
    ("smorer",                  "smører"),
    ("smore",                   "smøre"),
    ("stracker",                "strækker"),
    ("Tranger",                 "Trænger"),
    ("tranger",                 "trænger"),
    ("straler",                 "stråler"),
    ("Straler",                 "Stråler"),
    ("galder",                  "gælder"),
    ("gaet",                    "gået"),
    ("provet",                  "prøvet"),
    ("Provet",                  "Prøvet"),
    ("kobes",                   "købes"),
    ("kobte",                   "købte"),
    ("kobt ",                   "købt "),
    ("laenge",                  "længe"),
    ("nytar",                   "nytår"),
    ("naesen",                  "næsen"),
    ("laegen",                  "lægen"),
    ("rodmen",                  "rødmen"),
    ("Rodmen",                  "Rødmen"),
    ("skon ",                   "skøn "),
    ("male sig",                "måle sig"),
    ("loft og",                 "løft og"),
    ("pa ingen made",           "på ingen måde"),
    ("pa ingen måde",           "på ingen måde"),  # keep correct
    ("ogsa",                    "også"),
    ("ojnene",                  "øjnene"),
    ("ojne",                    "øjne"),
    ("morke",                   "mørke"),
    ("Monsted",                 "Mønsted"),
    ("vaerd",                   "værd"),
    ("Vaerd",                   "Værd"),
    ("foles",                   "føles"),
    ("Foles",                   "Føles"),
    ("gor det",                 "gør det"),
    ("gar mere",                "går mere"),
    ("glod",                    "glød"),
    ("faet",                    "fået"),
    ("faat",                    "fået"),
    ("forste",                  "første"),
    ("Forste",                  "Første"),
    ("Dessuden",                "Desuden"),
    ("maerke",                  "mærke"),

    # "blod" → "blød" carefully (avoid "blodere" which was already caught above)
    ("blod og",                 "blød og"),
    ("blod. ",                  "blød. "),
    ("blod,",                   "blød,"),
    ("blod!",                   "blød!"),
    ("blod\n",                  "blød\n"),
    ("blod halsen",             "blød halsen"),
    ("blod -",                  "blød -"),
    ("baby blod",               "baby blød"),
    ("blod og glat",            "blød og glat"),
    ("blod at smore",           "blød at smøre"),

    # "sma" → "små"
    ("sma fine",                "små fine"),
    ("sma. ",                   "små. "),
    ("sma rynker",              "små rynker"),
    ("sma poser",               "små poser"),
    ("er sma",                  "er små"),

    # "sa" → "så" in common phrases
    ("sa en klar",              "så en klar"),
    ("sa kun",                  "så kun"),
    ("sa tydeligt",             "så tydeligt"),
    ("sa blod",                 "så blød"),
    ("sa paen",                 "så pæn"),
    ("sa dybe",                 "så dybe"),
    ("sa laekkert",             "så lækkert"),
    ("sa store",                "så store"),
    ("sa fin",                  "så fin"),
    ("sa meget",                "så meget"),
    ("sa hjaelper",             "så hjælper"),
    ("sa jeg",                  "så jeg"),
    ("sa det",                  "så det"),
    ("sa virkelig",             "så virkelig"),
    ("Sa en",                   "Så en"),
    ("SA meget",                "SÅ meget"),

    # "pa" → "på" in common phrases
    ("pa min",                  "på min"),
    ("pa mine",                 "på mine"),
    ("pa at",                   "på at"),
    ("pa halsen",               "på halsen"),
    ("pa naese",                "på næse"),
    ("pa naesen",               "på næsen"),
    ("pa kinder",               "på kinder"),
    ("pa skonhedsklinikker",    "på skønhedsklinikker"),
    ("pa et",                   "på et"),
    ("pa ingen",                "på ingen"),
    ("pa mit",                  "på mit"),
    ("pa 68",                   "på 68"),
    ("pa 61",                   "på 61"),
    ("pa solskader",            "på solskader"),

    # "ar" → "år" in context
    ("i mange ar",              "i mange år"),
    ("i 2 ar",                  "i 2 år"),
    ("i et ar",                 "i et år"),
    ("et ar siden",             "et år siden"),
    ("i flere ar",              "i flere år"),
    ("63 ar",                   "63 år"),
    ("71 ar",                   "71 år"),
    ("68 ar",                   "68 år"),
    ("61 ar",                   "61 år"),
    ("60 ar",                   "60 år"),
    ("et halvt ars",            "et halvt års"),
    ("to ar",                   "to år"),
    ("cirka et ar",             "cirka et år"),
    ("et ar og",                "et år og"),
    ("i to ar",                 "i to år"),
    ("i to år",                 "i to år"),  # keep correct
    ("acne ar",                 "acne ar"),  # this "ar" is correct (acne scars)

    # "for" → "før" where it means "before"
    ("For jeg begyndte",        "Før jeg begyndte"),
    ("for jeg begyndte",        "før jeg begyndte"),
    ("haft sa paen en hud for", "haft så pæn en hud før"),
    ("haft sa paen en hud for.", "haft så pæn en hud før."),
    ("hud for.",                "hud før."),
    ("provet for.",             "prøvet før."),
    ("provet for,",             "prøvet før,"),
    ("ikke provet for",         "ikke prøvet før"),
    ("for pa et",               "før på et"),

    # "tor" → "tør"
    ("meget tor",               "meget tør"),
    ("gra og tor",              "grå og tør"),
    ("gra at",                  "grå at"),
    ("gra og",                  "grå og"),
    ("hud gra",                 "hud grå"),
    ("var gra",                 "var grå"),

    # "paen" → "pæn"
    ("paen en hud",             "pæn en hud"),
    ("paen og glat",            "pæn og glat"),

    # Remaining specific fixes
    ("Gronfeldt",               "Grønfeldt"),
    ("maerke",                  "mærke"),
    ("Maerke",                  "Mærke"),
    ("maerket",                 "mærket"),
]

base = Path("/Users/lunahansen/Desktop/Claude ads")

for fname in FILES:
    fpath = base / fname
    text = fpath.read_text(encoding="utf-8")
    original = text
    for wrong, right in REPLACEMENTS:
        text = text.replace(wrong, right)
    if text != original:
        fpath.write_text(text, encoding="utf-8")
        print(f"Fixed: {fname}")
    else:
        print(f"No changes: {fname}")

print("\nDone!")
