"""
Module pour le backtesting des stratégies d'optimisation de portefeuille.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

from src.models.ml_prediction import prepare_features, predict_returns, load_models
from simple_portfolio import calculate_portfolio_metrics, optimize_portfolio

def backtest_strategy(returns, window_size=252, rebalance_freq=21, use_ml=False, risk_free_rate=0.01):
    """
    Backtest une stratégie d'optimisation de portefeuille.
    
    Parameters:
    - returns: DataFrame des rendements journaliers
    - window_size: Taille de la fenêtre pour l'estimation des paramètres (jours)
    - rebalance_freq: Fréquence de rééquilibrage (jours)
    - use_ml: Utiliser les prédictions ML pour les rendements attendus
    - risk_free_rate: Taux sans risque annualisé
    
    Returns:
    - portfolio_values: Series des valeurs du portefeuille
    - all_weights: DataFrame des poids du portefeuille au fil du temps
    - metrics: DataFrame des métriques de performance
    """
    # Initialiser les variables
    portfolio_values = pd.Series(index=returns.index[window_size:], dtype=float)
    portfolio_values.iloc[0] = 1.0  # Valeur initiale du portefeuille
    
    all_weights = pd.DataFrame(index=returns.index[window_size:], columns=returns.columns)
    all_weights.iloc[0] = np.ones(len(returns.columns)) / len(returns.columns)  # Poids initiaux équipondérés
    
    # Charger les modèles ML si nécessaire
    if use_ml:
        try:
            models, scalers = load_models(returns.columns)
            ml_available = True
        except:
            print("Modèles ML non disponibles. Utilisation des rendements historiques.")
            ml_available = False
    else:
        ml_available = False
    
    # Boucle de backtesting
    for i in range(1, len(portfolio_values)):
        current_date = portfolio_values.index[i]
        prev_date = portfolio_values.index[i-1]
        
        # Appliquer les rendements du jour aux poids actuels
        daily_return = (returns.loc[current_date] * all_weights.loc[prev_date]).sum()
        portfolio_values.loc[current_date] = portfolio_values.loc[prev_date] * (1 + daily_return)
        
        # Vérifier si c'est le moment de rééquilibrer
        if i % rebalance_freq == 0:
            # Fenêtre de données pour l'estimation
            end_idx = returns.index.get_loc(prev_date)
            start_idx = end_idx - window_size + 1
            historical_returns = returns.iloc[start_idx:end_idx+1]
            
            # Calculer les rendements attendus
            if use_ml and ml_available:
                # Préparer les caractéristiques pour les modèles ML
                X, _ = prepare_features(historical_returns)
                # Prédire les rendements
                expected_returns = predict_returns(models, X, scalers)
            else:
                # Utiliser les rendements historiques moyens
                expected_returns, _ = calculate_portfolio_metrics(historical_returns)
            
            # Calculer la matrice de covariance
            _, cov_matrix = calculate_portfolio_metrics(historical_returns)
            
            # Optimiser le portefeuille
            frontier, optimal_weights = optimize_portfolio(expected_returns, cov_matrix)
            
            # Mettre à jour les poids
            all_weights.loc[current_date] = optimal_weights
        else:
            # Conserver les mêmes poids
            all_weights.loc[current_date] = all_weights.loc[prev_date]
    
    # Calculer les métriques de performance
    metrics = calculate_performance_metrics(portfolio_values, returns.index[window_size:], risk_free_rate)
    
    return portfolio_values, all_weights, metrics

def calculate_performance_metrics(portfolio_values, dates, risk_free_rate=0.01):
    """
    Calculer les métriques de performance du portefeuille.
    
    Parameters:
    - portfolio_values: Series des valeurs du portefeuille
    - dates: Index des dates
    - risk_free_rate: Taux sans risque annualisé
    
    Returns:
    - metrics: DataFrame des métriques de performance
    """
    # Calculer les rendements journaliers
    daily_returns = portfolio_values.pct_change().dropna()
    
    # Rendement total
    total_return = (portfolio_values.iloc[-1] / portfolio_values.iloc[0]) - 1
    
    # Rendement annualisé
    years = (dates[-1] - dates[0]).days / 365.25
    annual_return = (1 + total_return) ** (1 / years) - 1
    
    # Volatilité annualisée
    annual_volatility = daily_returns.std() * np.sqrt(252)
    
    # Ratio de Sharpe
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    
    # Drawdown maximal
    cumulative_returns = (1 + daily_returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns / running_max) - 1
    max_drawdown = drawdown.min()
    
    # Créer un DataFrame des métriques
    metrics = pd.DataFrame({
        'Métrique': ['Rendement Total', 'Rendement Annualisé', 'Volatilité Annualisée', 
                    'Ratio de Sharpe', 'Drawdown Maximal'],
        'Valeur': [total_return, annual_return, annual_volatility, sharpe_ratio, max_drawdown]
    })
    
    return metrics

def compare_strategies(returns, strategies, window_size=252, risk_free_rate=0.01):
    """
    Comparer différentes stratégies d'optimisation de portefeuille.
    
    Parameters:
    - returns: DataFrame des rendements journaliers
    - strategies: Dictionnaire des stratégies à comparer
    - window_size: Taille de la fenêtre pour l'estimation des paramètres (jours)
    - risk_free_rate: Taux sans risque annualisé
    
    Returns:
    - comparison: DataFrame des métriques de performance pour chaque stratégie
    - portfolio_values: DataFrame des valeurs du portefeuille pour chaque stratégie
    """
    portfolio_values = pd.DataFrame(index=returns.index[window_size:])
    all_metrics = []
    
    for name, params in strategies.items():
        print(f"Backtesting de la stratégie '{name}'...")
        values, _, metrics = backtest_strategy(
            returns, 
            window_size=params.get('window_size', window_size),
            rebalance_freq=params.get('rebalance_freq', 21),
            use_ml=params.get('use_ml', False),
            risk_free_rate=risk_free_rate
        )
        
        portfolio_values[name] = values
        metrics['Stratégie'] = name
        all_metrics.append(metrics)
    
    # Créer un DataFrame de comparaison
    comparison = pd.concat(all_metrics)
    
    return comparison, portfolio_values

def plot_strategy_comparison(portfolio_values, output_path=None):
    """
    Visualiser la comparaison des stratégies.
    
    Parameters:
    - portfolio_values: DataFrame des valeurs du portefeuille pour chaque stratégie
    - output_path: Chemin pour sauvegarder la figure
    
    Returns:
    - fig: Figure matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for column in portfolio_values.columns:
        ax.plot(portfolio_values.index, portfolio_values[column], label=column)
    
    ax.set_title('Comparaison des Stratégies')
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur du Portefeuille')
    ax.legend()
    ax.grid(True)
    
    if output_path:
        plt.savefig(output_path)
    
    return fig

if __name__ == "__main__":
    # Charger les rendements
    returns = pd.read_csv('../../data/processed/returns.csv', index_col=0, parse_dates=True)
    
    # Définir les stratégies à comparer
    strategies = {
        'Équipondérée': {
            'window_size': 252,
            'rebalance_freq': 63,  # Trimestriel
            'use_ml': False
        },
        'MPT Mensuelle': {
            'window_size': 252,
            'rebalance_freq': 21,  # Mensuel
            'use_ml': False
        },
        'MPT + ML': {
            'window_size': 252,
            'rebalance_freq': 21,
            'use_ml': True
        }
    }
    
    # Comparer les stratégies
    comparison, portfolio_values = compare_strategies(returns, strategies)
    
    # Sauvegarder les résultats
    os.makedirs('../../data/processed', exist_ok=True)
    os.makedirs('../../reports/figures', exist_ok=True)
    
    comparison.to_csv('../../data/processed/strategy_comparison.csv')
    portfolio_values.to_csv('../../data/processed/backtest_values.csv')
    
    # Visualiser les résultats
    plot_strategy_comparison(portfolio_values, '../../reports/figures/strategy_comparison.png')
    
    # Afficher les métriques
    print("\nComparaison des stratégies :")
    for strategy in strategies.keys():
        metrics = comparison[comparison['Stratégie'] == strategy]
        print(f"\n{strategy}:")
        for _, row in metrics.iterrows():
            value = row['Valeur']
            if row['Métrique'] in ['Rendement Total', 'Rendement Annualisé', 'Volatilité Annualisée', 'Drawdown Maximal']:
                value = f"{value:.2%}"
            elif row['Métrique'] == 'Ratio de Sharpe':
                value = f"{value:.2f}"
            print(f"  {row['Métrique']}: {value}")
