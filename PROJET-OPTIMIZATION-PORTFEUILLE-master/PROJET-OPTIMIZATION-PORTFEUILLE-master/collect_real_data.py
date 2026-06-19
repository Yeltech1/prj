"""
Script pour collecter des données financières réelles.
"""
import os
import argparse
from datetime import datetime, timedelta
from src.data.real_data_collector import get_market_data

def parse_arguments():
    """Parser les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Collecte de données financières réelles')
    
    parser.add_argument('--tickers', type=str, nargs='+',
                        help='Liste des symboles d\'actions à collecter')
    
    parser.add_argument('--start-date', type=str,
                        help='Date de début (format: YYYY-MM-DD)')
    
    parser.add_argument('--end-date', type=str, 
                        default=datetime.now().strftime('%Y-%m-%d'),
                        help='Date de fin (format: YYYY-MM-DD)')
    
    parser.add_argument('--years', type=int, default=5,
                        help='Nombre d\'années à récupérer si start-date n\'est pas spécifié')
    
    return parser.parse_args()

def main():
    """Fonction principale."""
    # Parser les arguments
    args = parse_arguments()
    
    # Créer les répertoires nécessaires
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/logs', exist_ok=True)
    
    print(f"Collecte de données financières réelles...")
    
    # Récupérer les données
    raw_data, returns = get_market_data(
        tickers=args.tickers,
        start_date=args.start_date,
        end_date=args.end_date,
        lookback_years=args.years
    )
    
    if returns is not None:
        print(f"Données récupérées avec succès pour {len(returns.columns)} actions sur {len(returns)} jours")
        print("\nAperçu des rendements:")
        print(returns.tail())
        
        print("\nStatistiques des rendements:")
        print(returns.describe())
        
        print(f"\nLes données ont été sauvegardées dans:")
        print(f"- Données brutes: data/raw/stock_data.csv")
        print(f"- Rendements: data/processed/returns.csv")
    else:
        print("Échec de la collecte de données.")

if __name__ == "__main__":
    main()
