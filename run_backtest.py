from src.data import DataLoader
from src.backtest import BackTester
from src.strategies import *
from src.metrics import metric_summary
import pandas as pd

def main():
    ticker = "AAPL"
    
    loader = DataLoader()
    data = loader.get_price_history(ticker = ticker,start = "2020-01-01",end = "2026-06-22")
    
    backtester = BackTester(starting_capital=1000)
    
    strategies = {
        "Moving Average Crossover": MovingAverageCrossover(),
        "Momentum": MomentumStrategy(),
        "Mean Reversion": MeanReversionStrategy(),
        "RSI": RSIStrategy(),
        "Bollinger Band": BollingerBandBreakoutStrategy(),
        "MACD": MACDStrategy(),
        "Volatility Breakout": VolatilityBreakoutStrategy()
    }
    
    results = {}
    for name, strategy in strategies.items():
        result = backtester.run_backtest(data=data,strategy=strategy)
        results[name] = metric_summary(result)
        print(f"Finished: {name}")
    
    comparison = pd.DataFrame(results).T
    print("\n--- Strategy Comparison ---")
    print(comparison.round(4))
    comparison.to_csv(f"outputs/{ticker}_comparison_results.csv")
    
if __name__ == "__main__":
    main()
