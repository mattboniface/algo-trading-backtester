import pandas as pd
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        ...

class MovingAverageCrossover(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_ma = data["Close"].rolling(50).mean()
        long_ma = data["Close"].rolling(200).mean()
        
        signals = (short_ma > long_ma).astype(int)
        return signals.fillna(0)
    
class MomentumStrategy(Strategy):
    def __init__(self,lookback: int = 20):
        self.lookback = lookback
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        returns = data["Close"].pct_change(self.lookback)
        
        signals = (returns > 0).astype(int)
        return signals.fillna(0)
    
class MeanReversionStrategy(Strategy):
    def __init__(self,lookback: int = 20, num_std: int = 2):
        self.lookback = lookback
        self.num_std = num_std
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        mean = data.rolling(self.lookback).mean()
        std = data.rolling(self.lookback).std()
        
        lower_band = mean - (std* self.num_std)
        
        signals = (data["Close"] < lower_band).astype(int)
        return signals.fillna(0)
    
class RSIStrategy(Strategy):   
    def __init__(self,window: int = 20, overbought: int = 70,oversold:int = 30):
        self.window = window
        
        self.overbought = overbought
        self.oversold = oversold
                     
    def calculate_rsi(self,data:pd.DataFrame):
        price_diff = data["Close"].diff()
        avg_gain = price_diff.where(price_diff > 0,0).rolling(self.window).mean()
        avg_loss = price_diff.where(price_diff < 0,0).rolling(self.window).mean()
        
        rs = avg_gain/avg_loss
        rsi = 100 - (100 / (1+rs))
        return rsi
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        rsi = self.calculate_rsi(data)
        
        signals = (rsi < self.oversold).astype(int)
        return signals.fillna(0)
    
class BollingerBandBreakoutStrategy(Strategy):
    def __init__(self,lookback: int = 20, num_std: int = 2):
        self.lookback = lookback
        self.num_std = num_std
        
    def bollinger_bands(self, data: pd.DataFrame):
        mean = data.rolling(self.lookback).mean()
        std = data.rolling(self.lookback).std()
        
        upper_band = mean + (self.num_std * std)
        lower_band = mean - (self.num_std * std)
        
        return lower_band,mean,upper_band
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        lower_band, middle_band,upper_band = self.bollinger_bands(data)
        signals = (data["Close"] > upper_band).astype(int)
        return signals.fillna(0)
    
class MACDStrategy(Strategy):
    def __init__(self,short_window: int = 12, long_window: int = 26, macd_span: int = 9):
        self.short_window = short_window
        self.long_window = long_window
        self.macd_span = macd_span
        
        
    def ema(self,data:pd.DataFrame,period: int):
        ema = data["Close"].ewm(span=period,adjust=False).mean()
        return ema
        
    def generate_signals(self,data:pd.DataFrame) -> pd.Series:
        ema_short = self.ema(data,self.short_window)
        ema_long = self.ema(data,self.long_window)
        
        macd_line = ema_short - ema_long
        signal_line = macd_line.ewm(span=self.macd_span, adjust=False).mean()
        
        signals = (macd_line > signal_line).astype(int)
        return signals.fillna(0)
    
class VolatilityBreakoutStrategy(Strategy):
    def __init__(self,lookback: int = 14,multiplier: int = 1.5):
        self.lookback = lookback
        self.multiplier = multiplier
        
          
    def get_atr(self,data: pd.DataFrame):
        high_low = data["High"] - data["Low"]
        high_close = (data["High"] - data["Close"].shift(1)).abs()
        low_close = (data["Low"] - data["Close"].shift(1)).abs()
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(self.atr_window).mean()
        
        return atr
    
    def generate_signals(self,data:pd.DataFrame) -> pd.Series:
        atr = self.get_atr()
        reference_price = data["Close"].shift(1)
        
        breakout_threshold = reference_price + (self.multiplier * atr)
        
        signals = (data["Close"] > breakout_threshold).astype(int)
        return signals.fillna(0)