import pandas as pd
import numpy as np
import os

def preprocess_data(input_path, output_path):
    """
    Preprocess stock data: calculate returns, handle missing values.

    Parameters:
    - input_path: Path to raw data CSV
    - output_path: Path to save processed data
    """
    df = pd.read_csv(input_path, index_col='Date', parse_dates=True)

    # Calculate daily returns
    returns = df.pct_change().dropna()

    # Handle missing values
    returns = returns.fillna(returns.mean())

    # Save processed data
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    returns.to_csv(output_path)

    return returns

if __name__ == "__main__":
    input_path = '../../data/raw/stock_data.csv'
    output_path = '../../data/processed/returns.csv'
    preprocess_data(input_path, output_path)