FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer les dépendances supplémentaires pour le développement
RUN pip install --no-cache-dir \
    jupyter \
    sphinx \
    sphinx-rtd-theme \
    sphinx-autobuild \
    pytest \
    pytest-cov \
    black \
    flake8

# Créer les répertoires nécessaires
RUN mkdir -p data/raw data/processed data/logs models reports/figures

# Copier le code source
COPY . .

# Exposer les ports pour Streamlit, Jupyter et Sphinx
EXPOSE 8501 8888 8000

# Commande par défaut pour lancer l'application Streamlit
CMD ["streamlit", "run", "app/dashboard.py"]
