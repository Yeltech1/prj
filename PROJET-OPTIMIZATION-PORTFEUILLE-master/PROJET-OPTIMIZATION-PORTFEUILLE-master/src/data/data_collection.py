import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(tickers, start_date, end_date, output_path):
    """
    Fetch historical stock data from Yahoo Finance and save to CSV.

    Parameters:
    - tickers: List of stock tickers (e.g., ['AAPL', 'MSFT', 'GOOGL'])
    - start_date: Start date for data (e.g., '2020-01-01')
    - end_date: End date for data (e.g., '2025-01-01')
    - output_path: Path to save CSV file
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    data = yf.download(tickers, start=start_date, end=end_date, progress=False)
    data['Adj Close'].to_csv(output_path)
    return data

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2020-01-01'
    end_date = '2025-01-01'
    output_path = '../../data/raw/stock_data.csv'
    fetch_stock_data(tickers, start_date, end_date, output_path)