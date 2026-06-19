"""
Script simplifié pour démontrer l'optimisation de portefeuille sans dépendances externes.
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Créer les répertoires nécessaires
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('reports/figures', exist_ok=True)

# Générer des données simulées
def generate_stock_data(tickers, start_date, end_date, n_days=1000):
    """Générer des données de prix simulées pour les actions."""
    np.random.seed(42)  # Pour la reproductibilité
    
    # Créer un DataFrame avec des dates
    dates = pd.date_range(start=start_date, end=end_date, periods=n_days)
    prices = pd.DataFrame(index=dates)
    
    # Générer des prix pour chaque ticker
    for ticker in tickers:
        # Paramètres spécifiques à chaque action
        if ticker == 'AAPL':
            mu = 0.0008  # Rendement journalier moyen (environ 20% annuel)
            sigma = 0.015  # Volatilité journalière
            price_start = 100.0
        elif ticker == 'MSFT':
            mu = 0.0007  # Rendement journalier moyen (environ 17% annuel)
            sigma = 0.014  # Volatilité journalière
            price_start = 200.0
        elif ticker == 'GOOGL':
            mu = 0.0006  # Rendement journalier moyen (environ 15% annuel)
            sigma = 0.016  # Volatilité journalière
            price_start = 1000.0
        else:
            mu = 0.0005  # Rendement journalier moyen par défaut
            sigma = 0.012  # Volatilité journalière par défaut
            price_start = 50.0
        
        # Générer des rendements journaliers suivant une distribution normale
        returns = np.random.normal(mu, sigma, n_days)
        
        # Calculer les prix cumulatifs
        prices[ticker] = price_start * (1 + returns).cumprod()
    
    return prices

# Calculer les rendements
def calculate_returns(prices):
    """Calculer les rendements journaliers à partir des prix."""
    returns = prices.pct_change().dropna()
    return returns

# Calculer les métriques du portefeuille
def calculate_portfolio_metrics(returns):
    """Calculer les rendements attendus et la matrice de covariance."""
    expected_returns = returns.mean() * 252  # Annualiser les rendements
    cov_matrix = returns.cov() * 252  # Annualiser la covariance
    return expected_returns, cov_matrix

# Optimisation de portefeuille simplifiée
def optimize_portfolio(expected_returns, cov_matrix, n_portfolios=10000):
    """
    Optimisation de portefeuille simplifiée en générant des portefeuilles aléatoires.
    """
    n_assets = len(expected_returns)
    results = np.zeros((3, n_portfolios))
    weights_record = []
    
    for i in range(n_portfolios):
        # Générer des poids aléatoires
        weights = np.random.random(n_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        # Calculer le rendement attendu
        portfolio_return = np.sum(expected_returns * weights)
        
        # Calculer la volatilité du portefeuille
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Calculer le ratio de Sharpe (supposant un taux sans risque de 1%)
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = (portfolio_return - 0.01) / portfolio_volatility
    
    # Trouver le portefeuille avec le ratio de Sharpe maximal
    max_sharpe_idx = np.argmax(results[2])
    
    # Créer un DataFrame pour la frontière efficiente
    frontier = pd.DataFrame({
        'Return': results[0],
        'Volatility': results[1],
        'Sharpe': results[2]
    })
    
    return frontier, weights_record[max_sharpe_idx]

# Visualiser la frontière efficiente
def plot_efficient_frontier(frontier, optimal_weights, tickers):
    """Visualiser la frontière efficiente et le portefeuille optimal."""
    plt.figure(figsize=(10, 6))
    plt.scatter(frontier['Volatility'], frontier['Return'], c=frontier['Sharpe'], cmap='viridis', alpha=0.5)
    
    # Marquer le portefeuille optimal
    max_sharpe_idx = frontier['Sharpe'].idxmax()
    plt.scatter(
        frontier.loc[max_sharpe_idx, 'Volatility'],
        frontier.loc[max_sharpe_idx, 'Return'],
        c='red', s=100, marker='*',
        label='Portefeuille Optimal'
    )
    
    plt.colorbar(label='Ratio de Sharpe')
    plt.xlabel('Volatilité (Risque)')
    plt.ylabel('Rendement Attendu')
    plt.title('Frontière Efficiente')
    plt.legend()
    plt.savefig('reports/figures/efficient_frontier.png')
    
    # Visualiser les poids du portefeuille optimal
    plt.figure(figsize=(10, 6))
    plt.bar(tickers, optimal_weights)
    plt.xlabel('Actifs')
    plt.ylabel('Poids dans le Portefeuille')
    plt.title('Allocation du Portefeuille Optimal')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/figures/optimal_allocation.png')

def main():
    # Paramètres
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'PG']
    start_date = '2018-01-01'
    end_date = '2023-01-01'
    
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
    
    print("Visualisation des résultats...")
    plot_efficient_frontier(frontier, optimal_weights, tickers)
    
    print("Terminé! Les résultats sont disponibles dans les répertoires 'data/processed' et 'reports/figures'.")
    
    # Afficher les poids optimaux
    print("\nPoids du portefeuille optimal:")
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight:.2%}")

if __name__ == "__main__":
    main()
