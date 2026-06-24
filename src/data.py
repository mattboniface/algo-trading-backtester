import yfinance as yf
from pathlib import Path
import pandas as pd

class DataLoader():
    def get_price_history(self,ticker: str,start: str,end: str) -> pd.DataFrame:
        yf_ticker = yf.Ticker(ticker)
        data = yf_ticker.history(start=start,
                               end=end
                               )
        if data.empty:
            raise ValueError(f"No data returned for {ticker} between {start} and {end}")

        data = pd.DataFrame(data)
        file_path = f"{Path('data')}/{ticker}_{start}-{end}.csv"
        data.to_csv(file_path,)
        
        return data