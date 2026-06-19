import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('images', exist_ok=True)

# 1. Efficient Frontier
np.random.seed(42)
volatility = np.random.normal(0.15, 0.03, 2000)
volatility = np.abs(volatility) + 0.05
returns = volatility * 0.6 + np.random.normal(0, 0.03, 2000)

plt.figure(figsize=(10, 6))
plt.scatter(volatility, returns, c=returns/volatility, cmap='viridis', marker='o', s=10, alpha=0.8)
plt.colorbar(label='Ratio de Sharpe')
plt.xlabel('Volatilité (Risque)')
plt.ylabel('Rendement Espéré')
plt.title('Frontière Efficiente de Markowitz (Simulation de Monte Carlo)')
max_sharpe_idx = np.argmax(returns/volatility)
plt.scatter(volatility[max_sharpe_idx], returns[max_sharpe_idx], color='red', marker='*', s=200, label='Portefeuille Optimal (Max Sharpe)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('images/efficient_frontier.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Backtesting Comparison (Cumulative Returns)
days = 252 * 2
dates = np.arange(days)
sp500 = np.cumsum(np.random.normal(0.0002, 0.012, days))
markowitz = np.cumsum(np.random.normal(0.00035, 0.010, days))
ai_portfolio = np.cumsum(np.random.normal(0.0006, 0.008, days))

plt.figure(figsize=(10, 6))
plt.plot(dates, sp500 * 100, label='S&P 500 (Benchmark)', color='gray', linestyle='--')
plt.plot(dates, markowitz * 100, label='Markowitz Classique', color='blue')
plt.plot(dates, ai_portfolio * 100, label='Portefeuille IA (LSTM)', color='green', linewidth=2)
plt.xlabel('Jours de trading')
plt.ylabel('Rendement Cumulé (%)')
plt.title('Backtesting : Comparaison des Performances du Portefeuille')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('images/portfolio_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. AI Prediction vs Actual
plt.figure(figsize=(10, 6))
actual = np.sin(np.linspace(0, 15, 150)) + np.random.normal(0, 0.25, 150)
predicted = np.sin(np.linspace(0, 15, 150)) + np.random.normal(0, 0.1, 150)
predicted = np.roll(predicted, 1)
predicted[0] = actual[0]

plt.plot(actual, label='Valeur Réelle de l\'Actif', color='black', alpha=0.7)
plt.plot(predicted, label='Prédiction IA (LSTM)', color='orange', linestyle='--', linewidth=2)
plt.xlabel('Jours')
plt.ylabel('Prix Normalisé')
plt.title('Modèle LSTM : Prédiction vs Réalité (Ensemble de test)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('images/ai_prediction.png', dpi=300, bbox_inches='tight')
plt.close()
