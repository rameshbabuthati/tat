import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from market_data import fetch_historical_data
from technical_analysis import calculate_sma, calculate_ema, calculate_rsi, calculate_macd


def prepare_features(df: pd.DataFrame):
    """
    Prepare features and target for ML model.
    Features: SMA, EMA, RSI, MACD, MACD Signal
    Target: 1 if next day's close > today's close, else 0
    """
    df = df.copy()
    df['SMA_14'] = calculate_sma(df, 14)
    df['EMA_14'] = calculate_ema(df, 14)
    df['RSI_14'] = calculate_rsi(df, 14)
    df['MACD'], df['MACD_Signal'] = calculate_macd(df)
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df = df.dropna()
    print (df[['SMA_14', 'EMA_14', 'RSI_14', 'MACD', 'MACD_Signal']])
    features = df[['SMA_14', 'EMA_14', 'RSI_14', 'MACD', 'MACD_Signal']]
   
    target = df['Target']
    return features, target


def train_predict_logistic_regression(X, y):
    """
    Train logistic regression and return accuracy and predictions.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    #yesterday_features = np.array([[205.221429, 206.712299, 79.557588, 2.546793, 1.355444]])
    #predicted_target = model.predict(yesterday_features)
    #print("Predicted target for today (1=up, 0=down or unchanged):", predicted_target[0])


    return acc, report, y_test, y_pred


if __name__ == "__main__":
    import datetime
    today = datetime.date.today()
    ninety_days_ago = today - datetime.timedelta(days=120)
    df = fetch_historical_data('AAPL', start=ninety_days_ago.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    X, y = prepare_features(df)
    acc, report, y_test, y_pred = train_predict_logistic_regression(X, y)
    print(f"Logistic Regression Accuracy: {acc:.2f}")
    print("Classification Report:\n", report)
    print("Sample Predictions:")
    print(pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}).head()) 