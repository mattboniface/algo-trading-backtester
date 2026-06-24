import pandas as pd
from strategies import Strategy

class BackTestResult():
    def __init__(self,
                 equity_curve: pd.Series,
                 positions: pd.Series,
                 trades: pd.Series,
                 starting_capital: float):
        self.equity_curve = equity_curve
        self.positions = positions
        self.trades = trades
        self.starting_capital = starting_capital

class BackTester():
    def __init__(self, starting_capital:float = 1000.0):
        self.starting_capital = starting_capital
        
    def run_backtest(self, data: pd.DataFrame,strategy: Strategy):
        signals = strategy.generate_signals(data)
        positions = signals.shift(1).fillna(0)
        
        returns = data["Close"].pct_change().fillna(0)
        strategy_returns = positions * returns
        
        trades_mask = positions.diff().fillna(0) != 0
        
        equity_curve = self.starting_capital * (1 + strategy_returns).cumprod()
        
        trades = pd.DataFrame(
            {
                "Date": data.index[trades_mask],
                "Position": positions[trades_mask]
            }
        )

        return BackTestResult(
            equity_curve=equity_curve,
            positions=positions,
            trades=trades,
            starting_capital=self.starting_capital
        )
