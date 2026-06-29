import matplotlib.pyplot as plt
import pandas as pd
from .backtest import BackTestResult

def plot_equity_curve(result: BackTestResult,data: pd.DataFrame,title: str = "Strategy vs Buy & Hold"):
    buy_hold_returns = data["Close"].pct_change().fillna(0)
    buy_hold_curve = result.starting_capital * (1 + buy_hold_returns).cumprod()
    
    plt.figure(figsize=(12, 6))
    plt.plot(result.equity_curve.index, result.equity_curve, label="Strategy")
    plt.plot(buy_hold_curve.index, buy_hold_curve, label="Buy & Hold", linestyle="--")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    
def plot_drawdown(result: BackTestResult, title: str = "Drawdown Over Time"):
    peak_value = result.equity_curve.cummax()
    trough_values = result.equity_curve
    
    drawdowns = (trough_values - peak_value)/peak_value * 100
    
    plt.figure(figsize=(12, 4))
    plt.fill_between(drawdowns.index, drawdowns, 0, color="red", alpha=0.3)
    plt.plot(drawdowns.index, drawdowns, color="red", linewidth=1)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    
def plot_strategy_comparison(comparison: pd.DataFrame, metric: str = "Sharpe Ratio"):
    plt.figure(figsize=(10, 5))
    comparison[metric].sort_values().plot(kind="barh", color="steelblue")
    plt.title(f"Strategy Comparison: {metric}")
    plt.xlabel(metric)
    plt.tight_layout()
    
    
def save_all_plots(result: BackTestResult, data: pd.DataFrame):
    plot_equity_curve(result, data)
    plt.savefig(f"outputs/equity_curve.png")
    plt.close()

    plot_drawdown(result)
    plt.savefig(f"outputs/drawdown.png")
    plt.close()