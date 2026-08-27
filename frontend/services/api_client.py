import os
import requests
from services import mock_data

BACKEND_URL = os.environ.get("ORIENTIA_BACKEND_URL", "")
TIMEOUT = 3


def _backend_disponible():
    return bool(BACKEND_URL)


def get_formations():
    if _backend_disponible():
        try:
            reponse = requests.get(f"{BACKEND_URL}/formations", timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException:
            pass
    return mock_data.FORMATIONS


def get_formation(formation_id):
    for formation in get_formations():
        if formation["id"] == formation_id:
            return formation
    return None


def obtenir_recommandation(profil):
    if _backend_disponible():
        try:
            reponse = requests.post(f"{BACKEND_URL}/agent/recommander", json=profil, timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException:
            pass
    return mock_data.recommandation_fictive(profil)


def obtenir_recommandation_academique(profil_academique):
    if _backend_disponible():
        try:
            reponse = requests.post(f"{BACKEND_URL}/agent/orientation", json=profil_academique, timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException:
            pass
    return mock_data.generer_recommandation_academique(profil_academique)


def get_registre_sources():
    if _backend_disponible():
        try:
            reponse = requests.get(f"{BACKEND_URL}/sources", timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException:
            pass
    return mock_data.REGISTRE_SOURCES


def envoyer_message_assistant(historique, message, profil):
    if _backend_disponible():
        try:
            payload = {"historique": historique, "message": message, "profil": profil}
            reponse = requests.post(f"{BACKEND_URL}/agent/chat", json=payload, timeout=TIMEOUT)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException:
            pass
    return mock_data.reponse_assistant_fictive(message)
