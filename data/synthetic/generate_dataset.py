import os
import random
import csv
import math

# Configuration
SEED = 42
TOTAL_STUDENTS = 750
TOTAL_PROFESSIONALS = 250
OUTPUT_DIR = "."

random.seed(SEED)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Referentiel des series et matieres
SERIES_SUBJECTS = {
    "A": {
        "Philosophie": 5, "Français": 5, "Malagasy": 4, "Histoire-Géographie": 4,
        "Anglais": 3, "LV2": 3, "Mathématiques": 2, "SVT / Sciences humaines": 2, "EPS": 2
    },
    "A1": {
        "Philosophie": 5, "Français": 5, "Malagasy": 4, "Histoire-Géographie": 4,
        "Anglais": 3, "LV2": 3, "Mathématiques": 2, "SVT / Sciences humaines": 2, "EPS": 2
    },
    "A2": {
        "Philosophie": 5, "Français": 5, "Malagasy": 4, "Histoire-Géographie": 4,
        "Anglais": 4, "LV2": 4, "Mathématiques": 2, "SVT / Sciences humaines": 2, "EPS": 2
    },
    "L": {
        "Philosophie": 5, "Français et Littérature": 5, "Anglais": 4, "LV2": 4,
        "Malagasy": 3, "Histoire-Géographie": 3, "Éducation civique": 2, "Mathématiques": 2,
        "Arts / options culturelles": 2, "EPS": 2
    },
    "C": {
        "Mathématiques": 7, "Sciences Physiques, Chimiques et Technologie (SPCT)": 6,
        "Français": 3, "Philosophie": 2, "Malagasy": 2, "Histoire-Géographie": 2,
        "Anglais": 2, "SVT": 3, "EPS": 2
    },
    "D": {
        "SVT": 6, "Sciences Physiques, Chimiques et Technologie (SPCT)": 5,
        "Mathématiques": 5, "Français": 3, "Philosophie": 2, "Malagasy": 2,
        "Histoire-Géographie": 2, "Anglais": 2, "EPS": 2
    },
    "S": {
        "Mathématiques": 7, "Sciences Physiques et Chimiques": 6, "SVT / Biologie-Géologie": 5,
        "Français": 3, "Philosophie": 2, "Malagasy": 2, "Histoire-Géographie": 2,
        "Anglais": 2, "EPS": 2
    },
    "G": {
        "Mathématiques de gestion": 5, "Gestion / Comptabilité": 6, "Français": 4,
        "Anglais": 4, "Économie": 4, "Histoire-Géographie": 2, "Philosophie": 2, "EPS": 2
    },
    "Technique": {
        "Mathématiques appliquées": 6, "Physique appliquée / Technologie": 6,
        "Dessin technique": 4, "Français": 3, "Anglais": 3, "Philosophie": 2, "EPS": 2
    }
}

# Referentiel des formations ISPM
FORMATIONS_ISPM = [
    {
        "code_filiere": "AEE", "nom_complet": "Agriculture et Élevage",
        "parcours_id": "P1", "parcours_nom": "Biotechnologie et Agronomie",
        "description": "Formation sur les techniques agronomiques modernes, la gestion des cultures et l'élevage durable.",
        "matieres_importantes": ["SVT", "SVT / Biologie-Géologie", "SVT / Sciences humaines", "Mathématiques", "SPCT", "Sciences Physiques et Chimiques", "Français", "Anglais"],
        "competences": ["Agronomie", "Zootechnie", "Analyse des sols", "Gestion d'exploitation"],
        "prerequis": "Basse exigence en maths pures, intérêt fort pour les sciences naturelles et l'environnement.",
        "series_admissibles": ["D", "S", "C", "A", "A1", "A2"],
        "metiers": ["Agronome", "Conseiller agricole", "Chef d'exploitation", "Responsable d'élevage"],
        "secteur": "Agriculture / Agronomie"
    },
    {
        "code_filiere": "IAA", "nom_complet": "Industrie Agroalimentaire",
        "parcours_id": "P1", "parcours_nom": "Biotechnologie et Agronomie",
        "description": "Transformation des produits agricoles, contrôle qualité sanitaire et procédés de conservation alimentaire.",
        "matieres_importantes": ["Sciences Physiques, Chimiques et Technologie (SPCT)", "Sciences Physiques et Chimiques", "SVT", "SVT / Biologie-Géologie", "Mathématiques", "Français", "Anglais"],
        "competences": ["Biochimie alimentaire", "Contrôle qualité HACCP", "Process agroalimentaires", "Microbiologie"],
        "prerequis": "Bases en chimie et biologie.",
        "series_admissibles": ["D", "S", "C", "Technique"],
        "metiers": ["Ingénieur Agroalimentaire", "Responsable Qualité HACCP", "Conducteur de ligne de production", "Biologiste industriel"],
        "secteur": "Industrie Agroalimentaire"
    },
    {
        "code_filiere": "PIP", "nom_complet": "Pharmacologie et Industries Pharmaceutiques",
        "parcours_id": "P1", "parcours_nom": "Biotechnologie et Agronomie",
        "description": "Étude des principes actifs, formulation pharmaceutique, contrôle qualité des médicaments et cosmétiques.",
        "matieres_importantes": ["Sciences Physiques, Chimiques et Technologie (SPCT)", "Sciences Physiques et Chimiques", "SVT", "SVT / Biologie-Géologie", "Mathématiques", "Français", "Anglais"],
        "competences": ["Chimie organique", "Pharmacologie", "Analyse en laboratoire", "Normes GMP/BPF"],
        "prerequis": "Excellentes notes en Chimie et Biologie.",
        "series_admissibles": ["C", "D", "S"],
        "metiers": ["Technicien supérieur en pharmacologie", "Responsable contrôle qualité labo", "Assistant de recherche galénique", "Délégué médical"],
        "secteur": "Industrie Pharmaceutique & Santé"
    },
    {
        "code_filiere": "EMII", "nom_complet": "Électro-Mécanique et Informatique Industrielle",
        "parcours_id": "P2", "parcours_nom": "Génie Industriel et Génie Civil",
        "description": "Conception, automatisation et maintenance des systèmes mécatroniques et chaînes industrielles.",
        "matieres_importantes": ["Mathématiques", "Mathématiques appliquées", "Sciences Physiques, Chimiques et Technologie (SPCT)", "Sciences Physiques et Chimiques", "Physique appliquée / Technologie", "Anglais"],
        "competences": ["Automatisme PLC", "Électrotechnique", "Maintenance industrielle", "CAO Mécanique"],
        "prerequis": "Solides bases en sciences physiques et mathématiques.",
        "series_admissibles": ["C", "S", "Technique", "D"],
        "metiers": ["Ingénieur Électromécanicien", "Automaticien", "Responsable Maintenance", "Concepteur Mécatronique"],
        "secteur": "Industrie & Automatisme"
    },
    {
        "code_filiere": "GCA", "nom_complet": "Génie Civil et Architecture",
        "parcours_id": "P2", "parcours_nom": "Génie Industriel et Génie Civil",
        "description": "Dimensionnement des structures, conception architecturale, calcul de béton armé et conduite de chantier BTP.",
        "matieres_importantes": ["Mathématiques", "Mathématiques appliquées", "Sciences Physiques, Chimiques et Technologie (SPCT)", "Sciences Physiques et Chimiques", "Dessin technique", "Histoire-Géographie"],
        "competences": ["Calcul de structures", "AutoCAD/Revit", "Métré et devis", "Conduite de chantier BTP"],
        "prerequis": "Esprit spatial, maîtrise de la physique et géométrie.",
        "series_admissibles": ["C", "S", "Technique", "D"],
        "metiers": ["Ingénieur Génie Civil", "Architecte collaborateur", "Chef de chantier BTP", "Conducteur de travaux"],
        "secteur": "Bâtiment et Travaux Publics (BTP)"
    },
    {
        "code_filiere": "ICMP", "nom_complet": "Industries Chimiques, Minières et Pétrolières",
        "parcours_id": "P2", "parcours_nom": "Génie Industriel et Génie Civil",
        "description": "Extraction des ressources géologiques, procédés de raffinage, traitement des minerais et normes QHSE.",
        "matieres_importantes": ["Sciences Physiques, Chimiques et Technologie (SPCT)", "Sciences Physiques et Chimiques", "Mathématiques", "SVT", "SVT / Biologie-Géologie"],
        "competences": ["Génie des procédés", "Géologie minière", "Normes QHSE", "Raffinage et extraction"],
        "prerequis": "Forte appétence pour la chimie des matériaux et la physique.",
        "series_admissibles": ["C", "S", "D", "Technique"],
        "metiers": ["Ingénieur Procédés", "Géologue minier", "Ingénieur QHSE", "Responsable d'extraction"],
        "secteur": "Mines, Énergie & Chimie"
    },
    {
        "code_filiere": "ESIIA", "nom_complet": "Electronique Système Informatique et Intelligence Artificielle",
        "parcours_id": "P3", "parcours_nom": "Informatique et Télécommunication",
        "description": "Conception de cartes électroniques, programmation bas niveau, systèmes embarqués et robotique intelligente.",
        "matieres_importantes": ["Mathématiques", "Mathématiques appliquées", "Sciences Physiques, Chimiques et Technologie (SPCT)", "Sciences Physiques et Chimiques", "Physique appliquée / Technologie", "Anglais"],
        "competences": ["C/C++ embarqué", "Microcontrôleurs IoT", "Électronique numérique", "Signal & Traitement"],
        "prerequis": "Compétences élevées en logique mathématique et physique appliquée.",
        "series_admissibles": ["C", "S", "Technique"],
        "metiers": ["Ingénieur Systèmes Embarqués", "Concepteur Électronique", "Ingénieur Robotique", "Développeur IoT"],
        "secteur": "Électronique & High-Tech"
    },
    {
        "code_filiere": "IGGLIA", "nom_complet": "Informatique de Gestion Génie Logiciel et Intelligence Artificielle",
        "parcours_id": "P3", "parcours_nom": "Informatique et Télécommunication",
        "description": "Ingénierie logicielle avancée, architecture des systèmes d'information, bases de données et modèles d'IA.",
        "matieres_importantes": ["Mathématiques", "Mathématiques de gestion", "Mathématiques appliquées", "Anglais", "Français"],
        "competences": ["Algorithmique & Python", "Génie Logiciel & Java/Web", "SQL & Bases de données", "Machine Learning"],
        "prerequis": "Grande rigueur logique, bon niveau en mathématiques et anglais.",
        "series_admissibles": ["C", "S", "D", "G", "Technique", "A", "A1", "A2"],
        "metiers": ["Développeur Fullstack", "Ingénieur Génie Logiciel", "Architecte SI", "Data Scientist / IA"],
        "secteur": "Informatique & Édition de Logiciels"
    },
    {
        "code_filiere": "IMTICIA", "nom_complet": "Informatique Multimédia Technologie de L'information et de la Communication et Intelligence Artificielle",
        "parcours_id": "P3", "parcours_nom": "Informatique et Télécommunication",
        "description": "Développement web/mobile, modélisation multimédia 3D, réseaux de communication et applications IA interactives.",
        "matieres_importantes": ["Mathématiques", "Français", "Anglais", "Arts / options culturelles", "Physique appliquée / Technologie"],
        "competences": ["UI/UX Design", "Développement Web/Mobile", "Infographie & 3D", "Réseaux informatiques"],
        "prerequis": "Créativité visuelle alliée à des compétences en logique numérique.",
        "series_admissibles": ["C", "S", "D", "L", "A", "A1", "A2", "G", "Technique"],
        "metiers": ["Développeur Web/Mobile", "Designer UI/UX", "Administrateur Réseaux & TIC", "Concepteur Multimédia"],
        "secteur": "Numérique & Multimédia"
    },
    {
        "code_filiere": "ISAIA", "nom_complet": "Informatique Statistique Appliquée et Intelligence Artificielle",
        "parcours_id": "P3", "parcours_nom": "Informatique et Télécommunication",
        "description": "Modélisation statistique avancée, Big Data, analyse prédictive et algorithmes d'apprentissage automatique.",
        "matieres_importantes": ["Mathématiques", "Mathématiques de gestion", "Mathématiques appliquées", "Anglais", "Français"],
        "competences": ["Statistiques inférentielles", "Python / R Data", "Machine Learning & Deep Learning", "PowerBI & Analytics"],
        "prerequis": "Très fort niveau en mathématiques pures et de gestion.",
        "series_admissibles": ["C", "S", "D", "G"],
        "metiers": ["Data Analyst", "Data Scientist", "Consultant Big Data", "Statisticien Décisionnel"],
        "secteur": "Data & Intelligence Artificielle"
    },
    {
        "code_filiere": "TEE", "nom_complet": "Tourisme et Environnement",
        "parcours_id": "P4", "parcours_nom": "Techniques du Tourisme",
        "description": "Valorisation du patrimoine naturel, gestion de projets d'écotourisme et conservation environnementale.",
        "matieres_importantes": ["Français", "Anglais", "LV2", "Histoire-Géographie", "SVT", "SVT / Biologie-Géologie", "SVT / Sciences humaines"],
        "competences": ["Ingénierie touristique", "Écotourisme & Biodiversité", "Gestion de projets durables", "Guide & Médiation"],
        "prerequis": "Aisance en langues, sensibilité écologique et ouverture culturelle.",
        "series_admissibles": ["A", "A1", "A2", "L", "D", "S", "G"],
        "metiers": ["Consultant Écotourisme", "Chef de projet Développement Durable", "Guide Patrimoine", "Responsable Parc Naturel"],
        "secteur": "Tourisme & Environnement"
    },
    {
        "code_filiere": "TEH", "nom_complet": "Tourisme et Hôtellerie",
        "parcours_id": "P4", "parcours_nom": "Techniques du Tourisme",
        "description": "Management des établissements hôteliers, organisation événementielle et accueil touristique international.",
        "matieres_importantes": ["Français", "Anglais", "LV2", "Histoire-Géographie", "Gestion / Comptabilité"],
        "competences": ["Management hôtelier", "Gestion événementielle", "Communication interculturelle", "Yield Management"],
        "prerequis": "Excellentes qualités relationnelles et maîtrise des langues étrangères.",
        "series_admissibles": ["A", "A1", "A2", "L", "G", "D"],
        "metiers": ["Manager d'Hôtel", "Chef de projet Événementiel", "Responsable d'Agence de Voyage", "Directeur de l'Hébergement"],
        "secteur": "Hôtellerie & Restauration"
    },
    {
        "code_filiere": "CAA", "nom_complet": "Commerce et Administration des Affaires",
        "parcours_id": "P5", "parcours_nom": "Techniques des Affaires",
        "description": "Développement commercial, techniques de négociation, marketing stratégique et gestion administrative des entreprises.",
        "matieres_importantes": ["Français", "Anglais", "Mathématiques de gestion", "Mathématiques", "Gestion / Comptabilité", "Économie"],
        "competences": ["Marketing Digital", "Techniques de Vente", "Negociation internationale", "Analyse Marché"],
        "prerequis": "Aisance orale, sens de la négociation et culture économique.",
        "series_admissibles": ["G", "A", "A1", "A2", "L", "D", "C", "S"],
        "metiers": ["Responsable Commercial", "Chef de Produit Marketing", "Directeur des Ventes", "Business Developer"],
        "secteur": "Commerce & Marketing"
    },
    {
        "code_filiere": "DTJA", "nom_complet": "Droit et Techniques Juridiques des Affaires",
        "parcours_id": "P5", "parcours_nom": "Techniques des Affaires",
        "description": "Droit des contrats, droit des sociétés, fiscalité des entreprises et réglementation du travail.",
        "matieres_importantes": ["Français", "Français et Littérature", "Philosophie", "Histoire-Géographie", "Éducation civique", "Anglais"],
        "competences": ["Rédaction juridique", "Droit des contrats", "Analyse fiscale", "Conseil d'entreprise"],
        "prerequis": "Excellente maîtrise du français écrit et capacité de raisonnement rigoureux.",
        "series_admissibles": ["A", "A1", "A2", "L", "G", "D"],
        "metiers": ["Juriste d'Entreprise", "Consultant Fiscaliste", "Assistant Juridique", "Gestionnaire de Contrats"],
        "secteur": "Droit & Juridique"
    },
    {
        "code_filiere": "EMP", "nom_complet": "Economie et Management de Projet",
        "parcours_id": "P5", "parcours_nom": "Techniques des Affaires",
        "description": "Analyse conjoncturelle, pilotage budgétaire, évaluation d'impact et méthodologies de gestion de projets complexes.",
        "matieres_importantes": ["Mathématiques", "Mathématiques de gestion", "Économie", "Français", "Anglais"],
        "competences": ["Gestion de projet Agile/PMP", "Analyse financière", "Étude d'impact économique", "Gestion des risques"],
        "prerequis": "Sens de l'organisation, leadership et maîtrise des outils analytiques.",
        "series_admissibles": ["G", "C", "S", "D", "A", "A1", "A2"],
        "metiers": ["Chef de Projet", "Consultant en Organisation", "Analyste Économique", "Scrum Master"],
        "secteur": "Management & Conseil"
    },
    {
        "code_filiere": "FIC", "nom_complet": "Finances et Comptabilités",
        "parcours_id": "P5", "parcours_nom": "Techniques des Affaires",
        "description": "Gestion comptable générale et analytique, audit financier, trésorerie et contrôle de gestion.",
        "matieres_importantes": ["Mathématiques de gestion", "Mathématiques", "Gestion / Comptabilité", "Économie", "Français"],
        "competences": ["Comptabilité générale & analytique", "Audit financier", "Contrôle de gestion", "Gestion de trésorerie"],
        "prerequis": "Grande rigueur avec les chiffres, précision et méthodes analytiques.",
        "series_admissibles": ["G", "C", "S", "D"],
        "metiers": ["Comptable Senior", "Auditeur Financier", "Contrôleur de Gestion", "Directeur Financier (CFO)"],
        "secteur": "Finance & Comptabilité"
    }
]

FILIERES_DICT = {f["code_filiere"]: f for f in FORMATIONS_ISPM}
ALL_FILIERE_CODES = list(FILIERES_DICT.keys())

FIRST_NAMES = ["Andry", "Hery", "Mialy", "Tiana", "Faly", "Rova", "Tojo", "Nary", "Fitia", "Sitraka", "Nomena", "Kanto", "Soa", "Hasina", "Lova", "Vero", "Toky", "Mirana", "Henintsoa", "Dina"]
LAST_NAMES = ["Razafindrakoto", "Ramanantsoa", "Rakotomalala", "Rasoanaivo", "Randriamampianina", "Andriantsitohaina", "Ratsimbazafy", "Rajaonarivelo", "Rabenjamina", "Rakotondrabe"]
CENTRES_INTERET_POOL = ["Programmation & Code", "Robotique", "Dessin & Design", "Lecture & Écriture", "Nature & Écologie", "Économie & Bourse", "Jeux de Stratégie", "Musique", "Sport d'équipe", "Volontariat"]
WORK_ENV_POOL = ["Bureau & Télétravail", "Laboratoire & R&D", "Sur le terrain / Chantier", "Espaces de Coworking / Startup", "Entreprise industrielle"]

# Fonctions utilitaires
def clamp(val, min_v=0.0, max_v=20.0):
    return max(min_v, min(max_v, round(val, 2)))

def generate_grades(series):
    subjects_dict = SERIES_SUBJECTS[series]
    grades = {}
    
    math_bias = 4.0 if series in ["C", "S", "Technique"] else (2.0 if series in ["D", "G"] else -2.5)
    science_bias = 3.5 if series in ["C", "D", "S", "Technique"] else -2.0
    literary_bias = 3.0 if series in ["A", "A1", "A2", "L"] else 0.0
    gestion_bias = 4.0 if series == "G" else 0.0

    for subj in subjects_dict.keys():
        base = random.gauss(11.5, 2.5)
        if "Math" in subj:
            base += math_bias
        elif any(k in subj for k in ["SPCT", "Physique", "Chimie", "SVT", "Biologie", "Technologie"]):
            base += science_bias
        elif any(k in subj for k in ["Français", "Philosophie", "Littérature", "LV2", "Civique", "Arts"]):
            base += literary_bias
        elif any(k in subj for k in ["Gestion", "Comptabilité", "Économie"]):
            base += gestion_bias
            
        grades[subj] = clamp(base)
    return grades

def compute_weighted_average(series, grades):
    subjs_coef = SERIES_SUBJECTS[series]
    total_points = sum(grades[subj] * subjs_coef[subj] for subj in grades)
    total_coef = sum(subjs_coef.values())
    return round(total_points / total_coef, 2)

def evaluate_compatibility(series, grades, target_filiere_code):
    filiere = FILIERES_DICT[target_filiere_code]
    
    series_admissible = series in filiere["series_admissibles"]
    series_score = 100.0 if series_admissible else 40.0
    
    relevant_grades = []
    for subj, grade in grades.items():
        if any(imp.lower() in subj.lower() or subj.lower() in imp.lower() for imp in filiere["matieres_importantes"]):
            relevant_grades.append(grade)
            
    if relevant_grades:
        avg_important = sum(relevant_grades) / len(relevant_grades)
    else:
        avg_important = sum(grades.values()) / len(grades)
        
    grade_score = (avg_important / 20.0) * 100.0
    
    raw_score = (0.6 * grade_score) + (0.4 * series_score) + random.gauss(0, 3.0)
    final_score = round(max(0.0, min(100.0, raw_score)), 2)
    
    if final_score >= 75.0 and series_admissible:
        level = "Élevé"
        admissible = "Oui"
    elif final_score >= 55.0:
        level = "Moyen"
        admissible = "Sous condition" if series_admissible else "Non"
    else:
        level = "Faible"
        admissible = "Non"
        
    return final_score, level, admissible

# Generation des etudiants
students_data = []
candidat_filiere_rows = []
series_list = list(SERIES_SUBJECTS.keys())

for i in range(1, TOTAL_STUDENTS + 1):
    std_id = f"STD_2026_{i:04d}"
    age = random.randint(16, 21)
    sexe = random.choice(["M", "F"])
    series = series_list[i % len(series_list)]
    
    grades = generate_grades(series)
    moyenne_generale = compute_weighted_average(series, grades)
    
    sorted_grades = sorted(grades.items(), key=lambda x: x[1], reverse=True)
    mat_fortes = [s[0] for s in sorted_grades[:2]]
    mat_faibles = [s[0] for s in sorted_grades[-2:]]
    
    rec_filiere_code = ALL_FILIERE_CODES[i % len(ALL_FILIERE_CODES)]
    rec_filiere = FILIERES_DICT[rec_filiere_code]
    
    score_compat, niv_confiance, admissible = evaluate_compatibility(series, grades, rec_filiere_code)
    
    interests = random.sample(CENTRES_INTERET_POOL, k=2)
    comps = random.sample(rec_filiere["competences"], k=2) + ["Résolution de problèmes"]
    job_target = random.choice(rec_filiere["metiers"])
    
    justification = (
        f"Excellente adéquation avec la série {series} et bonnes notes en "
        f"{', '.join(mat_fortes)}. Profil aligné avec l'objectif de {job_target}."
    )
    
    alt_filieres = random.sample([f for f in ALL_FILIERE_CODES if f != rec_filiere_code], k=2)
    
    student_record = {
        "student_id": std_id,
        "nom_complet": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "age": age,
        "sexe": sexe,
        "serie": series,
        "notes_detaillees": "; ".join([f"{k}:{v}" for k, v in grades.items()]),
        "moyenne_generale": moyenne_generale,
        "matieres_fortes": "; ".join(mat_fortes),
        "matieres_faibles": "; ".join(mat_faibles),
        "centres_interet": "; ".join(interests),
        "competences": "; ".join(comps),
        "preferences_env": random.choice(WORK_ENV_POOL),
        "objectif_professionnel": job_target,
        "filieres_compatibles": "; ".join([rec_filiere_code] + alt_filieres),
        "filiere_recommandee": rec_filiere_code,
        "parcours_recommande": rec_filiere["parcours_nom"],
        "score_compatibilite": score_compat,
        "niveau_confiance": niv_confiance,
        "justification": justification
    }
    students_data.append(student_record)
    
    for f_code in ALL_FILIERE_CODES:
        sc, lvl, adm = evaluate_compatibility(series, grades, f_code)
        candidat_filiere_rows.append({
            "candidat_id": std_id,
            "filiere_code": f_code,
            "parcours_id": FILIERES_DICT[f_code]["parcours_id"],
            "score_compatibilite": sc,
            "est_admissible": adm,
            "est_recommandee": "Oui" if f_code == rec_filiere_code else "Non"
        })

# Generation des professionnels
pros_data = []
pro_validation_rows = []

for i in range(1, TOTAL_PROFESSIONALS + 1):
    pro_id = f"PRO_2026_{i:04d}"
    age = random.randint(23, 50)
    sexe = random.choice(["M", "F"])
    
    filiere_ispm = ALL_FILIERE_CODES[i % len(ALL_FILIERE_CODES)]
    f_info = FILIERES_DICT[filiere_ispm]
    
    years_exp = random.randint(1, 20)
    job = random.choice(f_info["metiers"])
    comps = random.sample(f_info["competences"], k=2) + ["Gestion de projet", "Leadership"]
    
    match_score = round(random.uniform(70.0, 99.0), 2)
    
    pro_record = {
        "professional_id": pro_id,
        "nom_complet": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "age": age,
        "sexe": sexe,
        "a_etudie_ispm": "Oui",
        "formation_suivie": f"Diplôme ISPM - {f_info['nom_complet']}",
        "parcours_ispm": f_info["parcours_nom"],
        "filiere_etudiee": filiere_ispm,
        "annee_obtention": 2026 - years_exp,
        "competences": "; ".join(comps),
        "specialisation": f_info["nom_complet"],
        "metier_actuel": job,
        "secteur_professionnel": f_info["secteur"],
        "annees_experience": years_exp,
        "matieres_cles_retenues": "; ".join(f_info["matieres_importantes"][:3]),
        "adequation_formation_metier_score": match_score
    }
    pros_data.append(pro_record)
    
    pro_validation_rows.append({
        "professional_id": pro_id,
        "filiere_etudiee": filiere_ispm,
        "parcours_id": f_info["parcours_id"],
        "metier_exerce": job,
        "adequation_score": match_score,
        "parcours_valide": "Oui" if match_score >= 60.0 else "Non"
    })

# Fonction d'ecriture CSV
def write_csv(filename, fieldnames, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Ecriture des differents fichiers CSV
write_csv("profils_etudiants_synthetiques.csv", list(students_data[0].keys()), students_data)
write_csv("profils_professionnels_synthetiques.csv", list(pros_data[0].keys()), pros_data)

unified_rows = []
for s in students_data:
    unified_rows.append({
        "profile_id": s["student_id"],
        "type_profil": "Étudiant",
        "age": s["age"],
        "sexe": s["sexe"],
        "serie_ou_filiere": s["serie"],
        "competences_clefs": s["competences"],
        "objectif_ou_metier": s["objectif_professionnel"],
        "filiere_associee": s["filiere_recommandee"],
        "score_adéquation_global": s["score_compatibilite"]
    })
for p in pros_data:
    unified_rows.append({
        "profile_id": p["professional_id"],
        "type_profil": "Professionnel",
        "age": p["age"],
        "sexe": p["sexe"],
        "serie_ou_filiere": p["filiere_etudiee"],
        "competences_clefs": p["competences"],
        "objectif_ou_metier": p["metier_actuel"],
        "filiere_associee": p["filiere_etudiee"],
        "score_adéquation_global": p["adequation_formation_metier_score"]
    })
write_csv("profils_synthetiques.csv", list(unified_rows[0].keys()), unified_rows)

write_csv("candidat_filiere.csv", list(candidat_filiere_rows[0].keys()), candidat_filiere_rows)
write_csv("professional_validation.csv", list(pro_validation_rows[0].keys()), pro_validation_rows)

formations_rows = []
for f in FORMATIONS_ISPM:
    formations_rows.append({
        "code_filiere": f["code_filiere"],
        "nom_complet": f["nom_complet"],
        "parcours_id": f["parcours_id"],
        "parcours_nom": f["parcours_nom"],
        "description": f["description"],
        "matieres_principales": "; ".join(f["matieres_importantes"]),
        "competences_visees": "; ".join(f["competences"]),
        "prerequis": f["prerequis"],
        "series_admissibles": "; ".join(f["series_admissibles"]),
        "metiers_accessibles": "; ".join(f["metiers"]),
        "secteur_professionnel": f["secteur"]
    })
write_csv("formations_etablissement.csv", list(formations_rows[0].keys()), formations_rows)

admission_rows = []
for f in FORMATIONS_ISPM:
    admission_rows.append({
        "filiere_code": f["code_filiere"],
        "series_autorisees": "; ".join(f["series_admissibles"]),
        "matieres_obligatoires": f["matieres_importantes"][0],
        "note_minimale_requise": 10.0,
        "prerequis_detail": f["prerequis"]
    })
write_csv("admission_requirements.csv", list(admission_rows[0].keys()), admission_rows)

subjects_rows = []
for s_name, subjs in SERIES_SUBJECTS.items():
    for sub_name, coef in subjs.items():
        subjects_rows.append({
            "serie": s_name,
            "matiere": sub_name,
            "coefficient": coef
        })
write_csv("terminal_subjects.csv", list(subjects_rows[0].keys()), subjects_rows)

serie_mat_rows = []
for s_name in series_list:
    row = {"serie": s_name}
    for f_code, f_info in FILIERES_DICT.items():
        row[f_code] = "Compatible" if s_name in f_info["series_admissibles"] else "Non Compatible"
    serie_mat_rows.append(row)
write_csv("serie_filiere_matrix.csv", ["serie"] + ALL_FILIERE_CODES, serie_mat_rows)

all_unique_subjs = sorted(list(set([sub for s in SERIES_SUBJECTS.values() for sub in s.keys()])))
subj_mat_rows = []
for sub in all_unique_subjs:
    row = {"matiere": sub}
    for f_code, f_info in FILIERES_DICT.items():
        is_imp = any(imp.lower() in sub.lower() or sub.lower() in imp.lower() for imp in f_info["matieres_importantes"])
        row[f_code] = "Fort" if is_imp else "Faible"
    subj_mat_rows.append(row)
write_csv("subject_filiere_matrix.csv", ["matiere"] + ALL_FILIERE_CODES, subj_mat_rows)

comp_rows = []
c_id = 1
for f in FORMATIONS_ISPM:
    for c in f["competences"]:
        comp_rows.append({
            "competence_id": f"COMP_{c_id:03d}",
            "nom_competence": c,
            "filiere_code": f["code_filiere"],
            "secteur": f["secteur"]
        })
        c_id += 1
write_csv("competences.csv", list(comp_rows[0].keys()), comp_rows)

metier_rows = []
m_id = 1
for f in FORMATIONS_ISPM:
    for m in f["metiers"]:
        metier_rows.append({
            "metier_id": f"MET_{m_id:03d}",
            "intitule_metier": m,
            "filiere_code": f["code_filiere"],
            "parcours_nom": f["parcours_nom"]
        })
        m_id += 1
write_csv("metiers.csv", list(metier_rows[0].keys()), metier_rows)

sources_rows = [
    {"source_id": "SRC_01", "nom": "Guide de l'Étudiant ISPM", "type": "Officiel", "description": "Référentiel officiel des 5 parcours et 16 filières."},
    {"source_id": "SRC_02", "nom": "Base Données Baccalauréat", "type": "Statistique", "description": "Statistiques sur les séries du baccalauréat."}
]
write_csv("sources.csv", list(sources_rows[0].keys()), sources_rows)

print("Génération terminée avec succès.")