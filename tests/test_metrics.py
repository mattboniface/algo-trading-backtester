import pandas as pd

from src.backtest import BackTester
from src.metrics import *
from src.strategies import *

data = pd.read_csv("tests/sample_data.csv")

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
       
    correct_positions = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    correct_trades = pd.DataFrame({
    'Date': [6, 11, 21],
    'Position': [1.0, 0.0, 1.0]
})
    correct_curve = [1000.0000, 1000.0000, 1000.0000, 1000.0000, 1000.0000, 1000.0000, 1009.5541, 1012.7389, 1022.2930, 1025.4777, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 990.4459, 1000.7630, 1014.5192, 1024.8363, 1035.1535, 1038.5925, 1052.3487, 1069.5440, 1079.8611, 1097.0564]
    
    
    assert result.positions.to_list() == correct_positions
    pd.testing.assert_frame_equal(result.trades.reset_index(drop=True),correct_trades)
    assert round(result.equity_curve,4).to_list() == correct_curve
    assert result.starting_capital == 1000
    
def test_total_return():
    backtester = BackTester()
    result = backtester.run_backtest(data,MomentumStrategy(lookback=5))
    assert round(total_return(result),2) == 9.71
    
def test_sharpe_ratio():
    backtester = BackTester()
    result = backtester.run_backtest(data,MomentumStrategy(lookback=5))
    
    assert round(sharpe_ratio(result=result,total_risk_free_rate=0.0,num_of_periods=30),4) == 1.9313
    assert round(sharpe_ratio(result=result,total_risk_free_rate=0.1,num_of_periods=30),4) == -0.0554
    
def test_max_drawdown():
    backtester = BackTester()
    result = backtester.run_backtest(data,MomentumStrategy(lookback=5))
    assert round(max_drawdown(result),2) == -3.42
    
def test_win_rate():
    backtester = BackTester()
    result = backtester.run_backtest(data,MomentumStrategy(lookback=5))
    assert round(win_rate(result),2) == 0.93
    
def test_annualised_volatility():
    backtester = BackTester()
    result = backtester.run_backtest(data,MomentumStrategy(lookback=5))
    assert round(annualised_volatility(result,30),2) == 0.05

    
#python -m pytest tests/ -vv
    
    