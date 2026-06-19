# Guide de contribution

Merci de votre intérêt pour contribuer à ce projet d'optimisation de portefeuille ! Voici quelques lignes directrices pour vous aider à contribuer efficacement.

## Comment contribuer

1. **Fork** le dépôt sur GitHub
2. **Clone** votre fork sur votre machine locale
3. **Créez une branche** pour vos modifications (`git checkout -b feature/amazing-feature`)
4. **Committez** vos changements (`git commit -m 'Add some amazing feature'`)
5. **Poussez** votre branche vers votre fork (`git push origin feature/amazing-feature`)
6. Ouvrez une **Pull Request** vers la branche principale du projet

## Environnement de développement

1. Créez un environnement virtuel Python :
   ```bash
   python -m venv .venv
   # Sur Windows
   .venv\Scripts\activate
   # Sur Linux/Mac
   source .venv/bin/activate
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Structure du projet

Veuillez respecter la structure du projet lors de l'ajout de nouvelles fonctionnalités :

- `app/` - Application Streamlit
- `data/` - Données brutes et traitées
- `models/` - Modèles entraînés
- `notebooks/` - Notebooks Jupyter pour l'analyse
- `reports/` - Rapports et visualisations
- `src/` - Code source principal
  - `data/` - Scripts de collecte et prétraitement
  - `models/` - Modèles et algorithmes
  - `visualization/` - Fonctions de visualisation

## Standards de code

- Suivez les conventions PEP 8 pour le code Python
- Documentez vos fonctions et classes avec des docstrings
- Écrivez des messages de commit clairs et descriptifs
- Ajoutez des tests pour les nouvelles fonctionnalités

## Domaines de contribution

Voici quelques domaines où vous pouvez contribuer :

1. **Amélioration des modèles ML** - Implémentation de modèles plus avancés (LSTM, transformers, etc.)
2. **Optimisation des performances** - Amélioration de l'efficacité des calculs
3. **Interface utilisateur** - Amélioration du tableau de bord Streamlit
4. **Documentation** - Amélioration de la documentation et des exemples
5. **Tests** - Ajout de tests unitaires et d'intégration
6. **Nouvelles fonctionnalités** - Implémentation de nouvelles stratégies d'optimisation

## Signaler des bugs

Si vous trouvez un bug, veuillez créer une issue en incluant :
- Une description claire du bug
- Les étapes pour reproduire le problème
- Le comportement attendu
- Des captures d'écran si applicable
- Votre environnement (OS, version de Python, etc.)

## Questions

Si vous avez des questions, n'hésitez pas à ouvrir une issue avec le tag "question".

Merci de contribuer à ce projet !
