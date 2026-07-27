#!/usr/bin/env python3
"""Test parsing logic against a fake response that matches the real OpenRouter structure.
No API calls — zero cost."""
import base64, json
from pathlib import Path

# Simulate the exact response structure we saw in debug output
fake_response = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "I have generated the image for you.",
                "refusal": None,
                "reasoning": None,
                "images": [
                    {
                        "type": "image_url",
                        "image_url": {
                            # A tiny valid PNG (1x1 red pixel) as base64
                            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
                        }
                    }
                ]
            }
        }
    ]
}

# Run the exact same parsing logic as generate_ads.py
OUTPUT_DIR = Path("/Users/lunahansen/Desktop/Claude ads/output")
OUTPUT_DIR.mkdir(exist_ok=True)

found = False
for choice in fake_response.get("choices", []):
    message = choice.get("message", {})
    for img_part in message.get("images", []):
        if img_part.get("type") == "image_url":
            url = img_part["image_url"]["url"]
            if url.startswith("data:"):
                b64 = url.split(",", 1)[1]
                img_bytes = base64.b64decode(b64)
                out_path = OUTPUT_DIR / "test_parse_result.png"
                out_path.write_bytes(img_bytes)
                print(f"SUCCESS — image saved to: {out_path}")
                print(f"File size: {len(img_bytes)} bytes")
                found = True

if not found:
    print("FAILED — parsing did not find the image")
