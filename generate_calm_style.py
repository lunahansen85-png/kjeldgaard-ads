#!/usr/bin/env python3
import os, base64, requests
from pathlib import Path
from datetime import datetime

API_KEY = "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"

OUTPUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL = "google/gemini-3.1-flash-image"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

prompt = """Create a portrait 1080x1920 social media image that looks EXACTLY like the Calm app ad called 'Finding Yourself Back Routine'.

BACKGROUND: A moody dark nature photo — dark green water or pond with white daisy flowers floating/growing at the bottom. The photo fills the entire image. A dark semi-transparent overlay on the upper 75% to make text readable.

LAYOUT from top to bottom:

TOP SECTION (centered, white text):
- Large bold white title in two lines: "FIND DIG SELV IGEN RUTINEN"
- Smaller italic white subtitle: "Alt efter hvad du har mistet"
- A thin horizontal white divider line

MIDDLE SECTION: 4 equal columns side by side, each inside a dark semi-transparent rounded rectangle (dark gray/charcoal with slight transparency), small white text inside. Very compact text, small font size.

Column 1:
Header bold white: "DEN TABTE STEMME"
Subheader small italic white: "(People-pleaser)"
Bullet points in small white text:
• 07.00 Stå op
• 10.00–12.00 Giv én ærlig mening til kende
• 12.00 Spis frokost uden at undskylde
• 14.00–16.00 Sig "nej" til en lille anmodning
• 18.00–19.00 Stop med at analysere andres humør
• 23.00 Gå i seng

Column 2:
Header bold white: "DEN TABTE FORBINDELSE"
Subheader small italic white: "(Somatisk)"
Bullet points in small white text:
• 06.30 Stå op og mærk tyngden fra din dyne
• 08.00–12.00 Slap af i kæbe og skuldre
• 13.00–17.00 Læg skærmen fra dig et øjeblik
• 20.30 Mærk efter i kroppen
• 22.30 Gå i seng

Column 3:
Header bold white: "DEN TABTE GNIST"
Subheader small italic white: "(Robotten)"
Bullet points in small white text:
• 06.30 Stå op, uden at tage stilling til noget
• 07.00 Lad følelserne komme, uden at tvinge dem væk
• 09.00–12.00 Løs en simpel opgave uden panik
• 16.00–17.00 Gør noget kun for din egen skyld
• 18.00–19.00 Vær tryg i eget selskab
• 22.30 Gå i seng

Column 4:
Header bold white: "DEN TABTE AUTENTICITET"
Subheader small italic white: "(Masken)"
Bullet points in small white text:
• 07.30 Stå op
• 10.00–12.00 Stop med at øve dine sætninger
• 17.00–18.00 Lad nogen se den rigtige dig
• 18.00–21.00 Tag den tunge facade af
• 23.30 Gå i seng

BOTTOM: White daisy flowers visible at the bottom of the image through the photo.

Style: Exactly like the Calm wellness ad — dark atmospheric nature photo, white text, dark rounded boxes for each column, clean and moody. Portrait 1080x1920."""

payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": prompt}],
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

print(f"Bruger nøgle der starter med: {API_KEY[:12]}...")
print("Genererer billede...")
resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
if not resp.ok:
    print("FEJL fra OpenRouter:", resp.status_code, resp.text[:500])
    raise SystemExit()
resp.raise_for_status()
data = resp.json()

content = data["choices"][0]["message"]["content"]

# Extract base64 image
import re
match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content)
if match:
    img_data = base64.b64decode(match.group(1))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = OUTPUT_DIR / f"calm_style_find_dig_selv_{stamp}.png"
    out.write_bytes(img_data)
    print(f"Gemt: {out}")
else:
    # Try to find image URL
    url_match = re.search(r'https?://\S+\.(?:png|jpg|jpeg|webp)', content)
    if url_match:
        img_resp = requests.get(url_match.group(0))
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = OUTPUT_DIR / f"calm_style_find_dig_selv_{stamp}.png"
        out.write_bytes(img_resp.content)
        print(f"Gemt: {out}")
    else:
        print("RAW RESPONSE:")
        print(content[:2000])
