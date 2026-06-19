"""
Point d'entrée pour Streamlit Cloud.
Ce fichier collecte des données réelles via Yahoo Finance avant de lancer l'application.
"""
import streamlit as st

# Configuration de la page - DOIT être appelé en premier
st.set_page_config(
    page_title="Optimisation de Portefeuille",
    page_icon="📈",
    layout="wide"
)

import sys
import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go

# Créer les répertoires nécessaires
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/logs', exist_ok=True)

# Fonction pour collecter des données réelles
def collect_real_data():
    st.sidebar.title("Collecte de données")

    with st.sidebar.expander("⚙️ Paramètres de collecte", expanded=True):
        # Paramètres de collecte
        start_date = st.date_input(
            "Date de début",
            datetime.now() - timedelta(days=365*5)  # 5 ans par défaut
        )

        end_date = st.date_input(
            "Date de fin",
            datetime.now()
        )

        # Liste des tickers par défaut
        default_tickers = [
            # Indices majeurs
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

        # Sélection des tickers
        selected_tickers = st.multiselect(
            "Sélectionner les actifs",
            options=default_tickers,
            default=default_tickers[:10]  # 10 premiers tickers par défaut
        )

        if st.button("Collecter les données"):
            if not selected_tickers:
                st.error("Veuillez sélectionner au moins un actif.")
                return False

            # Afficher un message de chargement
            with st.spinner("Collecte des données en cours..."):
                # Récupérer les données pour chaque ticker
                all_data = pd.DataFrame()

                for ticker in selected_tickers:
                    try:
                        # Récupérer les données via yfinance
                        stock = yf.Ticker(ticker)
                        data = stock.history(start=start_date, end=end_date)

                        if data.empty:
                            st.warning(f"Aucune donnée trouvée pour {ticker}")
                            continue

                        # Ajouter une colonne pour identifier le ticker
                        data['Ticker'] = ticker

                        # Ajouter au DataFrame principal
                        all_data = pd.concat([all_data, data])

                        st.success(f"Données récupérées pour {ticker}: {len(data)} entrées")

                    except Exception as e:
                        st.error(f"Erreur lors de la récupération des données pour {ticker}: {e}")

                if all_data.empty:
                    st.error("Aucune donnée n'a été récupérée.")
                    return False

                # Sauvegarder les données brutes
                all_data_reset = all_data.reset_index()
                all_data_reset.to_csv('data/raw/stock_data.csv', index=False)

                # Prétraiter les données
                # Créer un DataFrame pivot manuellement
                # Réinitialiser l'index pour avoir Date comme colonne
                if 'Date' not in all_data.columns and isinstance(all_data.index, pd.DatetimeIndex):
                    all_data = all_data.reset_index()

                # Créer un dictionnaire pour stocker les séries de prix par ticker
                prices_dict = {}

                # Parcourir les tickers uniques
                for ticker in all_data['Ticker'].unique():
                    # Filtrer les données pour ce ticker
                    ticker_data = all_data[all_data['Ticker'] == ticker]
                    # Créer une série avec Date comme index et Close comme valeurs
                    prices_dict[ticker] = pd.Series(ticker_data['Close'].values, index=ticker_data['Date'])

                # Créer un DataFrame à partir du dictionnaire
                pivot_data = pd.DataFrame(prices_dict)

                # Calculer les rendements journaliers
                returns = pivot_data.pct_change().dropna()

                # Supprimer les valeurs aberrantes (rendements > 50% ou < -50%)
                returns = returns.mask((returns > 0.5) | (returns < -0.5), np.nan)

                # Remplir les valeurs manquantes avec la moyenne des rendements
                returns = returns.fillna(returns.mean())

                # Sauvegarder les rendements
                returns.to_csv('data/processed/returns.csv')

                st.success(f"Prétraitement terminé: {len(returns)} jours de rendements pour {len(returns.columns)} actions")
                return True

    return True  # Par défaut, continuer avec les données existantes ou simulées

# Collecter des données réelles
data_ready = collect_real_data()

if data_ready:
    # Ajouter le répertoire de l'application au chemin
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

    # Importer les modules nécessaires pour l'optimisation
    from simple_portfolio import (
        calculate_returns,
        calculate_portfolio_metrics,
        optimize_portfolio
    )

    # Afficher un message de transition
    st.success("Données collectées avec succès! Chargement du dashboard d'optimisation...")

    # Créer une séparation visuelle
    st.markdown("---")

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
        """)

    # Chargement des données
    @st.cache_data(show_spinner=False)
    def load_data():
        try:
            # Essayer de charger les données réelles depuis stock_data.csv
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

    # Sidebar pour les paramètres
    st.sidebar.header("Paramètres d'optimisation")

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
        risk_free_rate = st.sidebar.slider("Taux sans risque (%)", 0.0, 5.0, 1.0) / 100
        n_portfolios = st.sidebar.slider("Nombre de portefeuilles à simuler", 1000, 10000, 5000)

        if prices is not None and returns is not None and selected_tickers:
            # Filtrer les données pour les actifs sélectionnés
            returns_filtered = returns[selected_tickers]

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
        elif not selected_tickers:
            st.warning("Veuillez sélectionner au moins un actif dans la barre latérale.")
    else:
        st.error("Impossible de charger les données. Veuillez réessayer la collecte de données.")
else:
    st.error("Impossible de continuer sans données. Veuillez réessayer la collecte de données.")
