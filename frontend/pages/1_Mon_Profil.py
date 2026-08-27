import streamlit as st
from pathlib import Path

from state import init_session_state
from components.icons import inject_global_head
from components.header import render_header
from components.mention import render_mention_banner
from components.profile_form import render_profile_form


init_session_state()
inject_global_head()
st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

render_header("Mon profil", "Renseignez vos informations pour obtenir une recommandation personnalisée")
render_mention_banner()

st.info(
    "Seules les informations que vous déclarez explicitement (matières, compétences, intérêts, "
    "expérience, préférences) sont prises en compte. Aucune caractéristique personnelle sensible "
    "n'est demandée ni utilisée.",
    icon=":material/shield:",
)

render_profile_form()
