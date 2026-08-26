#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ORIENT'IA
07_inference.py

Inférence et recommandation de filières.

Objectif
--------
Utiliser le meilleur modèle sélectionné à l'étape 06 pour
produire un classement de filières pour un candidat.

Principe
--------
Entrée :

    candidat
        +
    ensemble des filières disponibles

Sortie :

    Top-K des filières recommandées

Modèle utilisé :

    ml/models/best_model.joblib

Données utilisées :

    data/synthetic/profils_etudiants_synthetiques.csv
    data/synthetic/candidat_filiere.csv
    data/synthetic/formations_etablissement.csv

Sorties :

    reports/ml/inference_predictions.csv
    reports/ml/inference_report.md
"""

from pathlib import Path
import sys
import warnings

import joblib
import numpy as np
import pandas as pd


warnings.filterwarnings("ignore")


# ============================================================
# 1. CONFIGURATION
# ============================================================

# Fichier :
#
# orient-ia/ml/notebooks/07_inference.py
#
# parents[0] = ml/notebooks
# parents[1] = ml
# parents[2] = orient-ia

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "synthetic"

MODELS_DIR = PROJECT_ROOT / "ml" / "models"

REPORTS_DIR = PROJECT_ROOT / "reports" / "ml"

MODEL_PATH = (
    MODELS_DIR / "best_model.joblib"
)

STUDENT_FILE = (
    DATA_DIR /
    "profils_etudiants_synthetiques.csv"
)

CANDIDATE_FILE = (
    DATA_DIR /
    "candidat_filiere.csv"
)

FORMATION_FILE = (
    DATA_DIR /
    "formations_etablissement.csv"
)

OUTPUT_PREDICTIONS = (
    REPORTS_DIR /
    "inference_predictions.csv"
)

OUTPUT_REPORT = (
    REPORTS_DIR /
    "inference_report.md"
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Nombre de recommandations retournées
TOP_K = 5


# ============================================================
# 2. UTILITAIRES
# ============================================================

def print_section(title):
    """Affiche une section lisible."""

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def check_file(path):
    """Vérifie qu'un fichier existe."""

    if not path.exists():

        raise FileNotFoundError(
            f"""
Fichier introuvable :

{path}
"""
        )


def normalize_text(value):
    """Normalise une valeur textuelle."""

    if pd.isna(value):
        return ""

    return str(value).strip()


def split_multivalue(value):
    """
    Transforme :

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
# 3. CHARGEMENT DU MODÈLE
# ============================================================

print_section(
    "ORIENT'IA — INFERENCE"
)

print(
    "Projet :",
    PROJECT_ROOT
)


print_section(
    "1. Vérification des fichiers"
)

check_file(
    MODEL_PATH
)

check_file(
    STUDENT_FILE
)

check_file(
    CANDIDATE_FILE
)

check_file(
    FORMATION_FILE
)


print(
    "[OK] Tous les fichiers sont disponibles."
)


# ============================================================
# 4. CHARGEMENT DU MODÈLE
# ============================================================

print_section(
    "2. Chargement du modèle"
)

try:

    model = joblib.load(
        MODEL_PATH
    )

except Exception as exc:

    raise RuntimeError(
        f"""
Impossible de charger :

{MODEL_PATH}

Erreur :
{exc}
"""
    )


print(
    "Modèle chargé :",
    MODEL_PATH.name
)

print(
    "Type :",
    type(model).__name__
)


# ============================================================
# 5. CHARGEMENT DES DONNÉES
# ============================================================

print_section(
    "3. Chargement des données"
)

students = pd.read_csv(
    STUDENT_FILE
)

candidate_filiere = pd.read_csv(
    CANDIDATE_FILE
)

formations = pd.read_csv(
    FORMATION_FILE
)


students.columns = (
    students.columns
    .str.strip()
)

candidate_filiere.columns = (
    candidate_filiere.columns
    .str.strip()
)

formations.columns = (
    formations.columns
    .str.strip()
)


print(
    "Profils étudiants :",
    students.shape
)

print(
    "Candidat-filière :",
    candidate_filiere.shape
)

print(
    "Formations :",
    formations.shape
)


# ============================================================
# 6. VÉRIFICATION DES IDENTIFIANTS
# ============================================================

print_section(
    "4. Vérification des identifiants"
)


required_student_columns = [
    "student_id"
]

required_candidate_columns = [
    "candidat_id",
    "filiere_code"
]

required_formation_columns = [
    "code_filiere"
]


for column in required_student_columns:

    if column not in students.columns:

        raise ValueError(
            f"Colonne absente des profils : {column}"
        )


for column in required_candidate_columns:

    if column not in candidate_filiere.columns:

        raise ValueError(
            f"Colonne absente de candidat_filiere : {column}"
        )


for column in required_formation_columns:

    if column not in formations.columns:

        raise ValueError(
            f"Colonne absente de formations : {column}"
        )


# ============================================================
# 7. NORMALISATION DES IDENTIFIANTS
# ============================================================

students["student_id"] = (
    students["student_id"]
    .astype(str)
    .str.strip()
)

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
# 8. CHOIX DU CANDIDAT
# ============================================================

print_section(
    "5. Sélection du candidat"
)


if len(sys.argv) > 1:

    candidate_id = str(
        sys.argv[1]
    ).strip()

else:

    candidate_id = (
        students["student_id"]
        .iloc[0]
    )


print(
    "Candidat sélectionné :",
    candidate_id
)


student = students[
    students["student_id"] == candidate_id
].copy()


if student.empty:

    raise ValueError(
        f"""
Candidat introuvable :

{candidate_id}

Exemple :

python ml/notebooks/07_inference.py candidat_0001
"""
    )


student = student.iloc[0]


# ============================================================
# 9. CONSTRUCTION DES CANDIDATURES POSSIBLES
# ============================================================

print_section(
    "6. Construction des possibilités"
)


# Un candidat est évalué contre toutes les filières
# disponibles dans candidat_filiere.

candidate_rows = candidate_filiere[
    candidate_filiere["candidat_id"] == candidate_id
].copy()


if candidate_rows.empty:

    raise ValueError(
        f"""
Aucune filière associée au candidat :

{candidate_id}
"""
    )


print(
    "Nombre de filières candidates :",
    len(candidate_rows)
)


# ============================================================
# 10. JOINTURE AVEC LE PROFIL
# ============================================================

student_df = student.to_frame().T


student_df = student_df.rename(
    columns={
        "student_id": "candidat_id"
    }
)


inference_data = candidate_rows.merge(
    student_df,
    on="candidat_id",
    how="left",
    suffixes=("_cf", "_student")
)


# ============================================================
# 11. AJOUT DES INFORMATIONS FILIÈRE
# ============================================================

formation_columns = [
    "code_filiere",
    "nom_complet",
    "parcours_id",
    "parcours_nom",
    "secteur_professionnel",
]


available_columns = [
    column
    for column in formation_columns
    if column in formations.columns
]


formations_small = formations[
    available_columns
].copy()


formations_small = formations_small.rename(
    columns={
        "code_filiere": "filiere_code",
        "nom_complet": "filiere_nom",
        "parcours_id": "filiere_parcours_id",
        "parcours_nom": "filiere_parcours_nom",
        "secteur_professionnel": "filiere_secteur",
    }
)


inference_data = inference_data.merge(
    formations_small,
    on="filiere_code",
    how="left"
)


# ============================================================
# 12. FEATURE ENGINEERING
# ============================================================

print_section(
    "7. Feature engineering"
)


if "age" in inference_data.columns:

    inference_data["age"] = pd.to_numeric(
        inference_data["age"],
        errors="coerce"
    )


if "moyenne_generale" in inference_data.columns:

    inference_data["moyenne_generale"] = pd.to_numeric(
        inference_data["moyenne_generale"],
        errors="coerce"
    )


if "competences" in inference_data.columns:

    inference_data["nombre_competences"] = (
        inference_data["competences"]
        .apply(
            lambda x:
            len(split_multivalue(x))
        )
    )


if "matieres_fortes" in inference_data.columns:

    inference_data["nombre_matieres_fortes"] = (
        inference_data["matieres_fortes"]
        .apply(
            lambda x:
            len(split_multivalue(x))
        )
    )


if "matieres_faibles" in inference_data.columns:

    inference_data["nombre_matieres_faibles"] = (
        inference_data["matieres_faibles"]
        .apply(
            lambda x:
            len(split_multivalue(x))
        )
    )


if "centres_interet" in inference_data.columns:

    inference_data["nombre_centres_interet"] = (
        inference_data["centres_interet"]
        .apply(
            lambda x:
            len(split_multivalue(x))
        )
    )


# ============================================================
# 13. SUPPRESSION DES COLONNES INUTILES
# ============================================================

DROP_COLUMNS = [

    "nom_complet",
    "nom_complet_student",

    "est_recommandee",

    "score_compatibilite",

    "score_compatibilite_cf",

    "est_admissible",

    "filiere_recommandee",

    "filiere_compatible",

    "justification",

    "candidat_id",

    "student_id",

    "target",

]


existing_drop = [
    column
    for column in DROP_COLUMNS
    if column in inference_data.columns
]


inference_features = inference_data.drop(
    columns=existing_drop
)


# ============================================================
# 14. SUPPRESSION DES TEXTES COMPLEXES
# ============================================================

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
    column
    for column in COMPLEX_TEXT_COLUMNS
    if column in inference_features.columns
]


inference_features = inference_features.drop(
    columns=complex_existing
)


# ============================================================
# 15. SUPPRESSION DES COLONNES REDONDANTES
# ============================================================

REDUNDANT_COLUMNS = [

    "type_profil",
    "profile_id",
    "professional_id",

]


redundant_existing = [
    column
    for column in REDUNDANT_COLUMNS
    if column in inference_features.columns
]


inference_features = inference_features.drop(
    columns=redundant_existing
)


# ============================================================
# 16. ALIGNEMENT AVEC LES FEATURES DU MODÈLE
# ============================================================

print_section(
    "8. Alignement avec le modèle"
)


if hasattr(model, "feature_names_in_"):

    expected_features = list(
        model.feature_names_in_
    )

elif hasattr(
    model,
    "named_steps"
):

    expected_features = []

    for step in model.named_steps.values():

        if hasattr(
            step,
            "feature_names_in_"
        ):

            expected_features = list(
                step.feature_names_in_
            )

            break

else:

    expected_features = []


if expected_features:

    print(
        "Features attendues :",
        len(expected_features)
    )


    missing_features = [
        column
        for column in expected_features
        if column not in inference_features.columns
    ]


    extra_features = [
        column
        for column in inference_features.columns
        if column not in expected_features
    ]


    if missing_features:

        raise ValueError(
            f"""
Features manquantes :

{missing_features}

Le modèle et le preprocessing ne sont
probablement pas synchronisés.
"""
        )


    inference_features = (
        inference_features[
            expected_features
        ]
    )


print(
    "Features utilisées :",
    inference_features.shape[1]
)


# ============================================================
# 17. PRÉDICTION
# ============================================================

print_section(
    "9. Prédiction"
)


try:

    probabilities = (
        model.predict_proba(
            inference_features
        )[:, 1]
    )

except Exception as exc:

    raise RuntimeError(
        f"""
Impossible de générer les prédictions.

Erreur :
{exc}

Vérifie que 02_preprocessing.py,
03_baseline.py, 04_train_models.py
et 06_model_selection.py ont été exécutés
dans cet ordre.
"""
    )


inference_data[
    "score_recommandation"
] = probabilities


# ============================================================
# 18. CLASSEMENT
# ============================================================

print_section(
    "10. Classement des filières"
)


inference_data = inference_data.sort_values(
    by="score_recommandation",
    ascending=False
).reset_index(
    drop=True
)


inference_data[
    "rang"
] = (
    inference_data.index + 1
)


# ============================================================
# 19. TOP-K
# ============================================================

top_k = inference_data.head(
    TOP_K
).copy()


# ============================================================
# 20. AFFICHAGE
# ============================================================

print_section(
    f"11. TOP {TOP_K} RECOMMANDATIONS"
)


display_columns = [
    "rang",
    "filiere_code",
]


for column in [
    "filiere_nom",
    "filiere_parcours_nom",
    "filiere_secteur",
]:

    if column in top_k.columns:

        display_columns.append(
            column
        )


display_columns.append(
    "score_recommandation"
)


print()

print(
    top_k[
        display_columns
    ].to_string(
        index=False
    )
)


# ============================================================
# 21. SAUVEGARDE DES PRÉDICTIONS
# ============================================================

print_section(
    "12. Sauvegarde des prédictions"
)


output_columns = [
    "rang",
    "candidat_id",
    "filiere_code",
]


for column in [
    "filiere_nom",
    "filiere_parcours_id",
    "filiere_parcours_nom",
    "filiere_secteur",
]:

    if column in inference_data.columns:

        output_columns.append(
            column
        )


output_columns.append(
    "score_recommandation"
)


predictions_output = inference_data[
    output_columns
].copy()


predictions_output.to_csv(
    OUTPUT_PREDICTIONS,
    index=False
)


print(
    "Prédictions sauvegardées :"
)

print(
    OUTPUT_PREDICTIONS
)


# ============================================================
# 22. RAPPORT MARKDOWN
# ============================================================

print_section(
    "13. Génération du rapport"
)


best_score = float(
    top_k[
        "score_recommandation"
    ].iloc[0]
)


report = f"""# ORIENT'IA — Rapport d'inférence

## 1. Objectif

Produire un classement des filières les plus adaptées
à un candidat à partir du modèle ML sélectionné.

## 2. Modèle

Modèle utilisé :

`best_model.joblib`

## 3. Candidat

Identifiant :

`{candidate_id}`

## 4. Nombre de filières évaluées

{len(inference_data)}

## 5. Nombre de recommandations

Top-{TOP_K}

## 6. Résultats

| Rang | Filière | Score |
|---:|---|---:|
"""


for _, row in top_k.iterrows():

    filiere_code = row[
        "filiere_code"
    ]

    score = float(
        row[
            "score_recommandation"
        ]
    )

    if "filiere_nom" in row.index:

        filiere_name = row[
            "filiere_nom"
        ]

    else:

        filiere_name = ""


    report += (
        f"| {int(row['rang'])} "
        f"| {filiere_name} "
        f"({filiere_code}) "
        f"| {score:.4f} |\n"
    )


report += f"""

## 7. Meilleure recommandation

La filière classée première possède un score de :

**{best_score:.4f}**

## 8. Interprétation

Le score représente la probabilité estimée par le modèle
que la paire candidat-filière corresponde à la classe
`Recommandée`.

Les filières sont ensuite classées par ordre décroissant
de ce score.

## 9. Fichier généré

`reports/ml/inference_predictions.csv`

## 10. Prochaine étape

Intégrer cette fonction d'inférence dans le backend/API
d'ORIENT'IA afin de permettre à l'application de recevoir
un profil candidat et de retourner dynamiquement ses
recommandations.
"""


with open(
    OUTPUT_REPORT,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        report
    )


print(
    "Rapport sauvegardé :"
)

print(
    OUTPUT_REPORT
)


# ============================================================
# 23. RÉSUMÉ FINAL
# ============================================================

print_section(
    "INFÉRENCE TERMINÉE"
)

print(
    f"Candidat : {candidate_id}"
)

print(
    f"Filières évaluées : {len(inference_data)}"
)

print(
    f"Top-K : {TOP_K}"
)

print()

print(
    "Meilleure recommandation :"
)

print(
    f"  {top_k.iloc[0]['filiere_code']}"
)

print(
    f"  Score : {best_score:.4f}"
)

print()

print(
    "Fichiers générés :"
)

print(
    f"  ✓ {OUTPUT_PREDICTIONS}"
)

print(
    f"  ✓ {OUTPUT_REPORT}"
)

print()

print(
    "[OK] Étape 07 terminée avec succès."
)