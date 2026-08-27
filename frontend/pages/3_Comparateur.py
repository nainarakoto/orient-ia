import streamlit as st
import pandas as pd
from pathlib import Path

from state import init_session_state
from components.icons import inject_global_head
from components.header import render_header
from components.mention import render_mention_banner
from services.api_client import get_formations


init_session_state()
inject_global_head()
st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

render_header("Comparateur de parcours", "Comparez plusieurs formations sur les mêmes critères")
render_mention_banner()

formations = get_formations()
noms_disponibles = {f["nom"]: f["id"] for f in formations}
ids_selectionnes = st.session_state.parcours_a_comparer

noms_par_defaut = [n for n, i in noms_disponibles.items() if i in ids_selectionnes]
selection = st.multiselect("Parcours à comparer", list(noms_disponibles.keys()), default=noms_par_defaut)

if len(selection) < 2:
    st.info("Sélectionnez au moins deux parcours pour lancer la comparaison.", icon=":material/info:")
else:
    formations_selectionnees = [f for f in formations if f["nom"] in selection]
    tableau = {
        "Critère": ["Mention", "Niveau", "Matières", "Compétences", "Prérequis", "Débouchés", "Source"]
    }
    for formation in formations_selectionnees:
        tableau[formation["nom"]] = [
            formation["mention"],
            formation["niveau"],
            ", ".join(formation["matieres"]),
            ", ".join(formation["competences"]),
            ", ".join(formation["prerequis"]),
            ", ".join(formation["debouches"]),
            formation["source"],
        ]
    st.dataframe(pd.DataFrame(tableau).set_index("Critère"), use_container_width=True)
