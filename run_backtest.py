import datetime
import pandas as pd
from market_data import fetch_historical_data
from technical_analysis import calculate_sma, calculate_ema, calculate_rsi, calculate_macd
from ml_prediction import prepare_features, train_predict_logistic_regression
from news_data import fetch_news_headlines
from sentiment_analysis import analyze_sentiment
from signal_fusion import fuse_signals
from trade_execution import simulate_trading

# Parameters
symbol = 'AAPL'
lookback_days = 120
start_date = (datetime.date.today() - datetime.timedelta(days=lookback_days)).strftime('%Y-%m-%d')
end_date = datetime.date.today().strftime('%Y-%m-%d')

# 1. Fetch historical data
df = fetch_historical_data(symbol, start=start_date, end=end_date)

# 2. Calculate technical indicators
df['SMA_14'] = calculate_sma(df, 14)
df['EMA_14'] = calculate_ema(df, 14)
df['RSI_14'] = calculate_rsi(df, 14)
df['MACD'], df['MACD_Signal'] = calculate_macd(df)
df = df.dropna()

# 3. Prepare ML features and target
X, y = prepare_features(df)

# 4. Train ML model on first 70% of data, predict on last 30%
split_idx = int(len(X) * 0.7)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
from sklearn.linear_model import LogisticRegression
ml_model = LogisticRegression(max_iter=1000)
ml_model.fit(X_train, y_train)
ml_preds = ml_model.predict(X_test)

# 5. For each day in test set, get technical, ML, sentiment, and fuse signals
signals = []
prices = []
dates = X_test.index
for i, date in enumerate(dates):
    row = df.loc[date]
    # Technical signal: simple rule (buy if RSI < 30, sell if RSI > 70, else hold)
    if row['RSI_14'] < 30:
        technical_signal = 1
    elif row['RSI_14'] > 70:
        technical_signal = -1
    else:
        technical_signal = 0
    # ML signal: 1 for up, 0 for down
    ml_signal = ml_preds[i]
    # News sentiment for the day
    news = fetch_news_headlines(symbol, from_date=date.strftime('%Y-%m-%d'), to_date=date.strftime('%Y-%m-%d'), page_size=3)
    if news:
        # Average sentiment for all headlines that day
        sentiments = [analyze_sentiment(h['title'])[1] for h in news]
        # Use the most common sentiment
        sentiment_label = max(set(sentiments), key=sentiments.count)
    else:
        sentiment_label = 'neutral'
    # Fuse signals
    fused_signal = fuse_signals(ml_signal, technical_signal, sentiment_label)
    signals.append(fused_signal)
    prices.append(row['Close'])

# 6. Simulate trading
trade_log, cash, position, final_value = simulate_trading(prices, signals)

# 7. Print results
print("Trade Log:")
for entry in trade_log:
    print(entry)
print(f"\nFinal cash: {cash:.2f}, Final position: {position} shares, Final portfolio value: {final_value:.2f}") 