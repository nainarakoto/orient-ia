import streamlit as st
from pathlib import Path
from datetime import datetime

from state import init_session_state, get_profil
from components.icons import inject_global_head
from components.header import render_header
from components.mention import render_mention_banner
from services.api_client import envoyer_message_assistant


def _horodatage():
    return datetime.now().strftime("%H:%M")


init_session_state()
inject_global_head()
st.markdown(f"<style>{Path('styles/style.css').read_text()}</style>", unsafe_allow_html=True)

render_header("Assistant ORIENT'IA", "Posez vos questions sur les formations et votre orientation")
render_mention_banner()

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["contenu"])
        if message.get("sources"):
            st.caption("Sources : " + ", ".join(message["sources"]))

question = st.chat_input("Posez votre question sur les formations, les prérequis ou votre orientation")

if question:
    st.session_state.chat_history.append(
        {"role": "user", "contenu": question, "heure": _horodatage()}
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents et appel des outils..."):
            resultat = envoyer_message_assistant(st.session_state.chat_history, question, get_profil())
        st.markdown(resultat["reponse"])
        if resultat.get("sources"):
            st.caption("Sources : " + ", ".join(resultat["sources"]))
        if resultat.get("outils_appeles"):
            st.caption("Outils utilisés : " + ", ".join(resultat["outils_appeles"]))

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "contenu": resultat["reponse"],
            "sources": resultat.get("sources", []),
            "heure": _horodatage(),
        }
    )