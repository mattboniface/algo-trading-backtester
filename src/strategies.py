import pandas as pd

class MovingAverageCrossover():
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_ma = data["Close"].rolling(50).mean()
        long_ma = data["Close"].rolling(200).mean()
        
        signals = (short_ma > long_ma).astype(int)
        return signals.fillna(0)
    
class MomentumStrategy():
    def __init__(self,lookback: int = 20):
        self.lookback = lookback
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        returns = data["Close"].pct_change(self.lookback)
        
        signals = (returns > 0).astype(int)
        return signals.fillna(0)
    
class MeanReversionStrategy():
    def __init__(self,lookback: int = 20, num_std: int = 2):
        self.lookback = lookback
        self.num_std = num_std
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        mean = data.rolling(self.lookback).mean()
        std = data.rolling(self.lookback).std()
        
        lower_band = mean - (std* self.num_std)
        
        signals = (data["Close"] < lower_band).astype(int)
        return signals.fillna(0)