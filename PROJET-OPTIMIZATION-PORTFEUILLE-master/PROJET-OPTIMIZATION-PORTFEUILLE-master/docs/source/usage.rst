Utilisation
==========

Cette section explique comment utiliser les différentes fonctionnalités du projet d'optimisation de portefeuille.

Exécution du pipeline complet
----------------------------

Pour exécuter le pipeline complet d'optimisation de portefeuille, utilisez la commande suivante :

.. code-block:: bash

   python main.py

Cette commande exécutera toutes les étapes du pipeline :

1. Collecte de données financières
2. Prétraitement des données
3. Optimisation du portefeuille selon Markowitz
4. Entraînement des modèles d'apprentissage automatique
5. Backtesting des stratégies
6. Génération des visualisations

Modes d'exécution spécifiques
----------------------------

Le script principal prend en charge différents modes d'exécution pour cibler des parties spécifiques du pipeline :

.. code-block:: bash

   # Mode de collecte et prétraitement des données uniquement
   python main.py --mode data

   # Mode d'optimisation de portefeuille uniquement
   python main.py --mode optimize

   # Mode d'apprentissage automatique uniquement
   python main.py --mode ml

   # Mode de backtesting uniquement
   python main.py --mode backtest

   # Mode de comparaison des stratégies uniquement
   python main.py --mode compare

   # Mode simplifié (sans dépendances externes)
   python main.py --mode simplified

Personnalisation des paramètres
------------------------------

Vous pouvez personnaliser les paramètres d'exécution en utilisant différentes options :

.. code-block:: bash

   # Spécifier les tickers à analyser
   python main.py --tickers AAPL MSFT GOOGL AMZN

   # Spécifier la période d'analyse
   python main.py --start-date 2019-01-01 --end-date 2022-12-31

   # Combiner plusieurs options
   python main.py --mode optimize --tickers AAPL MSFT GOOGL --start-date 2020-01-01

Collecte de données réelles
--------------------------

Pour collecter des données financières réelles via Yahoo Finance, utilisez le script dédié :

.. code-block:: bash

   # Collecter des données pour les 20 actions et indices par défaut
   python collect_real_data.py

   # Collecter des données pour des actions spécifiques
   python collect_real_data.py --tickers AAPL MSFT GOOGL AMZN META

   # Collecter des données pour une période spécifique
   python collect_real_data.py --start-date 2020-01-01 --end-date 2023-12-31

   # Collecter des données pour les 3 dernières années
   python collect_real_data.py --years 3

Lancement de l'application Streamlit
-----------------------------------

Pour lancer l'interface utilisateur interactive, utilisez l'une des commandes suivantes :

.. code-block:: bash

   # Méthode simple (recommandée)
   python run_dashboard.py

   # Méthode alternative
   streamlit run app/dashboard.py

L'application sera accessible dans votre navigateur à l'adresse http://localhost:8501.

Utilisation de l'interface Streamlit
----------------------------------

L'interface Streamlit vous permet de :

1. **Sélectionner les actifs** à inclure dans votre portefeuille
2. **Ajuster les paramètres d'optimisation** comme le taux sans risque
3. **Visualiser la frontière efficiente** et le portefeuille optimal
4. **Explorer les rendements historiques** des actifs sélectionnés
5. **Télécharger les résultats** pour une analyse plus approfondie

Exécution des composants individuels
----------------------------------

Vous pouvez également exécuter les composants individuels du projet :

.. code-block:: bash

   # Collecte de données
   python -m src.data.data_collection

   # Prétraitement
   python -m src.data.preprocessing

   # Optimisation MPT
   python -m src.models.mpt

   # Modèles ML
   python -m src.models.ml_models

   # Prédiction ML avancée
   python -m src.models.ml_prediction

   # Backtesting des stratégies
   python -m src.models.backtest
