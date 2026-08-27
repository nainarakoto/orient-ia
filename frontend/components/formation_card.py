import streamlit as st


def render_formation_card(formation):
    with st.container(border=True):
        col_titre, col_niveau = st.columns([3, 1])
        with col_titre:
            st.markdown(f"### {formation['nom']}")
            st.caption(formation["mention"])
        with col_niveau:
            st.markdown(f"**{formation['niveau']}**")

        col_matieres, col_competences = st.columns(2)
        with col_matieres:
            st.markdown("**Matières principales**")
            for matiere in formation["matieres"]:
                st.markdown(f"- {matiere}")
        with col_competences:
            st.markdown("**Compétences développées**")
            for competence in formation["competences"]:
                st.markdown(f"- {competence}")

        st.markdown("**Prérequis**")
        st.markdown(", ".join(formation["prerequis"]))

        st.markdown("**Débouchés professionnels**")
        st.markdown(", ".join(formation["debouches"]))

        st.caption(f"Source : {formation['source']}")
