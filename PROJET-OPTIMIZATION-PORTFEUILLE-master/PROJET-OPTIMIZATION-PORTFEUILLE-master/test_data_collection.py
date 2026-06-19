"""
Script simple pour tester la collecte de données avec pandas-datareader.
"""
import pandas as pd
import os
import datetime as dt

def fetch_stock_data(tickers, start_date, end_date, output_path):
    """
    Fetch historical stock data using pandas and save to CSV.
    
    Parameters:
    - tickers: List of stock tickers (e.g., ['AAPL', 'MSFT', 'GOOGL'])
    - start_date: Start date for data (e.g., '2020-01-01')
    - end_date: End date for data (e.g., '2025-01-01')
    - output_path: Path to save CSV file
    """
    try:
        # Utiliser pandas-datareader avec Yahoo Finance
        import pandas_datareader.data as web
        
        # Convertir les dates en objets datetime
        start = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end = dt.datetime.strptime(end_date, '%Y-%m-%d')
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Récupérer les données pour chaque ticker
        data_frames = []
        for ticker in tickers:
            print(f"Récupération des données pour {ticker}...")
            try:
                df = web.DataReader(ticker, 'yahoo', start, end)
                df['Ticker'] = ticker  # Ajouter une colonne pour identifier le ticker
                data_frames.append(df)
            except Exception as e:
                print(f"Erreur lors de la récupération des données pour {ticker}: {e}")
        
        # Combiner tous les dataframes
        if data_frames:
            combined_data = pd.concat(data_frames)
            combined_data.to_csv(output_path)
            print(f"Données sauvegardées dans {output_path}")
            return combined_data
        else:
            print("Aucune donnée n'a été récupérée.")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des données: {e}")
        return None

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2020-01-01'
    end_date = '2023-01-01'
    output_path = 'data/raw/stock_data.csv'
    
    print("Début de la collecte des données...")
    fetch_stock_data(tickers, start_date, end_date, output_path)
    print("Fin de la collecte des données.")
