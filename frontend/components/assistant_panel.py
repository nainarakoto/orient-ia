import streamlit as st
from datetime import datetime
from state import get_profil_academique
from services.api_client import envoyer_message_assistant
from components.icons import render_html

SUGGESTIONS = [
    "Comparer IGGLIA et ESIIA",
    "Quels sont les débouchés ?",
    "Quels sont les prérequis ?",
]


def _horodatage():
    return datetime.now().strftime("%H:%M")


def _envoyer(message):
    st.session_state.chat_history.append({"role": "user", "contenu": message, "heure": _horodatage()})
    resultat = envoyer_message_assistant(st.session_state.chat_history, message, get_profil_academique())
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "contenu": resultat["reponse"],
            "heure": _horodatage(),
            "sources": resultat.get("sources", []),
        }
    )


def render_assistant_panel():
    with st.container(border=True):
        col_icone, col_titre = st.columns([1, 6])
        with col_icone:
            st.markdown('<div class="panel-icon"><span class="material-symbols-outlined">forum</span></div>', unsafe_allow_html=True)
        with col_titre:
            st.markdown('<div class="panel-title">Assistant Conversationnel (IA)</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-subtitle">Posez vos questions</div>', unsafe_allow_html=True)

        st.divider()

        if not st.session_state.chat_history:
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "contenu": "Bonjour ! Je suis votre assistant ORIENT'IA. Comment puis-je vous aider aujourd'hui ?",
                    "heure": _horodatage(),
                    "sources": [],
                }
            )

        with st.container(height=320):
            for message in st.session_state.chat_history:
                classe = "chat-bubble chat-user" if message["role"] == "user" else "chat-bubble chat-assistant"
                icone = "" if message["role"] == "user" else '<span class="material-symbols-outlined chat-avatar">school</span>'
                render_html(
                    f"""
                    <div class="chat-row {'chat-row-user' if message['role'] == 'user' else ''}">
                        {icone}
                        <div class="{classe}">
                            {message['contenu'].replace(chr(10), '<br>')}
                            <div class="chat-time">{message['heure']}</div>
                        </div>
                    </div>
                    """
                )

        col_a, col_b = st.columns(2)
        if col_a.button(SUGGESTIONS[0], use_container_width=True):
            _envoyer(SUGGESTIONS[0])
            st.rerun()
        if col_b.button(SUGGESTIONS[1], use_container_width=True):
            _envoyer(SUGGESTIONS[1])
            st.rerun()
        if st.button(SUGGESTIONS[2], use_container_width=True):
            _envoyer(SUGGESTIONS[2])
            st.rerun()

        with st.form("formulaire_assistant", clear_on_submit=True, border=False):
            col_saisie, col_envoyer = st.columns([5, 1])
            question = col_saisie.text_input(
                "Question", placeholder="Posez votre question à l'assistant...", label_visibility="collapsed"
            )
            envoyer = col_envoyer.form_submit_button("", icon=":material/arrow_forward:", use_container_width=True)

        if envoyer and question:
            _envoyer(question)
            st.rerun()
