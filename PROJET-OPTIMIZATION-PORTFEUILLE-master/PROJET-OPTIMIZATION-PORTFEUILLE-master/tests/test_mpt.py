"""
Tests pour le module d'optimisation de portefeuille selon Markowitz.
"""
import numpy as np
import pandas as pd
import pytest
from src.models.mpt import calculate_portfolio_metrics, optimize_portfolio

@pytest.fixture
def sample_returns():
    """Fixture pour générer des rendements d'exemple."""
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    
    # Générer des rendements aléatoires
    returns_data = np.random.normal(loc=0.001, scale=0.02, size=(100, 4))
    returns = pd.DataFrame(returns_data, index=dates, columns=tickers)
    
    return returns

def test_calculate_portfolio_metrics(sample_returns):
    """Test de la fonction calculate_portfolio_metrics."""
    # Calculer les métriques du portefeuille
    expected_returns, cov_matrix = calculate_portfolio_metrics(sample_returns)
    
    # Vérifier que les types de retour sont corrects
    assert isinstance(expected_returns, pd.Series)
    assert isinstance(cov_matrix, pd.DataFrame)
    
    # Vérifier que les dimensions sont correctes
    assert len(expected_returns) == 4
    assert cov_matrix.shape == (4, 4)
    
    # Vérifier que les indices correspondent aux tickers
    assert all(ticker in expected_returns.index for ticker in ['AAPL', 'MSFT', 'GOOGL', 'AMZN'])
    assert all(ticker in cov_matrix.index for ticker in ['AAPL', 'MSFT', 'GOOGL', 'AMZN'])
    
    # Vérifier que les valeurs sont dans des plages raisonnables
    assert all(-0.1 < r < 0.1 for r in expected_returns)
    assert all(0 <= cov_matrix.values[i, i] <= 0.1 for i in range(4))  # Variances positives

def test_optimize_portfolio(sample_returns):
    """Test de la fonction optimize_portfolio."""
    # Calculer les métriques du portefeuille
    expected_returns, cov_matrix = calculate_portfolio_metrics(sample_returns)
    
    # Optimiser le portefeuille
    frontier, weights = optimize_portfolio(expected_returns, cov_matrix, n_portfolios=100)
    
    # Vérifier que les types de retour sont corrects
    assert isinstance(frontier, pd.DataFrame)
    assert isinstance(weights, np.ndarray)
    
    # Vérifier que les dimensions sont correctes
    assert frontier.shape[0] == 100  # 100 portefeuilles
    assert frontier.shape[1] == 3    # Return, Volatility, Sharpe
    assert len(weights) == 4         # 4 actifs
    
    # Vérifier que les poids somment à 1
    assert np.isclose(np.sum(weights), 1.0)
    
    # Vérifier que les poids sont positifs (pas de vente à découvert)
    assert all(w >= 0 for w in weights)
    
    # Vérifier que la frontière efficiente contient les colonnes attendues
    assert all(col in frontier.columns for col in ['Return', 'Volatility', 'Sharpe'])
    
    # Vérifier que les valeurs sont dans des plages raisonnables
    assert all(-0.1 < r < 0.1 for r in frontier['Return'])
    assert all(0 < v < 0.5 for v in frontier['Volatility'])

def test_portfolio_optimization_with_risk_free_rate():
    """Test de l'optimisation de portefeuille avec différents taux sans risque."""
    # Créer des rendements d'exemple
    np.random.seed(42)
    returns = pd.DataFrame({
        'A': [0.01, 0.02, -0.01, 0.03, 0.01],
        'B': [0.02, 0.01, 0.02, -0.01, 0.02],
        'C': [0.03, -0.02, 0.01, 0.02, 0.01]
    })
    
    # Calculer les métriques du portefeuille
    expected_returns, cov_matrix = calculate_portfolio_metrics(returns)
    
    # Optimiser avec différents taux sans risque
    frontier1, weights1 = optimize_portfolio(expected_returns, cov_matrix, risk_free_rate=0.0, n_portfolios=50)
    frontier2, weights2 = optimize_portfolio(expected_returns, cov_matrix, risk_free_rate=0.02, n_portfolios=50)
    
    # Vérifier que les ratios de Sharpe sont différents
    max_sharpe1 = frontier1['Sharpe'].max()
    max_sharpe2 = frontier2['Sharpe'].max()
    
    assert max_sharpe1 != max_sharpe2
    
    # Vérifier que les poids optimaux sont différents
    assert not np.array_equal(weights1, weights2)
