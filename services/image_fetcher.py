import os
import sys
import json
import time
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

IMAGES_DIR = os.path.join("data", "images")
CACHE_FILE = os.path.join("data", "articles_cache.json")

# Ensure image storage directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

USER_AGENT = "WikiAgent-RAG/2.0 (Engineering Knowledge Assistant; contact@localproject.org)"

def slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in text.lower()).strip("_")

def download_image(url: str, save_path: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp, open(save_path, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"    [WARN] Failed to download {url}: {e}")
        return False

def create_fallback_svg(topic_title: str, save_path: str):
    """Generate a clean SVG banner image for curated topics without a Wikipedia thumbnail."""
    clean_title = topic_title.replace("<", "&lt;").replace(">", "&gt;")
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <rect width="400" height="200" rx="12" fill="#1e293b"/>
  <rect x="10" y="10" width="380" height="180" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="200" y="90" font-family="sans-serif" font-size="40" text-anchor="middle" fill="#38bdf8">💡</text>
  <text x="200" y="130" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#f8fafc">{clean_title}</text>
  <text x="200" y="155" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#94a3b8">WikiAgent Engineering Guide</text>
</svg>"""
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

def fetch_and_cache_images():
    if not os.path.exists(CACHE_FILE):
        print(f"[ERROR] {CACHE_FILE} not found!")
        return

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"🖼️ Fetching offline images for {len(articles)} topics...")
    updated = False

    for idx, (title, data) in enumerate(articles.items(), 1):
        slug = slugify(title)
        
        # Check if already downloaded
        existing_files = [f for f in os.listdir(IMAGES_DIR) if f.startswith(slug)]
        if existing_files:
            filename = existing_files[0]
            data["image_url"] = f"/static/images/{filename}"
            data["local_image_path"] = f"data/images/{filename}"
            print(f"  [{idx}/{len(articles)}] [EXISTS] {title} -> {filename}")
            continue

        print(f"  [{idx}/{len(articles)}] [FETCHING] {title}...")
        
        # Query Wikimedia REST API for thumbnail URL
        encoded_topic = urllib.parse.quote(title.replace(" ", "_"))
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_topic}"
        
        image_downloaded = False
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=5) as resp:
                summary_data = json.loads(resp.read().decode())
                
                thumb_info = summary_data.get("thumbnail") or summary_data.get("originalimage")
                if thumb_info and "source" in thumb_info:
                    img_src = thumb_info["source"]
                    ext = img_src.split(".")[-1].split("?")[0].lower()
                    if ext not in ["jpg", "jpeg", "png", "webp", "gif"]:
                        ext = "jpg"
                    
                    filename = f"{slug}.{ext}"
                    save_path = os.path.join(IMAGES_DIR, filename)
                    
                    if download_image(img_src, save_path):
                        data["image_url"] = f"/static/images/{filename}"
                        data["local_image_path"] = f"data/images/{filename}"
                        image_downloaded = True
                        updated = True
                        print(f"    [OK] Downloaded Wikipedia image: {filename}")
        except Exception as e:
            print(f"    [INFO] Wikimedia summary API not found for '{title}': {e}")

        # Fallback to local generated SVG badge if no Wikipedia image
        if not image_downloaded:
            filename = f"{slug}.svg"
            save_path = os.path.join(IMAGES_DIR, filename)
            create_fallback_svg(title, save_path)
            data["image_url"] = f"/static/images/{filename}"
            data["local_image_path"] = f"data/images/{filename}"
            updated = True
            print(f"    [OK] Created local SVG badge: {filename}")

        time.sleep(0.3)

    # Save updated cache with image URLs
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print("\n✅ All topic images successfully saved locally in 'data/images/'!")

if __name__ == "__main__":
    fetch_and_cache_images()
