import streamlit as st
from pathlib import Path

from state import init_session_state, get_profil, profil_rempli_a, profil_champs_manquants
from components.icons import inject_global_head
from components.header import render_header
from components.mention import render_mention_banner
from services.api_client import obtenir_recommandation


init_session_state()
inject_global_head()
st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

render_header("Recommandation personnalisée", "Résultat du modèle de Machine Learning et de l'agent")
render_mention_banner()

if not profil_rempli_a():
    manquants = profil_champs_manquants()
    st.warning(
        f"Votre profil est incomplet ({len(manquants)} champ(s) manquant(s)). "
        "La recommandation sera plus fiable si vous le complétez.",
        icon=":material/warning:",
    )
    st.page_link("pages/1_Mon_Profil.py", label="Compléter mon profil", icon=":material/person:")

if st.button("Obtenir une recommandation", icon=":material/insights:", type="primary"):
    with st.spinner("Analyse du profil et appel du modèle..."):
        st.session_state.recommandation = obtenir_recommandation(get_profil())

recommandation = st.session_state.recommandation

if recommandation:
    st.caption(f"Origine des scores : {recommandation['origine']}")
    for resultat in recommandation["resultats"]:
        with st.container(border=True):
            col_nom, col_score = st.columns([3, 1])
            with col_nom:
                st.markdown(f"### {resultat['parcours']}")
            with col_score:
                st.metric("Adéquation", f"{resultat['score_adequation'] * 100:.0f} %")
            st.progress(resultat["score_adequation"])
            st.markdown("**Facteurs pris en compte**")
            for facteur in resultat["facteurs"]:
                st.markdown(f"- {facteur}")
            st.caption("Sources : " + ", ".join(resultat["sources"]))

    st.warning(recommandation["incertitude"], icon=":material/error_outline:")
    st.caption(
        "Cette recommandation combine un résultat de Machine Learning, des informations "
        "documentaires et une explication générée par l'assistant. Elle ne constitue pas une décision d'admission."
    )
