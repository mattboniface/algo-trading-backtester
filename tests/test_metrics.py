import pandas as pd

from src.backtest import BackTester
from src.metrics import *
from src.strategies import *

data = pd.read_csv("tests/sample_data.csv")
print(data)

def test_moving_avg_crossover():
    strategy = MovingAverageCrossover(short_window=5,long_window=10)
    
    data["signal"] = strategy.generate_signals(data)
    
    correct_signal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    assert data["signal"].tolist() == correct_signal
    
def test_momentum():
    strategy = MomentumStrategy(lookback=5)
    data["signal"] = strategy.generate_signals(data)

    correct_signal = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert data["signal"].tolist() == correct_signal

def test_mean_reversion():
    strategy = MeanReversionStrategy(lookback=5,num_std=0.5)
    data["signal"] = strategy.generate_signals(data)

    correct_signal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert data["signal"].tolist() == correct_signal
    
def test_rsi():
    strategy = RSIStrategy(window=1)
    data["signal"] = strategy.generate_signals(data)

    correct_signal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert data["signal"].tolist() == correct_signal
    
def test_bollingerband():
    strategy = BollingerBandBreakoutStrategy(lookback=5,num_std=0.5)
    data["signal"] = strategy.generate_signals(data)

    correct_signal = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert data["signal"].tolist() == correct_signal
    
def test_macd():
    strategy = MACDStrategy(short_window=5,long_window=10,macd_span=3)
    data["signal"] = strategy.generate_signals(data)

    correct_signal = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert data["signal"].tolist() == correct_signal
    
def test_volatility_breakout():
    strategy = VolatilityBreakoutStrategy(lookback=5,multiplier=0.1)
    data["signal"] = strategy.generate_signals(data)

    correct_signal = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert data["signal"].tolist() == correct_signal

def test_backtester():
    backtester = BackTester()
    result = backtester.run_backtest(data,MomentumStrategy(lookback=5))
    print(result.trades.reset_index(drop=True)) 
       
    correct_positions = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    correct_trades = pd.DataFrame({
    'Date': [6, 11, 21],
    'Position': [1.0, 0.0, 1.0]
})
    print(correct_trades)
    #correct_curve = [1000.0]
    
    
    assert result.positions.to_list() == correct_positions
    pd.testing.assert_frame_equal(result.trades.reset_index(drop=True),correct_trades)
    #assert result.equity_curve.to_list() == correct_curve
    assert result.starting_capital == 1000
    

if __name__ == "__main__":
    test_moving_avg_crossover()
    
#python -m pytest tests/ -vv
    
    