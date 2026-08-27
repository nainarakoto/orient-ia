import streamlit as st
import pandas as pd
from pathlib import Path

from state import init_session_state
from components.icons import inject_global_head
from components.header import render_header
from components.mention import render_mention_banner
from services.api_client import get_registre_sources


init_session_state()
inject_global_head()
st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

render_header("Registre des sources", "Traçabilité des documents utilisés par le système")
render_mention_banner()

sources = get_registre_sources()
colonnes = {
    "titre": "Titre",
    "origine": "Origine",
    "date_consultation": "Date de consultation",
    "statut": "Statut",
    "donnees_extraites": "Données extraites",
    "limites": "Limites constatées",
}
tableau = pd.DataFrame(sources).rename(columns=colonnes)
st.dataframe(tableau, use_container_width=True, hide_index=True)

st.caption(
    "Une information non vérifiée n'est jamais présentée comme une information officielle. "
    "Ce registre liste, pour chaque source, son statut et ses limites connues."
)
