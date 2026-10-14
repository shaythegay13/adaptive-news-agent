"""Fetch current technology headlines from NewsAPI."""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


def pull_ai_news():
    """Return "title description" strings for current technology headlines.

    Returns an empty list when NEWS_API_KEY is unset or the request fails.
    Callers treat that as "no new articles" and do not store an error string
    in the knowledge base.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("NEWS_API_KEY is not set; skipping live news fetch.", file=sys.stderr)
        return []

    try:
        response = requests.get(
            NEWS_API_URL,
            params={"category": "technology", "apiKey": api_key},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        print("News fetch failed.", file=sys.stderr)
        return []

    if payload.get("status") != "ok":
        print("NewsAPI returned an error.", file=sys.stderr)
        return []

    articles = payload.get("articles") or []
    result = []
    for article in articles:
        title = (article.get("title") or "No title").strip()
        description = (article.get("description") or "").strip()
        result.append(f"{title} {description}".strip())
    return result


if __name__ == "__main__":
    news = pull_ai_news()
    print(f"Found {len(news)} news articles:")
    for i, article in enumerate(news, 1):
        print(f"\n{i}. {article}")
