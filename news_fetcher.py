import requests

def pull_ai_news():
    resp = requests.get("https://newsapi.org/v2/top-headlines?category=technology&apiKey=a798667e31184322bdd5a220a6730c12")
    articles = resp.json().get('articles', [])
    result = []
    for a in articles:
        title = a.get('title', '').strip() if a.get('title') else 'No title'
        description = a.get('description', '').strip() if a.get('description') else ''
        result.append(f"{title} {description}".strip())
    return result

if __name__ == "__main__":
    # Test the function
    news = pull_ai_news()
    print(f"Found {len(news)} news articles:")
    for i, article in enumerate(news, 1):
        print(f"\n{i}. {article}")
