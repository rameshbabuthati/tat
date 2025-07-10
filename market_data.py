import yfinance as yf


def fetch_historical_data(symbol: str, start: str, end: str, interval: str = '1d'):
    """
    Fetch historical stock data for a given symbol using yfinance.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL').
        start (str): Start date in 'YYYY-MM-DD' format.
        end (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval ('1d', '1h', etc.). Default is '1d'.
    Returns:
        pandas.DataFrame: Historical price data.
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start, end=end, interval=interval)
    return data


if __name__ == "__main__":
    # Example usage and test: Fetch last 30 days of AAPL data
    import datetime
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    df = fetch_historical_data('AAPL', start=thirty_days_ago.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    print(df.head()) 