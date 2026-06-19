Installation
============

Prérequis
---------

Avant d'installer le projet, assurez-vous que votre système répond aux exigences suivantes :

* Python 3.8 ou supérieur
* pip (gestionnaire de paquets Python)
* Git (pour cloner le dépôt)

Installation depuis GitHub
-------------------------

1. Clonez le dépôt GitHub :

   .. code-block:: bash

      git clone https://github.com/Baudelaire12/PROJET-OPTIMIZATION-PORTFEUILLE.git
      cd PROJET-OPTIMIZATION-PORTFEUILLE

2. Créez un environnement virtuel Python :

   .. code-block:: bash

      # Sur Windows
      python -m venv .venv
      .venv\Scripts\activate

      # Sur Linux/Mac
      python -m venv .venv
      source .venv/bin/activate

3. Installez les dépendances :

   .. code-block:: bash

      pip install -r requirements.txt

Dépendances principales
----------------------

Le projet dépend des bibliothèques Python suivantes :

* **numpy** et **pandas** : Pour la manipulation et l'analyse des données
* **scipy** : Pour les algorithmes d'optimisation
* **matplotlib** et **plotly** : Pour la visualisation des données
* **scikit-learn** : Pour les modèles d'apprentissage automatique
* **yfinance** : Pour la collecte de données financières
* **streamlit** : Pour l'interface utilisateur interactive

Installation pour le développement
--------------------------------

Si vous souhaitez contribuer au projet, vous devrez installer des dépendances supplémentaires pour le développement :

.. code-block:: bash

   pip install -r requirements-dev.txt

Cela installera des outils supplémentaires comme :

* **pytest** : Pour les tests unitaires
* **flake8** : Pour l'analyse statique du code
* **sphinx** : Pour la génération de documentation
* **black** : Pour le formatage du code

Vérification de l'installation
-----------------------------

Pour vérifier que l'installation a réussi, exécutez le script de test :

.. code-block:: bash

   python simple_portfolio.py

Si tout est correctement installé, vous devriez voir un message indiquant que les données simulées ont été générées et que l'optimisation du portefeuille a été effectuée avec succès.

Installation avec Docker
----------------------

Si vous préférez utiliser Docker, vous pouvez construire et exécuter le projet dans un conteneur :

1. Construisez l'image Docker :

   .. code-block:: bash

      docker build -t portfolio-optimization .

2. Exécutez le conteneur :

   .. code-block:: bash

      docker run -p 8501:8501 portfolio-optimization

L'application Streamlit sera alors accessible à l'adresse http://localhost:8501.
