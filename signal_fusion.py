def fuse_signals(ml_signal: int, technical_signal: int, sentiment_label: str) -> str:
    """
    Fuse signals from ML, technical analysis, and sentiment analysis.
    Args:
        ml_signal (int): 1 for up/buy, 0 for down/sell.
        technical_signal (int): 1 for buy, -1 for sell, 0 for neutral.
        sentiment_label (str): 'positive', 'neutral', or 'negative'.
    Returns:
        str: 'buy', 'sell', or 'hold'.
    """
    # Convert sentiment label to numeric
    sentiment_signal = 1 if sentiment_label == 'positive' else (-1 if sentiment_label == 'negative' else 0)
    # Convert ml_signal to -1/1
    ml_vote = 1 if ml_signal == 1 else -1
    # Count votes
    votes = [ml_vote, technical_signal, sentiment_signal]
    buy_votes = votes.count(1)
    sell_votes = votes.count(-1)
    if buy_votes >= 2:
        return 'buy'
    elif sell_votes >= 2:
        return 'sell'
    else:
        return 'hold'


if __name__ == "__main__":
    # Example: ML predicts up, technical is buy, sentiment is positive
    print("Example 1:", fuse_signals(1, 1, 'positive'))  # buy
    # Example: ML predicts down, technical is sell, sentiment is negative
    print("Example 2:", fuse_signals(0, -1, 'negative'))  # sell
    # Example: ML predicts up, technical is sell, sentiment is neutral
    print("Example 3:", fuse_signals(1, -1, 'neutral'))  # hold 