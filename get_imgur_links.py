import requests
import json

# Imgur anonymous Client ID (public)
CLIENT_ID = "546c25a59c58ad7"
ALBUM_ID = "TKY9w3R"

headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
response = requests.get(f"https://api.imgur.com/3/album/{ALBUM_ID}/images", headers=headers)

data = response.json()
print("Status:", response.status_code)
print("Success:", data.get("success"))

if data.get("success"):
    images = data["data"]
    print(f"\nFandt {len(images)} billeder:\n")
    for img in images:
        print(f"{img['id']}\t{img['link']}\t{img.get('name','')}")

    # Gem til fil
    with open("imgur_links.txt", "w") as f:
        f.write("id\tlink\tnavn\n")
        for img in images:
            f.write(f"{img['id']}\t{img['link']}\t{img.get('name','')}\n")
    print("\nGemt til imgur_links.txt")
else:
    print("Fejl:", data)
