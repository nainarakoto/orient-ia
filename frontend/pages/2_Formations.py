import streamlit as st
from pathlib import Path

from state import init_session_state
from components.icons import inject_global_head
from components.header import render_header
from components.mention import render_mention_banner
from components.formation_card import render_formation_card
from services.api_client import get_formations


init_session_state()
inject_global_head()
st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

render_header("Formations", "Mentions, parcours et débouchés proposés par l'ISPM")
render_mention_banner()

formations = get_formations()

col_recherche, col_niveau = st.columns([2, 1])
with col_recherche:
    recherche = st.text_input("Rechercher une formation", placeholder="Nom, mention ou matière")
with col_niveau:
    niveaux = ["Tous"] + sorted({f["niveau"] for f in formations})
    niveau_choisi = st.selectbox("Niveau", niveaux)

formations_filtrees = formations
if recherche:
    recherche_min = recherche.lower()
    formations_filtrees = [
        f for f in formations_filtrees
        if recherche_min in f["nom"].lower()
        or recherche_min in f["mention"].lower()
        or any(recherche_min in m.lower() for m in f["matieres"])
    ]
if niveau_choisi != "Tous":
    formations_filtrees = [f for f in formations_filtrees if f["niveau"] == niveau_choisi]

st.caption(f"{len(formations_filtrees)} formation(s) trouvée(s)")

for formation in formations_filtrees:
    render_formation_card(formation)
    if st.button(f"Ajouter {formation['nom']} au comparateur", key=f"comparer_{formation['id']}"):
        if formation["id"] not in st.session_state.parcours_a_comparer:
            st.session_state.parcours_a_comparer.append(formation["id"])
            st.success(f"{formation['nom']} ajouté au comparateur")
