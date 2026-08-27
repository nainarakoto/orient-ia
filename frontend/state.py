import streamlit as st

PROFILE_FIELDS = [
    "matieres_preferees",
    "resultats_scolaires",
    "competences",
    "centres_interet",
    "activites_projets",
    "preferences_professionnelles",
    "environnement_travail",
]

NOTES_MATIERES = ["Mathématiques", "Français", "Physique-Chimie", "Anglais", "SVT", "Gestion / Éco / Philo"]

SERIES_BAC = ["Série A", "Série C", "Série D", "Série L", "Série Technique"]

CENTRES_INTERET = [
    "Informatique / Logiciel",
    "Réseaux / Sécurité",
    "Mathématiques / Sciences",
    "Gestion / Économie",
    "Sciences humaines",
    "Autre",
]

CENTRE_INTERET_AUTRE = "Autre"


def init_session_state():
    if "profil" not in st.session_state:
        st.session_state.profil = {champ: "" for champ in PROFILE_FIELDS}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "recommandation" not in st.session_state:
        st.session_state.recommandation = None
    if "parcours_a_comparer" not in st.session_state:
        st.session_state.parcours_a_comparer = []
    if "profil_academique" not in st.session_state:
        st.session_state.profil_academique = {
            "serie_bac": SERIES_BAC[0],
            "centre_interet": CENTRES_INTERET[0],
            "centre_interet_precision": "",
            "notes": {matiere: 12.0 for matiere in NOTES_MATIERES},
        }
    if "resultat_orientation" not in st.session_state:
        st.session_state.resultat_orientation = None
    if "afficher_details_resultat" not in st.session_state:
        st.session_state.afficher_details_resultat = False


def get_profil_academique():
    return st.session_state.profil_academique


def get_centre_interet_effectif(profil_academique):
    """Retourne le centre d'intérêt à utiliser pour le scoring/l'affichage :
    le texte libre saisi si 'Autre' est sélectionné, sinon la catégorie choisie."""
    centre = profil_academique.get("centre_interet", "")
    if centre == CENTRE_INTERET_AUTRE:
        precision = (profil_academique.get("centre_interet_precision") or "").strip()
        return precision or CENTRE_INTERET_AUTRE
    return centre


def update_profil_academique(champ, valeur):
    st.session_state.profil_academique[champ] = valeur


def update_note(matiere, valeur):
    st.session_state.profil_academique["notes"][matiere] = valeur


def get_profil():
    return st.session_state.profil


def update_profil(champ, valeur):
    st.session_state.profil[champ] = valeur


def profil_rempli_a(pourcentage_requis=0.5):
    valeurs = st.session_state.profil.values()
    remplis = sum(1 for v in valeurs if v not in ("", [], None))
    return remplis / len(PROFILE_FIELDS) >= pourcentage_requis


def profil_champs_manquants():
    return [c for c, v in st.session_state.profil.items() if v in ("", [], None)]
