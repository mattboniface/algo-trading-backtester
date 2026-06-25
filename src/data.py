import yfinance as yf
from pathlib import Path
import pandas as pd


class DataLoader():
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(__file__).parent.parent / cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def get_price_history(self, ticker: str, start: str = None, end: str = None,period: str = None) -> pd.DataFrame:
        yf_ticker = yf.Ticker(ticker)
        data = yf_ticker.history(start=start, end=end, period=period)
        yf.download()

        if data.empty:
            raise ValueError(f"No data returned for {ticker} between {start} and {end}")

        data = pd.DataFrame(data)
        file_path = self.cache_dir / f"{ticker}_{start}-{end}.csv"
        data.to_csv(file_path)

        return data