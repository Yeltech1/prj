"""
Script pour lancer l'application Streamlit.
"""
import os
import subprocess
import sys

def main():
    """Fonction principale pour lancer l'application Streamlit."""
    # Vérifier si Streamlit est installé
    try:
        import streamlit
        print("Streamlit est déjà installé.")
    except ImportError:
        print("Streamlit n'est pas installé. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("Streamlit a été installé avec succès.")
    
    # Vérifier si les données existent
    if not os.path.exists('data/processed/returns.csv'):
        print("Les données de rendements n'existent pas. Génération de données simulées...")
        
        # Exécuter le script de génération de données simulées
        if os.path.exists('simple_portfolio.py'):
            subprocess.check_call([sys.executable, "simple_portfolio.py"])
        else:
            print("Le script simple_portfolio.py n'existe pas. Veuillez d'abord exécuter le script principal.")
            return
    
    # Lancer l'application Streamlit
    print("Lancement de l'application Streamlit...")
    subprocess.check_call([sys.executable, "-m", "streamlit", "run", "app/dashboard.py"])

if __name__ == "__main__":
    main()
