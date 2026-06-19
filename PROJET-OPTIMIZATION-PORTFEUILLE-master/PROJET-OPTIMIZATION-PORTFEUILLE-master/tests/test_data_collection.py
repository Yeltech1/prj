"""
Tests pour le module de collecte de données.
"""
import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.data.real_data_collector import fetch_stock_data, preprocess_stock_data

@pytest.fixture
def sample_stock_data():
    """Fixture pour générer des données d'actions d'exemple."""
    # Créer des données d'exemple
    data = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=10),
        'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
        'Low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
        'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900],
        'Ticker': ['AAPL'] * 10
    })
    
    # Ajouter des données pour un autre ticker
    data2 = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=10),
        'Open': [200, 201, 202, 203, 204, 205, 206, 207, 208, 209],
        'High': [202, 203, 204, 205, 206, 207, 208, 209, 210, 211],
        'Low': [198, 199, 200, 201, 202, 203, 204, 205, 206, 207],
        'Close': [201, 202, 203, 204, 205, 206, 207, 208, 209, 210],
        'Volume': [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900],
        'Ticker': ['MSFT'] * 10
    })
    
    return pd.concat([data, data2]).reset_index(drop=True)

@patch('src.data.real_data_collector.yf.Ticker')
def test_fetch_stock_data(mock_ticker, tmp_path):
    """Test de la fonction fetch_stock_data avec des mocks."""
    # Configurer le mock
    mock_instance = MagicMock()
    mock_ticker.return_value = mock_instance
    
    # Créer des données d'exemple pour le mock
    history_data = pd.DataFrame({
        'Open': [100, 101],
        'High': [102, 103],
        'Low': [98, 99],
        'Close': [101, 102],
        'Volume': [1000, 1100]
    }, index=pd.date_range(start='2020-01-01', periods=2))
    
    mock_instance.history.return_value = history_data
    
    # Créer un chemin temporaire pour le fichier de sortie
    output_path = os.path.join(tmp_path, 'test_data.csv')
    
    # Appeler la fonction avec des tickers de test
    result = fetch_stock_data(
        tickers=['AAPL', 'MSFT'],
        start_date='2020-01-01',
        end_date='2020-01-02',
        output_path=output_path
    )
    
    # Vérifier que la fonction a été appelée correctement
    assert mock_ticker.call_count == 2
    mock_instance.history.assert_called_with(start='2020-01-01', end='2020-01-02', interval='1d')
    
    # Vérifier que le résultat n'est pas None
    assert result is not None
    
    # Vérifier que le fichier a été créé
    assert os.path.exists(output_path)

def test_preprocess_stock_data(sample_stock_data, tmp_path):
    """Test de la fonction preprocess_stock_data."""
    # Créer un chemin temporaire pour le fichier de sortie
    output_path = os.path.join(tmp_path, 'test_returns.csv')
    
    # Appeler la fonction avec les données d'exemple
    returns = preprocess_stock_data(sample_stock_data, output_path)
    
    # Vérifier que le résultat n'est pas None
    assert returns is not None
    
    # Vérifier que le DataFrame a la bonne structure
    assert isinstance(returns, pd.DataFrame)
    assert 'AAPL' in returns.columns
    assert 'MSFT' in returns.columns
    
    # Vérifier que les rendements sont calculés correctement
    # Le premier jour devrait être NaN, puis les rendements devraient être calculés
    assert returns.shape[0] == 9  # 10 jours - 1 (NaN supprimé)
    
    # Vérifier que le fichier a été créé
    assert os.path.exists(output_path)
