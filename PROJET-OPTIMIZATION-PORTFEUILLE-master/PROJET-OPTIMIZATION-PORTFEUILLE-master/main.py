"""
Script principal pour exécuter le pipeline complet d'optimisation de portefeuille.
"""
import os
import pandas as pd
import numpy as np
import argparse
from datetime import datetime

# Importer les modules du projet
try:
    # Essayer d'importer les modules du projet
    from src.data.data_collection import fetch_stock_data
    from src.data.preprocessing import preprocess_data
    from src.models.mpt import calculate_portfolio_metrics, optimize_portfolio, efficient_frontier
    from src.models.ml_models import prepare_ml_data, train_models
    from src.models.optimization import backtest_portfolio
    from src.visualization.visualize import (
        plot_returns_distribution,
        plot_correlation_matrix,
        plot_efficient_frontier,
        plot_portfolio_performance
    )
    from src.models.ml_prediction import prepare_features, train_models as train_ml_models, save_models, predict_returns
    from src.models.backtest import backtest_strategy, compare_strategies, plot_strategy_comparison

    # Modules disponibles
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Avertissement: Certains modules ne sont pas disponibles. Utilisation des fonctions simplifiées. ({e})")
    # Importer les fonctions simplifiées
    from simple_portfolio import (
        calculate_returns,
        calculate_portfolio_metrics,
        optimize_portfolio
    )

    # Modules non disponibles
    MODULES_AVAILABLE = False

def ensure_directories():
    """Créer les répertoires nécessaires s'ils n'existent pas."""
    directories = [
        'data/raw',
        'data/processed',
        'reports/figures'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def run_data_pipeline(tickers, start_date, end_date):
    """Exécuter le pipeline de collecte et prétraitement des données."""
    print("Collecte des données...")
    raw_data_path = 'data/raw/stock_data.csv'
    processed_data_path = 'data/processed/returns.csv'

    # Collecter les données
    data = fetch_stock_data(tickers, start_date, end_date, raw_data_path)

    # Prétraiter les données
    returns = preprocess_data(raw_data_path, processed_data_path)

    return returns

def run_portfolio_optimization(returns):
    """Exécuter l'optimisation de portefeuille avec MPT."""
    print("Optimisation du portefeuille avec MPT...")

    # Calculer les métriques du portefeuille
    expected_returns, cov_matrix = calculate_portfolio_metrics(returns)

    # Générer la frontière efficiente
    ef = efficient_frontier(expected_returns, cov_matrix)
    ef.to_csv('data/processed/efficient_frontier.csv')

    # Trouver le portefeuille optimal (ratio de Sharpe maximal)
    # Taux sans risque supposé à 0.01 (1%)
    risk_free_rate = 0.01
    sharpe_ratios = (ef['Return'] - risk_free_rate) / ef['Volatility']
    optimal_idx = sharpe_ratios.idxmax()
    optimal_portfolio = ef.iloc[optimal_idx]

    # Sauvegarder les poids optimaux
    weights = optimal_portfolio['Weights']
    pd.Series(weights, index=returns.columns).to_csv('data/processed/optimal_weights.csv')

    # Visualiser la frontière efficiente
    fig = plot_efficient_frontier(
        ef,
        optimal_portfolio=(optimal_portfolio['Return'], optimal_portfolio['Volatility']),
        save_path='reports/figures/efficient_frontier.html'
    )

    return expected_returns, cov_matrix, weights

def run_ml_pipeline(returns):
    """Exécuter le pipeline d'apprentissage automatique."""
    print("Entraînement des modèles d'apprentissage automatique...")

    # Préparer les données pour ML
    features = prepare_ml_data(returns)

    # Diviser les données
    train_size = int(0.8 * len(features))
    X_train = features.iloc[:train_size, 1:]
    X_test = features.iloc[train_size:, 1:]

    # Pour chaque actif, entraîner un modèle
    ml_predictions = {}

    for i, asset in enumerate(returns.columns):
        print(f"Entraînement du modèle pour {asset}...")
        y_train = features.iloc[:train_size, i]
        y_test = features.iloc[train_size:, i]

        # Entraîner les modèles
        results = train_models(X_train, y_train, X_test, y_test)

        # Utiliser le meilleur modèle pour les prédictions
        best_model = min(results, key=results.get)
        ml_predictions[asset] = results[best_model]

    # Convertir en Series pour l'optimisation
    predicted_returns = pd.Series(ml_predictions)
    predicted_returns.to_csv('data/processed/predicted_returns.csv')

    return predicted_returns

def run_backtest(returns, predicted_returns, cov_matrix):
    """Exécuter le backtest du portefeuille optimisé."""
    print("Backtesting du portefeuille...")

    # Backtest avec les rendements prédits
    portfolio_values, weights = backtest_portfolio(returns, predicted_returns, cov_matrix)

    # Sauvegarder les résultats
    portfolio_values.to_csv('data/processed/portfolio_performance.csv')
    pd.Series(weights, index=returns.columns).to_csv('data/processed/backtest_weights.csv')

    # Créer un benchmark (portefeuille équipondéré)
    equal_weights = np.ones(len(returns.columns)) / len(returns.columns)
    benchmark = (returns @ equal_weights).cumsum()

    # Visualiser la performance
    fig = plot_portfolio_performance(
        portfolio_values,
        benchmark=benchmark,
        save_path='reports/figures/portfolio_performance.html'
    )

    return portfolio_values, benchmark

def run_ml_prediction_pipeline(returns):
    """Exécuter le pipeline de prédiction ML avec les nouveaux modèles."""
    print("Exécution du pipeline de prédiction ML...")

    # Préparer les caractéristiques
    X, y = prepare_features(returns)

    # Entraîner les modèles
    models, X_test, y_test, scalers = train_ml_models(X, y)

    # Sauvegarder les modèles
    save_models(models, scalers)

    # Prédire les rendements futurs
    predictions = predict_returns(models, X, scalers)
    predictions.to_csv('data/processed/ml_predicted_returns.csv')

    print("Prédictions des rendements futurs :")
    for ticker, pred in predictions.items():
        print(f"{ticker}: {pred:.6f}")

    return predictions

def run_strategy_comparison(returns):
    """Exécuter la comparaison des stratégies."""
    print("Comparaison des stratégies d'investissement...")

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
    comparison.to_csv('data/processed/strategy_comparison.csv')
    portfolio_values.to_csv('data/processed/backtest_values.csv')

    # Visualiser les résultats
    plot_strategy_comparison(portfolio_values, 'reports/figures/strategy_comparison.png')

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

    return comparison, portfolio_values

def run_simplified_pipeline():
    """Exécuter un pipeline simplifié lorsque les modules complets ne sont pas disponibles."""
    print("Exécution du pipeline simplifié...")

    # Paramètres
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'PG']
    start_date = '2018-01-01'
    end_date = '2023-01-01'

    # Générer des données simulées
    from simple_portfolio import generate_stock_data, calculate_returns

    print("Génération des données simulées...")
    prices = generate_stock_data(tickers, start_date, end_date)
    prices.to_csv('data/raw/stock_prices.csv')

    print("Calcul des rendements...")
    returns = calculate_returns(prices)
    returns.to_csv('data/processed/returns.csv')

    print("Calcul des métriques du portefeuille...")
    expected_returns, cov_matrix = calculate_portfolio_metrics(returns)

    print("Optimisation du portefeuille...")
    frontier, optimal_weights = optimize_portfolio(expected_returns, cov_matrix)
    frontier.to_csv('data/processed/efficient_frontier.csv')

    # Sauvegarder les poids optimaux
    pd.Series(optimal_weights, index=tickers).to_csv('data/processed/optimal_weights.csv')

    print("Terminé! Les résultats sont disponibles dans les répertoires 'data/processed'.")

    # Afficher les poids optimaux
    print("\nPoids du portefeuille optimal:")
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight:.2%}")

    return returns, expected_returns, cov_matrix, optimal_weights

def parse_arguments():
    """Parser les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Pipeline d\'optimisation de portefeuille')

    parser.add_argument('--mode', type=str, default='full',
                        choices=['full', 'data', 'optimize', 'ml', 'backtest', 'compare', 'simplified'],
                        help='Mode d\'exécution du pipeline')

    parser.add_argument('--tickers', type=str, nargs='+',
                        default=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'PG'],
                        help='Liste des tickers à analyser')

    parser.add_argument('--start-date', type=str, default='2018-01-01',
                        help='Date de début pour les données (format: YYYY-MM-DD)')

    parser.add_argument('--end-date', type=str, default='2023-01-01',
                        help='Date de fin pour les données (format: YYYY-MM-DD)')

    return parser.parse_args()

def main():
    """Fonction principale."""
    # Parser les arguments
    args = parse_arguments()

    # Assurer que les répertoires existent
    ensure_directories()

    # Vérifier si les modules complets sont disponibles
    if not MODULES_AVAILABLE:
        print("Les modules complets ne sont pas disponibles. Exécution du pipeline simplifié.")
        run_simplified_pipeline()
        return

    # Exécuter le pipeline selon le mode
    if args.mode == 'simplified':
        run_simplified_pipeline()
        return

    # Pour les autres modes, nous avons besoin des données
    if args.mode in ['full', 'data']:
        returns = run_data_pipeline(args.tickers, args.start_date, args.end_date)
    else:
        # Charger les données existantes
        try:
            returns = pd.read_csv('data/processed/returns.csv', index_col=0, parse_dates=True)
        except FileNotFoundError:
            print("Données non trouvées. Exécution du pipeline de données...")
            returns = run_data_pipeline(args.tickers, args.start_date, args.end_date)

    # Visualisations des données
    if args.mode in ['full', 'data']:
        plot_returns_distribution(returns, save_path='reports/figures/returns_distribution.png')
        plot_correlation_matrix(returns, save_path='reports/figures/correlation_matrix.png')

    # Optimisation de portefeuille
    if args.mode in ['full', 'optimize']:
        expected_returns, cov_matrix, mpt_weights = run_portfolio_optimization(returns)
    else:
        # Calculer les métriques si nécessaire pour d'autres modes
        if args.mode in ['ml', 'backtest', 'compare']:
            expected_returns, cov_matrix = calculate_portfolio_metrics(returns)

    # Pipeline ML
    if args.mode in ['full', 'ml']:
        # Ancien pipeline ML
        predicted_returns_old = run_ml_pipeline(returns)

        # Nouveau pipeline ML
        try:
            predicted_returns = run_ml_prediction_pipeline(returns)
        except Exception as e:
            print(f"Erreur lors de l'exécution du pipeline ML: {e}")
            predicted_returns = predicted_returns_old

    # Backtest
    if args.mode in ['full', 'backtest']:
        try:
            predicted_returns = pd.read_csv('data/processed/ml_predicted_returns.csv', index_col=0, squeeze=True)
        except FileNotFoundError:
            try:
                predicted_returns = pd.read_csv('data/processed/predicted_returns.csv', index_col=0, squeeze=True)
            except FileNotFoundError:
                print("Prédictions non trouvées. Exécution du pipeline ML...")
                predicted_returns = run_ml_pipeline(returns)

        portfolio_values, benchmark = run_backtest(returns, predicted_returns, cov_matrix)

    # Comparaison des stratégies
    if args.mode in ['full', 'compare']:
        comparison, portfolio_values = run_strategy_comparison(returns)

    print("Pipeline d'optimisation de portefeuille terminé avec succès!")
    print(f"Les résultats sont disponibles dans les répertoires 'data/processed' et 'reports/figures'")

if __name__ == "__main__":
    main()
