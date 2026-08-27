import streamlit as st
from state import get_profil, update_profil
from services.api_client import get_ml_schema

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


def _step_key():
    return "profil_etape"


def _valeur_numerique(profil, champ, defaut):
    valeur = profil.get(champ)
    if valeur in ("", None):
        return defaut
    return valeur


def render_profile_form():
    if _step_key() not in st.session_state:
        st.session_state[_step_key()] = 0

    etape = st.session_state[_step_key()]
    profil = get_profil()
    schema_ml = get_ml_schema()

    st.progress((etape + 1) / len(ETAPES))
    st.markdown(f"**Étape {etape + 1} sur {len(ETAPES)} — {ETAPES[etape]}**")

    if etape == 0:
        col_age, col_serie, col_moyenne = st.columns(3)
        with col_age:
            age = st.number_input(
                "Âge",
                min_value=14,
                max_value=60,
                value=int(_valeur_numerique(profil, "age", 18)),
                step=1,
            )
        with col_serie:
            options_serie = [""] + schema_ml.get("series", [])
            serie_actuelle = profil.get("serie", "")
            serie = st.selectbox(
                "Série du bac",
                options_serie,
                index=options_serie.index(serie_actuelle) if serie_actuelle in options_serie else 0,
            )
        with col_moyenne:
            moyenne = st.number_input(
                "Moyenne générale",
                min_value=0.0,
                max_value=20.0,
                value=float(_valeur_numerique(profil, "moyenne_generale", 10.0)),
                step=0.1,
            )

        matieres = st.multiselect("Matières préférées", MATIERES, default=profil.get("matieres_preferees") or [])
        matieres_faibles = st.multiselect(
            "Matières les moins fortes",
            MATIERES,
            default=profil.get("matieres_faibles") or [],
        )
        resultats = st.text_area(
            "Résultats scolaires",
            value=profil.get("resultats_scolaires", ""),
            placeholder="Niveau actuel, moyenne ou mention obtenue",
        )
        update_profil("age", age)
        update_profil("serie", serie)
        update_profil("moyenne_generale", moyenne)
        update_profil("matieres_preferees", matieres)
        update_profil("matieres_faibles", matieres_faibles)
        update_profil("resultats_scolaires", resultats)

    elif etape == 1:
        competences = st.multiselect("Compétences déclarées", COMPETENCES, default=profil.get("competences") or [])
        interets = st.text_area(
            "Centres d'intérêt",
            value=profil.get("centres_interet", ""),
            placeholder="Décrivez vos centres d'intérêt, séparés par des virgules",
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
            "Métiers qui vous intéressent", METIERS, default=profil.get("preferences_professionnelles") or []
        )

        options_objectif = [""] + schema_ml.get("objectifs_professionnels", [])
        objectif_actuel = profil.get("objectif_professionnel", "")
        objectif_professionnel = st.selectbox(
            "Objectif professionnel principal",
            options_objectif,
            index=options_objectif.index(objectif_actuel) if objectif_actuel in options_objectif else 0,
            help="Utilisé par le modèle de recommandation pour évaluer l'adéquation avec chaque filière.",
        )

        options_env = [""] + schema_ml.get("preferences_env", [])
        env_actuel = profil.get("environnement_travail", "")
        environnement = st.selectbox(
            "Type d'environnement de travail recherché",
            options_env,
            index=options_env.index(env_actuel) if env_actuel in options_env else 0,
        )
        update_profil("preferences_professionnelles", metiers)
        update_profil("objectif_professionnel", objectif_professionnel)
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