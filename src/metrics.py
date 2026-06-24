import pandas as pd
import numpy as np
from backtest import BackTestResult


def total_return(result: BackTestResult) -> float:
    return result.equity_curve.iloc[-1] / result.starting_capital - 1

def sharpe_ratio(result: BackTestResult, total_risk_free_rate: float = 0.0,num_of_periods:int = 252) -> float:
    periodic_risk_free_rate = total_risk_free_rate / num_of_periods
    
    returns = result.equity_curve.pct_change().dropna()
    excess_returns = returns - periodic_risk_free_rate
    
    if excess_returns.std() == 0:
        return 0.0
    periodic_sharpe = excess_returns.mean() / excess_returns.std()
    
    annual_sharpe = periodic_sharpe * np.sqrt(num_of_periods)
    
    return annual_sharpe

def max_drawdown(result: BackTestResult) -> float:
    peak_value = result.equity_curve.cummax()
    trough_values = result.equity_curve
    
    drawdowns = (trough_values - peak_value)/peak_value * 100
    return drawdowns.min()

def win_rate(result:BackTestResult) -> float:
    daily_returns = result.equity_curve.pct_change().dropna()
    trading_days = daily_returns[daily_returns != 0]

    total_trades = len(trading_days)
    winning_trades = (trading_days > 0).sum()
    
    if total_trades == 0:
        return 0.0
    
    win_rate = winning_trades / total_trades
    return win_rate

def annualised_volatility(result: BackTestResult,num_of_periods:int = 252) -> float:
    returns = result.equity_curve.pct_change().dropna()
    return returns.std() * np.sqrt(num_of_periods)
        
def metric_summary(result: BackTestResult):
    return pd.Series(
        {
           "Total Return": total_return(result),
           "Sharpe Ratio": sharpe_ratio(result),
           "Max Drawdown": max_drawdown(result),
           "Win Rate": win_rate(result),
           "Annualised Volatility": annualised_volatility(result)
        }
    )