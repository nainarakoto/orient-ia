import streamlit as st
from state import SERIES_BAC, CENTRES_INTERET, NOTES_MATIERES, get_profil_academique, update_profil_academique, update_note
from services.api_client import obtenir_recommandation_academique


def render_profil_panel():
    with st.container(border=True):
        col_icone, col_titre = st.columns([1, 6])
        with col_icone:
            st.markdown('<div class="panel-icon"><span class="material-symbols-outlined">person</span></div>', unsafe_allow_html=True)
        with col_titre:
            st.markdown('<div class="panel-title">Profil Académique</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-subtitle">Renseignez votre parcours et vos notes</div>', unsafe_allow_html=True)

        st.divider()
        profil = get_profil_academique()

        st.markdown("**Informations générales**")
        serie = st.selectbox("Série du Baccalauréat", SERIES_BAC, index=SERIES_BAC.index(profil["serie_bac"]))
        centre = st.selectbox("Centre d'intérêt principal", CENTRES_INTERET, index=CENTRES_INTERET.index(profil["centre_interet"]))
        update_profil_academique("serie_bac", serie)
        update_profil_academique("centre_interet", centre)

        if centre == "Autre":
            precision = st.text_input(
                "Précisez votre centre d'intérêt",
                value=profil.get("centre_interet_precision", ""),
                placeholder="Ex. Robotique, Design, Environnement, Santé...",
            )
            update_profil_academique("centre_interet_precision", precision)

        st.markdown("**Notes au Bac (sur 20)**")
        for i in range(0, len(NOTES_MATIERES), 2):
            paire = NOTES_MATIERES[i:i + 2]
            colonnes = st.columns(len(paire))
            for colonne, matiere in zip(colonnes, paire):
                with colonne:
                    valeur = st.number_input(
                        matiere, min_value=0.0, max_value=20.0, step=0.25,
                        value=profil["notes"][matiere], key=f"note_{matiere}",
                    )
                    update_note(matiere, valeur)

        if st.button("Analyser mon profil", icon=":material/monitoring:", type="primary", use_container_width=True):
            with st.spinner("Analyse du profil en cours..."):
                st.session_state.resultat_orientation = obtenir_recommandation_academique(get_profil_academique())
            st.session_state.afficher_details_resultat = False
