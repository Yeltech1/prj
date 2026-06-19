# Guide Utilisateur - Optimisation de Portefeuille

Ce guide vous explique comment utiliser l'application d'optimisation de portefeuille pour analyser et optimiser vos investissements.

## Table des matières

1. [Installation](#installation)
2. [Collecte de données](#collecte-de-données)
3. [Interface Streamlit](#interface-streamlit)
4. [Interprétation des résultats](#interprétation-des-résultats)
5. [Modes d'exécution avancés](#modes-dexécution-avancés)
6. [Dépannage](#dépannage)

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le dépôt)

### Installation depuis GitHub

1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/Baudelaire12/PROJET-OPTIMIZATION-PORTFEUILLE.git
   cd PROJET-OPTIMIZATION-PORTFEUILLE
   ```

2. Créez un environnement virtuel Python :
   ```bash
   # Sur Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Sur Linux/Mac
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Installation avec Docker

Si vous préférez utiliser Docker :

1. Construisez et lancez les services avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

2. Accédez à l'application dans votre navigateur à l'adresse http://localhost:8501

## Collecte de données

### Utilisation des données par défaut

Pour générer des données simulées :

```bash
python simple_portfolio.py
```

### Collecte de données réelles

Pour collecter des données financières réelles via Yahoo Finance :

```bash
# Collecter des données pour les 20 actions et indices par défaut
python collect_real_data.py

# Collecter des données pour des actions spécifiques
python collect_real_data.py --tickers AAPL MSFT GOOGL AMZN META

# Collecter des données pour une période spécifique
python collect_real_data.py --start-date 2020-01-01 --end-date 2023-12-31
```

## Interface Streamlit

### Lancement de l'application

```bash
python run_dashboard.py
```

### Navigation dans l'interface

L'interface Streamlit est divisée en plusieurs sections :

#### Panneau latéral

- **Sélection des actifs** : Choisissez les actions à inclure dans votre portefeuille
- **Paramètres d'optimisation** : Ajustez le taux sans risque et le nombre de portefeuilles à simuler

#### Section principale

1. **Frontière Efficiente** : Graphique montrant la relation entre le risque et le rendement
2. **Allocation du Portefeuille Optimal** : Répartition des actifs dans le portefeuille optimal
3. **Métriques du Portefeuille** : Indicateurs clés de performance
4. **Analyse des Rendements Historiques** : Graphique des rendements cumulés

### Personnalisation des paramètres

- **Taux sans risque** : Ajustez ce paramètre pour refléter le rendement d'un actif sans risque (comme les bons du Trésor)
- **Nombre de portefeuilles** : Augmentez ce nombre pour une simulation plus précise (au détriment du temps de calcul)
- **Période d'analyse** : Utilisez le curseur pour sélectionner la période d'analyse des rendements historiques

## Interprétation des résultats

### Frontière Efficiente

La frontière efficiente représente l'ensemble des portefeuilles optimaux qui offrent le rendement attendu le plus élevé pour un niveau de risque donné. Chaque point sur la courbe représente un portefeuille différent.

- **Axe X (Volatilité)** : Mesure du risque du portefeuille
- **Axe Y (Rendement)** : Rendement attendu du portefeuille
- **Couleur (Ratio de Sharpe)** : Mesure du rendement ajusté au risque
- **Point rouge** : Portefeuille optimal (meilleur ratio de Sharpe)

### Allocation du Portefeuille

Ce graphique montre la répartition des actifs dans le portefeuille optimal.

- **Actifs avec des poids élevés** : Contribuent davantage au portefeuille
- **Diversification** : Un portefeuille bien diversifié répartit les investissements entre plusieurs actifs

### Métriques du Portefeuille

- **Rendement Annuel Attendu** : Estimation du rendement annuel du portefeuille
- **Volatilité Annuelle** : Mesure du risque du portefeuille
- **Ratio de Sharpe** : Mesure du rendement ajusté au risque (plus il est élevé, mieux c'est)

### Rendements Historiques

Ce graphique montre l'évolution des rendements cumulés pour chaque actif sélectionné.

- **Tendances à la hausse** : Indiquent des périodes de performance positive
- **Tendances à la baisse** : Indiquent des périodes de performance négative
- **Volatilité** : Les lignes avec de grandes fluctuations indiquent des actifs plus volatils

## Modes d'exécution avancés

Pour les utilisateurs avancés, le script principal prend en charge différents modes d'exécution :

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
```

## Dépannage

### Problèmes courants

1. **Erreur de dépendance manquante** :
   ```
   Solution : Assurez-vous d'avoir installé toutes les dépendances avec pip install -r requirements.txt
   ```

2. **Données non trouvées** :
   ```
   Solution : Exécutez python simple_portfolio.py pour générer des données simulées ou python collect_real_data.py pour collecter des données réelles
   ```

3. **Erreur lors de la collecte de données** :
   ```
   Solution : Vérifiez votre connexion Internet et assurez-vous que les symboles d'actions sont valides
   ```

4. **L'application Streamlit ne démarre pas** :
   ```
   Solution : Vérifiez que Streamlit est installé et que vous exécutez la commande depuis le répertoire racine du projet
   ```

### Obtenir de l'aide

Si vous rencontrez des problèmes non résolus, veuillez :

1. Consulter la documentation complète dans le répertoire `docs/`
2. Ouvrir une issue sur GitHub avec une description détaillée du problème
3. Contacter l'équipe de développement à [votre-email@example.com]
