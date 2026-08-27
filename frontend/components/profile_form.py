import streamlit as st
from state import get_profil, update_profil

ETAPES = [
    "Parcours scolaire",
    "Compétences et intérêts",
    "Expérience",
    "Préférences professionnelles",
]

MATIERES = [
    "Mathématiques", "Physique", "Informatique", "Programmation",
    "Analyse de données", "Langues", "Économie", "Sciences humaines",
    "Développement d'interfaces", "Gestion de projet",
]

COMPETENCES = [
    "Programmation", "Analyse de données", "Communication", "Travail en équipe",
    "Résolution de problèmes", "Conception", "Administration système", "Rédaction",
]

METIERS = [
    "Développeur logiciel", "Data analyst", "Ingénieur réseau", "Chef de projet",
    "Chercheur", "Consultant", "Administrateur système",
]

ENVIRONNEMENTS = ["Bureau", "Terrain", "Mixte", "À distance", "Pas de préférence"]


def _step_key():
    return "profil_etape"


def render_profile_form():
    if _step_key() not in st.session_state:
        st.session_state[_step_key()] = 0

    etape = st.session_state[_step_key()]
    profil = get_profil()

    st.progress((etape + 1) / len(ETAPES))
    st.markdown(f"**Étape {etape + 1} sur {len(ETAPES)} — {ETAPES[etape]}**")

    if etape == 0:
        matieres = st.multiselect("Matières préférées", MATIERES, default=profil.get("matieres_preferees") or [])
        resultats = st.text_area(
            "Résultats scolaires",
            value=profil.get("resultats_scolaires", ""),
            placeholder="Niveau actuel, moyenne ou mention obtenue",
        )
        update_profil("matieres_preferees", matieres)
        update_profil("resultats_scolaires", resultats)

    elif etape == 1:
        competences = st.multiselect("Compétences déclarées", COMPETENCES, default=profil.get("competences") or [])
        interets = st.text_area(
            "Centres d'intérêt",
            value=profil.get("centres_interet", ""),
            placeholder="Décrivez vos centres d'intérêt personnels ou académiques",
        )
        update_profil("competences", competences)
        update_profil("centres_interet", interets)

    elif etape == 2:
        activites = st.text_area(
            "Activités ou projets déjà réalisés",
            value=profil.get("activites_projets", ""),
            placeholder="Projets scolaires, stages, activités associatives, réalisations personnelles",
            height=120,
        )
        update_profil("activites_projets", activites)

    elif etape == 3:
        metiers = st.multiselect(
            "Préférences professionnelles", METIERS, default=profil.get("preferences_professionnelles") or []
        )
        environnement = st.selectbox(
            "Type d'environnement de travail recherché",
            ENVIRONNEMENTS,
            index=ENVIRONNEMENTS.index(profil["environnement_travail"])
            if profil.get("environnement_travail") in ENVIRONNEMENTS
            else 0,
        )
        update_profil("preferences_professionnelles", metiers)
        update_profil("environnement_travail", environnement)

    col_precedent, col_suivant = st.columns(2)
    with col_precedent:
        if etape > 0:
            if st.button("Précédent", icon=":material/arrow_back:", use_container_width=True):
                st.session_state[_step_key()] -= 1
                st.rerun()
    with col_suivant:
        if etape < len(ETAPES) - 1:
            if st.button("Suivant", icon=":material/arrow_forward:", use_container_width=True, type="primary"):
                st.session_state[_step_key()] += 1
                st.rerun()
        else:
            st.success("Profil complété. Vous pouvez demander une recommandation.", icon=":material/check_circle:")
