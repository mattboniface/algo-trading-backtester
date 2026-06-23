import pandas as pd
from strategies import Strategy

class BackTester():
    def __init__(self, starting_capital:float = 1000.0):
        self.starting_capital = starting_capital
        
    def run_backtest(self, data: pd.DataFrame,strategy:str):
        signals = Strategy.generate_signals(data)
        positions = signals.shift(1).fillna(0)
        
        returns = data["Close"].pct_change().fillna(0)
        strategy_returns = positions * returns
        
        trades_mask = positions.diff().fillna(0) != 0
        
        equity_curve = self.starting_capital * (1 + strategy_returns).cumprod()
        
        trades = pd.DataFrame(
            {
                "Date": data.index[trades_mask],
                "Position": positions.index[trades_mask]
            }
        )

        return equity_curve,positions,trades,self.inital_capital
    