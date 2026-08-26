import streamlit as st


# ------------------------------------------------------------------------------
# 0. INJECTION DE CSS ET ANIMATIONS
# ------------------------------------------------------------------------------
def injecter_style_et_animations():
    st.markdown("""
        <!-- Chargement d'Animate.css pour des animations fluides -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

        <style>
        /* 1. Animation & style sur la Barre Latérale (Navigation / Sidebar) */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            transition: all 0.4s ease-in-out;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        /* Animation des éléments du menu dans le Sidebar au survol */
        [data-testid="stSidebar"] .stRadio label {
            padding: 10px 15px;
            border-radius: 8px;
            transition: transform 0.2s ease, background 0.3s ease;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(8px);
        }

        /* 2. Style des Cartes & Conteneurs avec effets Hover */
        .stAlert, div[data-testid="stForm"] {
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        div[data-testid="stForm"]:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        /* 3. Boutons Stylisés avec animation de pression */
        .stButton>button, div[data-testid="stForm"] button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
            color: white !important;
            border: none !important;
        }

        .stButton>button:hover, div[data-testid="stForm"] button:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 1. BASE DE DONNÉES DES 16 PARCOURS OFFICIELS ISPM
# ------------------------------------------------------------------------------
PARCOURS_ISPM = [
    # 1. Mention : Informatique et Télécommunications
    {
        "sigle": "IGGLIA",
        "mention": "Informatique et Télécommunications",
        "nom": "Informatique de Gestion Génie Logiciel et Intelligence Artificielle (IGGLIA)",
        "mots_cles": ["Mathématiques", "Informatique / TIC", "Développement Logiciel & Web",
                      "Intelligence Artificielle & Data Science", "Esprit d'analyse & Logique"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)",
                       "Série Technique / DTI (Informatique, Génie Civil, Électronique, etc.)",
                       "Série D (Sciences de la Vie et de la Terre)"],
        "description": "Génie logiciel, développement web/mobile, bases de données et algorithmes d'IA."
    },
    {
        "sigle": "ESIIA",
        "mention": "Informatique et Télécommunications",
        "nom": "Electronique Système Informatique et Intelligence Artificielle (ESIIA)",
        "mots_cles": ["Physique-Chimie", "Mathématiques", "Informatique / TIC", "Cybersécurité & Réseaux",
                      "Résolution de problèmes complexes"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)",
                       "Série Technique / DTI (Informatique, Génie Civil, Électronique, etc.)"],
        "description": "Systèmes embarqués, réseaux informatiques, automatisation et capteurs intelligents."
    },
    {
        "sigle": "IMTICIA",
        "mention": "Informatique et Télécommunications",
        "nom": "Informatique Multimédia Technologie de L'information et de la Communication et Intelligence Artificielle (IMTICIA)",
        "mots_cles": ["Informatique / TIC", "Design & Métiers Créatifs", "Communication orale & écrite",
                      "Créativité & Graphisme"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)", "Série A1 / A2 (Littéraire & Langues)",
                       "Série Technique / DTI (Informatique, Génie Civil, Électronique, etc.)"],
        "description": "Création multimédia, développement web frontal, UX/UI design et technologies du Web."
    },
    {
        "sigle": "ISAIA",
        "mention": "Informatique et Télécommunications",
        "nom": "Informatique Statistique Appliquée et Intelligence Artificielle (ISAIA)",
        "mots_cles": ["Mathématiques", "Informatique / TIC", "Intelligence Artificielle & Data Science",
                      "Esprit d'analyse & Logique"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)", "Série D (Sciences de la Vie et de la Terre)"],
        "description": "Analyse de données, modélisation statistique, apprentissage automatique et Big Data."
    },

    # 2. Mention : Génie Industriel
    {
        "sigle": "EMII",
        "mention": "Génie Industriel",
        "nom": "Electro-Mécanique et Informatique Industrielle (EMII)",
        "mots_cles": ["Physique-Chimie", "Mathématiques", "Informatique / TIC", "Résolution de problèmes complexes"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)",
                       "Série Technique / DTI (Informatique, Génie Civil, Électronique, etc.)"],
        "description": "Maintenance industrielle, robotique, mécatronique et contrôle de procédés."
    },
    {
        "sigle": "ICMP",
        "mention": "Génie Industriel",
        "nom": "Industries Chimiques, Minières et Pétrolières (ICMP)",
        "mots_cles": ["Physique-Chimie", "SVT (Sciences de la Vie et de la Terre)",
                      "Environnement & Développement Durable"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)", "Série D (Sciences de la Vie et de la Terre)"],
        "description": "Ingénierie des procédés chimiques, extraction minière, raffinage et sécurité industrielle."
    },

    # 3. Mention : Génie Civil et Architecture
    {
        "sigle": "GCA",
        "mention": "Génie Civil et Architecture",
        "nom": "Génie Civil et Architecture (GCA)",
        "mots_cles": ["Mathématiques", "Physique-Chimie", "Design & Métiers Créatifs", "Créativité & Graphisme"],
        "series_fav": ["Série C (Mathématiques & Sciences Physiques)",
                       "Série Technique / DTI (Informatique, Génie Civil, Électronique, etc.)"],
        "description": "Conception de structures, BTP, dessin architectural et urbanisme."
    },

    # 4. Mention : Droit et Techniques des Affaires
    {
        "sigle": "CAA",
        "mention": "Droit et Techniques des Affaires",
        "nom": "Commerce et Administration des Affaires (CAA)",
        "mots_cles": ["Économie & Droit", "Gestion / Comptabilité", "Entrepreneuriat & Business",
                      "Marketing & Commerce", "Gestion de projet & Leadership"],
        "series_fav": ["Série Tertiaire (Gestion, Commerce, Comptabilité)",
                       "Série OSE (Organisation, Société, Économie)"],
        "description": "Négociation commerciale, stratégie marketing, vente et gestion administrative."
    },
    {
        "sigle": "EMP",
        "mention": "Droit et Techniques des Affaires",
        "nom": "Economie et Management de Projet (EMP)",
        "mots_cles": ["Économie & Droit", "Gestion / Comptabilité", "Entrepreneuriat & Business",
                      "Gestion de projet & Leadership"],
        "series_fav": ["Série OSE (Organisation, Société, Économie)",
                       "Série Tertiaire (Gestion, Commerce, Comptabilité)"],
        "description": "Montage de projets, analyse micro/macro-économique et planification stratégique."
    },
    {
        "sigle": "FIC",
        "mention": "Droit et Techniques des Affaires",
        "nom": "Finances et Comptabilités (FIC)",
        "mots_cles": ["Gestion / Comptabilité", "Mathématiques", "Finance & Banque", "Économie & Droit"],
        "series_fav": ["Série Tertiaire (Gestion, Commerce, Comptabilité)",
                       "Série C (Mathématiques & Sciences Physiques)"],
        "description": "Analyse financière, comptabilité générale et analytique, audit et fiscalité."
    },
    {
        "sigle": "DTJA",
        "mention": "Droit et Techniques des Affaires",
        "nom": "Droit et Techniques Juridiques des Affaires (DTJA)",
        "mots_cles": ["Économie & Droit", "Philosophie", "Français / Littérature", "Communication orale & écrite"],
        "series_fav": ["Série A1 / A2 (Littéraire & Langues)", "Série OSE (Organisation, Société, Économie)"],
        "description": "Droit des affaires, droit du travail, juriste d'entreprise et rédaction de contrats."
    },

    # 5. Mention : Biotechnologie et Agronomie
    {
        "sigle": "IAA",
        "mention": "Biotechnologie et Agronomie",
        "nom": "Industrie Agroalimentaire (IAA)",
        "mots_cles": ["SVT (Sciences de la Vie et de la Terre)", "Physique-Chimie", "Transformation Agro-alimentaire",
                      "Biologie & Transformation"],
        "series_fav": ["Série D (Sciences de la Vie et de la Terre)", "Série C (Mathématiques & Sciences Physiques)"],
        "description": "Transformation des produits agricoles, conservation, biochimie et contrôle qualité."
    },
    {
        "sigle": "AEE",
        "mention": "Biotechnologie et Agronomie",
        "nom": "Agriculture et Elevage (AEE)",
        "mots_cles": ["SVT (Sciences de la Vie et de la Terre)", "Agronomie & Agriculture",
                      "Environnement & Développement Durable"],
        "series_fav": ["Série D (Sciences de la Vie et de la Terre)"],
        "description": "Production végétale, zootechnie, gestion des exploitations agricoles et élevage."
    },
    {
        "sigle": "PIP",
        "mention": "Biotechnologie et Agronomie",
        "nom": "Pharmacologie et Industries Pharmaceutiques (PIP)",
        "mots_cles": ["SVT (Sciences de la Vie et de la Terre)", "Physique-Chimie", "Biologie & Transformation",
                      "Santé & Pharmacologie"],
        "series_fav": ["Série D (Sciences de la Vie et de la Terre)", "Série C (Mathématiques & Sciences Physiques)"],
        "description": "Chimie thérapeutique, fabrication de médicaments, cosmétologie et recherche pharmacologique."
    },

    # 6. Mention : Tourisme
    {
        "sigle": "TEE",
        "mention": "Tourisme",
        "nom": "Tourisme et Environnement (TEE)",
        "mots_cles": ["Histoire-Géographie", "Environnement & Développement Durable", "Anglais",
                      "Français / Littérature"],
        "series_fav": ["Série A1 / A2 (Littéraire & Langues)", "Série OSE (Organisation, Société, Économie)",
                       "Série D (Sciences de la Vie et de la Terre)"],
        "description": "Écotourisme, valorisation du patrimoine naturel et développement territorial durable."
    },
    {
        "sigle": "TEH",
        "mention": "Tourisme",
        "nom": "Tourisme et Hôtellerie (TEH)",
        "mots_cles": ["Anglais", "Français / Littérature", "Marketing & Commerce", "Gestion de projet & Leadership"],
        "series_fav": ["Série A1 / A2 (Littéraire & Langues)", "Série Tertiaire (Gestion, Commerce, Comptabilité)"],
        "description": "Management hôtelier, accueil, événementiel et gestion d'agences de voyage."
    }
]


# ------------------------------------------------------------------------------
# 2. MOTEUR DE CALCUL DES RECOMMANDATIONS
# ------------------------------------------------------------------------------
def calculer_recommandations(serie_bacc, matieres, interets, competences):
    profil_mots = set(matieres + interets + competences)
    resultats = []

    for parcours in PARCOURS_ISPM:
        score = 0

        if serie_bacc in parcours["series_fav"]:
            score += 35
        else:
            score += 15

        correspondances = set(parcours["mots_cles"]).intersection(profil_mots)
        score += len(correspondances) * 18

        score_final = min(score, 98)
        resultats.append({
            "sigle": parcours["sigle"],
            "mention": parcours["mention"],
            "nom": parcours["nom"],
            "score": score_final,
            "description": parcours["description"]
        })

    resultats.sort(key=lambda x: x["score"], reverse=True)
    return resultats


# ------------------------------------------------------------------------------
# 3. INTERFACE UTILISATEUR AVEC ANIMATIONS
# ------------------------------------------------------------------------------
def afficher_profil():
    # Injection des styles et animations CSS
    injecter_style_et_animations()

    # En-tête avec animation Animate.css
    st.markdown("""
        <div class="animate__animated animate__fadeInDown">
            <h1 style="color: #1e3a8a; font-weight: 800; margin-bottom: 0;">🎓 ORIENT'IA</h1>
            <p style="color: #64748b; font-size: 1.1rem; margin-top: -5px;">
                Système d'orientation intelligent vers les 16 parcours officiels de l'ISPM.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Formulaire principal
    with st.form("form_profil"):
        st.subheader("👤 Informations Personnelles")

        col1, col2 = st.columns(2)
        with col1:
            nom_etudiant = st.text_input("Nom & Prénom(s) :", placeholder="ex: Minosoa Rafalimanana")
        with col2:
            niveau_etude = st.selectbox(
                "Niveau d'études actuel :",
                ["Terminale (En cours)", "Bachelier (Bac)", "Licence 1 (L1)", "Licence 2 (L2)", "Licence 3 (L3)",
                 "Master"]
            )

        st.write("---")
        st.subheader("🎓 Parcours du Baccalauréat")

        col_bac1, col_bac2 = st.columns(2)
        with col_bac1:
            serie_bacc = st.selectbox(
                "Série du Bacc :",
                [
                    "Série C (Mathématiques & Sciences Physiques)",
                    "Série D (Sciences de la Vie et de la Terre)",
                    "Série A1 / A2 (Littéraire & Langues)",
                    "Série OSE (Organisation, Société, Économie)",
                    "Série Technique / DTI (Informatique, Génie Civil, Électronique, etc.)",
                    "Série Tertiaire (Gestion, Commerce, Comptabilité)"
                ]
            )
        with col_bac2:
            mention_bacc = st.selectbox(
                "Mention obtenue ou visée :",
                ["Passable", "Assez Bien", "Bien", "Très Bien"]
            )

        st.write("---")
        st.subheader("📚 Matières de Terminale fortes")

        matieres_terminale_options = [
            "Mathématiques", "Physique-Chimie", "SVT (Sciences de la Vie et de la Terre)",
            "Informatique / TIC", "Philosophie", "Français / Littérature",
            "Anglais", "Économie & Droit", "Histoire-Géographie", "Gestion / Comptabilité"
        ]
        matieres_choisies = st.multiselect(
            "Matières où vous obtenez vos meilleures notes :",
            options=matieres_terminale_options,
            default=[]
        )

        st.write("---")
        st.subheader("💡 Intérêts & Domaines d'Activité")

        interets_options = [
            "Agronomie & Agriculture",
            "Transformation Agro-alimentaire",
            "Santé & Pharmacologie",
            "Développement Logiciel & Web",
            "Intelligence Artificielle & Data Science",
            "Entrepreneuriat & Business",
            "Finance & Banque",
            "Marketing & Commerce",
            "Design & Métiers Créatifs",
            "Environnement & Développement Durable",
            "Cybersécurité & Réseaux"
        ]
        interets_choisis = st.multiselect(
            "Domaines qui vous passionnent :",
            options=interets_options,
            default=[]
        )

        st.write("---")
        st.subheader("🛠️ Compétences & Aptitudes")

        competences_options = [
            "Résolution de problèmes complexes", "Esprit d'analyse & Logique",
            "Créativité & Graphisme", "Gestion de projet & Leadership",
            "Communication orale & écrite", "Biologie & Transformation",
            "Autonomie"
        ]
        competences_choisies = st.multiselect(
            "Vos points forts majeurs :",
            options=competences_options,
            default=[]
        )

        st.write("---")
        submit_button = st.form_submit_button("🎯 Obtenir mes recommandations")

    # Soumission du formulaire
    if submit_button:
        if not nom_etudiant.strip():
            st.warning("⚠️ Veuillez renseigner votre nom et prénom avant de lancer l'orientation.")
            return

        if not matieres_choisies and not interets_choisis:
            st.warning("⚠️ Veuillez sélectionner au moins une matière de Terminale ou un domaine d'intérêt.")
            return

        st.session_state["recommandations"] = calculer_recommandations(
            serie_bacc, matieres_choisies, interets_choisis, competences_choisies
        )
        st.session_state["nom_etudiant"] = nom_etudiant.strip()
        st.session_state["serie_bacc"] = serie_bacc

    # --------------------------------------------------------------------------
    # AFFICHAGE DES RÉSULTATS + ANIMATIONS DES CARTES
    # --------------------------------------------------------------------------
    if "recommandations" in st.session_state:
        recommandations = st.session_state["recommandations"]
        nom = st.session_state["nom_etudiant"]
        serie = st.session_state["serie_bacc"]

        st.markdown("<br>", unsafe_allow_html=True)
        st.success(f"Bienvenue **{nom}** ! Analyse effectuée parmi les 16 parcours ISPM.")

        st.write("---")
        st.subheader(f"📊 Recommandations personnalisées pour {nom}")

        # Top 1 - Carte Principale Animée (Animate.css zoomIn)
        top_1 = recommandations[0]
        st.markdown(f"""
            <div class="animate__animated animate__zoomIn" style="
                background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                color: white;
                padding: 24px;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
                margin-bottom: 25px;
            ">
                <span style="background: #f59e0b; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85rem;">
                    🏆 RECOMMANDATION PRINCIPALE ({top_1['score']}% MATCH)
                </span>
                <h2 style="color: white; margin-top: 10px; font-weight: 800;">{top_1['sigle']}</h2>
                <p style="font-size: 1.1rem; opacity: 0.9;"><strong>Mention :</strong> {top_1['mention']}</p>
                <p style="font-size: 1rem; opacity: 0.95;"><strong>{top_1['nom']}</strong></p>
                <hr style="border-color: rgba(255,255,255,0.2);">
                <p style="margin-bottom: 0;">{top_1['description']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Top 2 & 3 - Cartes Secondaires Animées (Animate.css fadeInUp)
        st.markdown("### 🥈 Alternative(s) Recommandée(s)")
        col_rec1, col_rec2 = st.columns(2)

        top_2 = recommandations[1]
        top_3 = recommandations[2]

        with col_rec1:
            st.markdown(f"""
                <div class="animate__animated animate__fadeInUp animate__delay-1s" style="
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-left: 5px solid #10b981;
                    padding: 18px;
                    border-radius: 12px;
                    height: 100%;
                ">
                    <span style="color: #10b981; font-weight: bold; font-size: 0.9rem;">TOP 2 ({top_2['score']}%)</span>
                    <h3 style="margin-top: 5px; color: #0f172a;">{top_2['sigle']}</h3>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 5px;"><em>{top_2['mention']}</em></p>
                    <p style="font-weight: 600; color: #334155;">{top_2['nom']}</p>
                    <p style="color: #475569; font-size: 0.9rem;">{top_2['description']}</p>
                </div>
            """, unsafe_allow_html=True)

        with col_rec2:
            st.markdown(f"""
                <div class="animate__animated animate__fadeInUp animate__delay-1s" style="
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-left: 5px solid #06b6d4;
                    padding: 18px;
                    border-radius: 12px;
                    height: 100%;
                ">
                    <span style="color: #06b6d4; font-weight: bold; font-size: 0.9rem;">TOP 3 ({top_3['score']}%)</span>
                    <h3 style="margin-top: 5px; color: #0f172a;">{top_3['sigle']}</h3>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 5px;"><em>{top_3['mention']}</em></p>
                    <p style="font-weight: 600; color: #334155;">{top_3['nom']}</p>
                    <p style="color: #475569; font-size: 0.9rem;">{top_3['description']}</p>
                </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    afficher_profil()