import os
import logging
import streamlit as st
import requests
from dotenv import load_dotenv
from services import mock_data

load_dotenv()

logger = logging.getLogger("OrientIA.frontend")

BACKEND_URL = os.environ.get("ORIENTIA_BACKEND_URL", "")

# Timeout court pour les endpoints simples (lecture de données statiques).
TIMEOUT = 3

# Timeout long pour le chat : l'agent peut enchaîner appel ML + RAG + LLM,
# et le fallback Gemini -> Groq peut à lui seul prendre 20-30s le temps que
# l'erreur de quota Gemini remonte avant la bascule.
TIMEOUT_CHAT = 60


def _backend_disponible():
    return bool(BACKEND_URL)


def get_formations():
    if _backend_disponible():
        try:
            reponse = requests.get(f"{BACKEND_URL}/formations", timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as e:
            logger.warning("Backend indisponible pour /formations (%s) - repli mock_data", e)
    return mock_data.FORMATIONS


def get_formation(formation_id):
    for formation in get_formations():
        if formation["id"] == formation_id:
            return formation
    return None


def obtenir_recommandation(profil):
    if _backend_disponible():
        try:
            reponse = requests.post(f"{BACKEND_URL}/agent/recommander", json=profil, timeout=TIMEOUT_CHAT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as e:
            logger.warning("Backend indisponible pour /agent/recommander (%s) - repli mock_data", e)
    return mock_data.recommandation_fictive(profil)


def obtenir_recommandation_academique(profil_academique):
    if _backend_disponible():
        try:
            reponse = requests.post(f"{BACKEND_URL}/agent/orientation", json=profil_academique, timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as e:
            logger.warning("Backend indisponible pour /agent/orientation (%s) - repli mock_data", e)
    return mock_data.generer_recommandation_academique(profil_academique)


def get_registre_sources():
    if _backend_disponible():
        try:
            reponse = requests.get(f"{BACKEND_URL}/sources", timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as e:
            logger.warning("Backend indisponible pour /sources (%s) - repli mock_data", e)
    return mock_data.REGISTRE_SOURCES


@st.cache_data(ttl=3600)
def get_ml_schema():
    """
    Récupère les catégories exactes attendues par le modèle ML (série du
    bac, préférence d'environnement, objectifs professionnels connus).
    Mis en cache 1h par session Streamlit pour éviter un appel réseau à
    chaque re-render du formulaire de profil.
    """
    if _backend_disponible():
        try:
            reponse = requests.get(f"{BACKEND_URL}/ml/schema", timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as e:
            logger.warning("Backend indisponible pour /ml/schema (%s) - listes vides", e)
    return {"series": [], "preferences_env": [], "objectifs_professionnels": []}


def envoyer_message_assistant(historique, message, profil):
    if _backend_disponible():
        try:
            payload = {"historique": historique, "message": message, "profil": profil}
            reponse = requests.post(f"{BACKEND_URL}/agent/chat", json=payload, timeout=TIMEOUT_CHAT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as e:
            logger.warning("Backend indisponible pour /agent/chat (%s) - repli mock_data", e)
    return mock_data.reponse_assistant_fictive(message)