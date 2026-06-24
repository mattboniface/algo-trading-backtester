import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.backtest import BackTestResult
from src.metrics import *

def test_total_return_doubles_capital():
    equity_curve = pd.Series([1000, 1500, 2000])
    result = BackTestResult(
        equity_curve=equity_curve,
        positions=pd.Series([1, 1, 1]),
        trades=pd.DataFrame(),
        starting_capital=1000,
    )
    assert total_return(result) == 1.0  # went from 1000 to 2000 = 100% return
    
    
def test_max_drawdown_is_zero_if_always_rising():
    equity_curve = pd.Series([1000, 1100, 1200, 1300])
    result = BackTestResult(
        equity_curve=equity_curve,
        positions=pd.Series([1, 1, 1, 1]),
        trades=pd.DataFrame(),
        starting_capital=1000,
    )
    assert max_drawdown(result) == 0.0
    
def test_sharpe_ratio_zero_volatility():
    result = BackTestResult(
        equity_curve=pd.Series([100, 100, 100, 100]),
        positions=pd.Series([1, 1, 1, 1]),
        trades=pd.DataFrame(),
        starting_capital=100,
    )

    assert sharpe_ratio(result) == 0.0
    
def test_sharpe_ratio_known_returns():
    result = BackTestResult(
        equity_curve=pd.Series([100.0, 101.0, 103.02, 106.1106]),
        positions=pd.Series([1, 1, 1, 1]),
        trades=pd.DataFrame(),
        starting_capital=100,
    )

    assert abs(sharpe_ratio(result) - 2.0) < 1e-6
    
    
    
    
if __name__ == "__main__":
    test_total_return_doubles_capital()
    test_max_drawdown_is_zero_if_always_rising()
    test_sharpe_ratio_zero_volatility()
    test_sharpe_ratio_known_returns()
    
    