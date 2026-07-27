#!/usr/bin/env python3
"""
Vanea Ad Image Generator
Generates 3 ad image concepts using OpenRouter (google/gemini-3.1-flash-image).
"""

import os
import base64
import json
import requests
from pathlib import Path
from datetime import datetime

API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: OPENROUTER_API_KEY not set. Run: export OPENROUTER_API_KEY=your_key")

OUTPUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUTPUT_DIR.mkdir(exist_ok=True)
RUN_STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

MODEL = "google/gemini-3.1-flash-image"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Previous concepts kept for reference — new batch below
AD_CONCEPTS = [
    {
        "name": "diagnosis_kender_du_det",
        "prompt": (
            "Create a square 1080x1080 social media image in the style of a viral wellness post. "
            "BACKGROUND: soft lavender (#E8D5F5). "
            "DECORATIONS: small hand-drawn daisy/flower doodles in each corner — pink, yellow and white flowers, simple and charming. A few small sparkle stars scattered lightly. "
            "NO phone mockups. NO app screenshots. Text only. "
            "HEADLINE at top center in a very large bold rounded black font — this text takes up roughly the top 35% of the image: 'Kender du det her?' "
            "Below the headline, a bullet list in medium-large black text with generous line spacing: "
            "'• Du ved præcis hvad du burde gøre — du gør det bare ikke' "
            "'• Du starter forfra hver mandag' "
            "'• Du har prøvet 5 apps og brugt ingen af dem' "
            "'• Du føler dig skyldig når du springer en dag over' "
            "'• Du ved godt det handler om system — du har bare ikke fundet det endnu' "
            "BOTTOM: small centered text in dark purple: 'Vanea er lavet til det. Find den i App Store.' "
            "Warm pastel feel, hand-drawn doodles, very readable. Square 1080x1080."
        ),
    },
    {
        "name": "psa_starter_forfra",
        "prompt": (
            "Create a square 1080x1080 social media image that looks exactly like an organic text post — NOT an advertisement. "
            "BACKGROUND: clean off-white (#FAFAF8). "
            "NO decorations. NO images. NO phone mockups. Pure text on plain background. "
            "TOP LEFT: small bold text 'PSA 📢' "
            "Below that, large bold black text taking up about 30% of the image: 'Kære dig der altid starter forfra:' "
            "Below that, medium-sized black regular text with comfortable line spacing: "
            "'At have svært ved at holde gode vaner er ikke et spørgsmål om viljestyrke.' "
            "'' "
            "'Det er et spørgsmål om system.' "
            "'' "
            "'Vanea giver dig overblikket og strukturen — så du ikke starter forfra næste mandag.' "
            "'Du tilføjer dine vaner, sætter en daglig påmindelse og kan følge din fremgang dag for dag.' "
            "'' "
            "'Det er det hele.' "
            "BOTTOM: small text: 'Find Vanea i App Store' "
            "Minimal, authentic, like a real post. Black text on off-white. Square 1080x1080."
        ),
    },
    {
        "name": "twitter_udmattet_foer_efter",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. "
            "NO phone frame. The tweet fills the entire square. "
            "Profile: small round gray circle for profile photo. Name: 'Maja K.' in white bold. Handle: '@majak' in gray. "
            "Tweet text in white Twitter-style font, medium size, with generous empty lines between each paragraph so it is very easy to read: "
            "'Jeg gik fra at være konstant udmattet til at have mere overskud end nogensinde før\\n\\n"
            "Før\\n"
            "• Udsætter alt og falder ned i et hul\\n"
            "• Bliver overvældet af selv de mindste ting\\n"
            "• Planlægger den perfekte rutine — men starter aldrig\\n\\n"
            "Efter\\n"
            "• Holder hjemmet ryddeligt uden at tænke over det\\n"
            "• Starter dagen roligt i stedet for stresset\\n"
            "• Har faktisk lyst til at komme ud og se folk\\n\\n"
            "Vanea hjælper dig med at bygge de vaner du vil have — og holde dig til dem.\\n"
            "Du tilføjer dem selv, krydser af hver dag og følger dine streaks.\\n\\n"
            "Jeg begyndte at bruge appen for 2 måneder siden og jeg har aldrig haft så meget overskud.' "
            "Below tweet: realistic gray Twitter engagement icons (comment, retweet, like, share) with small numbers. "
            "Looks 100% like a real organic tweet. Square 1080x1080."
        ),
    },
    {
        "name": "twitter_sofie_dopamin",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. "
            "NO phone frame. The tweet fills the entire square. "
            "Profile: small round gray circle for profile photo. Name: 'Sofie M.' in white bold with a small blue verified checkmark. Handle: '@sofiem' in gray. "
            "Tweet text in white Twitter-style font, medium size, with generous spacing between each paragraph so it is easy to read: "
            "'Til alle der altid har gode intentioner men aldrig holder ved:\\n\\n"
            "Prokrastinering og handlingslammelse er ikke dovenskab.\\n"
            "Det er din hjerne der mangler dopamin til at gøre de ting du faktisk gerne vil.\\n\\n"
            "Denne app er lavet til at ændre det – du tilføjer selv dine vaner, krydser af hver dag og følger dine streaks.\\n"
            "På den måde får din hjerne dopamin for de ting der faktisk gør dig glad.\\n\\n"
            "Og det bedste? Du kan prøve den helt gratis.' "
            "Below tweet: realistic gray Twitter engagement icons (comment, retweet, like, share) with small numbers. "
            "Looks 100% like a real organic tweet. Square 1080x1080."
        ),
    },
    {
        "name": "twitter_maja_vaner",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. "
            "NO phone frame. The tweet fills the entire square. "
            "Profile: small round gray circle for profile photo. Name: 'Maja K.' in white bold. Handle: '@majak' in gray. "
            "Tweet text in white Twitter-style font, medium size: "
            "'Til jer der altid har de bedste intentioner, men aldrig rigtigt holder ved:\\n\\n"
            "Det er ikke fordi I er dovne. Det er fordi I mangler et system.\\n\\n"
            "Jeg fandt en app der hedder Vanea – en slags daglig planlægger.\\n\\n"
            "Du tilføjer dine opgaver og sætter kryds hver dag.\\n\\n"
            "Uge 1: jeg gennemførte alle mine opgaver 4 ud af 7 dage. Rekord for mig.\\n"
            "Uge 3: jeg har ikke misset én eneste dag.\\n\\n"
            "Jeg ville ønske jeg havde fundet den tidligere.' "
            "Below tweet: realistic gray Twitter icons for comment, retweet, like, share. "
            "Looks 100% like a real organic tweet. Square 1080x1080."
        ),
    },
    {
        "name": "notes_story_aldrig_holdt_vane",
        "prompt": (
            "Create a square 1080x1080 image in the style of a LinkedIn or Facebook personal story post. "
            "BACKGROUND: pure white. "
            "NO phone frame. NO decorations. Text only, filling the image comfortably. "
            "HEADLINE at the top in a very large bold black serif font, taking up the top 38% of the image, three lines: "
            "'Jeg har aldrig kunnet holde\\nen god vane i mere\\nend to uger.' "
            "Below the headline, medium-sized regular black text with generous spacing between each paragraph — lots of white space so it feels effortless to read: "
            "'Jeg prøvede kalendere, påmindelser og dagbøger. Intet virkede.' "
            "[large empty line] "
            "'Så prøvede jeg Vanea.' "
            "[large empty line] "
            "'Uge 1: Gennemførte alle de opgaver jeg havde sat mig 4 ud af 7 dage. Rekord.' "
            "'Uge 2: 6 ud af 7.' "
            "'Uge 4: Ikke misset én eneste dag.' "
            "[large empty line] "
            "'Jeg ville ønske jeg havde fundet den tidligere.' "
            "NO bottom CTA text. End the image after the last line. "
            "Clean, authentic, story-driven. No decorations. Square 1080x1080."
        ),
    },
    {
        "name": "challenge_14dages_bevaegelse",
        "prompt": (
            "Create a square 1080x1080 image in the style of a phone Notes app screenshot. "
            "BACKGROUND: white, like an iPhone Notes page. "
            "TOP: small gray status bar UI (time '11:11', signal icons) to look like a phone Notes screenshot. "
            "Below: a simple Notes-style header with back arrow '< All iCloud' and a small smiley icon. "
            "NO phone frame around it — just the content fills the square. "
            "HEADLINE in very large bold black text: '14-dages Bevægelsesudfordring 🏃' "
            "Subtitle in medium text: 'Bevæg dig i mindst 20 minutter hver dag' "
            "Below, a numbered list in regular black text: "
            "'dag 1: en tur på 20 minutter — det er nok' "
            "'dag 2: dans, gå, løb — bare bevæg dig' "
            "'dag 3: registrer dit humør i Vanea — mærk forskel allerede nu' "
            "'dag 4: sæt en fast tid du bevæger dig' "
            "'dag 5: tag trappen i stedet for elevatoren' "
            "'dag 6: 20 min frisk luft — ingen undskyldninger' "
            "'dag 7: du er halvvejs — tjek din streak i Vanea 🔥' "
            "'dag 8-14: hold det kørende. Hver dag tæller.' "
            "BOTTOM bold text: 'Vanea holder styr på det for dig. Er du med?' "
            "Small cute penguin or bird doodle illustration in one corner — simple and charming. "
            "Authentic Notes app feel. Square 1080x1080."
        ),
    },
    {
        "name": "before_after_udmattet",
        "prompt": (
            "Create a square 1080x1080 social media image in a retro style, closely modelled on the 'I went from bed rotting to that girl' ad format. "
            "BACKGROUND: warm cream/off-white (#F5F0E8). "
            "BORDER: thick decorative tiled border all the way around — colorful retro tiles in red, orange, yellow, green, blue with small circular eye/target motifs in the corners, exactly like a retro mosaic frame. About 70px wide. "
            "BOTTOM INTERIOR: a retro red-and-white checkered floor pattern at the very bottom of the inner area, like a vintage diner floor. "
            "NO phone mockups. "
            "HEADLINE at the top of the inner area in very large bold purple/dark purple serif font, two lines: "
            "'Jeg gik fra at være konstant udmattet\\ntil at have mere overskud end nogensinde før' "
            "Below the headline: two columns side by side. "
            "LEFT COLUMN: handwritten-style italic label 'Før' at the top. Simple illustrated sad drooping skeleton figure. Below the figure, bullet points in small black handwritten-style font: "
            "'• Udsætter alt og falder ned i et hul' "
            "'• Bliver overvældet af selv de mindste ting' "
            "'• Planlægger den perfekte rutine — men starter aldrig' "
            "RIGHT COLUMN: handwritten-style italic label 'Efter' at the top. Simple illustrated upright confident skeleton figure holding a broom. Below the figure, bullet points in small black handwritten-style font: "
            "'• Holder hjemmet ryddeligt uden at tænke over det' "
            "'• Starter dagen roligt i stedet for stresset' "
            "'• Har faktisk lyst til at komme ud og se folk' "
            "BOTTOM TEXT (above the checkered floor): centered bold dark text: "
            "'Vanea hjælper dig med at bygge de vaner du vil have — og holde dig til dem.\\nDu tilføjer dem selv, krydser af hver dag og følger dine streaks.' "
            "Below that, centered italic text: 'Jeg begyndte at bruge appen for 2 måneder siden og jeg har aldrig haft så meget overskud.' "
            "Retro warm palette. Charming illustrated style. Square 1080x1080."
        ),
    },
    {
        "name": "before_after_mandag",
        "prompt": (
            "Create a square 1080x1080 social media image in a retro 70s style. "
            "BACKGROUND: warm cream (#FDF6E3). "
            "BORDER: thick rainbow checkered border all the way around — small alternating squares in red, orange, yellow, green, blue, purple. About 55px wide. "
            "NO phone mockups. Text and simple hand-drawn stick figures only. "
            "HEADLINE centered near top in enormous bold retro display font, dark brown, taking up top 38% of the inner image, two lines: "
            "'Fra jeg starter på mandag\\ntil jeg gør det i dag' "
            "BELOW: two equal columns. "
            "LEFT column: bold 'FØR' label. Simple sad drooping stick figure with frown. Small italic text: 'Gode intentioner. Ingen system. Starter forfra hver uge.' "
            "RIGHT column: bold 'EFTER' label. Simple happy upright stick figure with smile and small star. Small italic text: 'Følger sine vaner. Ser fremgangen. Føler sig i kontrol.' "
            "BOTTOM: very small centered muted text: 'Vanea — prøv 7 dage gratis med årsabonnement' "
            "Retro warm palette: mustard, terracotta, olive, cream. Square 1080x1080."
        ),
    },
    {
        "name": "gentle_reminder_baggrund",
        "prompt": (
            "Create a square 1080x1080 social media image in the style of a 'gentle reminder' post. "
            "BACKGROUND: a soft blurred warm photo — a cozy morning scene with soft morning light, slightly out of focus, very warm and gentle. The photo should be subtle and not distract from the text. "
            "NO phone mockups. "
            "Large white text centered in the middle of the image with a soft dark overlay behind it for readability: "
            "First line in medium white italic: 'Påmindelse:' "
            "Below in large bold white text: 'At ville leve sundere kræver ikke perfekt viljestyrke.' "
            "Below in medium white regular text: 'Det kræver en plan du faktisk kan følge.' "
            "Below in medium white text: 'Vanea hjælper dig med det — én dag ad gangen.' "
            "BOTTOM small white text: 'Find Vanea i App Store' "
            "Soft, warm, empathetic feel. Text is the focus. Square 1080x1080."
        ),
    },
    {
        "name": "bold_psa_viljestyrke",
        "prompt": (
            "Create a square 1080x1080 social media image with bold minimal typography — like a powerful poster. "
            "BACKGROUND: pure white. "
            "NO images. NO decorations. NO phone mockups. Just bold text. "
            "Center of image: enormous bold black text, taking up most of the image, left-aligned or centered, with dramatic line breaks: "
            "'Det er\\nikke\\ndovenskab.' "
            "Below that, slightly smaller but still large bold black text: "
            "'Det er et\\nmanglende\\nsystem.' "
            "Below that, a thin horizontal line. "
            "Below the line, medium regular black text: 'Vanea giver dig systemet.' "
            "BOTTOM small gray text: 'Find Vanea i App Store — til iPhone' "
            "Extremely minimal. Black on white. Typography-driven. Powerful and direct. Square 1080x1080."
        ),
    },
    {
        "name": "challenge_cta_morgenrutine",
        "prompt": (
            "Create a square 1080x1080 social media image with a dark background and bold white text — like a viral challenge post. "
            "BACKGROUND: very dark navy blue (#0D1B2A) or near-black. "
            "Subtle texture: faint hand-drawn white squiggly lines and small asterisks scattered across the dark background — light and not distracting. "
            "NO phone mockups. "
            "TOP: medium white text, slightly italic or handwritten style: 'Til alle der altid siger' "
            "Below that, very large bold white text: '\"jeg starter på mandag\"' "
            "Below that, a gap, then medium white regular text: "
            "'På mandag starter vi 30-dages Morgenrutine-udfordringen med Vanea.' "
            "'' "
            "'Dag 2: du stresser ikke om morgenen.' "
            "'Dag 7: du mærker allerede forskellen.' "
            "'Dag 30: din morgen er ikke til at kende igen.' "
            "Bottom bold large white text: 'Er du med? 👇' "
            "Small text below: 'Find Vanea i App Store' "
            "Dark, bold, energetic. High contrast white on dark. Square 1080x1080."
        ),
    },
    {
        "name": "template_ugeoversigt",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style weekly planner template card. "
            "NO phone mockups. NO app screenshots. Pure graphic design. "
            "BACKGROUND: warm peach/coral (#FFD4B2). "
            "Decorations: small hand-drawn sun, star and heart doodles in corners and scattered lightly — cheerful and warm. "
            "TITLE at top center in large bold black rounded font: 'Din uge med Vanea 📅' "
            "Subtitle: 'Sæt kryds. Mærk fremgangen.' "
            "Below: a 7-row layout, one row per weekday. Each row has the day name bold on the left and a habit suggestion on the right: "
            "'Mandag — Drik 2 liter vand' "
            "'Tirsdag — 20 min bevægelse' "
            "'Onsdag — Læs 15 minutter' "
            "'Torsdag — Ingen skærm efter kl. 21' "
            "'Fredag — Ryd op i ét rum' "
            "'Lørdag — Skriv 3 ting du er taknemmelig for' "
            "'Søndag — Planlæg næste uge i Vanea' "
            "BOTTOM: small centered black text: 'Tilpas dine egne vaner i Vanea — find den i App Store' "
            "Colorful, structured, Pinterest-saveable. Square 1080x1080."
        ),
    },
]

# --- 10 NEW CONCEPTS (June 2026 batch) ---
NEW_CONCEPTS = [
    {
        "name": "psa_halvfaerdige_planer",
        "prompt": (
            "Create a square 1080x1080 social media image that looks exactly like an organic text post — NOT an advertisement. "
            "BACKGROUND: clean off-white (#FAFAF8). NO decorations. NO images. NO phone mockups. Pure text on plain background. "
            "TOP LEFT: small bold text 'PSA 📢' "
            "Below that, large bold black text: 'Til dig med for mange halvfærdige planer:' "
            "Below that, medium black text with comfortable line spacing: "
            "'Du har sikkert prøvet at starte forfra mange gange.\\n"
            "Ny uge, ny plan, nyt forsæt.\\n\\n"
            "Det er ikke fordi du er doven.\\n"
            "Det er fordi du mangler et system der faktisk passer til dig.\\n\\n"
            "Vanea er en simpel vanesporing-app til iPhone.\\n"
            "Du tilføjer dine vaner, sætter kryds hver dag og følger din fremgang.\\n\\n"
            "Det er det hele.' "
            "BOTTOM: small text: 'Find Vanea i App Store' "
            "Minimal, authentic, like a real post. Black text on off-white. Square 1080x1080."
        ),
    },
    {
        "name": "twitter_kl_2247",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. NO phone frame. Tweet fills the entire square. "
            "Profile: small round gray circle for profile photo. Name: 'Emma J.' in white bold. Handle: '@emmaj' in gray. "
            "Tweet text in white Twitter-style font, medium size, with generous spacing between paragraphs: "
            "'Kl. 22.47\\n\\n"
            "Du ved du burde sove.\\n"
            "Men du scroller videre.\\n\\n"
            "Og i morgen tidlig starter det hele forfra:\\n"
            "Træt. Bagud. Dårlig samvittighed.\\n\\n"
            "Jeg fandt en app der hedder Vanea.\\n"
            "Du tilføjer de vaner du gerne vil have — og sætter kryds hver dag.\\n\\n"
            "Efter 3 uger:\\n"
            "• Jeg er i seng inden kl. 23 næsten hver aften\\n"
            "• Jeg vågner ikke længere med dårlig samvittighed\\n"
            "• Jeg har mere energi end jeg har haft i årevis\\n\\n"
            "Jeg ville ønske jeg havde fundet den tidligere.' "
            "Below tweet: realistic gray Twitter engagement icons (comment, retweet, like, share) with small numbers. "
            "Looks 100% like a real organic tweet. Square 1080x1080."
        ),
    },
    {
        "name": "notes_fra_rod_til_orden",
        "prompt": (
            "Create a square 1080x1080 image in the style of a LinkedIn or Facebook personal story post. "
            "BACKGROUND: pure white. NO phone frame. NO decorations. Text only, filling the image comfortably. "
            "HEADLINE at the top in a very large bold black font, taking up the top 35% of the image, two lines: "
            "'Fra rod til orden —\\nSådan skete det.' "
            "Below the headline, medium-sized regular black text — VERY generous spacing between every single paragraph, almost double line spacing, so it is effortless to read: "
            "'Mit hjem var altid rodet.\\n"
            "Ikke fordi jeg var ligeglad — men fordi jeg aldrig vidste hvor jeg skulle starte.\\n\\n\\n"
            "Så prøvede jeg at give mig selv ét lille mål ad gangen med Vanea.\\n\\n\\n"
            "Uge 1: Ryd op i køkkenet inden sengetid. Klarede det 5 ud af 7 dage.\\n\\n"
            "Uge 2: Sæt en vask over om dagen. Klarede det næsten hver dag.\\n\\n"
            "Uge 4: Jeg kan slet ikke genkende mit hjem.\\n\\n\\n"
            "Det er ikke magi. Det er bare et system der virker.' "
            "NO bottom CTA text. End after last line. Clean, authentic. Square 1080x1080."
        ),
    },
    {
        "name": "before_after_aften_morgen",
        "prompt": (
            "Create a square 1080x1080 social media image in a retro style, modelled on the 'I went from bed rotting to that girl' ad format. "
            "BACKGROUND: warm cream/off-white (#F5F0E8). "
            "BORDER: thick decorative tiled border all around — colorful retro tiles in red, orange, yellow, green, blue with circular motifs in corners. About 70px wide. "
            "BOTTOM INTERIOR: a retro red-and-white checkered floor pattern at the very bottom of the inner area. "
            "NO phone mockups. "
            "HEADLINE at the top of inner area in very large bold dark purple font, two lines: "
            "'Fra stressede aftener og tunge morgener\\ntil ro og overskud hver dag' "
            "Below: two columns side by side. "
            "LEFT COLUMN: handwritten-style italic label 'Aften — FØR' at top. Simple sad drooping illustrated figure. Bullet points in small handwritten-style font: "
            "'• Scroller til kl. 01 om natten\\n"
            "• Vågner og hader at stå op\\n"
            "• Starter dagen bagud og stresset' "
            "RIGHT COLUMN: handwritten-style italic label 'Morgen — EFTER' at top. Simple happy confident illustrated figure. Bullet points: "
            "'• I seng inden kl. 23 næsten hver aften\\n"
            "• Vågner uden alarmen\\n"
            "• Starter dagen roligt og med overskud' "
            "BOTTOM TEXT centered bold dark: 'Vanea hjælper dig med at bygge de vaner du vil have — én dag ad gangen.' "
            "Retro warm palette. Charming illustrated style. Square 1080x1080."
        ),
    },
    {
        "name": "diagnosis_traet_hver_dag",
        "prompt": (
            "Create a square 1080x1080 social media image in the style of a viral wellness post. "
            "BACKGROUND: soft warm yellow (#FFF4CC). "
            "DECORATIONS: small hand-drawn sun, star and flower doodles in each corner. A few small sparkle dots scattered lightly. NO phone mockups. Text only. "
            "HEADLINE at top center in very large bold rounded black font, top 35% of image: 'Er du også altid træt?' "
            "Below, a bullet list in medium-large black text with generous line spacing: "
            "'• Du sover nok — men vågner stadig udmattet\\n"
            "• Du vil gerne motionere, men det bliver ved intentionen\\n"
            "• Du siger 'jeg starter på mandag' — og mandag kommer aldrig\\n"
            "• Du har prøvet at ændre vaner, men giver op efter en uge\\n"
            "• Du ved godt hvad du burde gøre — du gør det bare ikke' "
            "BOTTOM: small centered text in dark brown: 'Vanea er lavet til det. Find den i App Store.' "
            "Warm pastel feel, hand-drawn doodles, very readable. Square 1080x1080."
        ),
    },
    {
        "name": "template_morgenrutine_kort",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style daily routine template card. "
            "NO phone mockups. NO app screenshots. Pure graphic design. "
            "BACKGROUND: soft dusty rose/pink (#F4C2C2). "
            "Decorations: small hand-drawn hearts, stars and simple flower doodles in corners — cheerful and feminine. "
            "TITLE at top center in large bold black rounded font: 'En rolig morgen starter aftenen før ☀️' "
            "Below: a numbered list of simple habits, each on its own row with generous spacing: "
            "'1. Læg telefonen fra dig kl. 22.30\\n"
            "2. Læs 10 minutter inden du sover\\n"
            "3. Stå op samme tid hver dag\\n"
            "4. Drik et glas vand inden kaffen\\n"
            "5. Skriv 3 ting du vil nå i dag\\n"
            "6. 10 minutters frisk luft inden middag' "
            "BOTTOM: small centered black text: 'Følg dine egne morgenrutiner i Vanea — find den i App Store' "
            "Colorful, structured, Pinterest-saveable. Square 1080x1080."
        ),
    },
    {
        "name": "challenge_7_dages_oprydning",
        "prompt": (
            "Create a square 1080x1080 image in the style of a phone Notes app screenshot. "
            "BACKGROUND: white, like an iPhone Notes page. "
            "TOP: small gray status bar UI (time '11:11', signal icons). Below: simple Notes-style header '< All iCloud'. "
            "NO phone frame — content fills the square. "
            "HEADLINE in very large bold black text: '7 dages oprydning 🧹' "
            "Subtitle in medium text: 'Ét rum ad gangen — du kan sagtens' "
            "Below, a numbered list in regular black text: "
            "'dag 1: ryd af køkkenbordet og vask op\\n"
            "dag 2: gå badeværelset igennem\\n"
            "dag 3: sorter tøj — behold, donér eller smid ud\\n"
            "dag 4: støvsug hele lejligheden\\n"
            "dag 5: ryd skuffer og hylder i stuen\\n"
            "dag 6: rens køleskabet og fyld op\\n"
            "dag 7: nyd et rent hjem — sæt kryds i Vanea 🏡' "
            "BOTTOM bold text: 'Vanea holder styr på det for dig. Er du med?' "
            "Authentic Notes app feel. No phone frame. Square 1080x1080."
        ),
    },
    {
        "name": "baggrund_ikke_din_skyld",
        "prompt": (
            "Create a square 1080x1080 social media image. "
            "BACKGROUND: a soft blurred warm photo of a cozy living room with morning light coming through curtains — very soft and out of focus, warm amber tones. The photo is subtle and does not distract from text. "
            "NO phone mockups. "
            "A soft semi-transparent dark overlay covers the center third of the image for text readability. "
            "Large white text centered in the middle: "
            "First line in medium white italic: 'Husk:' "
            "Below in large bold white text: 'Det er ikke fordi du er doven.' "
            "Below in medium white regular text: 'Det er fordi du aldrig fik et system der passede til dig.' "
            "Below a thin white divider line, then: 'Vanea giver dig systemet — du bestemmer vanerne.' "
            "BOTTOM small white text: 'Find Vanea i App Store' "
            "Soft, warm, empathetic. Text is the clear focus. Square 1080x1080."
        ),
    },
    {
        "name": "twitter_mit_hjem_rodet",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. NO phone frame. Tweet fills the entire square. "
            "Profile: small round gray circle for profile photo. Name: 'Ellie P.' in white bold with small blue verified checkmark. Handle: '@elliep' in gray. "
            "Tweet text in white Twitter-style font, medium size, with generous spacing between paragraphs: "
            "'Mit hjem var altid rodet og jeg var altid i dårligt humør.\\n\\n"
            "Jeg vidste godt hvad jeg burde gøre — jeg bare aldrig fik gjort det.\\n\\n"
            "Så prøvede jeg Vanea. En simpel app hvor du tilføjer dine vaner og sætter kryds hver dag.\\n\\n"
            "Uge 1: Ryddede op i køkkenet 5 ud af 7 dage. Det er rekord for mig.\\n"
            "Uge 3: Jeg har ikke misset én eneste dag.\\n\\n"
            "Mit hjem er ikke til at kende igen.\\n\\n"
            "Jeg ville ønske jeg havde fundet den tidligere.' "
            "Below tweet: realistic gray Twitter engagement icons with small numbers. "
            "Looks 100% like a real organic tweet. Square 1080x1080."
        ),
    },
    {
        "name": "bold_ikke_viljestyrke",
        "prompt": (
            "Create a square 1080x1080 social media image with bold minimal typography — like a powerful poster. "
            "BACKGROUND: pure white. NO images. NO decorations. NO phone mockups. Just bold text. "
            "Center of image: enormous bold black text, left-aligned with good margins, dramatic line breaks: "
            "'Det handler\\nikke om\\nviljestyrke.' "
            "Below that, slightly smaller but still large bold black text: "
            "'Det handler\\nom et system\\nder virker.' "
            "Below that, a thin horizontal black line. "
            "Below the line, medium regular black text: 'Vanea giver dig systemet.' "
            "BOTTOM small gray text: 'Find Vanea i App Store — til iPhone' "
            "Extremely minimal. Black on white. Typography-driven. Powerful and direct. Square 1080x1080."
        ),
    },
]

# --- JUNE 2026 BATCH 2: 5 Templates + 5 Background with text ---
BATCH2_CONCEPTS = [
    {
        "name": "template_aftenrutine",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style routine template card. "
            "NO phone mockups. NO app screenshots. Pure graphic design. "
            "BACKGROUND: soft pink-to-purple gradient (#FFB6C1 to #C9A0DC). "
            "Decorations: small hand-drawn moon, star and cloud doodles scattered lightly in corners and background — charming and feminine. "
            "TITLE at top center in very large bold black rounded font, taking up top 25% of image: 'Din aftenrutine der giver dig en bedre morgen 🌙' "
            "Below the title: five time-blocked rows, each in its own soft colored pill/rounded rectangle, alternating pastel colors (pink, lavender, peach, mint, lilac). "
            "Each row has a time on the left in bold and a habit on the right: "
            "'kl. 21:00 — Ingen skærm fra nu af' "
            "'kl. 21:15 — Ryd af køkkenbordet' "
            "'kl. 21:30 — Forbered tøj til i morgen' "
            "'kl. 22:00 — Læs 10 minutter' "
            "'kl. 22:30 — Sluk lyset' "
            "BOTTOM: small centered black text: 'Spor dine aftenvaner i Vanea — find den i App Store' "
            "Colorful, structured, very Pinterest-saveable. Large text, easy to read. Square 1080x1080."
        ),
    },
    {
        "name": "template_7dage_rent_hjem",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style weekly challenge card. "
            "NO phone mockups. Pure graphic design. "
            "BACKGROUND: clean warm white (#FFFDF8). "
            "BORDER: thin decorative border in dusty rose/terracotta around the whole image. "
            "Decorations: small hand-drawn cleaning and home icons (broom, plant, heart) in corners — simple and charming. "
            "TITLE at top in very large bold black font: '7 dage til et rent hjem' "
            "Subtitle in medium italic: '— ét rum ad gangen —' "
            "Below: seven rows, one per day, each with a bold day label and a task: "
            "'Dag 1 — Ryd køkkenbordet og vask op' "
            "'Dag 2 — Gå badeværelset igennem' "
            "'Dag 3 — Sorter tøj: behold, donér, smid ud' "
            "'Dag 4 — Støvsug hele hjemmet' "
            "'Dag 5 — Rens køleskabet' "
            "'Dag 6 — Tør støv af og skift sengetøj' "
            "'Dag 7 — Nyd et rent hjem ✨' "
            "BOTTOM: small text centered: 'Sæt kryds i Vanea — find den i App Store' "
            "Clean, structured, saveable. Square 1080x1080."
        ),
    },
    {
        "name": "template_5_vaner",
        "prompt": (
            "Create a square 1080x1080 bold social media graphic — modelled on a viral '5 things' list post. "
            "NO phone mockups. Pure graphic design. "
            "BACKGROUND: very dark navy blue (#0D1B2A), almost black. "
            "Decorations: faint subtle hand-drawn white asterisks and small dots scattered on the dark background — light and not distracting. "
            "TOP: large bold white text centered: '5 vaner der ændrer din uge' "
            "Below: five numbered items in white, each on its own line with generous spacing, bold number followed by regular text: "
            "'1. Ryd af én flade inden du går i seng' "
            "'2. Drik et glas vand inden kaffen' "
            "'3. Bevæg dig i mindst 20 minutter' "
            "'4. Læg telefonen fra dig kl. 22' "
            "'5. Planlæg næste dag inden du sover' "
            "BOTTOM: large bold white text: 'Er du med? 👇' "
            "Below that, small white text: 'Hold styr på dine vaner i Vanea — find den i App Store' "
            "High contrast, dark and bold, scroll-stopping. Square 1080x1080."
        ),
    },
    {
        "name": "template_overvaeldet",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style wellness tip card. "
            "NO phone mockups. Pure graphic design. "
            "BACKGROUND: soft lilac/lavender (#E8D5F5). "
            "Decorations: small hand-drawn flowers, hearts and sparkle stars in corners and scattered lightly. "
            "TITLE at top in large bold black rounded font, taking up top 30% of image: 'Hvad gør du når du vågner og føler dig overvældet?' "
            "Below the title: a bullet list in medium-large black text with generous line spacing: "
            "'💜 Bliv liggende i 2 minutter — ånd roligt' "
            "'💜 Drik et glas vand inden du kigger på telefonen' "
            "'💜 Vælg ÉN ting du vil nå i dag — ikke ti' "
            "'💜 Åbn Vanea og sæt kryds på det du allerede har gjort' "
            "'💜 Gå udenfor i 10 minutter inden middag' "
            "BOTTOM: small centered dark purple text: 'Vanea hjælper dig med at holde overblikket — find den i App Store' "
            "Soft, warm, empathetic. Easy to read. Square 1080x1080."
        ),
    },
    {
        "name": "template_uge_med_vanea",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style weekly habit planner card. "
            "NO phone mockups. Pure graphic design. "
            "BACKGROUND: warm peach/coral (#FFDAB9). "
            "Decorations: small hand-drawn sun, star and heart doodles in all four corners. "
            "TITLE at top center in large bold black font: 'En uge med Vanea ✅' "
            "Subtitle in medium italic black: '— ét kryds ad gangen —' "
            "Below: a 7-row grid, one row per weekday. Each row has the day name bold on the left and a habit suggestion in regular text on the right: "
            "'Mandag — Drik 2 liter vand' "
            "'Tirsdag — 20 min bevægelse' "
            "'Onsdag — Ingen skærm efter kl. 21' "
            "'Torsdag — Læs 15 minutter inden sengetid' "
            "'Fredag — Ryd op i ét rum' "
            "'Lørdag — Skriv 3 ting du er taknemmelig for' "
            "'Søndag — Planlæg den kommende uge' "
            "BOTTOM: small centered black text: 'Tilpas dine egne vaner i Vanea — find den i App Store' "
            "Colorful, structured, Pinterest-saveable. Square 1080x1080."
        ),
    },
    {
        "name": "baggrund_handskrevet_veninde",
        "prompt": (
            "Create a square 1080x1080 image that looks exactly like a handwritten personal note on aged cream/off-white paper. "
            "BACKGROUND: warm aged paper texture — cream/slightly yellowed, with subtle paper grain and slight creases. Like a real torn notebook page. "
            "NO phone frame. No decorations. Just handwriting on paper. "
            "The entire image is filled with handwritten text in a natural, slightly imperfect handwriting style — mix of black pen and some words underlined or circled in blue or red pen for emphasis: "
            "'Min veninde spurgte hvordan jeg pludselig havde fået styr på mit hjem og mit liv.' "
            "[line break] "
            "'Jeg fortalte hende om Vanea.' "
            "[line break] "
            "'En simpel app til iPhone hvor du tilføjer dine vaner og sætter kryds hver dag.' "
            "[line break] "
            "'Det lyder kedeligt.' "
            "'Det virker ikke kedeligt.' "
            "[line break] "
            "'Nu har jeg ikke misset én eneste dag i tre uger.' "
            "The word 'Vanea' should be underlined or circled for emphasis. "
            "Text fills the page naturally, slight angle as if really handwritten. Very authentic. Square 1080x1080."
        ),
    },
    {
        "name": "baggrund_illustration_psa",
        "prompt": (
            "Create a square 1080x1080 image with a busy, colorful illustrated background covered in cute hand-drawn animals, flowers and doodles (dogs, cats, birds, plants, stars) in bright cheerful colors. "
            "Over the illustrated background, a white semi-transparent text box in the center of the image contains the following text in black: "
            "Large bold title: 'Til dig der altid giver op efter en uge:' "
            "Below in medium regular text: "
            "'Det er ikke dig der er forkert.' "
            "[line break] "
            "'Det er systemet du prøver at bruge.' "
            "[line break] "
            "'Vanea er bygget til dig der har prøvet det mange gange.' "
            "'Du tilføjer dine egne vaner, sætter kryds hver dag og følger din fremgang.' "
            "[line break] "
            "'Uden krav. Uden perfektionisme. Bare ét kryds ad gangen.' "
            "The white text box has slightly rounded corners and soft drop shadow. "
            "Colorful, charming, stops the scroll. Square 1080x1080."
        ),
    },
    {
        "name": "baggrund_beton_prokrastinering",
        "prompt": (
            "Create a square 1080x1080 image with a dark gritty urban concrete texture as the background — like a subway wall or a rough concrete pillar, dark gray/charcoal. "
            "NO phone mockups. "
            "On the concrete background, bold white stencil-style text, left-aligned with generous margins: "
            "Very large bold caps text taking up most of the image: "
            "'PROKRASTI-\\nNERING ER\\nIKKE\\nDOVENSKAB.' "
            "Below that, slightly smaller but still large bold white text: "
            "'DET ER DIN\\nHJERNE DER\\nMANGLER EN\\nSTRUKTUR.' "
            "Below that, a thin white horizontal line. "
            "Below the line, medium white text: 'Vanea giver dig strukturen.' "
            "Very small white text at bottom: 'Find Vanea i App Store' "
            "Gritty, powerful, raw. High contrast white on dark concrete. Square 1080x1080."
        ),
    },
    {
        "name": "baggrund_blid_paamindelse",
        "prompt": (
            "Create a square 1080x1080 image with a soft blurred warm portrait photo as background — a young woman with soft morning light on her face, very slightly out of focus, warm golden tones. The photo feels gentle and relatable, not glamorous. "
            "Over the photo, a semi-transparent frosted white overlay covers the middle portion of the image for text readability — like a frosted glass panel. "
            "On the frosted panel, dark text centered: "
            "Small italic text: 'En blid påmindelse til dig:' "
            "Large bold dark text: 'Du behøver ikke ændre alt på én gang.' "
            "Below in medium regular text: "
            "'Begynd med én ting.' "
            "'Sæt kryds i Vanea.' "
            "'Gør det igen i morgen.' "
            "Small text at bottom of panel: 'Find Vanea i App Store' "
            "Soft, warm, empathetic. Feels personal and real. Square 1080x1080."
        ),
    },
    {
        "name": "baggrund_mork_bekendt",
        "prompt": (
            "Create a square 1080x1080 image with a dark atmospheric background — deep dark purple/navy blue, slightly textured, with a very subtle soft blur suggesting a night-time indoor scene. Moody and intimate. "
            "NO phone mockups. "
            "White text centered in the image, generous line spacing, intimate confessional style — like a real personal post: "
            "'Jeg har ikke altid haft styr på tingene.' "
            "[large line break] "
            "'Mit hjem var rodet.' "
            "'Jeg udsatte alt.' "
            "'Jeg startede forfra hver uge.' "
            "[large line break] "
            "'Og så fandt jeg Vanea.' "
            "[large line break] "
            "'Det tog 3 uger.' "
            "'Nu sætter jeg kryds næsten hver eneste dag.' "
            "[large line break] "
            "Small italic white text: 'Find Vanea i App Store' "
            "Dark, moody, vulnerable and real. High contrast white on dark. Square 1080x1080."
        ),
    },
]

# --- JUNE 2026 BATCH 3: 15 hooks ---
BATCH3_CONCEPTS = [
    {
        "name": "hook1_morgenmenneske",
        "prompt": (
            "Create a square 1080x1080 image in the style of a LinkedIn or Facebook personal story post. "
            "BACKGROUND: pure white. NO phone frame. NO decorations. Text only, filling the image comfortably. "
            "HEADLINE at top in very large bold black font taking up top 38% of image: "
            "'Du kommer ikke til at tro på hvad der rent faktisk fik mig til at være et morgenmenneske' "
            "Below, medium black text with generous spacing between each paragraph: "
            "'Jeg har aldrig kunnet stå op om morgenen. Aldrig.\\n\\n"
            "Jeg satte 4 alarmer. Trykkede snooze på dem alle.\\n\\n"
            "Og så prøvede jeg noget så simpelt at det næsten var pinligt.\\n\\n"
            "Jeg downloadede Vanea og tilføjede tre vaner:\\n"
            "• Stå op ved første alarm\\n"
            "• Drik et glas vand\\n"
            "• Kom ud i frisk luft inden kl. 9\\n\\n"
            "Uge 1: Klarede det 4 ud af 7 dage. Rekord.\\n"
            "Uge 4: Jeg har ikke misset én eneste dag.\\n\\n"
            "Jeg ville ønske jeg havde prøvet det tidligere.' "
            "Clean, authentic, story-driven. Square 1080x1080."
        ),
    },
    {
        "name": "hook2_twitter_umulige_ting",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. NO phone frame. Tweet fills the entire square. "
            "Profile: small round gray circle. Name: 'Sofie M.' in white bold with blue verified checkmark. Handle: '@sofiem' in gray. "
            "Tweet text in white Twitter-style font, medium size, generous spacing between paragraphs: "
            "'Ting jeg gør nu der ville have virket umuligt for et år siden:\\n\\n"
            "• Spiser morgenmad næsten hver dag\\n"
            "• Er ude af sengen inden alarmen ringer\\n"
            "• Har ikke sprunget en eneste vane over i 3 uger\\n"
            "• Rydder op inden jeg går i seng\\n"
            "• Kan faktisk mærke forskel på mine dage\\n\\n"
            "Jeg startede bare med at sætte kryds i en app.\\n\\n"
            "App: Vanea' "
            "Below tweet: realistic gray Twitter icons with small numbers. Looks 100% like a real tweet. Square 1080x1080."
        ),
    },
    {
        "name": "hook3_before_after_vaner",
        "prompt": (
            "Create a square 1080x1080 social media image in a retro style, modelled on the 'I went from bed rotting to that girl' ad format. "
            "BACKGROUND: warm cream/off-white (#F5F0E8). "
            "BORDER: thick decorative tiled border all around — colorful retro tiles in red, orange, yellow, green, blue with circular motifs in corners. About 70px wide. "
            "BOTTOM INTERIOR: retro red-and-white checkered floor pattern at the very bottom of the inner area. "
            "NO phone mockups. NO text that says 'Before/after'. "
            "HEADLINE at top of inner area in very large bold dark purple font: 'Jeg genkender ikke mig selv' "
            "Below: two columns side by side. "
            "LEFT COLUMN: handwritten italic label 'Før' at top. Simple sad drooping illustrated figure. Bullet points in small handwritten-style font: "
            "'• Sprang morgenmad over næsten hver dag\\n"
            "• Motivationen kom og gik\\n"
            "• Startede forfra hver uge\\n"
            "• Følte mig altid bagud' "
            "RIGHT COLUMN: handwritten italic label 'Efter' at top. Simple happy upright illustrated figure. Bullet points: "
            "'• Spiser morgenmad 6 ud af 7 dage\\n"
            "• Har ikke misset en dag i 3 uger\\n"
            "• Starter dagen med ro\\n"
            "• Har faktisk overskud' "
            "BOTTOM TEXT centered: 'Vanea hjælper dig med at bygge de vaner du vil have — ét kryds ad gangen.' "
            "Retro warm palette. Charming illustrated style. Square 1080x1080."
        ),
    },
    {
        "name": "hook4_twitter_produktiv",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. NO phone frame. "
            "The image shows a tweet REPLY thread. "
            "At the top: a small quoted/replied-to tweet in a gray rounded box: small gray profile circle, name 'Lena' in gray, text '@majak hvorfor er du altid så produktiv?' "
            "Below that: the main reply tweet. Profile: small round gray circle. Name: 'Maja K.' in white bold. Handle: '@majak' in gray. "
            "Reply tweet text in white Twitter-style font, medium size, generous spacing: "
            "'Ærligt? Jeg fandt en app der hedder Vanea.\\n\\n"
            "Du tilføjer dine egne vaner og sætter kryds hver dag.\\n\\n"
            "Det er SÅ simpelt at jeg næsten skammer mig over at det virker.\\n\\n"
            "Men det gør.\\n\\n"
            "Jeg har ikke misset én eneste dag i 5 uger.' "
            "Below tweet: realistic gray Twitter icons. Looks 100% like a real tweet thread. Square 1080x1080."
        ),
    },
    {
        "name": "hook5_baggrund_udbraendt",
        "prompt": (
            "Create a square 1080x1080 image with a dark atmospheric background — deep dark navy blue/purple, slightly textured, moody and intimate. "
            "NO phone mockups. "
            "Large white text centered in the image with generous spacing between each line: "
            "'Jeg lagde ikke mærke til\\nhvor udbrændt jeg var\\n\\n"
            "indtil selv de mest basale ting\\nbegyndte at føles svære.\\n\\n"
            "At lave mad.\\nAt svare på en besked.\\nAt stå op.\\n\\n"
            "Jeg begyndte med én ting om dagen i Vanea.\\n\\n"
            "Bare ét kryds.\\n\\n"
            "Det var nok til at komme i gang.' "
            "Small white text at bottom: 'Find Vanea i App Store' "
            "Dark, moody, vulnerable and deeply relatable. High contrast white on dark. Square 1080x1080."
        ),
    },
    {
        "name": "hook6_template_balance",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style wellness template card. "
            "NO phone mockups. Pure graphic design. "
            "BACKGROUND: soft lavender (#E8D5F5). "
            "Decorations: small hand-drawn flowers, moons and sparkle stars scattered lightly in corners. "
            "TITLE at top center in very large bold black rounded font, taking up top 28% of image: '5 små vaner der hjælper dig med at finde indre balance 💜' "
            "Below: five numbered rows with generous spacing, each in a soft white rounded pill shape: "
            "'1. Drik et glas vand inden du kigger på telefonen' "
            "'2. Kom udenfor i mindst 10 minutter' "
            "'3. Spis noget ordentligt til frokost' "
            "'4. Sæt kryds — også for de helt små ting' "
            "'5. Læg telefonen fra dig 30 minutter inden du sover' "
            "BOTTOM: small centered dark purple text: 'Spor dine vaner i Vanea — find den i App Store' "
            "Soft, warm, Pinterest-saveable. Square 1080x1080."
        ),
    },
    {
        "name": "hook7_notes_velfungerende_voksen",
        "prompt": (
            "Create a square 1080x1080 image in the style of a LinkedIn or Facebook personal story post. "
            "BACKGROUND: pure white. NO phone frame. NO decorations. Text only. "
            "HEADLINE at top in very large bold black font taking up top 35% of image: "
            "'Jeg blev ved et uheld en velfungerende voksen efter...' "
            "Below, medium black text with very generous spacing between paragraphs: "
            "'...efter at have downloadet en vanesporing-app.\\n\\n"
            "Ikke fordi jeg er disciplineret.\\n\\n"
            "Ikke fordi jeg er blevet et nyt menneske.\\n\\n"
            "Men fordi appen mindede mig om at sætte kryds — og det føltes godt nok til at fortsætte.\\n\\n"
            "Uge 1: Ryddede op 4 dage ud af 7.\\n"
            "Uge 3: 6 ud af 7.\\n"
            "Uge 6: Jeg genkender ikke mit hjem.\\n\\n"
            "Appen hedder Vanea. Find den i App Store.' "
            "Clean, authentic, story-driven. Square 1080x1080."
        ),
    },
    {
        "name": "hook8_template_bedre_med_dig",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style wellness list card. "
            "NO phone mockups. Pure graphic design. "
            "BACKGROUND: soft mint green (#C8F0DC). "
            "Decorations: small hand-drawn leaves, hearts and sun doodles in corners — fresh and gentle. "
            "TITLE at top in very large bold black rounded font, taking up top 30% of image: '5 ting du kan gøre én gang om dagen for at have det bedre med dig selv 🌿' "
            "Below: five numbered rows with generous spacing: "
            "'1. Gå en tur — selv hvis det bare er 15 minutter' "
            "'2. Spis noget der giver dig energi' "
            "'3. Drik nok vand gennem hele dagen' "
            "'4. Gør én ting du har udsat' "
            "'5. Læg telefonen fra dig inden sengetid' "
            "BOTTOM: small centered dark green text: 'Sæt kryds på dine vaner i Vanea — find den i App Store' "
            "Fresh, calm, encouraging. Square 1080x1080."
        ),
    },
    {
        "name": "hook9_baggrund_depression_vane",
        "prompt": (
            "Create a square 1080x1080 image with a soft blurred warm portrait photo as background — a young woman with soft window light on her face, very slightly out of focus, warm tones. Gentle and relatable, not glamorous. "
            "Over the photo, a semi-transparent frosted white overlay panel covers the center of the image. "
            "On the frosted panel, dark text centered: "
            "Large bold dark text: 'Efter et år med depression begyndte jeg at bruge en vane-app hver dag.' "
            "Below in medium regular text with generous spacing: "
            "'Ikke fordi det kurerede noget.\\n\\n"
            "Men fordi det gav mig en struktur at holde fast i\\n— selv de dage hvor alt føltes tungt.\\n\\n"
            "Ét kryds. Én dag ad gangen.' "
            "Small text at bottom: 'Find Vanea i App Store' "
            "Soft, warm, empathetic. Square 1080x1080."
        ),
    },
    {
        "name": "hook10_psa_kaotiske_dage",
        "prompt": (
            "Create a square 1080x1080 social media image that looks like an organic text post. "
            "BACKGROUND: clean off-white (#FAFAF8). NO decorations. NO images. Pure text on plain background. "
            "Medium bold black text at top: 'Før jeg fandt denne app var mine dage kaotiske.' "
            "Below, medium black regular text with generous spacing between each paragraph: "
            "'Jeg sprang måltider over.\\n"
            "Jeg ignorerede mine egne behov.\\n"
            "Jeg følte at jeg bare drev gennem livet.\\n\\n"
            "Så prøvede jeg Vanea.\\n\\n"
            "En simpel vanesporing-app til iPhone.\\n"
            "Du tilføjer dine vaner og sætter kryds hver dag.\\n\\n"
            "For første gang i lang tid følte jeg at jeg havde styr på noget.\\n\\n"
            "Find Vanea i App Store.' "
            "Minimal, authentic. Black text on off-white. Square 1080x1080."
        ),
    },
    {
        "name": "hook11_twitter_fitness",
        "prompt": (
            "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
            "Pure black background. White text. Authentic Twitter UI layout. NO phone frame. "
            "Shows a reply thread. "
            "At the top: small quoted tweet in gray rounded box: gray profile circle, name 'Nanna' in gray, text '@emmaj hvad fik dig til at begynde i fitnesscenteret?' "
            "Below: main reply. Profile: small round gray circle. Name: 'Emma J.' in white bold. Handle: '@emmaj' in gray. "
            "Reply tweet text, white Twitter-style font, generous spacing: "
            "'Jeg begyndte med en vane-app faktisk 😅\\n\\n"
            "Jeg tilføjede bare \\'gå en tur\\' som én af mine daglige vaner i Vanea.\\n\\n"
            "Dag 1: 20 minutter rundt om blokken.\\n"
            "Dag 14: Jeg gik til fitnesscenteret for første gang i 2 år.\\n"
            "Dag 30: Jeg er der 4 gange om ugen.\\n\\n"
            "Det startede med et kryds i en app.\\n\\n"
            "Jeg ville ønske jeg havde fundet den tidligere.' "
            "Below tweet: realistic gray Twitter icons. Looks 100% like a real tweet. Square 1080x1080."
        ),
    },
    {
        "name": "hook12_baggrund_ny_version",
        "prompt": (
            "Create a square 1080x1080 image with a soft warm blurred background photo — a cozy morning scene with golden sunlight through a window, soft and dreamy, slightly out of focus. Warm peach/amber tones. "
            "NO phone mockups. "
            "A gentle semi-transparent white overlay covers the center of the image for text readability. "
            "Centered text on the overlay in dark warm brown/charcoal: "
            "Large bold text: 'Giv dig selv lov til at blive en ny version af dig selv.' "
            "Below in medium regular text with generous spacing: "
            "'Du behøver ikke være perfekt fra dag 1.\\n"
            "Du behøver ikke have styr på det hele.\\n\\n"
            "Begynd med én vane.\\n"
            "Sæt kryds.\\n"
            "Gør det igen i morgen.\\n\\n"
            "Vanea hjælper dig med resten.' "
            "Small text at bottom: 'Find Vanea i App Store' "
            "Warm, gentle, hopeful. Square 1080x1080."
        ),
    },
    {
        "name": "hook13_bold_nulstil",
        "prompt": (
            "Create a square 1080x1080 social media image with bold minimal typography — like a powerful poster. "
            "BACKGROUND: pure white. NO images. NO decorations. NO phone mockups. Just bold text. "
            "Left-aligned text with generous left margin, dramatic line breaks: "
            "Very large bold black text taking up most of the image: "
            "'Du kan\\nenten\\nnulstille.' "
            "Below that, slightly smaller bold black text: "
            "'Eller bruge resten\\naf livet på at\\nforklare hvorfor\\ndu ikke gjorde.' "
            "Below that, a thin horizontal black line. "
            "Below the line, medium regular black text: 'Vanea giver dig strukturen til at starte.' "
            "Very small gray text at bottom: 'Find Vanea i App Store — til iPhone' "
            "Extremely minimal. Black on white. Bold and direct. Square 1080x1080."
        ),
    },
    {
        "name": "hook14_baggrund_pov",
        "prompt": (
            "Create a square 1080x1080 image with a dark dramatic background — very dark navy/charcoal, slightly textured with faint hand-drawn white squiggly lines and asterisks scattered lightly. "
            "NO phone mockups. "
            "Large white text centered, generous spacing between each section: "
            "First line in medium white italic: 'POV:' "
            "Below in large bold white text: 'Du har været igennem et helvede' "
            "Below in large regular white text: 'og er stadig villig til at møde op for dig selv og nulstille dit liv.' "
            "Below a thin white line, medium white text: "
            "'Det er præcis hvem Vanea er lavet til.' "
            "Small white text at bottom: 'Find Vanea i App Store' "
            "Dark, powerful, deeply validating. High contrast white on dark. Square 1080x1080."
        ),
    },
    {
        "name": "hook15_handskrevet_yndlingsapp",
        "prompt": (
            "Create a square 1080x1080 image that looks exactly like a handwritten personal note on aged cream paper. "
            "BACKGROUND: warm aged paper texture — cream/slightly yellowed, with subtle paper grain and slight creases. Like a real notebook page. "
            "NO phone frame. No decorations. Just handwriting on paper. "
            "Entire image filled with handwritten text in natural slightly imperfect handwriting — mix of black pen with some words underlined in blue or circled in red for emphasis: "
            "'Mig før jeg fandt min yndlingsapp:\\n\\n"
            "Aldrig styr på noget. Altid bagud.\\n"
            "Startede forfra hver uge.\\n\\n"
            "Mig nu:\\n\\n"
            "Har ikke misset én eneste vane i 3 uger.\\n"
            "Mit hjem er rent.\\n"
            "Jeg har faktisk overskud til at se venner.\\n\\n"
            "Appen hedder Vanea.\\n"
            "Du tilføjer bare dine vaner og sætter kryds.\\n\\n"
            "Det lyder for simpelt.\\n\\n"
            "Det er det ikke.' "
            "The word 'Vanea' should be underlined or circled for emphasis. "
            "Text fills the page naturally, slight angle as if really handwritten. Very authentic. Square 1080x1080."
        ),
    },
]

BATCH4_CONCEPTS = [
    {
        "name": "template_anspandt_morgen",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style wellness infographic. "
            "BACKGROUND: soft light blue (#B8E8F0). "
            "TITLE at top center in large bold handwritten-style teal/dark teal font, two lines: 'Ting du kan gøre når du vågner op og føler dig anspændt' "
            "Below the title: a 3x3 grid of 9 items. Each item has a cute flat-style illustration on top and a short caption below in small dark handwritten-style font. "
            "Item 1: illustration of a woman drinking a glass of water. Caption: 'Drik et glas vand' "
            "Item 2: illustration of a woman breathing with hand on chest. Caption: 'Træk vejret ind gennem næsen' "
            "Item 3: illustration of a megaphone with hearts and stars. Caption: 'Sig højt: \"Jeg er tryg lige nu\"' "
            "Item 4: illustration of a woman stretching/doing yoga. Caption: 'Stræk arme og ben' "
            "Item 5: illustration of hands writing in a journal with coffee. Caption: 'Skriv ned hvad du føler' "
            "Item 6: illustration of an open window with green plant. Caption: 'Åbn et vindue for frisk luft' "
            "Item 7: illustration of rocks/stones on the ground. Caption: 'Ground dig selv ved at røre noget fast' "
            "Item 8: illustration of a music player/mp3 with headphones and music notes. Caption: 'Spil afslappende musik' "
            "Item 9: illustration of a cute sleeping pillow/cushion with ZZZ. Caption: 'Kram noget blødt' "
            "Style: soft pastel light blue background, teal/dark teal handwritten font, cute colorful flat illustrations, clean and airy layout. No watermarks. Square 1080x1080."
        ),
    },
    {
        "name": "template_7dages_hjemme_reset",
        "prompt": (
            "Create a square 1080x1080 Pinterest infographic. "
            "Style: warm cream background (#F5F0E0), dark brown bold italic serif font for day labels, gold 4-pointed sparkle stars along a vertical center line, small cute flat household illustrations, two alternating columns per day. "
            "Title at top: '7-dages Hjemme-Reset' in large bold dark brown serif. "
            "7 days alternating left/right with small room illustrations: "
            "Dag Et — RYD OP I DET ESSENTIELLE — Tør borde af, Sortér papirer, Sorter rodet skuffe. Illustration: dining table. "
            "Dag To — OPFRISKNING AF STUEN — Tør støv af, Bank puder, Rengør skærme. Illustration: floor lamp. "
            "Dag Tre — RESET AF SOVEVÆRELSET — Skift sengetøj, Ryd natborde, Organisér garderobe. Illustration: bed. "
            "Dag Fire — OPRYDNING I KØKKENET — Rengør køleskab, Organisér spisekammer, Tør mikroovn. Illustration: fridge. "
            "Dag Fem — OPFRISKNING AF BADEVÆRELSET — Skrub bruser, Tør spejle, Ryd skabe. Illustration: bathroom vanity. "
            "Dag Seks — ENTRÉ OG GULVE — Støvsug og vask gulve, Tør dørhåndtag, Organisér sko. Illustration: lamp. "
            "Dag Syv — SIDSTE TOUCH — Luft ud eller tænd stearinlys, Køb blomster. Illustration: candle. "
            "Bottom: small cute purple smiley heart. No watermarks. Clean Pinterest style. Square 1080x1080."
        ),
    },
]

BATCH4_CONCEPTS.append({
    "name": "template_9_ting_overvaeldet",
    "prompt": (
        "Create a square 1080x1080 Pinterest-style wellness infographic. "
        "BACKGROUND: soft warm cream/beige (#F5EDD8). "
        "TITLE at top center in large bold dark orange/rust serif font, three lines: '9 ting du kan gøre rent\\nnår du føler dig overvældet' "
        "Below title, small centered dark gray regular text: 'Når du ikke ved hvor du skal starte, så start i det små.\\nDisse små sejre kan hjælpe med at rydde op i både dit hoved og dit hus.' "
        "Below: a 3x3 grid of 9 items. Each item has a cute flat-style illustration inside a soft colored oval/circle (alternating light blue, peach, light gray), a bold orange/rust colored title below, and small dark gray description text. "
        "Item 1 — blue circle, illustration of kitchen sink: Title 'Køkkenvasken' Description '– en ren vask gør hele køkkenet hyggeligere' "
        "Item 2 — peach circle, illustration of bedside table with lamp: Title 'Dit natbord' Description '– det er det første og sidste du ser' "
        "Item 3 — gray circle, illustration of trash bin: Title 'Skraldespanden' Description '– tør den af, skift posen, færdig' "
        "Item 4 — yellow circle, illustration of laundry basket with colorful clothes: Title 'Vasketøj' Description '– bare vask, tør eller fold – ikke alle tre' "
        "Item 5 — peach circle, illustration of front door with floor: Title 'Gulvet ved entrédøren' Description '– sko, post, tasker – ryd kaosset' "
        "Item 6 — blue circle, illustration of bathroom sink and mirror: Title 'Vasken/spejlet' Description '– en 2-minutters oprydning der føles som et reset' "
        "Item 7 — pink circle, illustration of sofa with cushions: Title 'Dine sofapuder' Description '– bank dem, fold et tæppe – hygge med det samme' "
        "Item 8 — yellow circle, illustration of cluttered pile/dump zone: Title '\"Dumpe-zonen\"' Description '– der hvor rod hober sig op – tag fat dér' "
        "Item 9 — gray circle, illustration of open drawer: Title 'Én skuffe' Description '– vælg én, et hvilket som helst rum. Den ene, og du er færdig' "
        "Style: warm cream background, rust/orange bold titles, small gray description text, cute colorful flat illustrations in soft oval backgrounds. No watermarks. Square 1080x1080."
    ),
})

BATCH4_CONCEPTS.append({
    "name": "twitter_sofie_ny_tekst",
    "prompt": (
        "Create a square 1080x1080 image that looks EXACTLY like a real Twitter/X screenshot in dark mode. "
        "Pure black background. White text. Authentic Twitter UI layout. NO phone frame. Tweet fills the entire square. "
        "Profile: small round blue-gray circle for profile photo. Name: 'Sofie M.' in white bold with small blue verified checkmark. Handle: '@sofiem' in gray. "
        "Tweet text in white Twitter-style font, medium size, with generous spacing between paragraphs: "
        "'Til alle der altid har gode intentioner men aldrig holder ved:\\n\\n"
        "Når du laver overspringshandlinger eller går i stå er det ikke på grund af dovenskab.\\n"
        "Det er din hjerne der mangler dopamin til at gøre de ting du faktisk gerne vil.\\n\\n"
        "Denne app er lavet til at ændre det – du tilføjer selv dine vaner, krydser af hver dag og følger dine streaks.\\n"
        "På den måde får din hjerne dopamin for de ting der faktisk gør dig glad.\\n\\n"
        "Og det bedste? Du kan prøve den helt gratis.' "
        "Below tweet: realistic gray Twitter engagement icons — comment with 12, retweet with 28, like with 112, share. "
        "Looks 100% like a real organic tweet. Square 1080x1080."
    ),
})

BATCH4_CONCEPTS.append({
    "name": "template_morgenrutine_stjernetegn",
    "prompt": (
        "Create a square 1080x1080 social media infographic styled exactly like a 'That Girl Morning Routine based on zodiac sign' Pinterest post. "
        "BACKGROUND: white. "
        "TITLE at very top in large bold black rounded font: 'Den Perfekte Morgenrutine' "
        "Below title in bold pink/rose caps font: 'BASERET PÅ DIT STJERNETEGN' "
        "Below: four side-by-side illustrated portrait panels, each showing a different woman in a soft flat illustration style with a cozy morning vibe and a zodiac symbol above: "
        "Panel 1 — Jomfru symbol (♍), woman writing in journal at desk, green plants, sage green tones. "
        "Panel 2 — Fiskene symbol (♓), woman holding pink mug in bed, soft pink tones. "
        "Panel 3 — Løven symbol (♌), woman stretching/posing confidently, white athletic wear, warm tones. "
        "Panel 4 — Stenbuk symbol (♑), woman at desk with coffee and planner, sage green tones. "
        "Below the four panels: four columns of schedule text in small black font, centered under each panel: "
        "Column 1 — Bold title 'JOMFRUEN:' then: '5:30: Stå op' '5:35: Red sengen' '5:45: Citronvand + hudpleje' '6:00: Dagbog + to-do liste' '6:30: Pilates' '7:30: Matcha + morgenmad' "
        "Column 2 — Bold title 'FISKENE:' then: '7:00: Stå roligt op' '7:15: Meditation' '7:30: Varmt citronvand' '7:45: Blid yoga' '8:30: Dagbog + tarot' '9:00: Matcha + læs' "
        "Column 3 — Bold title 'LØVEN:' then: '6:00: Stå op' '6:05: Spejlaffirmationer' '6:15: Hot girl walk' '7:15: Kold bruser + hudpleje' '7:45: Proteinsmoothie' '8:00: Tøj + GRWM' "
        "Column 4 — Bold title 'STENBUKKEN:' then: '5:00: Stå op' '5:05: Kold bruser' '5:20: Træning' '6:30: Hudpleje + morgenmad' '7:00: Planlæg dagen' '7:30: Dybt arbejde' "
        "BOTTOM: a small rounded pill button with text 'Find Vanea i App Store' with small arrow/sparkle decorations on each side. "
        "Style: white background, bold black title, pink accent subtitle, soft flat illustration panels, clean minimal schedule columns. No watermarks. Square 1080x1080."
    ),
})

BATCH5_CONCEPTS = [
    {
        "name": "zodiac_elegant",
        "prompt": (
            "Create a square 1080x1080 Pinterest infographic in an elegant, soft, realistic style. "
            "BACKGROUND: warm off-white/cream (#F8F2ED). "
            "TITLE at top: 'Den Perfekte' in pink rose italic script font, then 'Morgenrutine' in large bold dark serif font below it. "
            "Below title in small elegant gray serif: 'Baseret på dit stjernetegn' with a small pink heart below. "
            "A thin pink divider line. "
            "FOUR PORTRAIT PANELS side by side, each a realistic soft AI-illustration of a woman in morning setting: "
            "Panel 1 (Jomfruen ♍): woman with dark hair bun writing in journal at desk, matcha latte, sage green tones, cozy morning light. Zodiac symbol ♍ above panel. "
            "Panel 2 (Fiskene ♓): woman with dark hair holding white mug in bed, soft pink bedroom, morning light through sheer curtains. Zodiac symbol ♓ above. "
            "Panel 3 (Løven ♌): blonde woman in white crop top stretching arms up confidently, bright sunny room. Zodiac symbol ♌ above. "
            "Panel 4 (Stenbukken ♑): dark-haired woman in blazer writing in planner at desk with coffee, professional morning setting. Zodiac symbol ♑ above. "
            "Below panels: four columns of schedule in small clean black font with small icons per row: "
            "JOMFRUEN: 5:30 Stå op / 5:35 Red sengen / 5:45 Citronvand + hudpleje / 6:00 Dagbog + to-do liste / 6:30 Pilates / 7:30 Matcha + morgenmad "
            "FISKENE: 7:00 Stå roligt op / 7:15 Meditation / 7:30 Varmt citronvand / 7:45 Blid yoga / 8:30 Dagbog + tarot / 9:00 Matcha + læs "
            "LØVEN: 6:00 Stå op / 6:05 Spejlaffirmationer / 6:15 Hot girl walk / 7:15 Kold bruser + hudpleje / 7:45 Proteinsmoothie / 8:00 Tøj + GRWM "
            "STENBUKKEN: 5:00 Stå op / 5:05 Kold bruser / 5:20 Træning / 6:30 Hudpleje + morgenmad / 7:00 Planlæg dagen / 7:30 Dybt arbejde "
            "BOTTOM: small decorative leaf/branch illustrations and a pill button 'Find Vanea i App Store'. "
            "Elegant, soft, sophisticated. Realistic illustration style. Square 1080x1080."
        ),
    },
    {
        "name": "zodiac_barbie_pink",
        "prompt": (
            "Create a square 1080x1080 Pinterest infographic in a bold Barbie-pink glam style. "
            "BACKGROUND: hot pink gradient (#FF69B4 to #FFB6C1) with gold sparkle stars and gem decorations scattered. "
            "TITLE: 'That Girl' in pink italic cursive with butterfly emoji, then 'MORGENRUTINE' in very large bold white outlined font with pink 3D shadow. "
            "Below title: a purple pill banner 'BASERET PÅ DIT STJERNETEGN' with heart emojis. "
            "Pink gem/crystal decorations in corners. "
            "FOUR PORTRAIT PANELS side by side with rounded corners, each a glamorous AI-illustration: "
            "Panel 1 (♍): glamorous dark-haired woman writing in journal, green aesthetic, pink shelves in background. "
            "Panel 2 (♓): blonde woman in purple/lavender silk robe holding pink mug, moon and stars background, glowing candles. "
            "Panel 3 (♌): confident dark-skinned woman in white workout set doing yoga pose, golden water bottle, pink gym. "
            "Panel 4 (♑): woman in pink blazer with sunglasses holding coffee cup, city view, planner on desk. "
            "Below panels: four white rounded rectangle cards, each with colored bold zodiac title and small emoji icons per row: "
            "GREEN — JOMFRUEN: 5:30 Stå op / 5:35 Red sengen / 5:45 Citronvand + hudpleje / 6:00 Dagbog + to-do liste / 6:30 Pilates / 7:30 Matcha + morgenmad "
            "PURPLE — FISKENE: 7:00 Stå roligt op / 7:15 Meditation / 7:30 Varmt citronvand / 7:45 Blid yoga / 8:30 Dagbog + tarot / 9:00 Matcha + læs "
            "GOLD — LØVEN: 6:00 Stå op / 6:05 Spejlaffirmationer / 6:15 Hot girl walk / 7:15 Kold bruser + hudpleje / 7:45 Proteinsmoothie / 8:00 Tøj + GRWM "
            "PINK — STENBUKKEN: 5:00 Stå op / 5:05 Kold bruser / 5:20 Træning / 6:30 Hudpleje + morgenmad / 7:00 Planlæg dagen / 7:30 Dybt arbejde "
            "BOTTOM: large pink rounded button 'Find Vanea i App Store' with hearts. Pink gem decorations. "
            "Bold, glam, maximalist Barbie-pink style. Square 1080x1080."
        ),
    },
    {
        "name": "zodiac_pink_refined",
        "prompt": (
            "Create a square 1080x1080 Pinterest infographic in a pink glam style, slightly more refined than full Barbie. "
            "BACKGROUND: soft pink (#FFD6E0) with subtle gold star sparkles scattered. "
            "TITLE: 'That Girl' in pink italic cursive script with small heart, then 'MORGENRUTINE' in very large bold white font with soft pink outline. "
            "Below: small text 'BASERET PÅ DIT STJERNETEGN' with small star decorations. "
            "FOUR TALL PORTRAIT PANELS side by side with soft rounded corners: "
            "Panel 1 (♍): beautiful dark-haired woman in green hoodie writing in journal, green matcha, cozy aesthetic. "
            "Panel 2 (♓): pretty woman in lavender silk robe holding pink mug, purple dreamy bedroom with moon, candles, crystals. "
            "Panel 3 (♌): fit woman in white sports set doing yoga stretch, golden water bottle, bright pink gym. "
            "Panel 4 (♑): stylish woman in beige blazer with coffee and planner, city background. "
            "Below each panel: small colored heart emoji (green/purple/gold/pink), then bold colored zodiac name, then schedule in small black font: "
            "JOMFRUEN: 5:30 Stå op / 5:35 Red sengen / 5:45 Citronvand + hudpleje / 6:00 Dagbog + to-do liste / 6:30 Pilates / 7:30 Matcha + morgenmad "
            "FISKENE: 7:00 Stå roligt op / 7:15 Meditation / 7:30 Varmt citronvand / 7:45 Blid yoga / 8:30 Dagbog + tarot / 9:00 Matcha + læs "
            "LØVEN: 6:00 Stå op / 6:05 Spejlaffirmationer / 6:15 Hot girl walk / 7:15 Kold bruser + hudpleje / 7:45 Proteinsmoothie / 8:00 Tøj + GRWM "
            "STENBUKKEN: 5:00 Stå op / 5:05 Kold bruser / 5:20 Træning / 6:30 Hudpleje + morgenmad / 7:00 Planlæg dagen / 7:30 Dybt arbejde "
            "BOTTOM: pink rounded pill button 'Find Vanea i App Store' with small heart. Gold star sparkles around button. "
            "Glam but elegant pink style. Square 1080x1080."
        ),
    },
]

BATCH6_CONCEPTS = [
    {
        "name": "starter_pack_broderi",
        "prompt": (
            "Create a square 1080x1080 image styled to look like embroidered fabric patches on a linen/canvas background. "
            "BACKGROUND: warm off-white linen/canvas texture (#E8E0D0), slightly wrinkled like real fabric. "
            "TITLE at top in large bold dark olive green embroidered-style serif font: 'That Girl\\nStarter Pack' "
            "Below: four embroidered patch items arranged in a 2x2 grid: "
            "TOP LEFT — circular patch with olive green embroidered border: inside, a realistic embroidered matcha latte cup with latte art and steam. Below the cup, bold embroidered caps text: 'MATCHA' "
            "TOP RIGHT — rounded square patch with dusty rose/pink embroidered border: inside, an embroidered woman in white workout clothes holding a pilates ball, sitting on floor. Below, bold caps: 'PILATES' "
            "BOTTOM LEFT — octagon patch with gold/mustard embroidered border: inside, an embroidered open journal/notebook with a daisy flower and pen. Below, bold caps: 'DAGBOG' "
            "BOTTOM RIGHT — rounded rectangle patch with sage green embroidered border: inside, a realistic embroidered smartphone showing a simple habit tracker app interface. Below, bold caps: 'FØLG MED VANEA' "
            "All patches look like real embroidered fabric badges — textured stitching, slightly raised look, warm muted colors. "
            "No phone mockups beyond the embroidered phone. Square 1080x1080."
        ),
    },
    {
        "name": "starter_pack_retro_gron",
        "prompt": (
            "Create a square 1080x1080 image in a vintage retro illustration style on aged parchment/cream paper texture. "
            "BACKGROUND: warm aged cream/parchment (#F0E8D8) with subtle paper grain. "
            "TITLE at top left in very large bold dark forest green retro display font with slight texture: 'That Girl' with a small orange asterisk/star doodle to the right, then 'Starter Pack' on the next line. A short orange underline beneath 'Starter Pack'. "
            "Below: a 2x2 grid of four panels, each with a thin dark green/orange hand-drawn border: "
            "TOP LEFT panel: detailed hand-drawn illustration of a large steaming matcha bowl/cup from above, dark green on cream. Caption below in small lowercase italic: 'matcha > alt' "
            "TOP RIGHT panel: detailed hand-drawn illustration of a woman in dark green athletic wear doing a pilates boat pose on a mat. Caption: 'pilates prinsesse' "
            "BOTTOM LEFT panel: detailed hand-drawn illustration of an open journal/notebook with handwritten words 'taknemmelighed / mål / mindset / selvkærlighed / vækst' and a small botanical leaf drawing, with a pen. Caption: 'skriv det ned' "
            "BOTTOM RIGHT panel: detailed hand-drawn illustration of a simple smartphone showing habit tracking rings/circles. Caption: 'fremgang, ikke perfektion' "
            "Each caption has a small orange underline. Vintage, earthy, hand-crafted feel. Dark forest green and terracotta orange on aged cream. Square 1080x1080."
        ),
    },
    {
        "name": "starter_pack_hvid_plan",
        "prompt": (
            "Create a square 1080x1080 clean minimal ad image. "
            "BACKGROUND: pure white with a very faint, barely visible watermark-style calendar grid in light gray/rose behind the text — like a blurred monthly calendar. "
            "TOP LEFT: a small rounded square app icon (soft rose/peach with a simple sunrise/sun icon inside) followed by the text 'Vanea' in medium gray font. "
            "Main text, left-aligned, taking up most of the image: "
            "Very large bold dark charcoal/near-black serif font, two lines: 'Hun vågner ikke\\nop motiveret.' "
            "Below that: a short horizontal black line divider. "
            "Below the line: large bold rose/dusty pink font, two lines: 'Hun vågner op\\nmed en plan.' "
            "Below that in small regular gray text: 'Dit vanesystem til hverdagen.\\nFra morgen til aften — allerede planlagt.' "
            "BOTTOM LEFT: a black rounded rectangle App Store download button with Apple logo and text 'Hent på\\nApp Store' in white. "
            "Clean, minimal, sophisticated. White background, charcoal + rose pink text. Square 1080x1080."
        ),
    },
]

BATCH7_CONCEPTS = [
    {
        "name": "that_girl_kalender",
        "prompt": (
            "Create a square 1080x1080 image styled like a lifestyle app screenshot/ad. "
            "BACKGROUND: warm off-white/cream (#F5F0EB). "
            "TOP LEFT: small gray back arrow '‹' followed by '2025' in gray. "
            "Below that, large bold rose/dusty pink italic serif font: 'Træd ind i din\\n\"That Girl\" era' "
            "Below: a faint calendar grid in light gray — column headers in small caps: 'S  M  T  O  T  F  L' — with dates 1-31 visible but very faint/light. "
            "On the left and right sides of the calendar: small square lifestyle product photos placed at various date positions — a candle, a matcha cup, a meditation cushion, skincare products, a succulent plant, a gold sun necklace, dried flowers, a pink flower, folded towels, a smoothie bowl. "
            "CENTER: a frosted white semi-transparent rounded rectangle card overlaid on the calendar, containing: "
            "Italic serif title: 'Hemmeligheden bag \"That Girl\"?' "
            "Small gray subtitle: 'Du behøver ikke motivation. Du har brug for struktur.' "
            "A list of 5 habit rows, each with a small rose icon on left, bold habit name, small gray description, and small gray time on right: "
            "'Morgen  •  Aktiv — Start dagen med intention — 0' "
            "'Hydrering — Drik et stort glas vand — 1 min ›' "
            "'Meditation — 5-10 min mindfulness — 10 min ›' "
            "'Morgenhudpleje — Rens, tone, fugt, SPF — 10 min ›' "
            "'Stræk eller yoga — 5-10 min blid bevægelse — 10 min ›' "
            "Bottom of card in small centered gray italic: 'Alt hvad du har brug for, allerede planlagt.' "
            "BOTTOM: bold small caps centered text: 'DAG 31 OG FREMAD' "
            "Below that: a black rounded App Store button 'Hent på App Store' with Apple logo. "
            "Below: two small lifestyle photos (sage bundle and candle). "
            "Elegant, clean, warm cream. Square 1080x1080."
        ),
    },
    {
        "name": "that_girl_telefon_mockup",
        "prompt": (
            "Create a square 1080x1080 lifestyle app ad image. "
            "BACKGROUND: soft pink-to-lavender gradient (#FFE4EC to #E8D5F5), very soft and dreamy. "
            "CENTER: a realistic iPhone 15 Pro mockup in rose gold/pink frame, portrait orientation, taking up about 50% of the image height. The phone screen shows a simple clean app interface with: a small sunrise/sun icon at top, bold dark text 'Træd ind i din clean-girl era.' below the icon, smaller gray text 'Vanea er dit vanesystem til hverdagen — skabt til at hjælpe dig med at blomstre og leve som den rolige, balancerede version af dig selv.', and a lavender rounded button 'ÅBEN VANEA'. "
            "AROUND THE PHONE: four floating rounded photo cards positioned at corners: "
            "LEFT side: photo card showing person writing in journal, label 'Morgen & Aften Rutiner' in small white bold text on dark overlay. "
            "TOP RIGHT: photo card showing skincare products on marble surface, label 'Vanesporing'. "
            "BOTTOM RIGHT: photo card showing matcha/green tea in elegant glass, label 'Wellness Ritualer'. "
            "BELOW THE PHONE: a grid of small numbered lifestyle product photos (days 5-31) — candles, coffee cups, berries, skincare, scrunchies, flowers, yoga pose, smoothie bowl, avocado toast, plants, tote bag, slippers etc. Each with a small day number above. "
            "Dreamy, aesthetic, pastel pink/lavender. Square 1080x1080."
        ),
    },
    {
        "name": "that_girl_moodboard",
        "prompt": (
            "Create a square 1080x1080 aesthetic mood board collage image. "
            "BACKGROUND: a grid of real-looking aesthetic lifestyle photos arranged in a collage covering the entire image — approximately 3 columns and 4 rows of slightly overlapping photos: "
            "Photos include: woman with white towel on head drinking from glass, glass of lemon water with orange slices, woman in bed with laptop and notebook, woman with green clay face mask selfie, rainfall shower head with steam, skincare products on shelf, woman in white lying on bed relaxing, avocado toast with fried eggs, woman doing yoga, clean minimalist bedroom. "
            "Muted, moody, earthy green/beige/cream tones throughout all photos. "
            "CENTER OVERLAY: a large frosted white/translucent rounded rectangle card over the middle of the collage, with soft blur effect behind it. Card contains: "
            "Large italic dark serif font: 'Hemmeligheden bag \"That Girl\"?' "
            "Small gray text: 'Du behøver ikke motivation. Du har brug for struktur.' "
            "5 habit rows with small icons, bold name, small description, time on right: "
            "'Morgen  •  Aktiv — Start dagen med intention' "
            "'Hydrering — Drik et stort glas vand — 1 min ›' "
            "'Meditation — 5-10 min mindfulness — 10 min ›' "
            "'Morgenhudpleje — Rens, tone, fugt, SPF — 10 min ›' "
            "'Stræk eller yoga — 5-10 min blid bevægelse — 10 min ›' "
            "Bottom of card: small centered italic: 'Alt hvad du har brug for, allerede planlagt.' "
            "BOTTOM CENTER: black rounded App Store button 'Hent på App Store' with Apple logo, overlaid on the collage. "
            "Moody, aesthetic, earthy tones. Square 1080x1080."
        ),
    },
]

BATCH8_CONCEPTS = [
    {
        "name": "starter_forfra_mandag",
        "prompt": (
            "Create a square 1080x1080 Pinterest-style infographic. "
            "BACKGROUND: warm cream/off-white (#F5EFE6). "
            "TITLE at top in large bold dark italic serif font: 'Starter du forfra' then on next line in very large bold rose/dusty pink caps: 'HVER MANDAG?' with a short pink underline. "
            "Below title: four overlapping circular illustrated badges connected by a flowing line, alternating left-right: "
            "Circle 1 (left, large): illustrated woman in pink sports top with water bottle, confident pose. Below: bold dark text '1: ENERGI' small gray text 'Ny uge, klare intentioner.' "
            "Circle 2 (center, slightly lower): illustrated open planner/journal with goals list. Below: '2: EN PLAN' 'Store mål, konkrete skridt.' "
            "Circle 3 (right, large): illustrated calendar with an X marked. Below: '3: ET FEJLTRIN' 'Livet er dynamisk, fremgang er ikke lineær.' "
            "Circle 4 (right, lower): illustrated trash bin with 'Arkiv' label. Below: '4: BRYD MØNSTRET' 'Start ikke forfra. Juster.' "
            "Below the circles: a large rounded white card with soft drop shadow containing: "
            "Center title: '✦ VANEA ✦' in large rose pink caps, below it small caps: 'EN BEDRE MÅDE AT BYGGE ET LIV DU ELSKER.' "
            "Three columns inside the card: "
            "LEFT column header 'SMÅ VANER' — three green pill items: water drop 'Drik vand' / dumbbell 'Bevæg kroppen' / book 'Læs 10 sider' "
            "CENTER column header 'DAGLIG STREAK' — large circle with flame icon and '21' big text, 'dages streak' below, italic 'Fremgang, ikke perfektion.' "
            "RIGHT column header 'UGENS RUTINE' — list: 'MAN Træning ✓ / TIR Læs ✓ / ONS Hydrering ✓ / TOR Egenomsorg ✓ / FRE Dagbog ○ / LØR Bevæg ○ / SØN Planlæg ○' "
            "Bottom of card: three small icon+label items: leaf 'SMÅ VANER' / calendar 'DAGLIGE KRYDS' / chart 'ÆGTE KONSISTENS' "
            "BOTTOM TEXT: regular italic serif: 'Stop med at starte forfra.' bold italic: 'Byg rutiner der er en glæde at holde.' "
            "Two small heart outlines on sides. Center pink rounded button: 'HENT VANEA'. "
            "Warm cream, rose pink accents, elegant. Square 1080x1080."
        ),
    },
    {
        "name": "clean_girl_era_mockup",
        "prompt": (
            "Create a square 1080x1080 elegant app advertisement image. "
            "BACKGROUND: warm soft taupe/greige (#D4C5B5), smooth and clean. "
            "TITLE at top center in large bold dark serif font: 'Træd ind i din clean-girl era.' "
            "Below in small centered gray regular text: 'Skabt til at hjælpe dig med at blomstre, holde styr på tingene\\nog leve som den rolige, balancerede og bevidste version af dig selv.' "
            "CENTER: a realistic iPhone 15 Pro mockup in dark frame, portrait orientation. Phone screen shows a simple clean app — date 'Torsdag 3. april', bold italic 'Min Daglige Rutine ☀️', simple habit list with morning/afternoon/evening sections, gratitude prompts. "
            "FLOATING FROSTED GLASS CARDS around the phone: "
            "TOP LEFT card: 'Din stil' header, small lifestyle thumbnail images, 'Mål:' with pills 'Kom i form' 'Få styr på det' 'Føl dig tilpas' "
            "BOTTOM LEFT card: 'Vanesporing' header, a small calendar grid M T O T F L S with dates 1-31, some dates highlighted in rose. "
            "TOP RIGHT card: 'Udfordringer' header, list items with progress bars: '7-dages oprydning' / 'Digital detox' / 'Ny morgenrutine' "
            "BOTTOM RIGHT card: 'Ugentlig oversigt' and 'Streaks & fremgang' with a small upward trending line chart. "
            "BOTTOM: three soft rounded pill tags: 'Daglige rutiner' / 'Wellness ritualer' / 'Månedligt reset' "
            "Below that, small centered italic: 'Konsistens bliver let når dine vaner føles gode.' "
            "Warm taupe, soft elegant feel. Square 1080x1080."
        ),
    },
    {
        "name": "papirdagbog_vs_vanea",
        "prompt": (
            "Create a square 1080x1080 elegant comparison ad image. "
            "BACKGROUND: warm soft cream/greige (#EDE8E1). "
            "TITLE at top center: large bold dark serif font 'Papirdagbøger starter stærkt.' then on next line large bold rose/pink italic serif: 'Vanea holder dig i gang.' small sparkle star to the right. "
            "Below title, small centered gray text: 'Fra gode intentioner til daglig opfølgning.' "
            "MAIN SECTION: two columns side by side taking up top half: "
            "LEFT column — label 'PAPIRDAGBOG' in small bold caps gray. Photo of a taupe/beige linen journal with a sticky note showing handwritten to-do list 'stå tidligt op / drik vand / stræk / dagbog / vær produktiv' with pen on top. Warm cozy aesthetic. "
            "CENTER: bold dark text 'VS' between columns. "
            "RIGHT column — label 'VANEA APP' in small bold caps gray. A realistic iPhone mockup showing a clean habit tracker app interface with daily rituals list. Two small floating info cards beside the phone showing 'Ugentlig oversigt' and 'Streaks & fremgang' with a small chart. "
            "BOTTOM: a large white rounded rectangle card with four comparison rows, each row has: left side pink/rose icon + gray text, center dark arrow →, right side green icon + dark text: "
            "'📅 Tomme ugeskemaer → 📅 Daglige rutiner' "
            "'✏️ Svær at opdatere → ⚡ Hurtige kryds' "
            "'○ Intet overblik → 📈 Streaks og fremgang' "
            "'⏰ Glemt efter en uge → 🔔 Daglige påmindelser' "
            "Below the card, small centered italic serif: 'Konsistens og forandring føles let når dine redskaber støtter dig. ♡' "
            "BOTTOM: two side-by-side buttons — left: cream outlined rounded button 'Hent nu', right: black App Store button 'Hent på App Store' with Apple logo. "
            "Warm cream, elegant, soft. Square 1080x1080."
        ),
    },
]

BATCH9_CONCEPTS = [
    {
        "name": "that_girl_telefon_mockup_v2",
        "prompt": (
            "Create a square 1080x1080 lifestyle app advertisement image. "
            "BACKGROUND: soft pink-to-lavender gradient (#FFE4EC to #E8D5F5), very soft and dreamy. "
            "CENTER TOP: a realistic iPhone 15 Pro mockup in rose gold/pink frame, portrait orientation, taking up about 50% of the image height. The phone screen shows a simple clean app interface with: a small sunrise/sun icon at top, bold dark text 'Træd ind i din clean-girl era.' below the icon, smaller gray text 'Vanea er dit vanesystem til hverdagen — skabt til at hjælpe dig med at blomstre og leve som den rolige, balancerede version af dig selv.', and a lavender rounded button 'ÅBEN VANEA'. "
            "AROUND THE PHONE: three floating rounded photo cards: "
            "LEFT side: photo card showing hands writing in journal in cozy pink setting, label 'Morgen & Aften Rutiner' in small white bold text on dark overlay. "
            "TOP RIGHT: photo card showing skincare products on marble surface, label 'Vanesporing'. "
            "BOTTOM RIGHT: photo card showing matcha/green smoothie in elegant glass, label 'Wellness Ritualer'. "
            "BELOW THE PHONE: a grid of small square lifestyle product photos arranged in TWO rows. Each photo has a single small number in a white circle in the top-left corner. The numbers go in order from 5 to 31, each number appearing EXACTLY ONCE, left to right, top to bottom: "
            "Row 1: 5(candles), 6(latte cup), 7(berries bowl), 8(skincare products), 9(scrunchie), 10(pink flowers), 11(woman yoga), 12(smoothie bowl), 13(nail polish) "
            "Row 2: 14(acai bowl), 15(pink smoothie), 16(avocado toast), 17(plant), 18(tote bag), 19(slippers), 20(pink flower), 21(journal), 22(diffuser sticks), 23(cozy socks) "
            "Numbers must be sequential and unique — 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 only shown once each. "
            "Dreamy, aesthetic, pastel pink/lavender. Square 1080x1080."
        ),
    },
]

BATCH10_CONCEPTS = [
    {
        "name": "starter_pack_broderi_v2",
        "prompt": (
            "Create a square 1080x1080 image styled to look like embroidered fabric patches on a linen/canvas background. "
            "BACKGROUND: warm off-white linen/canvas texture (#E8E0D0), slightly wrinkled like real fabric. "
            "TITLE at top in large bold dark olive green embroidered-style serif font: 'That Girl\\nStarter Pack' "
            "Below: four embroidered patch items arranged in a 2x2 grid: "
            "TOP LEFT — circular patch with olive green embroidered border: inside, a realistic embroidered matcha latte cup with latte art and steam. Below the cup, bold embroidered caps text: 'MATCHA' "
            "TOP RIGHT — rounded square patch with dusty rose/pink embroidered border: inside, an embroidered woman in white workout clothes holding a pilates ball, sitting on floor. Below, bold caps: 'PILATES' "
            "BOTTOM LEFT — octagon patch with gold/mustard embroidered border: inside, an embroidered open journal/notebook with a daisy flower and pen. Below, bold caps: 'DAGBOG' "
            "BOTTOM RIGHT — rounded rectangle patch with sage green embroidered border: inside, a realistic embroidered smartphone showing a simple habit tracker app interface. Below, bold caps: 'TRACK MED VANEA' "
            "All patches look like real embroidered fabric badges — textured stitching, slightly raised look, warm muted colors. "
            "No phone mockups beyond the embroidered phone. Square 1080x1080."
        ),
    },
]

BATCH11_CONCEPTS = [
    {
        "name": "that_girl_kalender_v2",
        "prompt": (
            "Create a square 1080x1080 image styled like a lifestyle app screenshot/ad. "
            "BACKGROUND: warm off-white/cream (#F5F0EB). "
            "TOP LEFT: small gray back arrow '‹' followed by '2025' in gray. "
            "Below that, large bold rose/dusty pink italic serif font: 'Træd ind i din\\n\"That Girl\" era' "
            "Below: a calendar grid in light gray. Column headers in small bold caps: 'M  T  O  T  F  L  S' (Danish weekday initials — Mandag, Tirsdag, Onsdag, Torsdag, Fredag, Lørdag, Søndag). Below headers, show dates 1-6 on first row, then 7-13, 14-20, 21-27, 28-31. Dates in small gray numbers. "
            "ABOVE THE CALENDAR IMAGES: a frosted white semi-transparent rounded rectangle card overlaid on the upper portion of the calendar, containing: "
            "Italic serif title: 'Hemmeligheden bag \"That Girl\"?' "
            "Small gray subtitle: 'Du behøver ikke motivation. Du har brug for struktur.' "
            "A list of 5 habit rows, each with a small rose flower icon on left, bold habit name, small gray description, and small gray time on right: "
            "'Morgen  •  Aktiv — Start dagen med intention — 0' "
            "'Hydrering — Drik et stort glas vand — 1 min ›' "
            "'Meditation — 5-10 min mindfulness — 10 min ›' "
            "'Morgenhudpleje — Rens, tone, fugt, SPF — 10 min ›' "
            "'Stræk eller yoga — 5-10 min blid bevægelse — 10 min ›' "
            "Bottom of card in small centered gray italic: 'Alt hvad du har brug for, allerede planlagt.' "
            "BELOW THE FROSTED CARD, filling the lower portion of the calendar grid: small square lifestyle product photos placed at the lower calendar date positions (dates 19-31 area) — a gold sun necklace, dried pink flowers, folded towels, smoothie bowl, sage bundle, candle, pink flower. These photos sit BELOW the white card, inside the calendar grid area. "
            "On the left side of the calendar (outside the card): a few small lifestyle photos stacked vertically — a candle, a matcha cup, a meditation cushion, a skincare product tube. "
            "On the right side: a few small lifestyle photos — a succulent plant, a necklace, dried flowers, folded towels. "
            "BOTTOM: bold small caps centered text: '31 DAGE OG FREMAD' "
            "Below that: a black rounded App Store button 'Hent på App Store' with Apple logo. "
            "Elegant, clean, warm cream. Square 1080x1080."
        ),
    },
]

CALM_STYLE_CONCEPTS = [
    {
        "name": "calm_find_dig_selv_igen",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'Finding Yourself Back Routine' ad. "
            "BACKGROUND: a moody dark nature photo — dark green water/pond with white daisy flowers at the bottom edge of the image. A dark semi-transparent overlay covers most of the image so white text is clearly readable. "
            "LAYOUT top to bottom: "
            "TOP SECTION centered white text: very large bold white title in two lines: 'FIND DIG SELV IGEN RUTINEN'. Below that, smaller white italic subtitle: 'Alt efter hvad du har mistet'. Below that, a thin horizontal white divider line spanning the width. "
            "MIDDLE SECTION: four equal columns side by side, each inside a dark semi-transparent rounded rectangle card. Small compact white text inside each card. "
            "Column 1 — bold white header: 'DEN TABTE STEMME'. Small white italic: '(People-pleaser)'. Bullet points in small white text: '• 07.00 Stå op' '• 10.00–12.00 Giv én ærlig mening til kende' '• 12.00 Spis frokost uden at undskylde' '• 14.00–16.00 Sig \"nej\" til en lille anmodning' '• 18.00–19.00 Stop med at analysere andres humør' '• 23.00 Gå i seng'. "
            "Column 2 — bold white header: 'DEN TABTE FORBINDELSE'. Small white italic: '(Somatisk)'. Bullet points: '• 06.30 Stå op og mærk tyngden fra din dyne' '• 08.00–12.00 Slap af i kæbe og skuldre' '• 13.00–17.00 Læg skærmen fra dig et øjeblik' '• 20.30 Mærk efter i kroppen' '• 22.30 Gå i seng'. "
            "Column 3 — bold white header: 'DEN TABTE GNIST'. Small white italic: '(Robotten)'. Bullet points: '• 06.30 Stå op, uden at tage stilling til noget' '• 07.00 Lad følelserne komme, uden at tvinge dem væk' '• 09.00–12.00 Løs en simpel opgave uden panik' '• 16.00–17.00 Gør noget kun for din egen skyld' '• 18.00–19.00 Vær tryg i eget selskab' '• 22.30 Gå i seng'. "
            "Column 4 — bold white header: 'DEN TABTE AUTENTICITET'. Small white italic: '(Masken)'. Bullet points: '• 07.30 Stå op' '• 10.00–12.00 Stop med at øve dine sætninger' '• 17.00–18.00 Lad nogen se den rigtige dig' '• 18.00–21.00 Tag den tunge facade af' '• 23.30 Gå i seng'. "
            "BOTTOM: white daisy flowers visible through the dark photo at the very bottom. No button. "
            "Style: dark atmospheric nature photo, white text, dark rounded boxes for each column, exactly like the Calm wellness ad. Portrait 1080x1920."
        ),
    },
]

CALM_STYLE_CONCEPTS_2 = [
    {
        "name": "calm_jeg_savner_den_jeg_var",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'I Miss The Person I Used To Be' ad. "
            "BACKGROUND: a moody atmospheric nature photo — a forest path with tall trees and soft misty light filtering through from above, like early morning fog in a green forest. A lone person walks away from the camera down the path. Dark, cinematic, emotional. "
            "A subtle dark overlay makes the text clearly readable against the photo. "
            "TEXT layout centered on the image: "
            "TOP CENTER: very large bold white text in caps, three lines taking up the top third of the image: 'JEG SAVNER\\nDEN JEG\\nENGANG VAR' "
            "BELOW that, centered medium white regular text with generous line spacing — NOT bold, softer weight: "
            "'Jeg plejede at være til stede. Levende.\\n"
            "Nu føles de ting jeg elskede bare tomme.\\n"
            "Jeg venter bare på at dagen skal slutte.\\n"
            "En veninde anbefalede Vanea.\\n"
            "En app? Til vaner??\\n"
            "Jeg troede ikke det ville gøre en forskel.\\n"
            "Jeg forstår ikke helt hvorfor det virker.\\n"
            "Men noget skete.\\n"
            "Tågen lettede. For første gang i måneder\\n"
            "følte jeg mig som mig selv igen.' "
            "Style: exactly like the Calm 'I Miss The Person I Used To Be' ad — dark moody forest photo, large bold caps headline, softer regular body text below, all white. Portrait 1080x1920. No logo, no button."
        ),
    },
]

CALM_STYLE_CONCEPTS_3 = [
    {
        "name": "calm_jeg_savnede_mig_selv",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'I Missed Me. So I Went And Got Her Back' ad. "
            "BACKGROUND: a beautiful floral pattern covering the entire image — soft blue/teal background with colorful hand-painted flowers: pink tulips, white daisies, orange flowers, green leaves scattered all over, very dense and pretty, like a vintage floral wallpaper. "
            "CENTER: a large cream/ivory ornate rounded rectangle card in the middle of the image, with a decorative vintage border/frame around it (thin ornate lines). The card has a soft cream/off-white background. "
            "Inside the card, all text centered: "
            "HEADLINE in very large bold dark burgundy/dark purple font, three lines: 'JEG SAVNEDE MIG SELV.\\nSÅ JEG GIK UD\\nOG FIK HENDE TILBAGE.' "
            "Below headline, medium regular dark text with comfortable line spacing: "
            "'Jeg savner pigen der grinte ad sine egne jokes.\\n"
            "Sagde ja til tingene. Dansede mens hun lavede mad.\\n"
            "Bag alt stressen forsvandt hun stille og roligt. Hun blev stille.\\n"
            "Det mest skræmmende? Jeg lagde ikke engang mærke til at hun var væk.\\n"
            "En veninde fortalte mig om Vanea.\\n\\n"
            "Jeg troede ikke en vane-app kunne bringe mig tilbage.\\n"
            "Men den her var anderledes.\\n"
            "Jeg begyndte bare med én vane ad gangen —\\n"
            "og for første gang i lang tid\\n"
            "begyndte jeg at føle mig som mig selv igen.' "
            "The word 'Vanea' should be bold inside the body text. "
            "Style: exactly like the Calm floral ad — dense colorful floral background, ornate cream card center, dark burgundy/purple headline, dark regular body text. Portrait 1080x1920. No button."
        ),
    },
]

CALM_STYLE_CONCEPTS_4 = [
    {
        "name": "calm_overstimulerede_kvinder",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'Overstimulated Women' ad. "
            "BACKGROUND: a bold red/dark red African-inspired wax print fabric pattern covering the entire image — dense geometric and floral shapes in deep red, burgundy, black and gold, like a kente or ankara fabric texture. Very bold and eye-catching. "
            "CENTER: a large cream/ivory rounded rectangle card overlaid on the patterned background, with a soft gradient from cream at top to light pink at bottom inside the card. "
            "Inside the card, all text centered: "
            "HEADLINE at top in very large bold black hand-drawn/marker style font, three lines — the text fills the full width of the card: 'OVERSTIMULEREDE KVINDER\\nHAR IKKE BRUG FOR MERE HVILE.\\nDE HAR BRUG FOR ET SYSTEM' "
            "Below headline, bold black centered text: 'VI LEDER EFTER KVINDER I ALDEREN 35–55' "
            "Below that, regular dark centered text: 'der er klar til at prøve at bygge vaner med Vanea — og bevæge sig fra at føle sig udmattede til at føle sig rodfæstede og lettede.' "
            "Below that, three bold/regular lines with generous spacing: "
            "'I starten: Den fysiske spænding i kroppen begynder at løsne sig.' "
            "'Efter et par uger: Behovet for at komme sig efter alt begynder at aftage.' "
            "'Over tid: Du holder op med at vente på det næste, der sker — og begynder at leve igen.' "
            "The labels 'I starten:' 'Efter et par uger:' 'Over tid:' should be bold, the rest regular. "
            "Bottom of card in very large bold black text, two lines: 'TRYK PÅ SKÆRMEN\\nOG KOM I GANG!' "
            "Style: exactly like the Calm overstimulated women ad — bold red African wax print background, cream-to-pink card, large bold hand-drawn headline font, clean body text. Portrait 1080x1920."
        ),
    },
]

CALM_STYLE_CONCEPTS_5 = [
    {
        "name": "calm_du_sover_nok",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'Getting Enough Sleep But Still Feeling Completely Drained? Same.' ad. "
            "BACKGROUND: a dark moody photo of a nightclub or concert scene — deep purple and pink neon lights, bokeh green and pink light dots scattered, a dark silhouette of a person visible, very atmospheric and dark. "
            "A subtle dark overlay makes the text clearly readable. "
            "All text is white, centered on the image. "
            "TOP: very large bold white text in caps, three lines: 'DU SOVER NOK\\nMEN VÅGNER STADIG\\nHELT UDMATTET?' "
            "Below that, same large bold white caps: 'DET KENDER JEG.' "
            "Below that, medium regular white text with generous line spacing: "
            "'Plot twist: Det er ikke altid søvnen, der er problemet.\\n"
            "Når du har for mange ting at holde styr på uden overblik,\\n"
            "kan dit nervesystem aldrig rigtig falde til ro\\n"
            "— og så føles alt uoverskueligt,\\n"
            "selv efter en god nats søvn.' "
            "Below that, medium regular white text: "
            "'Med Vanea kan du opbygge små daglige vaner\\n"
            "og holde styr på dem over tid — så du får det overblik,\\n"
            "der gør, at du rent faktisk kan slappe af.' "
            "Below that, large bold white italic text: "
            "'Prøv det i dag, og se hvordan\\ndet ændrer resten af din uge.' "
            "Style: exactly like the Calm sleep ad — dark neon nightclub background, large bold caps headline, softer regular body text, all white. Portrait 1080x1920. No button."
        ),
    },
]

CALM_STYLE_CONCEPTS_6 = [
    {
        "name": "calm_autopilot_paamindelse",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'Gentle reminder' ad with the star/light burst background. "
            "BACKGROUND: a dramatic dark space/warp speed photo — dark black background with colorful streaks of light bursting outward from the center like a star warp or speed of light effect. Colors: teal/cyan, orange, gold, blue streaks radiating outward. Very dramatic and atmospheric. "
            "At the very top of the image: a thin light gray iOS status bar UI showing '< All iCloud' on the left and a share icon and '...' on the right — exactly like an iPhone Notes screenshot header. "
            "All text is white, centered on the image, with generous line spacing between each paragraph: "
            "'En venlig påmindelse om, at det ikke er normalt\\nat gå gennem dagene på autopilot\\nog føle, at dit liv ikke helt er dit eget.' "
            "[large gap] "
            "'Derfor har vi lavet Vanea — et simpelt system\\ntil daglige vaner, der hjælper dig med at komme\\ntilbage til dig selv. Ét lille kryds ad gangen.' "
            "[large gap] "
            "'Ikke terapi. Ikke et kursus.\\nBare en konkret struktur, der kan hjælpe dig\\nmed at føle dig til stede igen.' "
            "[large gap] "
            "Large bold white italic text: 'Prøv det i dag.' "
            "Style: exactly like the Calm gentle reminder ad — dark warp speed light burst background, iOS Notes header at top, centered white text, no decorations. Portrait 1080x1920."
        ),
    },
]

CALM_STYLE_CONCEPTS_7 = [
    {
        "name": "calm_jeg_savnede_mig_selv_solnedgang",
        "prompt": (
            "Create a square 1080x1080 social media image styled exactly like the Calm 'I Missed Me So I Went And Got Her Back' dramatic sunset ad. "
            "BACKGROUND: a dramatic warm sunset photo — deep orange, amber and red sky with clouds, the silhouette of a woman's head/hair visible at the top center of the image against the glowing sky. Very cinematic and emotional. "
            "TEXT layout: "
            "TOP: a white rectangular highlight/banner behind the first line of text. Inside the banner in very large bold dark brown/rust caps: 'JEG SAVNEDE MIG SELV' "
            "Below the banner, very large bold white caps text, two lines: 'SÅ JEG BYGGEDE\\nMIG SELV OP IGEN' "
            "Below that, medium regular white text centered with comfortable line spacing: "
            "'Jeg savnede pigen, der grinede ad sine egne jokes.\\n"
            "Sagde ja til ting. Dansede, mens hun lavede mad.\\n"
            "Under alt stresset blev hun stille.\\n"
            "Det mest skræmmende?\\n"
            "Jeg lagde ikke engang mærke til, at hun var væk.\\n\\n"
            "En veninde fortalte mig om Vanea.\\n"
            "Et system til daglige vaner?\\n"
            "Jeg forventede ikke meget.\\n"
            "Men lidt efter lidt begyndte dagene\\n"
            "at føles mere overskuelige.\\n\\n"
            "Og jeg begyndte at føle mig som mig selv igen.' "
            "Style: exactly like the Calm sunset ad — dramatic warm orange/red sunset background, woman silhouette, white highlight box on first line, large bold white caps headline, softer white body text. Square 1080x1080."
        ),
    },
]

CALM_STYLE_CONCEPTS_8 = [
    {
        "name": "calm_mist_ikke_retningen",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image styled exactly like the Calm app 'Gentle reminder' ad with the star warp background. "
            "BACKGROUND: a dramatic dark space/warp speed photo — pure black background with white streaks of light bursting outward from the center like stars at warp speed. Only white/light gray streaks on black — monochrome and dramatic. "
            "At the top of the image: a thin iOS status bar UI showing '< All iCloud' on the left and a share icon and '...' on the right — exactly like an iPhone Notes screenshot header. "
            "All text is white, centered on the image, with very generous line spacing between each paragraph: "
            "First paragraph in medium regular white text: "
            "'En venlig påmindelse om, at du ikke bare skal\\nacceptere at miste din retning, føle dig fastlåst\\nog ikke vide, hvem du er ved at blive.' "
            "[large gap] "
            "Second paragraph in medium regular white text: "
            "'Derfor har vi skabt Vanea — et simpelt system\\ntil daglige vaner, der giver dig struktur,\\nnår alt andet føles kaotisk.' "
            "[large gap] "
            "Third paragraph in medium regular white text: "
            "'Ikke terapi. Ikke et kursus.\\nBare en konkret struktur, der kan hjælpe dig\\nmed at finde fodfæste igen.' "
            "[large gap] "
            "Last line in large bold white italic text: 'Prøv det i dag.' "
            "Style: exactly like the Calm warp speed gentle reminder ad — black background with white light streaks, iOS Notes header, centered white text, clean and minimal. Portrait 1080x1920."
        ),
    },
]

CALM_STYLE_CONCEPTS_9 = [
    {
        "name": "calm_burnout_hverdag",
        "prompt": (
            "Create a portrait 1080x1920 social media Story image that looks EXACTLY like the Calm app 'Burnout isn't about working too hard' ad. Copy the layout, spacing, and text sizes precisely. "
            "BACKGROUND: smooth gradient — warm cream/ivory at the very top and bottom, soft coral/salmon pink in the middle third. Gentle and warm. "
            "IMPORTANT: All text must be small and compact — NOT filling the whole image. There must be large empty margins on all sides and generous white space between sections, exactly like the original Calm ad. The text takes up only the center portion of the image with lots of breathing room. "
            "All text centered, dark near-black color. "
            "TOP — small compact headline: 'BURNOUT' in large bold hand-drawn marker font. Below that: 'DET HANDLER IKKE OM AT ARBEJDE FOR MEGET —' in medium bold hand-drawn marker font. Below that: 'Det handler om at miste grebet om sin egen hverdag' in a natural cursive handwriting script font (like Caveat or Pacifico) — the handwriting looks organic and slightly wavy/uneven as if written by hand with a pen, each letter connecting naturally, the baseline gently undulating. This cursive section is italic and significantly smaller than the bold lines above it. "
            "Large empty gap. "
            "MIDDLE — small bold text: 'VI LEDER EFTER FOLK I ALDEREN 35–55'. "
            "Below, small regular text: 'der er klar til at opbygge daglige vaner med Vanea — og bevæge sig fra at føle sig overvældede til at føle sig stærke og handlekraftige.' "
            "Large empty gap. "
            "Three small paragraphs: 'I starten: Du begynder at få overblik over det, der før føltes uoverskueligt.' then 'Efter et par uger: Følelsen af konstant at løbe bagud begynder at aftage.' then 'Over tid: Du får kontrollen tilbage — og med den, dig selv.' Labels bold, rest regular. "
            "Large empty gap. "
            "BOTTOM — medium bold text, two lines: 'TRYK PÅ SKÆRMEN\\nOG KOM I GANG!' "
            "Style: cream-to-coral gradient, small compact text with LOTS of white space and margins, hand-drawn headline, cursive subtitle — identical proportions and spacing to the Calm burnout ad. Portrait 1080x1920."
        ),
    },
]

RETINOL_CONCEPTS = [
    {
        "name": "retinol_vs_indkapslet_split",
        "prompt": (
            "Create a square 1080x1080 split-screen skincare comparison infographic. "
            "LAYOUT: two equal vertical halves side by side. "
            "LEFT HALF: dark charcoal background (#1C1C1C). All text white. "
            "RIGHT HALF: warm cream background (#FAF6F0). All text dark charcoal. "
            "A thin vertical dividing line in the center. "
            "All text must be SMALL and compact — headers around 18-20px, descriptions around 12-13px — so everything fits neatly without wrapping awkwardly. "
            "'Indkapslet retinol' must fit on ONE single line in the right header. "
            "LEFT HALF (top to bottom, white text, small font): "
            "Bold header: 'Retinol' "
            "Then three rows, each with: a small relevant flat icon/illustration, a bold subheader, and a short description: "
            "Row 1 — Icon: a small flat cross-section of skin showing molecules sitting only on the very top surface layer (not penetrating). Subheader: 'Bliver mest på overfladen'. Description: 'Ubeskyttet retinol frigives i det yderste hudlag og når sjældent ned i dybden.' "
            "Row 2 — Icon: a small burst/explosion symbol or a sudden release wave icon showing immediate release. Subheader: 'Frigives på én gang'. Description: 'Hele dosis frigives på én gang, og huden reagerer med rødme og irritation.' "
            "Row 3 — Icon: a small flat icon of skin surface with peeling/flaking top layer. Subheader: 'Forcerer huden udefra'. Description: 'Tvinger de øverste hudceller til at skalle af i højt tempo.' "
            "RIGHT HALF (top to bottom, dark text, small font): "
            "Bold header: 'Indkapslet retinol' — must be on ONE line, smaller font if needed. "
            "Then three rows, each with: a small relevant flat icon/illustration, a bold subheader, and a short description: "
            "Row 1 — Icon: a small flat cross-section of skin showing small round spherical capsules (NOT pills — smooth round spheres like microspheres) with arrows pointing downward into the deeper dermis layer. Subheader: 'Trænger ned i de dybere hudlag'. Description: 'Beskyttet af kapslen når retinolen sikkert ned i dybden, hvor kollagenet dannes.' "
            "Row 2 — Icon: a small gentle wave or slow-release curve icon, or a small hourglass/timer suggesting gradual release over time. Subheader: 'Frigives langsomt'. Description: 'Frigives langsomt over tid, så huden aldrig bliver irriteret.' "
            "Row 3 — Icon: a small flat icon of new cell layers building upward from the bottom of the skin, arrows pointing upward, suggesting regeneration from within. Subheader: 'Genopbygger indefra'. Description: 'I dybden sætter den gang i cellefornyelsen og skubber nye celler op mod overfladen.' "
            "Style: clean minimal scientific skincare infographic. Small compact text. Flat simple icons, not overdone. Dark left / light right. Square 1080x1080."
        ),
    },
]

RETINOL_CONCEPTS_2 = [
    {
        "name": "retinol_vs_indkapslet_v2",
        "prompt": (
            "Create a square 1080x1080 split-screen skincare comparison infographic. "
            "LAYOUT: two equal vertical halves side by side. "
            "LEFT HALF: dark charcoal background (#1C1C1C). All text white. "
            "RIGHT HALF: warm cream background (#FAF6F0). All text dark charcoal. "
            "A thin vertical dividing line in the center. "
            "LEFT HALF — 'Retinol' side (dark, white text): "
            "Bold header at top: 'Retinol' "
            "Three rows below, each with a small flat scientific icon and a short bold label — NO long descriptions, just the label text: "
            "Row 1 — Icon: flat skin cross-section with molecules sitting only on the very top surface, not penetrating. Label: 'Bliver mest på overfladen' "
            "Row 2 — Icon: a burst/flash symbol showing sudden release. Label: 'Frigives på én gang og skaber rødme og irritation' "
            "Row 3 — Icon: skin surface with peeling/flaking top layer. Label: 'Forcerer huden udefra' "
            "RIGHT HALF — 'Indkapslet retinol' side (cream, dark text): "
            "Bold header at top: 'Indkapslet retinol' — on ONE single line. "
            "Three rows below, each with a small flat scientific icon and a short bold label: "
            "Row 1 — Icon: flat skin cross-section with small smooth round microspheres (NOT pills) with arrows pointing deep into dermis. Label: 'Trænger ned i de dybere hudlag' "
            "Row 2 — Icon: a gentle slow wave or hourglass suggesting gradual release. Label: 'Frigives langsomt så huden aldrig bliver irriteret' "
            "Row 3 — Icon: arrows pointing upward from deep skin layers showing cell renewal from within. Label: 'Genopbygger indefra' "
            "Style: clean minimal scientific skincare infographic. Large clear icons, short bold labels only — no long body text. Dark left / light right. Square 1080x1080."
        ),
    },
]

BARRIER_DEFENSE_CONCEPTS = [
    {
        "name": "barrier_defense_ecooking_stil_v3",
        "prompt": (
            "Create a portrait 1080x1920 skincare product advertisement. "
            "Copy this EXACT layout from a reference Ecooking ad: "
            ""
            "BACKGROUND: solid muted dusty blue (#5B7FA6) covering the entire image. "
            ""
            "TOP SECTION — upper ~30% of the image, left-aligned with ~80px left padding: "
            "First line: tiny uppercase label with wide letter-spacing, white, very small font (~22px): 'BARRIER DEFENSE' "
            "Second element: a very large bold serif headline in white (~75px, bold, serif like Playfair Display or Georgia), left-aligned, spanning 3-4 lines: 'Indkapslet retinol, der reparerer din barriere, mens den fornyer huden indefra' "
            "Generous whitespace below the headline before the product section begins. "
            ""
            "MIDDLE SECTION — center ~55% of the image height: "
            "LEFT part (~55% of image width): the Kjeldgaard Barrier Defense product — a tall teal/turquoise glass dropper bottle with gold dropper cap, displayed large, centered in this left area. The bottle should be prominent and beautiful against the blue background. "
            "RIGHT part (~45% of image width), positioned vertically alongside the bottle: "
            "A vertical dotted white line runs down the center of this right area. "
            "3 large filled white circle dots along this dotted line, spaced evenly. "
            "Next to each dot, left-aligned white text: "
            "Dot 1 at top: Bold white text (~32px): 'Trænger ned i de dybere hudlag' — then on next lines, smaller regular white text (~26px): 'Beskyttet af kapslen når retinolen sikkert ned i dybden, hvor kollagenet dannes.' "
            "Dot 2 middle: Bold white text: 'Frigives langsomt' — smaller: 'Frigives langsomt over tid, så huden ikke bliver irriteret og rød.' "
            "Dot 3 bottom: Bold white text: 'Genopbygger indefra' — smaller: 'I dybden sætter den gang i cellefornyelsen og skubber nye celler op mod overfladen.' "
            ""
            "BOTTOM SECTION — lower ~15%: empty blue space. At the very bottom, very small white text centered: 'Klinisk testet * udviklet af dermatologer * 17.000+ danske kvinder' "
            ""
            "Style: clean premium skincare editorial. All text white. Blue background. Lots of breathing room. The layout is: [big serif headline at top] then [product photo left + dotted timeline right] — NOT two separate columns, the headline spans full width at the top. Portrait 1080x1920."
        ),
    },
]

SOCIAL_PROOF_CONCEPTS = [
    {
        "name": "kjeldgaard_social_proof_v2_no_product",
        "prompt": (
            "Create a square 1080x1080 premium skincare advertisement. NO product photo — the right side is intentionally left as clean empty background space. "
            ""
            "BACKGROUND: soft warm light gray gradient (#EBEBEB center fading to #D8D8D8 edges), very subtle, clean and airy. "
            ""
            "TOP RIGHT CORNER: brand name 'Kjeldgaard' in elegant medium-weight serif font, dark charcoal (#1C1C1C), font size ~28px. Below it a thin horizontal line ~60px wide. Positioned top-right with ~50px padding from edges. "
            ""
            "TOP LEFT AREA (~left 55% of image, starting ~60px from top and left): "
            "Large bold italic serif quote in dark charcoal. Font size ~58px. 3 lines of text: "
            "Line 1: '“Rynkerne retter' "
            "Line 2: 'sig nærmest' "
            "Line 3: 'bare ud.”' "
            "Generous line-height. Left-aligned. "
            "~25px below the quote: small uppercase text 'LIZZI, ÆGTE KUNDE' in very small font ~18px, wide letter-spacing 3px, light charcoal (#555555). "
            ""
            "CENTER-LEFT AREA (below the quote block, left-aligned): "
            "Very large bold sans-serif number: '+18.000' — font size ~88px, very bold, dark charcoal. "
            "Immediately below: 'glade kunder' — bold serif ~34px, dark charcoal. "
            "Below that: 5 gold stars in a row '★★★★★' — gold color (#D4A017), font size ~34px. "
            "Plenty of whitespace between these elements — do NOT crowd them together. "
            ""
            "LOWER LEFT (well below the stars, ~80px gap): "
            "A small sunburst/rosette seal badge icon (~55px) with a checkmark, dark charcoal outline. To the right of the badge: "
            "'100% tilfredshedsgaranti' in small bold text ~20px "
            "'eller dine penge tilbage!' in small regular text ~20px "
            ""
            "BOTTOM BAR: a clean white rectangle strip ~110px tall spanning the full width at the very bottom. Inside, centered: 'KLINISK TESTET  ·  UDVIKLET AF DERMATOLOGER' in bold uppercase dark charcoal, wide letter-spacing, font size ~22px. "
            ""
            "CRITICAL: lots of whitespace everywhere. Elements are small and spread out, NOT big and cramped. The right 45% of the image (excluding the brand name) is intentionally empty clean background — no product, no text there. Elegant, minimal, premium. Square 1080x1080."
        ),
    },
]

TEMPLATE_CONCEPTS = [
    {
        "name": "kjeldgaard_template_karina",
        "prompt": (
            "Create a square 1080x1080 skincare advertisement that looks EXACTLY like this reference layout: "
            ""
            "BACKGROUND: warm dark brownish-taupe gradient — dark brown/mocha at the top (#3D2E28), softening to a warm light beige/cream at the bottom (#E8DDD4). Smooth gradient from top-dark to bottom-light. "
            ""
            "TOP LEFT: brand logo 'KJELDGAARD' in small bold serif/caps font, white, with a small K-monogram or stylized K before it. ~22px, top-left corner with ~50px padding. "
            ""
            "LEFT SIDE (takes up ~55% of image width): "
            "Large bold white quote text, left-aligned, ~60px bold sans-serif or serif, generous line-height: "
            '"Jeg droppede natcremen og dagcremen — nu bruger jeg kun ét produkt" '
            "The quote fills about 3-4 lines. "
            "Below the quote: 6 gold star icons in a row ★★★★★★, gold color (#FFB800), ~32px. "
            "Below the stars: white text '- KARINA' in medium weight, ~22px, with a dash before the name. "
            ""
            "BOTTOM LEFT: a round navy blue rosette/badge seal (~140px diameter) with text around the edge and bold text inside: "
            "Around the top edge: 'PENGENE TILBAGE' "
            "Center large bold: '60' very large, 'DAGE' below it "
            "Around the bottom edge: 'GARANTI' "
            "Stars on left and right sides of the badge. Navy blue badge (#1B3A6B) with white text. "
            ""
            "RIGHT SIDE (~45% of image width): a realistic photo of a hand (feminine, light skin) holding a teal/turquoise frosted glass dropper bottle with gold cap. The dropper is being held upright with the cap/dropper being pulled out from above by another hand. The bottle has 'KJELDGAARD' and 'BARRIER DEFENSE' text on it. The hand and bottle are large, filling the right half of the image. "
            ""
            "Style: premium skincare ad, dark warm gradient background, white bold text left side, product photo right side, navy guarantee badge bottom-left. Square 1080x1080."
        ),
    },
]

ACTIVE_CONCEPTS = TEMPLATE_CONCEPTS


def generate_image(concept: dict, index: int):
    print(f"\n[{index+1}/{len(ACTIVE_CONCEPTS)}] Generating: {concept['name']}...")
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": concept["prompt"]}],
                "modalities": ["image", "text"],
            },
        )
        response.raise_for_status()
        data = response.json()

        # Extract image from response — image is in message.images[]
        for choice in data.get("choices", []):
            message = choice.get("message", {})
            for img_part in message.get("images", []):
                if img_part.get("type") == "image_url":
                    url = img_part["image_url"]["url"]
                    if url.startswith("data:"):
                        b64 = url.split(",", 1)[1]
                        img_bytes = base64.b64decode(b64)
                        out_path = OUTPUT_DIR / f"{RUN_STAMP}_{concept['name']}.png"
                        out_path.write_bytes(img_bytes)
                        print(f"    Saved: {out_path}")
                        return out_path

        print(f"    No image found. Response: {json.dumps(data, indent=2)[:300]}")
        return None
    except Exception as e:
        print(f"    ERROR generating {concept['name']}: {e}")
        return None


def main():
    print("=" * 50)
    print("Vanea Ad Generator — powered by OpenRouter + Gemini 3.1 Flash Image")
    print("=" * 50)
    print(f"Output folder: {OUTPUT_DIR}")

    results = []
    for i, concept in enumerate(ACTIVE_CONCEPTS):
        path = generate_image(concept, i)
        results.append({"concept": concept["name"], "path": str(path) if path else None})

    print("\n" + "=" * 50)
    print("DONE. Generated images:")
    for r in results:
        status = "OK" if r["path"] else "FAILED"
        print(f"  [{status}] {r['concept']}: {r['path'] or 'not generated'}")

    log_path = OUTPUT_DIR / "run_log.json"
    with open(log_path, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2)
    print(f"\nLog saved to: {log_path}")
    print(f"\nOpen the output folder to review your 3 ad images.")


if __name__ == "__main__":
    main()
