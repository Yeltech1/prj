import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import ta  # Technical Analysis library

def prepare_ml_data(returns):
    """
    Prepare data for ML: add technical indicators as features.
    """
    df = returns.copy()
    for col in df.columns:
        df[f'{col}_rsi'] = ta.momentum.RSIIndicator(df[col]).rsi()
        df[f'{col}_ma'] = df[col].rolling(window=14).mean()
    df = df.dropna()
    return df

def train_models(X_train, y_train, X_test, y_test):
    """
    Train and evaluate ML models.
    """
    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
    }

    # Neural Network
    nn_model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    nn_model.compile(optimizer='adam', loss='mse')

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        results[name] = rmse

    # Train Neural Network
    nn_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
    y_pred_nn = nn_model.predict(X_test)
    results['NeuralNetwork'] = np.sqrt(mean_squared_error(y_test, y_pred_nn))

    return results

if __name__ == "__main__":
    returns = pd.read_csv('../../data/processed/returns.csv', index_col='Date', parse_dates=True)
    features = prepare_ml_data(returns)

    # Split data
    train_size = int(0.8 * len(features))
    X_train, X_test = features.iloc[:train_size, 1:], features.iloc[train_size:, 1:]
    y_train, y_test = features.iloc[:train_size, 0], features.iloc[train_size:, 0]

    results = train_models(X_train, y_train, X_test, y_test)
    print("RMSE des modèles :", results)