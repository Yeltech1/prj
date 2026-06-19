"""
Module pour la prédiction des rendements futurs avec des modèles d'apprentissage automatique.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def prepare_features(returns, window_size=10):
    """
    Prépare les caractéristiques pour les modèles ML en utilisant des fenêtres glissantes.
    
    Parameters:
    - returns: DataFrame des rendements journaliers
    - window_size: Taille de la fenêtre pour les caractéristiques (jours précédents)
    
    Returns:
    - X: DataFrame des caractéristiques
    - y: DataFrame des cibles (rendements à prédire)
    """
    features = pd.DataFrame()
    
    # Pour chaque actif
    for ticker in returns.columns:
        # Créer des caractéristiques basées sur les rendements passés
        for i in range(1, window_size + 1):
            features[f'{ticker}_lag_{i}'] = returns[ticker].shift(i)
        
        # Ajouter des caractéristiques techniques simples
        features[f'{ticker}_ma_5'] = returns[ticker].rolling(window=5).mean()
        features[f'{ticker}_ma_10'] = returns[ticker].rolling(window=10).mean()
        features[f'{ticker}_std_5'] = returns[ticker].rolling(window=5).std()
        features[f'{ticker}_std_10'] = returns[ticker].rolling(window=10).std()
    
    # Supprimer les lignes avec des valeurs manquantes
    features = features.dropna()
    
    # Créer les cibles (rendements du jour suivant)
    y = returns.loc[features.index]
    
    return features, y

def train_models(X, y, test_size=0.2, random_state=42):
    """
    Entraîne des modèles ML pour prédire les rendements.
    
    Parameters:
    - X: DataFrame des caractéristiques
    - y: DataFrame des cibles
    - test_size: Proportion des données pour le test
    - random_state: Graine aléatoire pour la reproductibilité
    
    Returns:
    - models: Dictionnaire des modèles entraînés
    - X_test: Caractéristiques de test
    - y_test: Cibles de test
    - scalers: Dictionnaire des scalers pour chaque actif
    """
    models = {}
    scalers = {}
    X_test_all = {}
    y_test_all = {}
    
    # Pour chaque actif, entraîner un modèle séparé
    for ticker in y.columns:
        print(f"Entraînement des modèles pour {ticker}...")
        
        # Sélectionner les caractéristiques pertinentes pour cet actif
        ticker_features = [col for col in X.columns if ticker in col]
        X_ticker = X[ticker_features]
        y_ticker = y[ticker]
        
        # Diviser les données
        X_train, X_test, y_train, y_test = train_test_split(
            X_ticker, y_ticker, test_size=test_size, random_state=random_state
        )
        
        # Normaliser les données
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Entraîner les modèles
        models[ticker] = {}
        
        # Régression linéaire
        lr = LinearRegression()
        lr.fit(X_train_scaled, y_train)
        lr_pred = lr.predict(X_test_scaled)
        lr_mse = mean_squared_error(y_test, lr_pred)
        lr_r2 = r2_score(y_test, lr_pred)
        models[ticker]['LinearRegression'] = {
            'model': lr,
            'mse': lr_mse,
            'r2': lr_r2
        }
        
        # Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=random_state)
        rf.fit(X_train_scaled, y_train)
        rf_pred = rf.predict(X_test_scaled)
        rf_mse = mean_squared_error(y_test, rf_pred)
        rf_r2 = r2_score(y_test, rf_pred)
        models[ticker]['RandomForest'] = {
            'model': rf,
            'mse': rf_mse,
            'r2': rf_r2
        }
        
        # Sauvegarder le scaler et les données de test
        scalers[ticker] = scaler
        X_test_all[ticker] = X_test
        y_test_all[ticker] = y_test
        
        print(f"  Linear Regression - MSE: {lr_mse:.6f}, R²: {lr_r2:.4f}")
        print(f"  Random Forest - MSE: {rf_mse:.6f}, R²: {rf_r2:.4f}")
    
    return models, X_test_all, y_test_all, scalers

def predict_returns(models, X, scalers):
    """
    Prédit les rendements futurs en utilisant les modèles entraînés.
    
    Parameters:
    - models: Dictionnaire des modèles entraînés
    - X: DataFrame des caractéristiques
    - scalers: Dictionnaire des scalers pour chaque actif
    
    Returns:
    - predictions: Series des rendements prédits
    """
    predictions = {}
    
    for ticker in models.keys():
        # Sélectionner les caractéristiques pertinentes pour cet actif
        ticker_features = [col for col in X.columns if ticker in col]
        X_ticker = X[ticker_features]
        
        # Normaliser les données
        X_scaled = scalers[ticker].transform(X_ticker)
        
        # Sélectionner le meilleur modèle (basé sur MSE)
        best_model_name = min(models[ticker].items(), key=lambda x: x[1]['mse'])[0]
        best_model = models[ticker][best_model_name]['model']
        
        # Prédire le rendement
        pred = best_model.predict(X_scaled)
        predictions[ticker] = pred[-1]  # Prendre la dernière prédiction
    
    return pd.Series(predictions)

def save_models(models, scalers, output_dir='../../models'):
    """
    Sauvegarde les modèles et les scalers.
    
    Parameters:
    - models: Dictionnaire des modèles entraînés
    - scalers: Dictionnaire des scalers
    - output_dir: Répertoire de sortie
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for ticker in models.keys():
        ticker_dir = os.path.join(output_dir, ticker)
        os.makedirs(ticker_dir, exist_ok=True)
        
        # Sauvegarder le scaler
        joblib.dump(scalers[ticker], os.path.join(ticker_dir, 'scaler.pkl'))
        
        # Sauvegarder les modèles
        for model_name, model_info in models[ticker].items():
            joblib.dump(model_info['model'], os.path.join(ticker_dir, f'{model_name}.pkl'))

def load_models(tickers, input_dir='../../models'):
    """
    Charge les modèles et les scalers.
    
    Parameters:
    - tickers: Liste des tickers
    - input_dir: Répertoire d'entrée
    
    Returns:
    - models: Dictionnaire des modèles chargés
    - scalers: Dictionnaire des scalers chargés
    """
    models = {}
    scalers = {}
    
    for ticker in tickers:
        ticker_dir = os.path.join(input_dir, ticker)
        
        if not os.path.exists(ticker_dir):
            print(f"Aucun modèle trouvé pour {ticker}")
            continue
        
        # Charger le scaler
        scalers[ticker] = joblib.load(os.path.join(ticker_dir, 'scaler.pkl'))
        
        # Charger les modèles
        models[ticker] = {}
        for model_file in os.listdir(ticker_dir):
            if model_file.endswith('.pkl') and model_file != 'scaler.pkl':
                model_name = model_file.split('.')[0]
                model = joblib.load(os.path.join(ticker_dir, model_file))
                
                # Créer une structure similaire à celle utilisée lors de l'entraînement
                models[ticker][model_name] = {
                    'model': model,
                    'mse': 0.0,  # Ces valeurs seront mises à jour lors de l'évaluation
                    'r2': 0.0
                }
    
    return models, scalers

if __name__ == "__main__":
    # Charger les rendements
    returns = pd.read_csv('../../data/processed/returns.csv', index_col=0, parse_dates=True)
    
    # Préparer les caractéristiques
    X, y = prepare_features(returns)
    
    # Entraîner les modèles
    models, X_test, y_test, scalers = train_models(X, y)
    
    # Sauvegarder les modèles
    save_models(models, scalers)
    
    # Prédire les rendements futurs
    predictions = predict_returns(models, X, scalers)
    
    # Sauvegarder les prédictions
    predictions.to_csv('../../data/processed/predicted_returns.csv')
    
    print("Prédictions des rendements futurs :")
    for ticker, pred in predictions.items():
        print(f"{ticker}: {pred:.6f}")
