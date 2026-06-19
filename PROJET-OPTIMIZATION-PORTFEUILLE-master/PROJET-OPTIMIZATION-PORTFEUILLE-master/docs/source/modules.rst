Modules
=======

Cette section décrit les principaux modules du projet et leur fonctionnement.

Module de collecte de données
----------------------------

Le module de collecte de données est responsable de la récupération des données financières historiques à partir de sources externes.

.. code-block:: python

   from src.data.data_collection import fetch_stock_data

   # Exemple d'utilisation
   data = fetch_stock_data(
       tickers=['AAPL', 'MSFT', 'GOOGL'],
       start_date='2020-01-01',
       end_date='2023-12-31'
   )

Fonctionnalités principales :

- Récupération de données via Yahoo Finance
- Gestion des erreurs et des tentatives multiples
- Sauvegarde des données brutes

Module de prétraitement
----------------------

Le module de prétraitement transforme les données brutes en un format adapté à l'analyse et à l'optimisation.

.. code-block:: python

   from src.data.preprocessing import preprocess_stock_data

   # Exemple d'utilisation
   returns = preprocess_stock_data(data)

Fonctionnalités principales :

- Calcul des rendements journaliers
- Gestion des valeurs manquantes
- Détection et traitement des valeurs aberrantes
- Normalisation des données

Module d'optimisation de portefeuille
------------------------------------

Le module d'optimisation implémente la théorie de Markowitz pour trouver le portefeuille optimal.

.. code-block:: python

   from src.models.mpt import optimize_portfolio

   # Exemple d'utilisation
   frontier, weights = optimize_portfolio(
       expected_returns,
       covariance_matrix,
       risk_free_rate=0.01
   )

Fonctionnalités principales :

- Calcul de la frontière efficiente
- Optimisation du ratio de Sharpe
- Allocation optimale des actifs
- Visualisation des résultats

Module d'apprentissage automatique
---------------------------------

Le module d'apprentissage automatique utilise des modèles prédictifs pour estimer les rendements futurs.

.. code-block:: python

   from src.models.ml_prediction import train_models, predict_returns

   # Exemple d'utilisation
   models = train_models(features, returns)
   predictions = predict_returns(models, new_features)

Fonctionnalités principales :

- Préparation des caractéristiques
- Entraînement de modèles (régression linéaire, forêts aléatoires)
- Évaluation des modèles
- Prédiction des rendements

Module de backtesting
--------------------

Le module de backtesting évalue les performances des stratégies d'investissement sur des données historiques.

.. code-block:: python

   from src.models.backtest import backtest_strategy

   # Exemple d'utilisation
   performance = backtest_strategy(
       returns,
       weights,
       initial_investment=10000
   )

Fonctionnalités principales :

- Simulation des performances historiques
- Calcul des métriques de performance (rendement, volatilité, ratio de Sharpe)
- Comparaison de différentes stratégies
- Visualisation des résultats

Module de visualisation
---------------------

Le module de visualisation génère des graphiques et des figures pour représenter les résultats.

.. code-block:: python

   from src.visualization.visualize import plot_efficient_frontier

   # Exemple d'utilisation
   plot_efficient_frontier(frontier, optimal_portfolio)

Fonctionnalités principales :

- Visualisation de la frontière efficiente
- Graphiques des allocations de portefeuille
- Visualisation des rendements historiques
- Matrices de corrélation

Application Streamlit
-------------------

L'application Streamlit fournit une interface utilisateur interactive pour explorer les résultats.

Fonctionnalités principales :

- Sélection des actifs
- Ajustement des paramètres d'optimisation
- Visualisation interactive des résultats
- Téléchargement des résultats
