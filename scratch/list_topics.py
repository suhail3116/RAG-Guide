import json

with open("data/articles_cache.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total Topics: {len(data)}\n")
print(f"{'#':<3} | {'Topic Title':<45} | {'Image File in data/images/'}")
print("-" * 80)
for idx, (title, doc) in enumerate(data.items(), 1):
    img = doc.get('local_image_path', 'N/A')
    filename = img.replace("data/images/", "")
    print(f"{idx:<3} | {title:<45} | {filename}")
