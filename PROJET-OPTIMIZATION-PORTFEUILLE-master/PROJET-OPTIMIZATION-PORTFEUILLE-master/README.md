# Optimisation de Portefeuille d'Investissement

[![Portfolio Optimization CI](https://github.com/Baudelaire12/PROJET-OPTIMIZATION-PORTFEUILLE/actions/workflows/python-app.yml/badge.svg)](https://github.com/Baudelaire12/PROJET-OPTIMIZATION-PORTFEUILLE/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Website](https://img.shields.io/badge/Website-Visit-blue)](https://baudelaire12.github.io/PROJET-OPTIMIZATION-PORTFEUILLE/)

[🌐 Voir la démo en ligne](https://baudelaire12.github.io/PROJET-OPTIMIZATION-PORTFEUILLE/)

## Description
Ce projet optimise un portefeuille d'investissement en combinant la Théorie Moderne du Portefeuille (MPT) et des modèles d'apprentissage automatique. Il utilise des données historiques de Yahoo Finance pour prédire les rendements et minimiser les risques.

## 🆕 Mise à jour : Collecte de données réelles
Cette version inclut une fonctionnalité améliorée de collecte de données réelles depuis Yahoo Finance :
- Téléchargement automatique des données historiques pour 20 actions et indices majeurs
- Prétraitement des données pour calculer les rendements journaliers
- Gestion robuste des erreurs et des tentatives multiples
- Interface utilisateur Streamlit pour la collecte et la visualisation des données
- Optimisation de portefeuille basée sur des données réelles actualisées

## Fonctionnalités
- Collecte de données financières réelles via Yahoo Finance API
- Prétraitement et analyse exploratoire des données
- Optimisation de portefeuille selon Markowitz
- Modèles d'apprentissage automatique pour prédire les rendements
- Backtesting des stratégies d'investissement
- Comparaison de différentes stratégies d'allocation
- Tableau de bord interactif avec Streamlit
- Génération de données simulées pour les tests
- Pipeline modulaire avec différents modes d'exécution
- Gestion robuste des erreurs et des données manquantes
- Documentation technique complète avec Sphinx
- Tests unitaires avec pytest et couverture de code
- Déploiement simplifié avec Docker Compose
- Outils d'analyse de code (flake8, black)
- Guide utilisateur détaillé

## Structure du Projet
```
portfolio_optimization/
│
├── app/                    # Application Streamlit
│   └── dashboard.py        # Interface utilisateur interactive
│
├── data/                   # Données
│   ├── raw/                # Données brutes
│   └── processed/          # Données traitées
│
├── models/                 # Modèles ML entraînés
│
├── notebooks/              # Notebooks Jupyter pour l'analyse
│   └── 01_eda.ipynb        # Analyse exploratoire des données
│
├── reports/                # Rapports et visualisations
│   └── figures/            # Figures générées
│
├── src/                    # Code source
│   ├── data/               # Scripts de collecte et prétraitement
│   │   ├── __init__.py
│   │   ├── data_collection.py
│   │   └── preprocessing.py
│   │
│   ├── models/             # Modèles et algorithmes
│   │   ├── __init__.py
│   │   ├── mpt.py          # Théorie Moderne du Portefeuille
│   │   ├── ml_models.py    # Modèles d'apprentissage automatique
│   │   ├── ml_prediction.py # Prédiction avec ML avancé
│   │   ├── backtest.py     # Backtesting des stratégies
│   │   └── optimization.py # Optimisation du portefeuille
│   │
│   └── visualization/      # Visualisations
│       ├── __init__.py
│       └── visualize.py    # Fonctions de visualisation
│
├── Dockerfile              # Configuration Docker
├── main.py                 # Script principal avec différents modes
├── simple_portfolio.py     # Version simplifiée pour les tests
├── run_dashboard.py        # Script pour lancer l'application Streamlit
├── README.md               # Documentation
└── requirements.txt        # Dépendances
```

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Baudelaire12/PROJET-OPTIMIZATION-PORTFEUILLE.git
   cd PROJET-OPTIMIZATION-PORTFEUILLE
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv .venv
   # Sur Windows
   .venv\Scripts\activate
   # Sur Linux/Mac
   source .venv/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Pour le développement, installez les dépendances supplémentaires :
   ```bash
   pip install -r requirements-dev.txt
   ```

## Utilisation

### Exécution du pipeline complet
```bash
python main.py
```

### Exécution de modes spécifiques
```bash
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
```

### Personnalisation des paramètres
```bash
# Spécifier les tickers à analyser
python main.py --tickers AAPL MSFT GOOGL AMZN

# Spécifier la période d'analyse
python main.py --start-date 2019-01-01 --end-date 2022-12-31
```

### Collecte de données réelles
```bash
# Collecter des données réelles pour les 20 actions et indices par défaut
python collect_real_data.py

# Collecter des données pour des actions spécifiques
python collect_real_data.py --tickers AAPL MSFT GOOGL AMZN META

# Collecter des données pour une période spécifique
python collect_real_data.py --start-date 2020-01-01 --end-date 2023-12-31

# Collecter des données pour les 3 dernières années
python collect_real_data.py --years 3
```

Vous pouvez également utiliser l'interface Streamlit pour collecter des données réelles :
```bash
# Lancer l'application Streamlit avec collecte de données intégrée
streamlit run streamlit_app.py
```
Cette interface vous permet de :
- Sélectionner les actions et indices à analyser
- Définir la période d'analyse
- Visualiser les données collectées
- Optimiser votre portefeuille en temps réel

### Lancement de l'application Streamlit
```bash
# Méthode simple
python run_dashboard.py

# Méthode alternative
streamlit run app/dashboard.py
```

### Exécution des composants individuels
```bash
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
```

## Déploiement avec Docker
1. Construisez l'image :
   ```bash
   docker build -t portfolio-optimization .
   ```

2. Lancez le conteneur :
   ```bash
   docker run -p 8501:8501 portfolio-optimization
   ```

3. Ou utilisez Docker Compose pour lancer tous les services :
   ```bash
   docker-compose up -d
   ```

   Cela lancera trois services :
   - **app** : Application Streamlit (http://localhost:8501)
   - **jupyter** : Serveur Jupyter Notebook (http://localhost:8888)
   - **docs** : Documentation Sphinx (http://localhost:8000)

## Licence
Ce projet est sous licence MIT.

## Contact
Pour toute question ou suggestion, veuillez contacter [tpineldahoui@gmail.com].
