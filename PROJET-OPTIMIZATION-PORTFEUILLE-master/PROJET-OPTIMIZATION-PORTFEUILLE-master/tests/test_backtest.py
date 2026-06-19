"""
Tests pour le module de backtesting.
"""
import numpy as np
import pandas as pd
import pytest
from src.models.backtest import backtest_strategy, compare_strategies

@pytest.fixture
def sample_returns():
    """Fixture pour générer des rendements d'exemple."""
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=252, freq='B')  # Jours ouvrables
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    
    # Générer des rendements aléatoires
    returns_data = np.random.normal(loc=0.001, scale=0.02, size=(252, 4))
    returns = pd.DataFrame(returns_data, index=dates, columns=tickers)
    
    return returns

@pytest.fixture
def sample_weights():
    """Fixture pour générer des poids d'exemple."""
    return np.array([0.25, 0.25, 0.25, 0.25])  # Poids égaux

def test_backtest_strategy(sample_returns, sample_weights):
    """Test de la fonction backtest_strategy."""
    # Exécuter le backtesting
    performance = backtest_strategy(
        returns=sample_returns,
        weights=sample_weights,
        initial_investment=10000,
        rebalance_frequency='monthly'
    )
    
    # Vérifier que le résultat n'est pas None
    assert performance is not None
    
    # Vérifier que le DataFrame a la bonne structure
    assert isinstance(performance, dict)
    assert 'portfolio_value' in performance
    assert 'returns' in performance
    assert 'cumulative_returns' in performance
    assert 'metrics' in performance
    
    # Vérifier que les métriques sont calculées
    metrics = performance['metrics']
    assert 'total_return' in metrics
    assert 'annualized_return' in metrics
    assert 'annualized_volatility' in metrics
    assert 'sharpe_ratio' in metrics
    assert 'max_drawdown' in metrics
    
    # Vérifier que les valeurs sont dans des plages raisonnables
    assert metrics['total_return'] > -1.0  # Pas de perte totale
    assert -0.5 < metrics['annualized_return'] < 0.5  # Rendement annualisé raisonnable
    assert 0 < metrics['annualized_volatility'] < 0.5  # Volatilité positive et raisonnable
    assert -5 < metrics['sharpe_ratio'] < 5  # Ratio de Sharpe raisonnable
    assert 0 <= metrics['max_drawdown'] <= 1.0  # Drawdown entre 0 et 100%

def test_compare_strategies(sample_returns):
    """Test de la fonction compare_strategies."""
    # Définir différentes stratégies
    strategies = {
        'Equal Weight': np.array([0.25, 0.25, 0.25, 0.25]),
        'AAPL Heavy': np.array([0.7, 0.1, 0.1, 0.1]),
        'Tech Focus': np.array([0.4, 0.4, 0.1, 0.1])
    }
    
    # Comparer les stratégies
    comparison = compare_strategies(
        returns=sample_returns,
        strategies=strategies,
        initial_investment=10000,
        rebalance_frequency='monthly'
    )
    
    # Vérifier que le résultat n'est pas None
    assert comparison is not None
    
    # Vérifier que le DataFrame a la bonne structure
    assert isinstance(comparison, dict)
    assert 'portfolio_values' in comparison
    assert 'cumulative_returns' in comparison
    assert 'metrics_comparison' in comparison
    
    # Vérifier que toutes les stratégies sont incluses
    metrics_comparison = comparison['metrics_comparison']
    assert all(strategy in metrics_comparison.index for strategy in strategies.keys())
    
    # Vérifier que les métriques sont calculées pour chaque stratégie
    assert all(metric in metrics_comparison.columns for metric in 
               ['total_return', 'annualized_return', 'annualized_volatility', 'sharpe_ratio', 'max_drawdown'])
    
    # Vérifier que les valeurs du portefeuille sont cohérentes
    portfolio_values = comparison['portfolio_values']
    assert isinstance(portfolio_values, pd.DataFrame)
    assert all(strategy in portfolio_values.columns for strategy in strategies.keys())
    assert len(portfolio_values) == len(sample_returns)  # Même nombre de jours
