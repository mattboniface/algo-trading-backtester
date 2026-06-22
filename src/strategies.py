import pandas as pd

class MovingAverageCrossover():
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_ma = data["Close"].rolling(50).mean()
        long_ma = data["Close"].rolling(200).mean()
        
        signals = (short_ma > long_ma).astype(int)
        return signals.fillna(0)