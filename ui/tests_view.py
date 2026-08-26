import streamlit as st
import pandas as pd
import random


@st.cache_data
def charger_donnees_tests():
    nom_exemples = [
        "Minosoa Rafalimanana", "Rova Andriamanantena", "Toky Razafindrakoto",
        "Aina Rakotomalala", "Fitia Randrianarisoa", "Faniry Rajaonarivelo"
    ]
    parcours_list = ["IGGLIA", "ESIIA", "IMTICIA", "ISAIA", "EMII", "ICMP", "GCA", "CAA", "EMP", "FIC", "DTJA", "IAA"]
    series_list = ["Série C", "Série D", "Série A2", "Série OSE", "Série Technique (DTI)", "Série Tertiaire"]

    tests = []
    for i in range(1, 33):
        p_recommande = random.choice(parcours_list)
        score = random.randint(65, 98)
        tests.append({
            "ID Test": f"TEST-{i:03d}",
            "Étudiant": random.choice(nom_exemples) if i <= 6 else f"Étudiant #{i}",
            "Série Bacc": random.choice(series_list),
            "Parcours Recommandé": p_recommande,
            "Score Match (%)": score,
            "Statut": "Validé" if score >= 80 else "À confirmer"
        })
    return pd.DataFrame(tests)


def afficher_dashboard():

    st.markdown("""
            <style>
            /* 1. Masquer la barre d'outils au survol sur st.dataframe et st.table */
            [data-testid="stElementToolbar"] {
                display: none !important;
                visibility: hidden !important;
            }

            /* 2. Cibles spécifiques pour les versions récentes de Streamlit */
            div[data-testid="stElementToolbarButton"],
            button[title="View options"],
            button[aria-label="View options"] {
                display: none !important;
            }

            /* 3. Masquer le menu d'actions d'Altair / Vega / Plotly */
            details, 
            .vega-actions-wrapper, 
            .vega-actions, 
            .modebar-container {
                display: none !important;
            }
            </style>
        """, unsafe_allow_html=True)

    df_tests = charger_donnees_tests()

    # 1. EN-TÊTE ANIMÉ (Slide Down)
    st.markdown("""
        <div class="animate__animated animate__fadeInDown">
            <h1 style="color: #0f172a; font-weight: 800; margin-bottom: 0;">
                <i class="fa-solid fa-chart-pie" style="color: #2563eb; margin-right: 10px;"></i>Dashboard des Tests
            </h1>
            <p style="color: #64748b; font-size: 1rem; margin-top: 4px;">
                Vue synthétique et indicateurs de performance des 32 parcours.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. CARTES ANIMÉES
    score_moyen = round(df_tests["Score Match (%)"].mean(), 1)
    top_filiere = df_tests["Parcours Recommandé"].mode()[0]
    taux_valide = round((len(df_tests[df_tests["Statut"] == "Validé"]) / len(df_tests)) * 100)

    st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;" class="animate__animated animate__fadeInUp">
            <div style="background: white; padding: 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600;">TESTS EFFECTUÉS</div>
                <div style="color: #0f172a; font-size: 1.8rem; font-weight: 700;">{len(df_tests)} / 32</div>
                <div style="color: #16a34a; font-size: 0.8rem; font-weight: 600;">↑ 100% complété</div>
            </div>
            <div style="background: white; padding: 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600;">SCORE MATCH MOYEN</div>
                <div style="color: #0f172a; font-size: 1.8rem; font-weight: 700;">{score_moyen} %</div>
                <div style="color: #16a34a; font-size: 0.8rem; font-weight: 600;">↑ +2.4%</div>
            </div>
            <div style="background: white; padding: 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600;">TOP RECOMMANDATION</div>
                <div style="color: #2563eb; font-size: 1.8rem; font-weight: 700;">{top_filiere}</div>
                <div style="color: #64748b; font-size: 0.8rem;">Filière la plus demandée</div>
            </div>
            <div style="background: white; padding: 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600;">TAUX DE VALIDATION</div>
                <div style="color: #0f172a; font-size: 1.8rem; font-weight: 700;">{taux_valide} %</div>
                <div style="color: #16a34a; font-size: 0.8rem; font-weight: 600;">↑ Élevé</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # 3. GRAPHIQUES ET TABLEAUX ANIMÉS
    col_chart1, col_chart2 = st.columns([3, 2])

    with col_chart1:
        st.subheader("📈 Répartition par Parcours")
        filiere_counts = df_tests["Parcours Recommandé"].value_counts()
        st.bar_chart(filiere_counts, color="#2563eb")

    with col_chart2:
        st.subheader("🎯 Distribution des Statuts")
        counts_statut = df_tests["Statut"].value_counts()
        st.dataframe(
            counts_statut,
            column_config={"count": "Nombre d'étudiants"},
            use_container_width=True
        )

    st.write("---")

    # 4. TABLEAU DÉTAILLÉ
    st.subheader("📋 Liste Détaillée des 32 Tests")
    st.dataframe(
        df_tests,
        column_config={
            "Score Match (%)": st.column_config.ProgressColumn(
                "Score Match (%)",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
            "ID Test": st.column_config.TextColumn("Identifiant", help="ID unique du test"),
        },
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    afficher_dashboard()