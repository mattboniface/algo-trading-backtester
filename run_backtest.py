from src.data import DataLoader
from src.backtest import BackTester
from src.strategies import *
from src.metrics import metric_summary
from src.visualise import plot_equity_curve, plot_drawdown
from tests.test_metrics import *
import pandas as pd

def main():
    ticker = "SPY"
    
    loader = DataLoader()
    data = loader.get_price_history(ticker = ticker,start = "2020-01-01",end = "2025-12-31")
    
    backtester = BackTester(starting_capital=1000)
    
    strategies = {
        "Buy and Hold": BuyAndHold(),
        "Moving Average Crossover": MovingAverageCrossover(),
        "Momentum": MomentumStrategy(),
        "Mean Reversion": MeanReversionStrategy(),
        "RSI": RSIStrategy(),
        "Bollinger Band": BollingerBandBreakoutStrategy(),
        "MACD": MACDStrategy(),
        "Volatility Breakout": VolatilityBreakoutStrategy()
    }
    
    results_raw = {}
    results = {}
    for name, strategy in strategies.items():
        results_raw[name] = backtester.run_backtest(data=data,strategy=strategy)
        results[name] = metric_summary(results_raw[name])
        print(f"Finished: {name}")
    
    comparison = pd.DataFrame(results).T
    print("\n--- Strategy Comparison ---")
    print(comparison.round(4))
    comparison.to_csv(f"outputs/comparison_results.csv")
    
    plot_equity_curve(results_raw["Mean Reversion"], data, title="Mean Reversion vs Buy & Hold")
    plot_drawdown(results_raw["Mean Reversion"])
    
if __name__ == "__main__":
    main()
