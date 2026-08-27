#!/usr/bin/env python3

"""
ORIENT'IA - Préprocessing ML

Objectif
--------
Préparer les données synthétiques pour le système de recommandation
de filières.

Entrées principales
-------------------
data/synthetic/profils_etudiants_synthetiques.csv
data/synthetic/candidat_filiere.csv
data/synthetic/formations_etablissement.csv

Sorties
-------
ml/preprocessing/
├── ml_dataset.csv
├── X_train.csv
├── X_validation.csv
├── X_test.csv
├── y_train.csv
├── y_validation.csv
├── y_test.csv
├── feature_columns.txt
└── preprocessing_report.md

Principe
--------
Un exemple ML correspond à :

    candidat + filière

La cible est :

    est_recommandee

Le score_compatibilite est conservé uniquement pour analyse
et comparaison avec la baseline, afin d'éviter une fuite de données.
"""

from pathlib import Path
import sys
import json

import numpy as np
import pandas as pd

from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


# ============================================================
# 1. CONFIGURATION
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data" / "synthetic"
OUTPUT_DIR = ROOT_DIR / "ml" / "preprocessing"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


STUDENT_FILE = DATA_DIR / "profils_etudiants_synthetiques.csv"
CANDIDATE_FILE = DATA_DIR / "candidat_filiere.csv"
FORMATION_FILE = DATA_DIR / "formations_etablissement.csv"


# ============================================================
# 2. UTILITAIRES
# ============================================================

def print_section(title):
    """Affiche une section lisible dans le terminal."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def check_file(path):
    """Vérifie qu'un fichier existe."""
    if not path.exists():
        print(f"[ERREUR] Fichier introuvable : {path}")
        sys.exit(1)


def normalize_text(value):
    """Nettoyage simple des valeurs textuelles."""
    if pd.isna(value):
        return ""

    return str(value).strip()


def split_multivalue(value):
    """
    Transforme une cellule contenant plusieurs valeurs :

        "Mathématiques; Physique; Anglais"

    en :

        ["Mathématiques", "Physique", "Anglais"]
    """
    if pd.isna(value):
        return []

    value = str(value).strip()

    if not value:
        return []

    return [
        item.strip()
        for item in value.split(";")
        if item.strip()
    ]


# ============================================================
# 3. VÉRIFICATION DES FICHIERS
# ============================================================

print_section("1. Vérification des fichiers")

check_file(STUDENT_FILE)
check_file(CANDIDATE_FILE)
check_file(FORMATION_FILE)

print("[OK] Fichiers trouvés")


# ============================================================
# 4. CHARGEMENT
# ============================================================

print_section("2. Chargement des données")

students = pd.read_csv(STUDENT_FILE)
candidate_filiere = pd.read_csv(CANDIDATE_FILE)
formations = pd.read_csv(FORMATION_FILE)

print(f"Profils étudiants      : {students.shape}")
print(f"Candidat-filière       : {candidate_filiere.shape}")
print(f"Formations              : {formations.shape}")


# ============================================================
# 5. NORMALISATION DES COLONNES
# ============================================================

print_section("3. Vérification des colonnes")

students.columns = students.columns.str.strip()
candidate_filiere.columns = candidate_filiere.columns.str.strip()
formations.columns = formations.columns.str.strip()

print("\nColonnes profils étudiants :")
print(list(students.columns))

print("\nColonnes candidat-filière :")
print(list(candidate_filiere.columns))

print("\nColonnes formations :")
print(list(formations.columns))


# ============================================================
# 6. IDENTIFICATION DE L'ID CANDIDAT
# ============================================================

print_section("4. Identification des identifiants")

if "student_id" not in students.columns:
    raise ValueError(
        "La colonne 'student_id' est absente de "
        "profils_etudiants_synthetiques.csv"
    )

if "candidat_id" not in candidate_filiere.columns:
    raise ValueError(
        "La colonne 'candidat_id' est absente de candidat_filiere.csv"
    )

if "filiere_code" not in candidate_filiere.columns:
    raise ValueError(
        "La colonne 'filiere_code' est absente de candidat_filiere.csv"
    )

print("[OK] Identifiants disponibles")


# ============================================================
# 7. HARMONISATION DES IDENTIFIANTS
# ============================================================

print_section("5. Harmonisation des identifiants")

students["student_id"] = students["student_id"].astype(str).str.strip()
candidate_filiere["candidat_id"] = (
    candidate_filiere["candidat_id"]
    .astype(str)
    .str.strip()
)

candidate_filiere["filiere_code"] = (
    candidate_filiere["filiere_code"]
    .astype(str)
    .str.strip()
)

formations["code_filiere"] = (
    formations["code_filiere"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 8. RENOMMAGE POUR LA JOINTURE
# ============================================================

students = students.rename(
    columns={
        "student_id": "candidat_id"
    }
)


# ============================================================
# 9. JOINTURE PROFIL + CANDIDAT/FILIÈRE
# ============================================================

print_section("6. Construction du dataset candidat-filière")

data = candidate_filiere.merge(
    students,
    on="candidat_id",
    how="left",
    suffixes=("_cf", "_student")
)

print(f"Dataset après jointure : {data.shape}")


# ============================================================
# 10. VÉRIFICATION DE LA JOINTURE
# ============================================================

missing_profile = data["nom_complet_student"].isna().sum() \
    if "nom_complet_student" in data.columns else 0

print(f"Profils non trouvés : {missing_profile}")

if missing_profile > 0:
    print(
        "[ATTENTION] Certains candidats n'ont pas de profil étudiant."
    )


# ============================================================
# 11. AJOUT DES INFORMATIONS DE FILIÈRE
# ============================================================

print_section("7. Ajout des informations sur les filières")

formation_columns = [
    "code_filiere",
    "nom_complet",
    "parcours_id",
    "parcours_nom",
    "secteur_professionnel",
]

available_formation_columns = [
    c for c in formation_columns
    if c in formations.columns
]

formations_small = formations[available_formation_columns].copy()

formations_small = formations_small.rename(
    columns={
        "code_filiere": "filiere_code",
        "nom_complet": "filiere_nom",
        "parcours_id": "filiere_parcours_id",
        "parcours_nom": "filiere_parcours_nom",
        "secteur_professionnel": "filiere_secteur",
    }
)

data = data.merge(
    formations_small,
    on="filiere_code",
    how="left"
)

print(f"Dataset final après jointure : {data.shape}")


# ============================================================
# 12. VÉRIFICATION DE LA CIBLE
# ============================================================

print_section("8. Vérification de la cible")

TARGET = "est_recommandee"

if TARGET not in data.columns:
    raise ValueError(
        f"La colonne cible '{TARGET}' est absente."
    )

print("Distribution de la cible :")
print(data[TARGET].value_counts(dropna=False))


# ============================================================
# 13. CONVERSION DE LA CIBLE
# ============================================================

def convert_target(value):
    value = normalize_text(value).lower()

    if value in ["oui", "yes", "1", "true"]:
        return 1

    if value in ["non", "no", "0", "false"]:
        return 0

    return np.nan


data["target"] = data[TARGET].apply(convert_target)

unknown_target = data["target"].isna().sum()

if unknown_target > 0:
    print(
        f"[ATTENTION] {unknown_target} valeurs de cible "
        "n'ont pas pu être converties."
    )

data = data.dropna(subset=["target"])

data["target"] = data["target"].astype(int)


# ============================================================
# 14. SUPPRESSION DES INFORMATIONS SENSIBLES / INUTILES
# ============================================================

print_section("9. Suppression des colonnes inutiles")

DROP_COLUMNS = [
    "nom_complet",
    "nom_complet_student",

    TARGET,

    "score_compatibilite",
    "score_compatibilite_cf",
    "score_compatibilite_student",

    "est_admissible",

    "filiere_recommandee",
    "filiere_compatible",
    "filieres_compatibles",
    "parcours_recommande",
    "niveau_confiance",

    "justification",
]

existing_drop_columns = [
    c for c in DROP_COLUMNS
    if c in data.columns
]

data_ml = data.drop(
    columns=existing_drop_columns
)

print("Colonnes supprimées :")
for col in existing_drop_columns:
    print(f"  - {col}")


# ============================================================
# 15. FEATURE ENGINEERING
# ============================================================

print_section("10. Feature engineering")


# ------------------------------------------------------------
# 15.1 Âge
# ------------------------------------------------------------

if "age" in data_ml.columns:

    data_ml["age"] = pd.to_numeric(
        data_ml["age"],
        errors="coerce"
    )


# ------------------------------------------------------------
# 15.2 Moyenne générale
# ------------------------------------------------------------

if "moyenne_generale" in data_ml.columns:

    data_ml["moyenne_generale"] = pd.to_numeric(
        data_ml["moyenne_generale"],
        errors="coerce"
    )


# ------------------------------------------------------------
# 15.3 Nombre de compétences
# ------------------------------------------------------------

if "competences" in data_ml.columns:

    data_ml["nombre_competences"] = (
        data_ml["competences"]
        .apply(lambda x: len(split_multivalue(x)))
    )


# ------------------------------------------------------------
# 15.4 Nombre de matières fortes
# ------------------------------------------------------------

if "matieres_fortes" in data_ml.columns:

    data_ml["nombre_matieres_fortes"] = (
        data_ml["matieres_fortes"]
        .apply(lambda x: len(split_multivalue(x)))
    )


# ------------------------------------------------------------
# 15.5 Nombre de matières faibles
# ------------------------------------------------------------

if "matieres_faibles" in data_ml.columns:

    data_ml["nombre_matieres_faibles"] = (
        data_ml["matieres_faibles"]
        .apply(lambda x: len(split_multivalue(x)))
    )


# ------------------------------------------------------------
# 15.6 Nombre de centres d'intérêt
# ------------------------------------------------------------

if "centres_interet" in data_ml.columns:

    data_ml["nombre_centres_interet"] = (
        data_ml["centres_interet"]
        .apply(lambda x: len(split_multivalue(x)))
    )


# ============================================================
# 16. SUPPRESSION DES COLONNES TEXTUELLES COMPLEXES
# ============================================================

print_section("11. Sélection des variables ML")

# Ces colonnes nécessitent un traitement NLP / multi-label
# plus complexe. Pour la première baseline, on les retire.
COMPLEX_TEXT_COLUMNS = [
    "notes_detaillees",
    "competences",
    "matieres_fortes",
    "matieres_faibles",
    "centres_interet",
    "competences_clefs",
    "notes",
    "prerequis",
    "description",
    "matieres_principales",
    "competences_visees",
    "metiers_accessibles",
    "series_admissibles",
]

complex_existing = [
    c for c in COMPLEX_TEXT_COLUMNS
    if c in data_ml.columns
]

data_ml = data_ml.drop(
    columns=complex_existing
)

print("Variables textuelles complexes exclues :")
for col in complex_existing:
    print(f"  - {col}")


# ============================================================
# 17. SUPPRESSION DES COLONNES REDONDANTES
# ============================================================

REDUNDANT_COLUMNS = [
    "type_profil",
    "profile_id",
    "professional_id",
    "student_id",
]

redundant_existing = [
    c for c in REDUNDANT_COLUMNS
    if c in data_ml.columns
]

data_ml = data_ml.drop(
    columns=redundant_existing
)


# ============================================================
# 18. IDENTIFICATION DES FEATURES
# ============================================================

print_section("12. Identification des features")

if "target" not in data_ml.columns:
    raise ValueError("La cible 'target' n'existe pas.")

X = data_ml.drop(columns=["target"])
y = data_ml["target"]

# ------------------------------------------------------------
# Métadonnées utilisées uniquement pour l'évaluation ranking
# ------------------------------------------------------------

RANKING_METADATA_COLUMNS = [
    "candidat_id",
    "filiere_code",
]

ranking_metadata = data_ml[
    RANKING_METADATA_COLUMNS
].copy()

# Ces colonnes NE doivent PAS être utilisées comme features ML
X = data_ml.drop(
    columns=["target"] + RANKING_METADATA_COLUMNS
)

y = data_ml["target"]


# ============================================================
# 19. CONVERSION DES TYPES
# ============================================================

numeric_columns = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_columns = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print(f"Features numériques   : {len(numeric_columns)}")
print(f"Features catégorielles: {len(categorical_columns)}")

print("\nNumériques :")
for c in numeric_columns:
    print(f"  - {c}")

print("\nCatégorielles :")
for c in categorical_columns:
    print(f"  - {c}")


# ============================================================
# 20. SPLIT PAR CANDIDAT
# ============================================================

print_section("13. Séparation train / validation / test")

# Important :
#
# Un même candidat possède plusieurs lignes :
#
# candidat + filière 1
# candidat + filière 2
# ...
#
# Il faut donc éviter qu'un même candidat apparaisse
# simultanément dans train et test.
#
# Sinon le modèle pourrait apprendre indirectement son profil.

groups = data_ml.index

if "candidat_id" in data.columns:

    groups = data.loc[
        data_ml.index,
        "candidat_id"
    ]


# ------------------------------------------------------------
# Train = 70 %
# Temp = 30 %
# ------------------------------------------------------------

gss_1 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.30,
    random_state=42
)

train_idx, temp_idx = next(
    gss_1.split(
        X,
        y,
        groups=groups
    )
)


X_train = X.iloc[train_idx].copy()
X_temp = X.iloc[temp_idx].copy()

y_train = y.iloc[train_idx].copy()
y_temp = y.iloc[temp_idx].copy()

groups_temp = groups.iloc[temp_idx]


# ------------------------------------------------------------
# Validation = 15 %
# Test = 15 %
# ------------------------------------------------------------

gss_2 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=42
)

val_idx, test_idx = next(
    gss_2.split(
        X_temp,
        y_temp,
        groups=groups_temp
    )
)

X_validation = X_temp.iloc[val_idx].copy()
X_test = X_temp.iloc[test_idx].copy()

y_validation = y_temp.iloc[val_idx].copy()
y_test = y_temp.iloc[test_idx].copy()


print(f"Train      : {len(X_train)} lignes")
print(f"Validation : {len(X_validation)} lignes")
print(f"Test       : {len(X_test)} lignes")


# ============================================================
# 21. SAUVEGARDE DES DATASETS
# ============================================================

print_section("14. Sauvegarde")

X_train.to_csv(
    OUTPUT_DIR / "X_train.csv",
    index=False
)

X_validation.to_csv(
    OUTPUT_DIR / "X_validation.csv",
    index=False
)

X_test.to_csv(
    OUTPUT_DIR / "X_test.csv",
    index=False
)

y_train.to_csv(
    OUTPUT_DIR / "y_train.csv",
    index=False
)

y_validation.to_csv(
    OUTPUT_DIR / "y_validation.csv",
    index=False
)

y_test.to_csv(
    OUTPUT_DIR / "y_test.csv",
    index=False
)

data_ml.to_csv(
    OUTPUT_DIR / "ml_dataset.csv",
    index=False
)


# ============================================================
# 22. SAUVEGARDE DES FEATURES
# ============================================================

feature_columns = list(X.columns)

with open(
    OUTPUT_DIR / "feature_columns.txt",
    "w",
    encoding="utf-8"
) as f:

    for column in feature_columns:
        f.write(column + "\n")


# ============================================================
# 23. RAPPORT DE PRÉPROCESSING
# ============================================================

print_section("15. Génération du rapport")

report = []

report.append("# ORIENT'IA — Rapport de préprocessing\n")

report.append(
    "## 1. Objectif\n\n"
    "Préparer les données synthétiques pour l'entraînement "
    "du système de recommandation de filières.\n"
)

report.append(
    "## 2. Problème ML\n\n"
    "Le problème est formulé comme une recommandation "
    "candidat → filière.\n"
)

report.append(
    "Chaque ligne représente une paire candidat-filière.\n"
)

report.append(
    "## 3. Cible\n\n"
    "`target = est_recommandee`\n\n"
)

report.append(
    "La cible est encodée :\n\n"
    "- Oui → 1\n"
    "- Non → 0\n"
)

report.append(
    "## 4. Prévention de la fuite de données\n\n"
)

report.append(
    "Les variables suivantes ont été exclues du modèle car "
    "elles peuvent être directement liées à la génération "
    "de la recommandation :\n\n"
)

for column in existing_drop_columns:
    report.append(f"- `{column}`\n")


report.append(
    "\n## 5. Feature engineering\n\n"
)

engineered_features = [
    "nombre_competences",
    "nombre_matieres_fortes",
    "nombre_matieres_faibles",
    "nombre_centres_interet",
]

for feature in engineered_features:
    if feature in X.columns:
        report.append(f"- `{feature}`\n")


report.append(
    "\n## 6. Séparation des données\n\n"
)

report.append(
    f"- Train : {len(X_train)} lignes\n"
    f"- Validation : {len(X_validation)} lignes\n"
    f"- Test : {len(X_test)} lignes\n"
)

report.append(
    "\nLa séparation est effectuée par groupe de candidat afin "
    "d'éviter qu'un même candidat apparaisse dans plusieurs "
    "ensembles.\n"
)

report.append(
    "\n## 7. Features finales\n\n"
)

for column in feature_columns:
    report.append(f"- `{column}`\n")


report.append(
    "\n## 8. Fichiers produits\n\n"
)

output_files = [
    "ml_dataset.csv",
    "X_train.csv",
    "X_validation.csv",
    "X_test.csv",
    "y_train.csv",
    "y_validation.csv",
    "y_test.csv",
    "feature_columns.txt",
    "preprocessing_report.md",
]

for file in output_files:
    report.append(f"- `{file}`\n")


with open(
    OUTPUT_DIR / "preprocessing_report.md",
    "w",
    encoding="utf-8"
) as f:

    f.writelines(report)


# ============================================================
# 24. RÉSUMÉ FINAL
# ============================================================

print_section("PRÉPROCESSING TERMINÉ")

print(f"Dataset ML       : {len(data_ml)} lignes")
print(f"Nombre de features: {len(feature_columns)}")

print("\nTrain :")
print(f"  X : {X_train.shape}")
print(f"  y : {y_train.shape}")

print("\nValidation :")
print(f"  X : {X_validation.shape}")
print(f"  y : {y_validation.shape}")

print("\nTest :")
print(f"  X : {X_test.shape}")
print(f"  y : {y_test.shape}")

print("\nFichiers générés dans :")
print(OUTPUT_DIR)

print("\n[OK] Étape 02_preprocessing terminée.")