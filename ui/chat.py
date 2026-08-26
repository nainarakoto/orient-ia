import streamlit as st

def afficher_chatbot():

    # Contenu de la page Chatbot
    st.markdown("""
        <div class="animate__animated animate__fadeInDown">
            <h1 style="color: #0f172a; font-weight: 800;">🎯 Évaluation & Chatbot</h1>
            <p style="color: #64748b;">Posez vos questions sur votre parcours d'orientation.</p>
        </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Bonjour Minosoa ! Comment puis-je vous aider aujourd'hui ?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Votre message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        reponse = f"Assistant OrientIA : Reçu pour '{prompt}'."
        st.session_state.messages.append({"role": "assistant", "content": reponse})
        with st.chat_message("assistant"):
            st.write(reponse)