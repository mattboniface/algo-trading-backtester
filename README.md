# Algorithmic Trading Backtester

A Python backtesting framework for evaluating quantitative rule based trading strategies against historical price data.

## What it does
Given OHLCV price data for a single asset, this framework:
- Generates daily trading signals from one of several rule-based strategies
- Runs a vectorised backtest (signals shifted by 1 day to avoid lookahead bias)
- Computes standard performance metrics: Total Return, Sharpe Ratio, Max Drawdown, Win Rate, Annualised Volatility
- Supports grid-search parameter optimisation with checks for overfitting (parameter stability heatmaps, train/test splits)
- Benchmarks every strategy against a simple Buy & Hold baseline

## Strategies implemented

| Strategy | Key Parameters | Logic |
| ---- | ---- | ---- |
| Moving Average Crossover | short_window = 50, long_window = 200 | Buy the stock when short MA > Long MA |
| Momentum | lookback = 20 | Buy when N-day return is positive |
| Mean Reversion | lookback = 20, num_std = 2 | Buy when the price deviates too far from the mean |
| Relative Strength Index (RSI) | oversold = 30 | Buy when RSI falls below oversold level |
| Bollinger Band Breakout | lookback = 20, num_std = 2 | Buy when breaks above upper band |
| Moving Average Conversion Diversion (MACD) | short_window = 12, long_window = 26, macd_span = 9 | Buy when MACD line above signal line |
| Volatility Breakout | lookback = 14, multiplier = 1.5 | Buy on ATR-based breakout above prior close |
| Buy and Hold | | Buy on initial day and stay long |


## Results
[charts/table go here]

## Limitations
[be honest]

## How to run
\`\`\`
pip install -r requirements.txt
python src/backtest.py
\`\`\`