def simulate_trading(prices, signals, initial_cash=10000, max_position_frac=0.5):
    """
    Simulate trading based on signals and prices.
    Args:
        prices (list of float): Daily closing prices.
        signals (list of str): Daily signals ('buy', 'sell', 'hold').
        initial_cash (float): Starting cash.
        max_position_frac (float): Max fraction of cash to invest at once.
    Returns:
        trade_log (list of dict), final_cash, final_position, final_portfolio_value
    """
    cash = initial_cash
    position = 0  # number of shares
    trade_log = []
    for i, (price, signal) in enumerate(zip(prices, signals)):
        action = None
        shares_to_trade = 0
        if signal == 'buy' and position == 0:
            # Buy as much as allowed
            max_invest = cash * max_position_frac
            shares_to_trade = int(max_invest // price)
            if shares_to_trade > 0:
                cost = shares_to_trade * price
                cash -= cost
                position += shares_to_trade
                action = f'buy {shares_to_trade} shares'
        elif signal == 'sell' and position > 0:
            # Sell all
            cash += position * price
            action = f'sell {position} shares'
            position = 0
        else:
            action = 'hold'
        portfolio_value = cash + position * price
        trade_log.append({
            'day': i,
            'price': price,
            'signal': signal,
            'action': action,
            'cash': cash,
            'position': position,
            'portfolio_value': portfolio_value
        })
    final_portfolio_value = cash + position * prices[-1]
    return trade_log, cash, position, final_portfolio_value


if __name__ == "__main__":
    # Example: simulate 10 days with random signals and prices
    prices = [100, 102, 101, 105, 107, 106, 108, 110, 109, 111]
    signals = ['hold', 'buy', 'hold', 'hold', 'sell', 'hold', 'buy', 'hold', 'sell', 'hold']
    trade_log, cash, position, final_value = simulate_trading(prices, signals)
    print("Trade Log:")
    for entry in trade_log:
        print(entry)
    print(f"\nFinal cash: {cash:.2f}, Final position: {position} shares, Final portfolio value: {final_value:.2f}") 