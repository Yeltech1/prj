# Optimisation de Portefeuille d'Investissement

## Description
Ce projet optimise un portefeuille d'investissement en combinant la Théorie Moderne du Portefeuille (MPT) et des modèles d'apprentissage automatique. Il utilise des données historiques de Yahoo Finance pour prédire les rendements et minimiser les risques.

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/portfolio_optimization.git
   ```
2. Créez un environnement virtuel :
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Exécutez l'application Streamlit :
   ```bash
   streamlit run app/app.py
   ```

## Structure
- `data/` : Données brutes et traitées
- `notebooks/` : Notebooks Jupyter pour l'analyse
- `src/` : Scripts Python
- `app/` : Application Streamlit
- `reports/` : Rapport LaTeX/PDF

## Déploiement avec Docker
1. Construisez l'image :
   ```bash
   docker build -t portfolio-optimization .
   ```
2. Lancez le conteneur :
   ```bash
   docker run -p 8501:8501 portfolio-optimization
   ```

## Rapport
Un rapport détaillé est disponible dans `reports/report.pdf`.