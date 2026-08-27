import streamlit as st
from services.api_client import get_formation
from components.formation_card import render_formation_card
from components.icons import render_html

RANG_CLASSES = {1: "rank-badge rank-1", 2: "rank-badge rank-2", 3: "rank-badge rank-3"}


def render_resultat_panel():
    with st.container(border=True):
        col_icone, col_titre = st.columns([1, 6])
        with col_icone:
            st.markdown('<div class="panel-icon"><span class="material-symbols-outlined">track_changes</span></div>', unsafe_allow_html=True)
        with col_titre:
            st.markdown('<div class="panel-title">Résultat de l\'Orientation</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-subtitle">Recommandations personnalisées</div>', unsafe_allow_html=True)

        st.divider()
        resultat = st.session_state.resultat_orientation

        if not resultat:
            st.info(
                "Complétez votre profil à gauche puis cliquez sur \"Analyser mon profil\" "
                "pour obtenir une recommandation.",
                icon=":material/info:",
            )
            return

        principale = resultat["filiere_principale"]
        render_html(
            f"""
            <div class="filiere-principale">
                <div class="filiere-principale-label">
                    <span class="material-symbols-outlined">workspace_premium</span>
                    Filière principale recommandée
                </div>
                <div class="filiere-principale-row">
                    <span class="filiere-principale-code">{principale['code']}</span>
                    <span class="score-badge"><span class="material-symbols-outlined">arrow_upward</span>{principale['score']} %</span>
                </div>
                <div class="filiere-principale-footer">Score d'adéquation</div>
            </div>
            """
        )

        st.markdown("**Top 3 des parcours suggérés**")
        for item in resultat["top3"]:
            classe_rang = RANG_CLASSES.get(item["rang"], "rank-badge")
            render_html(
                f"""
                <div class="top-parcours-row">
                    <span class="{classe_rang}">{item['rang']}</span>
                    <span class="top-parcours-nom">{item['code']}</span>
                    <span class="top-parcours-score">{item['score']} %</span>
                </div>
                """
            )
            st.progress(min(item["score"] / 100, 1.0))

        st.markdown("**Pourquoi cette recommandation ?**")
        for justification in resultat["justifications"]:
            st.markdown(
                f'<div class="justification-item"><span class="material-symbols-outlined">check_circle</span>{justification}</div>',
                unsafe_allow_html=True,
            )

        if st.button("Voir plus de détails", icon=":material/arrow_forward:", use_container_width=True):
            st.session_state.afficher_details_resultat = not st.session_state.afficher_details_resultat

        if st.session_state.afficher_details_resultat:
            formation = get_formation(principale["code"].lower())
            if formation:
                render_formation_card(formation)
