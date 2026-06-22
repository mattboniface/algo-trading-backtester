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
    
class RSIStrategy():   
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
    
class BollingerBandBreakoutStrategy():
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
    
class MACDStrategy():
    def __init__(self,data:pd.DataFrame,short_window: int = 12, long_window: int = 26, macd_span: int = 9):
        self.short_window = short_window
        self.long_window = long_window
        self.macd_span = macd_span
        
        self.data = data
        
    def ema(self,period: int):
        ema = self.data["Close"].ewm(span=period,adjust=False).mean()
        return ema
        
    def generate_signals(self) -> pd.Series:
        ema_short = self.ema(self.short_window)
        ema_long = self.ema(self.long_window)
        
        macd_line = ema_short - ema_long
        signal_line = macd_line.ewm(span=self.macd_span, adjust=False).mean()
        ...
        