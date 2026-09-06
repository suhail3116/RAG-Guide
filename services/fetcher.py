import wikipediaapi
from typing import List, Dict, Optional
from config import config

class WikipediaFetcher:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent="WikiChatbot/1.0 (Educational Project; contact@example.com)",
            language="en"
        )

    def fetch(self, topic: str) -> Optional[Dict]:
        """Fetch a Wikipedia article and return structured data."""
        page = self.wiki.page(topic)

        if not page.exists():
            return None

        return {
            "title": page.title,
            "page_content": page.text,
            "summary": page.summary[:500],
            "full_text": page.text,
            "url": page.fullurl,
            "categories": list(page.categories.keys())[:10],
            "length": len(page.text)
        }

    def fetch_multiple(self, topics: List[str]) -> List[Dict]:
        """Fetch multiple Wikipedia articles."""
        results = []
        for topic in topics:
            data = self.fetch(topic)
            if data:
                results.append(data)
                print(f"  [OK] Fetched: {topic}")
            else:
                print(f"  [SKIP] Not found: {topic}")
        return results

    def search(self, query: str, limit: int = 5) -> List[str]:
        """Search Wikipedia for topics matching a query."""
        page = self.wiki.page(query)
        if page.exists():
            return [page.title]
        return []

# Singleton instance
fetcher = WikipediaFetcher()
