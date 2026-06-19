import numpy as np
import pandas as pd
from scipy.optimize import minimize

def calculate_portfolio_metrics(returns):
    """
    Calculate expected returns and covariance matrix.

    Parameters:
    - returns: DataFrame of daily returns
    """
    annual_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    return annual_returns, cov_matrix

def portfolio_performance(weights, returns, cov_matrix):
    """
    Calculate portfolio return and volatility.
    """
    portfolio_return = np.sum(returns.mean() * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    return portfolio_return, portfolio_volatility

def optimize_portfolio(returns, cov_matrix, target_return=None):
    """
    Optimize portfolio using Markowitz model.

    Parameters:
    - returns: Expected returns
    - cov_matrix: Covariance matrix
    - target_return: Target return for constrained optimization (optional)
    """
    num_assets = len(returns)
    args = (returns, cov_matrix)

    # Constraints
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # Sum of weights = 1
    if target_return is not None:
        constraints.append({'type': 'eq', 'fun': lambda x: portfolio_performance(x, returns, cov_matrix)[0] - target_return})

    # Bounds
    bounds = tuple((0, 1) for _ in range(num_assets))

    # Initial guess
    init_guess = num_assets * [1. / num_assets]

    # Optimization
    result = minimize(lambda x: portfolio_performance(x, returns, cov_matrix)[1],
                     init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    return result.x

def efficient_frontier(returns, cov_matrix, num_portfolios=100):
    """
    Generate the efficient frontier.
    """
    results = []
    return_range = np.linspace(returns.min(), returns.max(), num_portfolios)

    for target_return in return_range:
        weights = optimize_portfolio(returns, cov_matrix, target_return)
        ret, vol = portfolio_performance(weights, returns, cov_matrix)
        results.append([ret, vol, weights])

    return pd.DataFrame(results, columns=['Return', 'Volatility', 'Weights'])

if __name__ == "__main__":
    returns_df = pd.read_csv('../../data/processed/returns.csv', index_col='Date', parse_dates=True)
    returns, cov_matrix = calculate_portfolio_metrics(returns_df)
    frontier = efficient_frontier(returns, cov_matrix)
    frontier.to_csv('../../data/processed/efficient_frontier.csv')