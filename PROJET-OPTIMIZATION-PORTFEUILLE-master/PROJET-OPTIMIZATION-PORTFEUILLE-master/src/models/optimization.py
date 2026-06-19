import pandas as pd
import numpy as np
from src.models.mpt import optimize_portfolio, portfolio_performance, calculate_portfolio_metrics

def backtest_portfolio(returns, predicted_returns, cov_matrix):
    """
    Backtest portfolio using predicted returns.

    Parameters:
    - returns: Historical returns
    - predicted_returns: Predicted returns from ML model
    - cov_matrix: Covariance matrix
    """
    weights = optimize_portfolio(predicted_returns, cov_matrix)
    portfolio_return, portfolio_volatility = portfolio_performance(weights, returns, cov_matrix)

    # Simulate portfolio performance
    portfolio_values = (returns @ weights).cumsum()
    return portfolio_values, weights

if __name__ == "__main__":
    returns = pd.read_csv('../../data/processed/returns.csv', index_col='Date', parse_dates=True)
    predicted_returns = pd.Series([0.0005, 0.0004, 0.0006], index=returns.columns)  # Example predictions
    _, cov_matrix = calculate_portfolio_metrics(returns)

    portfolio_values, weights = backtest_portfolio(returns, predicted_returns, cov_matrix)
    portfolio_values.to_csv('../../data/processed/portfolio_performance.csv')
    print("Poids du portefeuille :", weights)