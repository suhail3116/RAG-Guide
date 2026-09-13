import wikipediaapi
from typing import List, Dict, Optional
from config import config

import time

class WikipediaFetcher:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent="WikiAgent-RAG/2.0 (Engineering Knowledge Assistant; contact@localproject.org)",
            language="en"
        )

    def fetch(self, topic: str, max_retries: int = 3) -> Optional[Dict]:
        """Fetch a Wikipedia article and return structured data with retry on rate limit."""
        for attempt in range(max_retries):
            try:
                page = self.wiki.page(topic)
                if not page.exists():
                    return None

                time.sleep(0.6)  # Polite delay between calls to respect Wikipedia API limits
                return {
                    "title": page.title,
                    "page_content": page.text,
                    "summary": page.summary[:500],
                    "full_text": page.text,
                    "url": page.fullurl,
                    "categories": list(page.categories.keys())[:10],
                    "length": len(page.text)
                }
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "rate_limit" in err_str:
                    wait_time = (attempt + 1) * 3
                    print(f"  [WAIT] Rate limit encountered for '{topic}', waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    if attempt == max_retries - 1:
                        print(f"  [ERROR] Failed to fetch '{topic}': {e}")
                        return None
                    time.sleep(1)
        return None

    def fetch_multiple(self, topics: List[str]) -> List[Dict]:
        """Fetch multiple Wikipedia articles with rate-limiting pauses."""
        results = []
        for idx, topic in enumerate(topics, 1):
            data = self.fetch(topic)
            if data:
                results.append(data)
                print(f"  [{idx}/{len(topics)}] [OK] Fetched: {topic}")
            else:
                print(f"  [{idx}/{len(topics)}] [SKIP] Not found: {topic}")
            time.sleep(0.5)
        return results

    def search(self, query: str, limit: int = 5) -> List[str]:
        """Search Wikipedia for topics matching a query."""
        page = self.wiki.page(query)
        if page.exists():
            return [page.title]
        return []

# Singleton instance
fetcher = WikipediaFetcher()
