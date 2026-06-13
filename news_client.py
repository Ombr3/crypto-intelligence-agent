import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def get_news(coin: str, max_articles: int = 5) -> list[dict]:
    """Fetch recent news articles for a given coin e.g. 'Ethereum'"""
    params = {
        "q": coin,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "published": a["publishedAt"],
            "url": a["url"],
            "description": a["description"]
        }
        for a in articles
    ]

if __name__ == "__main__":
    articles = get_news("Ethereum")
    for a in articles:
        print(f"[{a['source']}] {a['title']}")
        print(f"  {a['description']}")
        print()
