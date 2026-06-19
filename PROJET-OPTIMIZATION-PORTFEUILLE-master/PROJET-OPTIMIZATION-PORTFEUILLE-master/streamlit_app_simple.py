"""
Version simplifiée de l'application pour tester le déploiement sur Streamlit Cloud.
"""
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Test de Déploiement",
    page_icon="📈",
    layout="wide"
)

# Titre et description
st.title("📊 Test de Déploiement sur Streamlit Cloud")
st.markdown("""
Cette application est une version simplifiée pour tester le déploiement sur Streamlit Cloud.
""")

# Afficher un message
st.success("Si vous voyez ce message, le déploiement a réussi !")

# Ajouter un bouton
if st.button("Cliquez-moi"):
    st.balloons()
    st.write("Félicitations ! L'application fonctionne correctement.")
