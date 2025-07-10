import pandas as pd
from market_data import fetch_historical_data


def calculate_sma(df: pd.DataFrame, window: int = 14):
    """Calculate Simple Moving Average (SMA)."""
    return df['Close'].rolling(window=window).mean()


def calculate_ema(df: pd.DataFrame, window: int = 14):
    """Calculate Exponential Moving Average (EMA)."""
    return df['Close'].ewm(span=window, adjust=False).mean()


def calculate_rsi(df: pd.DataFrame, window: int = 14):
    """Calculate Relative Strength Index (RSI)."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(df: pd.DataFrame, span_short: int = 12, span_long: int = 26, span_signal: int = 9):
    """Calculate MACD (Moving Average Convergence Divergence)."""
    ema_short = df['Close'].ewm(span=span_short, adjust=False).mean()
    ema_long = df['Close'].ewm(span=span_long, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=span_signal, adjust=False).mean()
    return macd, signal


if __name__ == "__main__":
    import datetime
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=60)
    df = fetch_historical_data('AAPL', start=thirty_days_ago.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))

    df['SMA_14'] = calculate_sma(df, 14)
    df['EMA_14'] = calculate_ema(df, 14)
    df['RSI_14'] = calculate_rsi(df, 14)
    df['MACD'], df['MACD_Signal'] = calculate_macd(df)

    print(df[['Close', 'SMA_14', 'EMA_14', 'RSI_14', 'MACD', 'MACD_Signal']].tail()) 