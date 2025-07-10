import requests
import datetime

NEWS_API_KEY = "3a66aaf4b3ff4c619833536a8b7bb47e"
NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_news_headlines(query: str, from_date: str, to_date: str, api_key: str = NEWS_API_KEY, page_size: int = 10):
    """
    Fetch recent news headlines for a given query (e.g., stock ticker or company name).
    Args:
        query (str): Search query (e.g., 'AAPL' or 'Apple Inc').
        from_date (str): Start date in 'YYYY-MM-DD' format.
        to_date (str): End date in 'YYYY-MM-DD' format.
        api_key (str): NewsAPI key.
        page_size (int): Number of articles to fetch (max 100 per request).
    Returns:
        List of dicts with 'title' and 'publishedAt'.
    """
    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'sortBy': 'publishedAt',
        'apiKey': api_key,
        'language': 'en',
        'pageSize': page_size
    }
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    articles = response.json().get('articles', [])
    return [{'title': a['title'], 'publishedAt': a['publishedAt']} for a in articles]


if __name__ == "__main__":
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    headlines = fetch_news_headlines(
        query='AAPL',
        from_date=seven_days_ago.strftime('%Y-%m-%d'),
        to_date=today.strftime('%Y-%m-%d'),
        page_size=10
    )
    print("Recent News Headlines for AAPL:")
    for h in headlines:
        print(f"- {h['publishedAt']}: {h['title']}") 