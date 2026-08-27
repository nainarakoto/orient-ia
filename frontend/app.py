import streamlit as st
from pathlib import Path

from state import init_session_state
from components.icons import inject_global_head
from components.header import render_dashboard_header
from components.mention import render_mention_banner, render_footer
from components.profil_panel import render_profil_panel
from components.resultat_panel import render_resultat_panel
from components.assistant_panel import render_assistant_panel

st.set_page_config(
    page_title="ORIENT'IA",
    page_icon=":material/school:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_accueil():
    """Page d'accueil (tableau de bord) — anciennement 'app' dans le menu."""
    init_session_state()
    inject_global_head()
    st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

    render_dashboard_header()

    col_profil, col_resultat, col_assistant = st.columns(3, gap="medium")
    with col_profil:
        render_profil_panel()
    with col_resultat:
        render_resultat_panel()
    with col_assistant:
        render_assistant_panel()

    render_mention_banner()
    render_footer()


# Navigation : chaque entrée du menu porte désormais un titre lisible et une
# icône dédiée. La page "app" devient "Accueil". Les fichiers de pages/
# eux-mêmes ne sont ni déplacés ni renommés.
pages = [
    st.Page(render_accueil, title="Accueil", icon=":material/home:", default=True, url_path="accueil"),
    st.Page("pages/1_Mon_Profil.py", title="Mon Profil", icon=":material/person:"),
    st.Page("pages/2_Formations.py", title="Formations", icon=":material/school:"),
    st.Page("pages/3_Comparateur.py", title="Comparateur", icon=":material/compare_arrows:"),
    st.Page("pages/4_Recommandation.py", title="Recommandation", icon=":material/insights:"),
    st.Page("pages/5_Assistant.py", title="Assistant", icon=":material/chat:"),
    st.Page("pages/6_Sources.py", title="Sources", icon=":material/description:"),
]

navigation = st.navigation(pages)
navigation.run()
