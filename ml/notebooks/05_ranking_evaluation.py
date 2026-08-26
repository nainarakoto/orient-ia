#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ORIENT'IA
05_ranking_evaluation.py

Évaluation du ranking des recommandations candidat -> filière.

Objectif
--------
Évaluer si les modèles ML sont capables de classer correctement
les filières recommandées pour chaque candidat.

Entrées
-------
ml/preprocessing/ml_dataset.csv

Modèles
-------
ml/models/*.joblib

Sorties
-------
reports/ml/ranking_metrics.csv
reports/ml/ranking_report.md
reports/ml/ranking_comparison.png
reports/ml/ranking_predictions.csv

Métriques
---------
Precision@K
Recall@K
Hit Rate@K
NDCG@K

Important
---------
candidat_id n'est PAS une feature ML.
Il sert uniquement à regrouper les prédictions par candidat.

filiere_code sert uniquement à identifier la filière dans le ranking.
"""

from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import ndcg_score


warnings.filterwarnings("ignore")


# ============================================================
# 1. CONFIGURATION
# ============================================================

# Fichier :
# orient-ia/ml/notebooks/05_ranking_evaluation.py
#
# parents[0] = ml/notebooks
# parents[1] = ml
# parents[2] = orient-ia

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREPROCESSING_DIR = PROJECT_ROOT / "ml" / "preprocessing"
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
REPORTS_DIR = PROJECT_ROOT / "reports" / "ml"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATASET_PATH = PREPROCESSING_DIR / "ml_dataset.csv"

K_VALUES = [1, 3, 5]

print("PROJECT_ROOT :", PROJECT_ROOT)
print("DATASET      :", DATASET_PATH)
print("MODELS       :", MODELS_DIR)
print("REPORTS      :", REPORTS_DIR)


# ============================================================
# 2. AFFICHAGE
# ============================================================

def print_section(title):
    print()
    print("=" * 75)
    print(title)
    print("=" * 75)


# ============================================================
# 3. CHARGEMENT DATASET
# ============================================================

print_section("ORIENT'IA — RANKING EVALUATION")

print(f"Projet : {PROJECT_ROOT}")
print(f"Dataset : {DATASET_PATH}")


if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"""
Dataset introuvable :

{DATASET_PATH}

Exécute d'abord :

python ml/notebooks/02_preprocessing.py
"""
    )


df = pd.read_csv(DATASET_PATH)

print()
print(f"Dataset chargé : {df.shape}")


# ============================================================
# 4. VÉRIFICATION DES COLONNES
# ============================================================

print_section("1. Vérification des colonnes")

print("Colonnes disponibles :")

for column in df.columns:
    print(f"  - {column}")


# ------------------------------------------------------------
# Identification candidat
# ------------------------------------------------------------

candidate_candidates = [
    "candidat_id",
    "candidate_id",
    "student_id",
    "profile_id",
]

candidate_column = None

for column in candidate_candidates:
    if column in df.columns:
        candidate_column = column
        break


if candidate_column is None:

    raise ValueError(
        """
Impossible de trouver l'identifiant candidat.

Le dataset doit contenir :

candidat_id

Relance 02_preprocessing.py après avoir conservé
candidat_id dans ml_dataset.csv.
"""
    )


# ------------------------------------------------------------
# Identification filière
# ------------------------------------------------------------

filiere_candidates = [
    "filiere_code",
    "code_filiere",
    "filiere",
]


filiere_column = None

for column in filiere_candidates:

    if column in df.columns:

        filiere_column = column
        break


if filiere_column is None:

    raise ValueError(
        """
Impossible de trouver l'identifiant de filière.

Colonnes attendues :

filiere_code
code_filiere
ou
filiere
"""
    )


# ------------------------------------------------------------
# Identification cible
# ------------------------------------------------------------

target_candidates = [
    "target",
    "est_recommandee",
]


target_column = None

for column in target_candidates:

    if column in df.columns:

        target_column = column
        break


if target_column is None:

    raise ValueError(
        """
Impossible de trouver la cible.

Colonnes attendues :

target
ou
est_recommandee
"""
    )


print()
print(f"Candidat : {candidate_column}")
print(f"Filière  : {filiere_column}")
print(f"Cible    : {target_column}")


# ============================================================
# 5. NORMALISATION DE LA CIBLE
# ============================================================

print_section("2. Préparation de la cible")


def normalize_target(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip().lower()

    if value in [
        "1",
        "oui",
        "yes",
        "true",
    ]:
        return 1

    if value in [
        "0",
        "non",
        "no",
        "false",
    ]:
        return 0

    try:

        numeric = float(value)

        if numeric in [0, 1]:

            return int(numeric)

    except Exception:
        pass

    return np.nan


df["_ranking_target"] = (
    df[target_column]
    .apply(normalize_target)
)


unknown = df["_ranking_target"].isna().sum()


if unknown > 0:

    print(
        f"[ATTENTION] {unknown} lignes ont une cible invalide."
    )

    df = df.dropna(
        subset=["_ranking_target"]
    )


df["_ranking_target"] = (
    df["_ranking_target"]
    .astype(int)
)


print()
print("Distribution de la cible :")
print(
    df["_ranking_target"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 6. CONSTRUCTION DES FEATURES
# ============================================================

print_section("3. Construction des features")


# Colonnes utilisées uniquement pour le ranking
METADATA_COLUMNS = [
    candidate_column,
    filiere_column,
    target_column,
    "_ranking_target",
]


# Certaines colonnes ne doivent jamais être utilisées
# comme features ML.

LEAKAGE_COLUMNS = [
    "est_recommandee",
    "target",
    "filiere_recommandee",
    "justification",
    "score_compatibilite",
    "score_compatibilite_cf",
    "est_admissible",
]


# Identifiants / métadonnées
EXCLUDED_COLUMNS = (
    METADATA_COLUMNS
    + LEAKAGE_COLUMNS
)


feature_columns = [
    column
    for column in df.columns
    if column not in EXCLUDED_COLUMNS
]


# Retirer les colonnes entièrement vides
feature_columns = [
    column
    for column in feature_columns
    if not df[column].isna().all()
]


print()
print(f"Nombre de features : {len(feature_columns)}")

for column in feature_columns:
    print(f"  - {column}")


X = df[feature_columns].copy()


# ============================================================
# 7. CHARGEMENT DES MODÈLES
# ============================================================

print_section("4. Chargement des modèles")


if not MODELS_DIR.exists():

    raise FileNotFoundError(
        f"Répertoire modèles introuvable : {MODELS_DIR}"
    )


model_files = sorted(
    MODELS_DIR.glob("*.joblib")
)


if not model_files:

    raise FileNotFoundError(
        f"""
Aucun modèle .joblib trouvé dans :

{MODELS_DIR}

Exécute d'abord :

03_baseline.py
04_train_models.py
"""
    )


print()
print("Modèles trouvés :")

for model_file in model_files:
    print(f"  - {model_file.name}")


# ============================================================
# 8. FONCTION DE PRÉDICTION
# ============================================================

def generate_predictions(model, X):

    """
    Génère une probabilité de classe positive.

    Compatible avec :
        predict_proba
        decision_function
        predict
    """

    # --------------------------------------------------------
    # predict_proba
    # --------------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(X)

        probabilities = np.asarray(
            probabilities
        )

        if probabilities.ndim == 2:

            if probabilities.shape[1] >= 2:

                return probabilities[:, 1]

            if probabilities.shape[1] == 1:

                return probabilities[:, 0]

        return probabilities.ravel()


    # --------------------------------------------------------
    # decision_function
    # --------------------------------------------------------

    if hasattr(model, "decision_function"):

        scores = model.decision_function(X)

        scores = np.asarray(scores)

        if scores.ndim > 1:

            scores = scores[:, -1]

        # Transformation sigmoid
        probabilities = 1 / (
            1 + np.exp(-np.clip(scores, -500, 500))
        )

        return probabilities


    # --------------------------------------------------------
    # predict
    # --------------------------------------------------------

    if hasattr(model, "predict"):

        predictions = model.predict(X)

        return np.asarray(
            predictions,
            dtype=float
        )


    raise TypeError(
        "Le modèle ne possède ni predict_proba, "
        "ni decision_function, ni predict."
    )


# ============================================================
# 9. FONCTION RANKING
# ============================================================

def evaluate_ranking(
    ranking_df,
    score_column,
    target_column="_ranking_target",
):
    """
    Calcule les métriques ranking pour chaque candidat.
    """

    results = []


    for candidate_id, group in ranking_df.groupby(
        candidate_column
    ):

        group = group.copy()


        # ----------------------------------------------------
        # Trier par score décroissant
        # ----------------------------------------------------

        group = group.sort_values(
            score_column,
            ascending=False
        )


        relevance = (
            group[target_column]
            .astype(int)
            .values
        )


        # Nombre de filières réellement pertinentes
        total_relevant = relevance.sum()


        if total_relevant == 0:

            continue


        # ----------------------------------------------------
        # Évaluation pour chaque K
        # ----------------------------------------------------

        candidate_result = {
            candidate_column: candidate_id,
            "total_items": len(group),
            "relevant_items": int(total_relevant),
        }


        for k in K_VALUES:

            top_k = relevance[:k]


            # ------------------------------------------------
            # Precision@K
            # ------------------------------------------------

            precision_k = (
                top_k.sum() / k
            )


            # ------------------------------------------------
            # Recall@K
            # ------------------------------------------------

            recall_k = (
                top_k.sum() /
                total_relevant
            )


            # ------------------------------------------------
            # Hit Rate@K
            # ------------------------------------------------

            hit_rate_k = (
                1
                if top_k.sum() > 0
                else 0
            )


            # ------------------------------------------------
            # NDCG@K
            # ------------------------------------------------

            if len(relevance) > 1:

                ndcg_k = ndcg_score(
                    [relevance],
                    [group[score_column].values],
                    k=min(
                        k,
                        len(group)
                    )
                )

            else:

                ndcg_k = float(
                    relevance[0]
                )


            candidate_result[
                f"precision@{k}"
            ] = precision_k


            candidate_result[
                f"recall@{k}"
            ] = recall_k


            candidate_result[
                f"hit_rate@{k}"
            ] = hit_rate_k


            candidate_result[
                f"ndcg@{k}"
            ] = ndcg_k


        results.append(
            candidate_result
        )


    return pd.DataFrame(results)


# ============================================================
# 10. ÉVALUATION DES MODÈLES
# ============================================================

print_section("5. Évaluation des modèles")


all_predictions = []

ranking_results = []


for model_file in model_files:

    model_name = model_file.stem

    print()
    print("-" * 70)
    print(f"Modèle : {model_name}")
    print("-" * 70)


    try:

        model = joblib.load(
            model_file
        )

        print(
            f"Modèle chargé : {type(model).__name__}"
        )


    except Exception as exc:

        print(
            f"[ERREUR] Impossible de charger "
            f"{model_file.name}"
        )

        print(exc)

        continue


    # --------------------------------------------------------
    # Vérification des features attendues
    # --------------------------------------------------------

    try:

        if hasattr(
            model,
            "feature_names_in_"
        ):

            expected_features = list(
                model.feature_names_in_
            )

            missing_features = [
                c
                for c in expected_features
                if c not in X.columns
            ]

            if missing_features:

                print(
                    "[ERREUR] Features manquantes :"
                )

                for c in missing_features:
                    print(f"  - {c}")

                continue


            model_X = X[
                expected_features
            ]


        else:

            model_X = X


        # ----------------------------------------------------
        # Prédictions
        # ----------------------------------------------------

        scores = generate_predictions(
            model,
            model_X
        )


        if scores is None:

            print(
                "[ERREUR] Aucune prédiction."
            )

            continue


        scores = np.asarray(
            scores,
            dtype=float
        ).ravel()


        if len(scores) != len(df):

            print(
                "[ERREUR] Nombre de prédictions "
                "incorrect."
            )

            print(
                f"Predictions : {len(scores)}"
            )

            print(
                f"Dataset     : {len(df)}"
            )

            continue


        # ----------------------------------------------------
        # Dataset de ranking
        # ----------------------------------------------------

        prediction_df = pd.DataFrame(
            {
                candidate_column:
                    df[candidate_column].values,

                filiere_column:
                    df[filiere_column].values,

                "target":
                    df["_ranking_target"].values,

                "score":
                    scores,

                "model":
                    model_name,
            }
        )


        all_predictions.append(
            prediction_df
        )


        # ----------------------------------------------------
        # Ranking
        # ----------------------------------------------------

        ranking_df = evaluate_ranking(
            prediction_df,
            score_column="score",
            target_column="target",
        )


        if ranking_df.empty:

            print(
                "[ATTENTION] Aucun candidat "
                "évaluable."
            )

            continue


        ranking_df["model"] = model_name


        ranking_results.append(
            ranking_df
        )


        # ----------------------------------------------------
        # Résumé
        # ----------------------------------------------------

        print(
            f"Candidats évalués : "
            f"{len(ranking_df)}"
        )


        for k in K_VALUES:

            p = ranking_df[
                f"precision@{k}"
            ].mean()

            r = ranking_df[
                f"recall@{k}"
            ].mean()

            h = ranking_df[
                f"hit_rate@{k}"
            ].mean()

            n = ranking_df[
                f"ndcg@{k}"
            ].mean()


            print(
                f"@{k} | "
                f"Precision={p:.4f} | "
                f"Recall={r:.4f} | "
                f"HitRate={h:.4f} | "
                f"NDCG={n:.4f}"
            )


    except Exception as exc:

        print(
            f"[ERREUR] Échec du modèle "
            f"{model_name}"
        )

        print(
            f"{type(exc).__name__}: {exc}"
        )

        continue


# ============================================================
# 11. VÉRIFICATION DES PRÉDICTIONS
# ============================================================

print_section("6. Vérification des prédictions")


if not all_predictions:

    raise RuntimeError(
        """
Aucune prédiction n'a été générée.

Causes possibles :

1. Les modèles ne sont pas compatibles avec
   ml/preprocessing/ml_dataset.csv.

2. Les features ont changé après le preprocessing.

3. Les modèles ont été entraînés avant la modification
   de 02_preprocessing.py.

4. Les modèles .joblib doivent être recréés.

Solution recommandée :

    python ml/notebooks/02_preprocessing.py
    python ml/notebooks/03_baseline.py
    python ml/notebooks/04_train_models.py
    python ml/notebooks/05_ranking_evaluation.py
"""
    )


print(
    f"Nombre de modèles évalués : "
    f"{len(all_predictions)}"
)


# ============================================================
# 12. SAUVEGARDE DES PRÉDICTIONS
# ============================================================

print_section("7. Sauvegarde des prédictions")


predictions_df = pd.concat(
    all_predictions,
    ignore_index=True
)


predictions_path = (
    REPORTS_DIR /
    "ranking_predictions.csv"
)


predictions_df.to_csv(
    predictions_path,
    index=False
)


print(
    f"Prédictions : {predictions_path}"
)


# ============================================================
# 13. CONCATÉNATION DES RÉSULTATS
# ============================================================

ranking_df = pd.concat(
    ranking_results,
    ignore_index=True
)


# ============================================================
# 14. MÉTRIQUES MOYENNES
# ============================================================

print_section("8. Métriques ranking")


metric_rows = []


for model_name, group in ranking_df.groupby(
    "model"
):

    row = {
        "model": model_name,
        "candidates": len(group),
    }


    for k in K_VALUES:

        row[
            f"precision@{k}"
        ] = group[
            f"precision@{k}"
        ].mean()


        row[
            f"recall@{k}"
        ] = group[
            f"recall@{k}"
        ].mean()


        row[
            f"hit_rate@{k}"
        ] = group[
            f"hit_rate@{k}"
        ].mean()


        row[
            f"ndcg@{k}"
        ] = group[
            f"ndcg@{k}"
        ].mean()


    metric_rows.append(row)


metrics_df = pd.DataFrame(
    metric_rows
)


print(
    metrics_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# 15. SAUVEGARDE METRICS
# ============================================================

metrics_path = (
    REPORTS_DIR /
    "ranking_metrics.csv"
)


metrics_df.to_csv(
    metrics_path,
    index=False
)


print()
print(
    f"Métriques : {metrics_path}"
)


# ============================================================
# 16. GRAPHIQUE
# ============================================================

print_section("9. Génération du graphique")


plot_metric = "ndcg@5"


plt.figure(
    figsize=(10, 6)
)


plt.bar(
    metrics_df["model"],
    metrics_df[plot_metric]
)


plt.ylabel("NDCG@5")

plt.xlabel("Modèle")

plt.title(
    "Comparaison des modèles — NDCG@5"
)


plt.xticks(
    rotation=30,
    ha="right"
)


plt.tight_layout()


comparison_path = (
    REPORTS_DIR /
    "ranking_comparison.png"
)


plt.savefig(
    comparison_path,
    dpi=150
)


plt.close()


print(
    f"Graphique : {comparison_path}"
)


# ============================================================
# 17. RAPPORT MARKDOWN
# ============================================================

print_section("10. Génération du rapport")


report = []

report.append(
    "# ORIENT'IA — Rapport d'évaluation du ranking\n\n"
)


report.append(
    "## 1. Objectif\n\n"
)


report.append(
    "Évaluer la capacité des modèles à classer les filières "
    "pour chaque candidat.\n\n"
)


report.append(
    "Le problème est traité comme un problème de ranking :\n\n"
)


report.append(
    "```text\n"
    "Candidat\n"
    "   ↓\n"
    "Score de chaque filière\n"
    "   ↓\n"
    "Classement\n"
    "   ↓\n"
    "Top-K recommandations\n"
    "```\n\n"
)


report.append(
    "## 2. Identifiants\n\n"
)


report.append(
    f"- Identifiant candidat : `{candidate_column}`\n"
)


report.append(
    f"- Identifiant filière : `{filiere_column}`\n"
)


report.append(
    f"- Variable cible : `{target_column}`\n\n"
)


report.append(
    "L'identifiant candidat est utilisé uniquement pour "
    "regrouper les recommandations et n'est pas utilisé "
    "comme feature ML.\n\n"
)


report.append(
    "## 3. Modèles évalués\n\n"
)


for model_name in metrics_df["model"]:

    report.append(
        f"- `{model_name}`\n"
    )


report.append(
    "\n## 4. Métriques\n\n"
)


report.append(
    "- Precision@K\n"
    "- Recall@K\n"
    "- Hit Rate@K\n"
    "- NDCG@K\n\n"
)


report.append(
    "## 5. Résultats\n\n"
)


headers = [
    "Model",
    "Candidates",
]

for k in K_VALUES:

    headers.extend(
        [
            f"Precision@{k}",
            f"Recall@{k}",
            f"HitRate@{k}",
            f"NDCG@{k}",
        ]
    )


report.append(
    "| " +
    " | ".join(headers) +
    " |\n"
)


report.append(
    "|" +
    "|".join(
        ["---"] * len(headers)
    ) +
    "|\n"
)


for _, row in metrics_df.iterrows():

    values = [
        str(row["model"]),
        str(int(row["candidates"])),
    ]


    for k in K_VALUES:

        values.extend(
            [
                f"{row[f'precision@{k}']:.4f}",
                f"{row[f'recall@{k}']:.4f}",
                f"{row[f'hit_rate@{k}']:.4f}",
                f"{row[f'ndcg@{k}']:.4f}",
            ]
        )


    report.append(
        "| " +
        " | ".join(values) +
        " |\n"
    )


report.append(
    "\n## 6. Interprétation\n\n"
)


if not metrics_df.empty:

    best_row = metrics_df.loc[
        metrics_df["ndcg@5"].idxmax()
    ]

    report.append(
        f"Le meilleur modèle selon NDCG@5 est "
        f"`{best_row['model']}` avec un score de "
        f"**{best_row['ndcg@5']:.4f}**.\n\n"
    )


report.append(
    "NDCG@K mesure la qualité du classement en tenant "
    "compte de la position des filières pertinentes. "
    "Une filière pertinente placée en première position "
    "est donc mieux valorisée qu'une filière pertinente "
    "placée plus bas dans le classement.\n\n"
)


report.append(
    "## 7. Fichiers générés\n\n"
)


report.append(
    "- `ranking_metrics.csv`\n"
    "- `ranking_predictions.csv`\n"
    "- `ranking_comparison.png`\n"
    "- `ranking_report.md`\n"
)


report_path = (
    REPORTS_DIR /
    "ranking_report.md"
)


with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.writelines(report)


print(
    f"Rapport : {report_path}"
)


# ============================================================
# 18. RÉSUMÉ FINAL
# ============================================================

print_section("RANKING TERMINÉ")


print(
    f"Modèles évalués : "
    f"{len(metrics_df)}"
)


print(
    f"Candidats évalués : "
    f"{ranking_df[candidate_column].nunique()}"
)


print()
print("Fichiers générés :")

print(
    f"  ✓ {metrics_path}"
)

print(
    f"  ✓ {predictions_path}"
)

print(
    f"  ✓ {comparison_path}"
)

print(
    f"  ✓ {report_path}"
)


print()
print(
    "Évaluation ranking terminée avec succès."
)