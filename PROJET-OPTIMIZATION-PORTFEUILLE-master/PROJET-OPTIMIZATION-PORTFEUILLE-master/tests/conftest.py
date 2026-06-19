"""
Configuration pour les tests pytest.
"""
import os
import sys
import pytest

# Ajouter le répertoire racine au chemin Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configure l'environnement de test."""
    # Créer les répertoires nécessaires s'ils n'existent pas
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/logs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('reports/figures', exist_ok=True)
    
    yield
    
    # Nettoyage après les tests si nécessaire
