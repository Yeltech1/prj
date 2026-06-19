Contributing
============

Merci de votre intérêt pour contribuer à ce projet d'optimisation de portefeuille ! Voici quelques lignes directrices pour vous aider à contribuer efficacement.

Comment contribuer
----------------

1. **Fork** le dépôt sur GitHub
2. **Clone** votre fork sur votre machine locale
3. **Créez une branche** pour vos modifications
4. **Committez** vos changements
5. **Poussez** votre branche vers votre fork
6. Ouvrez une **Pull Request** vers la branche principale du projet

Environnement de développement
----------------------------

1. Créez un environnement virtuel Python :

   .. code-block:: bash

      python -m venv .venv
      # Sur Windows
      .venv\Scripts\activate
      # Sur Linux/Mac
      source .venv/bin/activate

2. Installez les dépendances de développement :

   .. code-block:: bash

      pip install -r requirements-dev.txt

Structure du projet
-----------------

Veuillez respecter la structure du projet lors de l'ajout de nouvelles fonctionnalités :

- **app/** - Application Streamlit
- **data/** - Données brutes et traitées
- **models/** - Modèles entraînés
- **notebooks/** - Notebooks Jupyter pour l'analyse
- **reports/** - Rapports et visualisations
- **src/** - Code source principal
  - **data/** - Scripts de collecte et prétraitement
  - **models/** - Modèles et algorithmes
  - **visualization/** - Fonctions de visualisation
- **tests/** - Tests unitaires et d'intégration

Standards de code
---------------

- Suivez les conventions PEP 8 pour le code Python
- Documentez vos fonctions et classes avec des docstrings au format Google
- Écrivez des messages de commit clairs et descriptifs
- Ajoutez des tests pour les nouvelles fonctionnalités

Exemple de docstring au format Google :

.. code-block:: python

   def optimize_portfolio(expected_returns, cov_matrix, risk_free_rate=0.01):
       """Optimise un portefeuille selon la théorie de Markowitz.
       
       Args:
           expected_returns (pd.Series): Rendements attendus des actifs.
           cov_matrix (pd.DataFrame): Matrice de covariance des rendements.
           risk_free_rate (float, optional): Taux sans risque. Defaults to 0.01.
           
       Returns:
           tuple: Un tuple contenant (frontier, weights) où frontier est un DataFrame
               avec les portefeuilles de la frontière efficiente et weights est un
               array des poids du portefeuille optimal.
       """

Tests
-----

Tous les tests doivent être placés dans le répertoire `tests/`. Nous utilisons pytest comme framework de test.

Pour exécuter les tests :

.. code-block:: bash

   pytest

Ou pour un test spécifique :

.. code-block:: bash

   pytest tests/test_specific_module.py

Domaines de contribution
----------------------

Voici quelques domaines où vous pouvez contribuer :

1. **Amélioration des modèles ML** - Implémentation de modèles plus avancés (LSTM, transformers, etc.)
2. **Optimisation des performances** - Amélioration de l'efficacité des calculs
3. **Interface utilisateur** - Amélioration du tableau de bord Streamlit
4. **Documentation** - Amélioration de la documentation et des exemples
5. **Tests** - Ajout de tests unitaires et d'intégration
6. **Nouvelles fonctionnalités** - Implémentation de nouvelles stratégies d'optimisation

Signaler des bugs
---------------

Si vous trouvez un bug, veuillez créer une issue sur GitHub en incluant :

- Une description claire du bug
- Les étapes pour reproduire le problème
- Le comportement attendu
- Des captures d'écran si applicable
- Votre environnement (OS, version de Python, etc.)

Questions
--------

Si vous avez des questions, n'hésitez pas à ouvrir une issue avec le tag "question".
