"""
Application Streamlit pour l'optimisation de portefeuille.
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simple_portfolio import (
    calculate_returns,
    calculate_portfolio_metrics,
    optimize_portfolio
)

# Configuration de la page (commenté car maintenant appelé dans streamlit_app.py)
# st.set_page_config(
#     page_title="Optimisation de Portefeuille",
#     page_icon="📈",
#     layout="wide"
# )

# Titre et description
st.title("📊 Optimisation de Portefeuille d'Investissement")
st.markdown("""
Cette application vous permet d'optimiser votre portefeuille d'investissement en utilisant la théorie moderne du portefeuille (MPT) et des modèles d'apprentissage automatique.
""")

# Afficher des informations sur les données
with st.expander("ℹ️ Informations sur les données"):
    st.markdown("""
    ### Source des données
    Les données utilisées dans cette application sont récupérées via Yahoo Finance. Elles incluent les prix historiques des actions et sont utilisées pour calculer les rendements journaliers.

    ### Prétraitement
    Les données brutes sont prétraitées pour :
    - Calculer les rendements journaliers
    - Supprimer les valeurs aberrantes
    - Gérer les valeurs manquantes

    ### Collecte de données réelles
    Vous pouvez collecter des données réelles directement depuis cette application :
    1. Utilisez le panneau "Collecte de données" dans la barre latérale
    2. Sélectionnez les actifs qui vous intéressent
    3. Cliquez sur "Collecter les données"

    Les données seront automatiquement mises à jour et utilisées pour l'optimisation du portefeuille.
    """)

# Sidebar pour les paramètres
st.sidebar.header("Paramètres")

# Chargement des données
@st.cache_data(show_spinner=False)
def load_data():
    try:
        # Essayer de charger les données réelles depuis stock_data.csv (collectées par streamlit_app.py)
        try:
            # Afficher un message de chargement
            with st.spinner("Chargement des données réelles..."):
                stock_data = pd.read_csv('data/raw/stock_data.csv')
                if 'Date' in stock_data.columns and 'Ticker' in stock_data.columns and 'Close' in stock_data.columns:
                    # Créer un dictionnaire pour stocker les séries de prix par ticker
                    prices_dict = {}

                    # Convertir la colonne Date en datetime
                    stock_data['Date'] = pd.to_datetime(stock_data['Date'], utc=True)

                    # Parcourir les tickers uniques
                    for ticker in stock_data['Ticker'].unique():
                        # Filtrer les données pour ce ticker
                        ticker_data = stock_data[stock_data['Ticker'] == ticker]
                        # Créer une série avec Date comme index et Close comme valeurs
                        prices_dict[ticker] = pd.Series(ticker_data['Close'].values, index=ticker_data['Date'])

                    # Créer un DataFrame à partir du dictionnaire
                    prices = pd.DataFrame(prices_dict)

                    # Charger les rendements calculés
                    returns = pd.read_csv('data/processed/returns.csv', index_col=0, parse_dates=True)

                    st.success("Données réelles chargées avec succès!")
                    return prices, returns
        except Exception as e:
            st.warning(f"Erreur lors du chargement des données réelles: {e}")
            st.exception(e)

        # Si les données réelles ne sont pas disponibles, essayer de charger les données simulées
        with st.spinner("Chargement des données simulées..."):
            prices = pd.read_csv('data/raw/stock_prices.csv', index_col=0, parse_dates=True)
            returns = pd.read_csv('data/processed/returns.csv', index_col=0, parse_dates=True)
            st.info("Utilisation de données simulées (les données réelles n'ont pas pu être chargées).")
            return prices, returns
    except FileNotFoundError:
        st.error("Données non trouvées. Veuillez d'abord exécuter le script de collecte de données.")
        return None, None

prices, returns = load_data()

# Sélection des actifs
# Utiliser les colonnes disponibles dans le DataFrame returns
if returns is not None:
    available_tickers = list(returns.columns)
    default_tickers = available_tickers
    selected_tickers = st.sidebar.multiselect(
        "Sélectionner les actifs",
        options=available_tickers,
        default=available_tickers[:5] if len(available_tickers) >= 5 else available_tickers
    )

    # Paramètres d'optimisation
    st.sidebar.subheader("Paramètres d'optimisation")
    risk_free_rate = st.sidebar.slider("Taux sans risque (%)", 0.0, 5.0, 1.0) / 100
    n_portfolios = st.sidebar.slider("Nombre de portefeuilles à simuler", 1000, 10000, 5000)
else:
    st.error("Impossible de charger les données. Veuillez exécuter le script de collecte de données.")
    st.stop()

if prices is not None and returns is not None:
    # Filtrer les données pour les actifs sélectionnés
    if selected_tickers:
        returns_filtered = returns[selected_tickers]
    else:
        st.warning("Veuillez sélectionner au moins un actif.")
        returns_filtered = returns[default_tickers[:5]]

    # Calculer les métriques du portefeuille
    expected_returns, cov_matrix = calculate_portfolio_metrics(returns_filtered)

    # Optimisation du portefeuille
    with st.spinner("Optimisation du portefeuille en cours..."):
        frontier, optimal_weights = optimize_portfolio(expected_returns, cov_matrix, n_portfolios)

    # Afficher les résultats dans deux colonnes
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Frontière Efficiente")

        # Créer un graphique interactif avec Plotly
        fig = px.scatter(
            frontier, x='Volatility', y='Return',
            color='Sharpe', color_continuous_scale='viridis',
            title='Frontière Efficiente',
            labels={'Volatility': 'Volatilité (Risque)', 'Return': 'Rendement Attendu', 'Sharpe': 'Ratio de Sharpe'}
        )

        # Ajouter le portefeuille optimal
        max_sharpe_idx = frontier['Sharpe'].idxmax()
        fig.add_trace(go.Scatter(
            x=[frontier.loc[max_sharpe_idx, 'Volatility']],
            y=[frontier.loc[max_sharpe_idx, 'Return']],
            mode='markers',
            marker=dict(size=15, color='red'),
            name='Portefeuille Optimal'
        ))

        # Ajouter la ligne du taux sans risque
        max_vol = frontier['Volatility'].max()
        max_ret = frontier.loc[max_sharpe_idx, 'Return']
        fig.add_trace(go.Scatter(
            x=[0, max_vol * 1.2],
            y=[risk_free_rate, risk_free_rate + (max_ret - risk_free_rate) * 1.2],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Ligne du Marché des Capitaux'
        ))

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Allocation du Portefeuille Optimal")

        # Créer un DataFrame pour l'allocation
        allocation = pd.DataFrame({
            'Actif': returns_filtered.columns,
            'Poids': optimal_weights
        })
        allocation = allocation.sort_values('Poids', ascending=False)

        # Créer un graphique interactif avec Plotly
        fig = px.bar(
            allocation, x='Actif', y='Poids',
            title='Allocation du Portefeuille Optimal',
            labels={'Actif': 'Actif', 'Poids': 'Poids dans le Portefeuille'},
            color='Poids', color_continuous_scale='viridis'
        )

        st.plotly_chart(fig, use_container_width=True)

    # Afficher les métriques du portefeuille optimal
    st.subheader("Métriques du Portefeuille Optimal")

    # Calculer les métriques
    optimal_return = frontier.loc[max_sharpe_idx, 'Return']
    optimal_volatility = frontier.loc[max_sharpe_idx, 'Volatility']
    optimal_sharpe = frontier.loc[max_sharpe_idx, 'Sharpe']

    # Afficher les métriques dans trois colonnes
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric(
            label="Rendement Annuel Attendu",
            value=f"{optimal_return:.2%}"
        )

    with metric_col2:
        st.metric(
            label="Volatilité Annuelle",
            value=f"{optimal_volatility:.2%}"
        )

    with metric_col3:
        st.metric(
            label="Ratio de Sharpe",
            value=f"{optimal_sharpe:.2f}"
        )

    # Afficher le tableau des poids
    st.subheader("Poids du Portefeuille Optimal")

    # Formater les poids en pourcentage
    allocation['Poids (%)'] = allocation['Poids'] * 100
    st.dataframe(allocation[['Actif', 'Poids (%)']], use_container_width=True)

    # Analyse des rendements historiques
    st.subheader("Analyse des Rendements Historiques")

    # Convertir l'index en datetime si ce n'est pas déjà fait
    if not isinstance(returns.index, pd.DatetimeIndex):
        returns.index = pd.to_datetime(returns.index, utc=True)

    # Convertir en UTC pour éviter les problèmes de fuseau horaire
    if returns.index.tz is not None:
        returns.index = returns.index.tz_convert('UTC').tz_localize(None)

    # Extraire les dates min et max
    min_date = returns.index.min()
    max_date = returns.index.max()

    # Convertir en date (pas datetime)
    if hasattr(min_date, 'date'):
        min_date = min_date.date()
        max_date = max_date.date()

    # Sélectionner la période
    date_range = st.slider(
        "Sélectionner la période",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    # Convertir les dates sélectionnées en datetime pour le filtrage
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    # Filtrer les données par période
    mask = (returns.index >= start_date) & (returns.index <= end_date)
    returns_period = returns.loc[mask]

    # Calculer les rendements cumulés
    cumulative_returns = (1 + returns_period[selected_tickers]).cumprod() - 1

    # Créer un graphique interactif avec Plotly
    fig = px.line(
        cumulative_returns, x=cumulative_returns.index, y=cumulative_returns.columns,
        title='Rendements Cumulés',
        labels={'value': 'Rendement Cumulé', 'variable': 'Actif'}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Téléchargement des résultats
    st.subheader("Télécharger les Résultats")

    # Créer un DataFrame pour les résultats
    results = pd.DataFrame({
        'Actif': allocation['Actif'],
        'Poids (%)': allocation['Poids (%)'],
        'Rendement Attendu (%)': [expected_returns[ticker] * 100 for ticker in allocation['Actif']],
        'Volatilité (%)': [np.sqrt(cov_matrix.loc[ticker, ticker]) * 100 for ticker in allocation['Actif']]
    })

    # Convertir en CSV pour le téléchargement
    csv = results.to_csv(index=False)
    st.download_button(
        label="Télécharger les résultats (CSV)",
        data=csv,
        file_name="portfolio_optimization_results.csv",
        mime="text/csv"
    )

else:
    st.error("Impossible de charger ou de générer les données. Veuillez vérifier les permissions d'écriture dans le répertoire 'data'.")
