#!/usr/bin/env python3
"""Debug script — sends ONE request and prints the full raw response so we can find the image data."""
import os, json, requests

API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: OPENROUTER_API_KEY not set.")

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "google/gemini-3.1-flash-image",
        "messages": [{"role": "user", "content": "Generate a small 100x100 red square image."}],
        "modalities": ["image", "text"],
    },
)

data = response.json()

# Print everything EXCEPT long base64 strings (truncate at 80 chars)
def truncate(obj, max_len=80):
    if isinstance(obj, str) and len(obj) > max_len:
        return obj[:max_len] + f"...[{len(obj)} chars total]"
    if isinstance(obj, dict):
        return {k: truncate(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [truncate(i) for i in obj]
    return obj

print(json.dumps(truncate(data), indent=2))
