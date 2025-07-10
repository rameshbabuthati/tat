from nltk.sentiment.vader import SentimentIntensityAnalyzer
from news_data import fetch_news_headlines
import datetime


def analyze_sentiment(text: str):
    """
    Analyze sentiment of a given text using VADER.
    Returns compound score and label (positive/neutral/negative).
    """
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        label = 'positive'
    elif score <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    return score, label


if __name__ == "__main__":
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    headlines = fetch_news_headlines(
        query='AAPL',
        from_date=seven_days_ago.strftime('%Y-%m-%d'),
        to_date=today.strftime('%Y-%m-%d'),
        page_size=10
    )
    print("Sentiment Analysis of Recent News Headlines for AAPL:")
    for h in headlines:
        score, label = analyze_sentiment(h['title'])
        print(f"- {h['publishedAt']}: {h['title']}\n  Sentiment: {label} (score={score:.2f})\n") 