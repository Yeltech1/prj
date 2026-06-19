"""
Script pour générer des données simulées pour le projet d'optimisation de portefeuille.
"""
import pandas as pd
import numpy as np
import os
import datetime as dt

def generate_stock_data(tickers, start_date, end_date, output_path):
    """
    Générer des données simulées pour les actions et les sauvegarder dans un fichier CSV.
    
    Parameters:
    - tickers: Liste des symboles d'actions (ex: ['AAPL', 'MSFT', 'GOOGL'])
    - start_date: Date de début (ex: '2020-01-01')
    - end_date: Date de fin (ex: '2023-01-01')
    - output_path: Chemin pour sauvegarder le fichier CSV
    """
    # Convertir les dates en objets datetime
    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')
    
    # Créer une plage de dates (jours ouvrables)
    date_range = pd.date_range(start=start, end=end, freq='B')
    
    # Créer un DataFrame vide avec les dates comme index
    all_data = pd.DataFrame(index=date_range)
    
    # Paramètres pour la simulation
    np.random.seed(42)  # Pour la reproductibilité
    
    # Générer des données pour chaque ticker
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
        returns = np.random.normal(mu, sigma, len(date_range))
        
        # Calculer les prix cumulatifs
        prices = price_start * (1 + returns).cumprod()
        
        # Ajouter au DataFrame principal
        all_data[f'{ticker}_Open'] = prices * 0.99
        all_data[f'{ticker}_High'] = prices * 1.02
        all_data[f'{ticker}_Low'] = prices * 0.98
        all_data[f'{ticker}_Close'] = prices
        all_data[f'{ticker}_Adj Close'] = prices
        all_data[f'{ticker}_Volume'] = np.random.randint(1000000, 10000000, len(date_range))
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Sauvegarder les données
    all_data.to_csv(output_path)
    print(f"Données simulées sauvegardées dans {output_path}")
    
    return all_data

def preprocess_data(input_path, output_path):
    """
    Prétraiter les données simulées et calculer les rendements.
    
    Parameters:
    - input_path: Chemin vers les données brutes
    - output_path: Chemin pour sauvegarder les données prétraitées
    """
    # Charger les données
    df = pd.read_csv(input_path, index_col=0, parse_dates=True)
    
    # Extraire les prix de clôture ajustés pour chaque ticker
    tickers = set([col.split('_')[0] for col in df.columns if 'Adj Close' in col])
    prices = pd.DataFrame()
    
    for ticker in tickers:
        prices[ticker] = df[f'{ticker}_Adj Close']
    
    # Calculer les rendements journaliers
    returns = prices.pct_change().dropna()
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Sauvegarder les rendements
    returns.to_csv(output_path)
    print(f"Rendements calculés et sauvegardés dans {output_path}")
    
    return returns

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'PG']
    start_date = '2018-01-01'
    end_date = '2023-01-01'
    raw_data_path = 'data/raw/stock_data.csv'
    processed_data_path = 'data/processed/returns.csv'
    
    print("Génération des données simulées...")
    generate_stock_data(tickers, start_date, end_date, raw_data_path)
    
    print("Prétraitement des données...")
    preprocess_data(raw_data_path, processed_data_path)
    
    print("Terminé!")
