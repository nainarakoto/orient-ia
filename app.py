import sys
import os
import streamlit as st

# Configuration de la page
st.set_page_config(page_title="ORIENT'IA", layout="wide")

# ------------------------------------------------------------------------------
# STYLE ET SIDEBAR GLOBALE
# ------------------------------------------------------------------------------
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        transition: all 0.4s ease-in-out;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 15px;
        border-radius: 8px;
        transition: transform 0.2s ease, background 0.3s ease;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(8px);
    }
    </style>
""", unsafe_allow_html=True)

# Imports des modules
from ui.tests_view import afficher_tests_view
from ui.profil import afficher_profil
from ui.chat import afficher_chatbot

# Navigation Principale
with st.sidebar:
    st.markdown("## 📌 ORIENT'IA Menu")

    choix_menu = st.radio(
        "Accès rapide :",
        options=["📝 Formulaire de Recommandation", "🎯 Chatbot Orient'IA", "📊 Dashboard (32 Tests)"],
        index=0
    )
    st.write("---")

# ------------------------------------------------------------------------------
# ROUTAGE DES MODULES
# ------------------------------------------------------------------------------
if choix_menu == "📝 Formulaire de Recommandation":
    afficher_profil()
elif choix_menu == "🎯 Chatbot Orient'IA":
    afficher_chatbot()
elif choix_menu == "📊 Dashboard (32 Tests)":
    afficher_tests_view()