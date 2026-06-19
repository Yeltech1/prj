"""
Module pour collecter des données financières réelles via Yahoo Finance.
"""
import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/logs/data_collection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("real_data_collector")

def fetch_stock_data(tickers, start_date, end_date, output_path=None, interval='1d'):
    """
    Récupère les données historiques des actions via Yahoo Finance.
    
    Parameters:
    - tickers: Liste des symboles d'actions (ex: ['AAPL', 'MSFT', 'GOOGL'])
    - start_date: Date de début (format: 'YYYY-MM-DD')
    - end_date: Date de fin (format: 'YYYY-MM-DD')
    - output_path: Chemin pour sauvegarder les données (optionnel)
    - interval: Intervalle des données ('1d', '1wk', '1mo', etc.)
    
    Returns:
    - DataFrame contenant les données historiques
    """
    logger.info(f"Récupération des données pour {len(tickers)} actions de {start_date} à {end_date}")
    
    # Créer le répertoire de sortie si nécessaire
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Créer un DataFrame vide pour stocker les données
    all_data = pd.DataFrame()
    
    # Récupérer les données pour chaque ticker avec gestion des erreurs et des tentatives
    for ticker in tickers:
        max_attempts = 3
        attempt = 0
        success = False
        
        while attempt < max_attempts and not success:
            try:
                logger.info(f"Tentative {attempt+1} pour {ticker}")
                # Récupérer les données via yfinance
                stock = yf.Ticker(ticker)
                data = stock.history(start=start_date, end=end_date, interval=interval)
                
                if data.empty:
                    logger.warning(f"Aucune donnée trouvée pour {ticker}")
                    attempt += 1
                    time.sleep(2)  # Attendre avant de réessayer
                    continue
                
                # Ajouter une colonne pour identifier le ticker
                data['Ticker'] = ticker
                
                # Ajouter au DataFrame principal
                all_data = pd.concat([all_data, data])
                
                logger.info(f"Données récupérées avec succès pour {ticker}: {len(data)} entrées")
                success = True
                
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des données pour {ticker}: {e}")
                attempt += 1
                time.sleep(2)  # Attendre avant de réessayer
        
        if not success:
            logger.error(f"Échec de la récupération des données pour {ticker} après {max_attempts} tentatives")
    
    # Vérifier si des données ont été récupérées
    if all_data.empty:
        logger.error("Aucune donnée n'a été récupérée pour tous les tickers")
        return None
    
    # Réorganiser les données
    all_data = all_data.reset_index()
    
    # Sauvegarder les données si un chemin est spécifié
    if output_path:
        all_data.to_csv(output_path, index=False)
        logger.info(f"Données sauvegardées dans {output_path}")
    
    return all_data

def preprocess_stock_data(data, output_path=None):
    """
    Prétraite les données brutes des actions pour calculer les rendements.
    
    Parameters:
    - data: DataFrame contenant les données brutes
    - output_path: Chemin pour sauvegarder les rendements (optionnel)
    
    Returns:
    - DataFrame contenant les rendements journaliers
    """
    logger.info("Prétraitement des données...")
    
    # Vérifier si les données sont valides
    if data is None or data.empty:
        logger.error("Aucune donnée à prétraiter")
        return None
    
    # Pivoter les données pour avoir les tickers en colonnes
    pivot_data = data.pivot(index='Date', columns='Ticker', values='Close')
    
    # Calculer les rendements journaliers
    returns = pivot_data.pct_change().dropna()
    
    # Supprimer les valeurs aberrantes (rendements > 50% ou < -50%)
    returns = returns.mask((returns > 0.5) | (returns < -0.5), np.nan)
    
    # Remplir les valeurs manquantes avec la moyenne des rendements
    returns = returns.fillna(returns.mean())
    
    logger.info(f"Prétraitement terminé: {len(returns)} jours de rendements pour {len(returns.columns)} actions")
    
    # Sauvegarder les rendements si un chemin est spécifié
    if output_path:
        # Créer le répertoire de sortie si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        returns.to_csv(output_path)
        logger.info(f"Rendements sauvegardés dans {output_path}")
    
    return returns

def get_market_data(tickers=None, start_date=None, end_date=None, lookback_years=5):
    """
    Récupère et prétraite les données de marché pour une liste d'actions.
    
    Parameters:
    - tickers: Liste des symboles d'actions (par défaut: indices et grandes capitalisations)
    - start_date: Date de début (format: 'YYYY-MM-DD')
    - end_date: Date de fin (format: 'YYYY-MM-DD')
    - lookback_years: Nombre d'années à récupérer si start_date n'est pas spécifié
    
    Returns:
    - Tuple (données brutes, rendements)
    """
    # Créer le répertoire de logs si nécessaire
    os.makedirs("data/logs", exist_ok=True)
    
    # Définir les tickers par défaut si non spécifiés
    if tickers is None:
        # Indices majeurs et grandes capitalisations
        tickers = [
            # Indices américains
            '^GSPC',  # S&P 500
            '^DJI',   # Dow Jones
            '^IXIC',  # NASDAQ
            # Grandes capitalisations technologiques
            'AAPL',   # Apple
            'MSFT',   # Microsoft
            'GOOGL',  # Alphabet (Google)
            'AMZN',   # Amazon
            'META',   # Meta (Facebook)
            'TSLA',   # Tesla
            'NVDA',   # NVIDIA
            # Grandes capitalisations financières et autres secteurs
            'JPM',    # JPMorgan Chase
            'V',      # Visa
            'PG',     # Procter & Gamble
            'JNJ',    # Johnson & Johnson
            'WMT',    # Walmart
            'XOM',    # Exxon Mobil
            'BAC',    # Bank of America
            'KO',     # Coca-Cola
            'DIS',    # Disney
            'NFLX'    # Netflix
        ]
    
    # Définir les dates par défaut si non spécifiées
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365 * lookback_years)).strftime('%Y-%m-%d')
    
    # Récupérer les données brutes
    raw_data_path = 'data/raw/stock_data.csv'
    raw_data = fetch_stock_data(tickers, start_date, end_date, raw_data_path)
    
    # Prétraiter les données
    returns_path = 'data/processed/returns.csv'
    returns = preprocess_stock_data(raw_data, returns_path)
    
    return raw_data, returns

if __name__ == "__main__":
    # Exemple d'utilisation
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 
        'TSLA', 'NVDA', 'JPM', 'V', 'PG'
    ]
    
    # Récupérer les données des 5 dernières années jusqu'à aujourd'hui
    raw_data, returns = get_market_data(tickers=tickers, lookback_years=5)
    
    if returns is not None:
        print(f"Données récupérées avec succès pour {len(returns.columns)} actions sur {len(returns)} jours")
        print("\nAperçu des rendements:")
        print(returns.tail())
