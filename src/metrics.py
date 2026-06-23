import pandas as pd
import numpy as np
from backtest import BackTestResult


def total_return(result: BackTestResult) -> float:
    return result.equity_curve.iloc[-1] / result.initial_capital - 1

