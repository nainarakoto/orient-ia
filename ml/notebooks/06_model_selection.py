#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ORIENT'IA
06_model_selection.py

Sélection automatique du meilleur modèle ML.

Objectif
--------
Comparer les modèles entraînés à partir des métriques de ranking
et sélectionner le meilleur modèle pour le système de recommandation
candidat → filière.

Entrée principale
------------------
reports/ml/ranking_metrics.csv

Entrées secondaires
-------------------
ml/models/*.joblib

Sorties
-------
reports/ml/model_selection_report.md
reports/ml/model_comparison.csv
reports/ml/model_selection.png

ml/models/
└── best_model.joblib

Critère principal
-----------------
NDCG@5

Critères secondaires
--------------------
Recall@5
Precision@5
HitRate@5

Pourquoi NDCG@5 ?
-----------------
Le système ORIENT'IA doit classer les filières recommandées.

NDCG@5 mesure donc la qualité du classement des 5 premières
filières proposées au candidat.
"""

from pathlib import Path
import shutil
import warnings

import joblib
import pandas as pd
import matplotlib.pyplot as plt


warnings.filterwarnings("ignore")


# ============================================================
# 1. CONFIGURATION
# ============================================================

# Fichier :
# orient-ia/ml/notebooks/06_model_selection.py
#
# parents[0] = ml/notebooks
# parents[1] = ml
# parents[2] = orient-ia

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "ml" / "models"
REPORTS_DIR = PROJECT_ROOT / "reports" / "ml"

RANKING_METRICS_PATH = (
    REPORTS_DIR / "ranking_metrics.csv"
)

OUTPUT_COMPARISON_PATH = (
    REPORTS_DIR / "model_comparison.csv"
)

OUTPUT_REPORT_PATH = (
    REPORTS_DIR / "model_selection_report.md"
)

OUTPUT_PLOT_PATH = (
    REPORTS_DIR / "model_selection.png"
)

BEST_MODEL_PATH = (
    MODELS_DIR / "best_model.joblib"
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. UTILITAIRES
# ============================================================

def print_section(title):
    """Affiche une section lisible dans le terminal."""

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

Vérifie que 05_ranking_evaluation.py
a bien été exécuté.
"""
        )


def find_column(df, candidates):
    """
    Trouve une colonne parmi plusieurs noms possibles.
    """

    for column in candidates:

        if column in df.columns:
            return column

    return None


# ============================================================
# 3. DÉBUT
# ============================================================

print_section(
    "ORIENT'IA — SÉLECTION DU MEILLEUR MODÈLE"
)

print(
    "Projet :",
    PROJECT_ROOT
)


# ============================================================
# 4. VÉRIFICATION DES FICHIERS
# ============================================================

print_section(
    "1. Vérification des fichiers"
)

check_file(
    RANKING_METRICS_PATH
)

print(
    "[OK] ranking_metrics.csv trouvé"
)


# ============================================================
# 5. CHARGEMENT DES MÉTRIQUES
# ============================================================

print_section(
    "2. Chargement des métriques"
)

metrics = pd.read_csv(
    RANKING_METRICS_PATH
)

print(
    "Shape :",
    metrics.shape
)

print()
print(
    "Colonnes :"
)

for column in metrics.columns:

    print(
        f"  - {column}"
    )


if metrics.empty:

    raise RuntimeError(
        """
Le fichier ranking_metrics.csv est vide.

Impossible de sélectionner un modèle.
"""
    )


# ============================================================
# 6. IDENTIFICATION DES COLONNES
# ============================================================

print_section(
    "3. Identification des métriques"
)


model_column = find_column(
    metrics,
    [
        "model",
        "model_name",
        "modele",
        "model_id",
    ]
)

if model_column is None:

    raise ValueError(
        f"""
Impossible d'identifier la colonne du modèle.

Colonnes disponibles :

{list(metrics.columns)}
"""
    )


ndcg_column = find_column(
    metrics,
    [
        "ndcg@5",
        "ndcg_5",
        "ndcg_at_5",
        "NDCG@5",
        "NDCG_5",
        "ndcg5",
    ]
)


if ndcg_column is None:

    raise ValueError(
        f"""
Impossible de trouver la métrique NDCG@5.

Colonnes disponibles :

{list(metrics.columns)}
"""
    )


recall_column = find_column(
    metrics,
    [
        "recall@5",
        "recall_5",
        "recall_at_5",
        "Recall@5",
    ]
)


precision_column = find_column(
    metrics,
    [
        "precision@5",
        "precision_5",
        "precision_at_5",
        "Precision@5",
    ]
)


hit_rate_column = find_column(
    metrics,
    [
        "hit_rate@5",
        "hitrate@5",
        "hit_rate_5",
        "HitRate@5",
        "hit@5",
    ]
)


print(
    "Modèle     :",
    model_column
)

print(
    "NDCG@5     :",
    ndcg_column
)

print(
    "Recall@5   :",
    recall_column
)

print(
    "Precision@5:",
    precision_column
)

print(
    "HitRate@5  :",
    hit_rate_column
)


# ============================================================
# 7. NETTOYAGE DES DONNÉES
# ============================================================

print_section(
    "4. Nettoyage des métriques"
)

comparison = metrics.copy()


numeric_columns = [
    column
    for column in [
        ndcg_column,
        recall_column,
        precision_column,
        hit_rate_column,
    ]
    if column is not None
]


for column in numeric_columns:

    comparison[column] = pd.to_numeric(
        comparison[column],
        errors="coerce"
    )


comparison = comparison.dropna(
    subset=[
        ndcg_column
    ]
)


if comparison.empty:

    raise RuntimeError(
        """
Aucun résultat valide après nettoyage.

Impossible de sélectionner un modèle.
"""
    )


# ============================================================
# 8. CLASSEMENT DES MODÈLES
# ============================================================

print_section(
    "5. Classement des modèles"
)


sort_columns = [
    ndcg_column
]


ascending_values = [
    False
]


if recall_column is not None:

    sort_columns.append(
        recall_column
    )

    ascending_values.append(
        False
    )


if precision_column is not None:

    sort_columns.append(
        precision_column
    )

    ascending_values.append(
        False
    )


if hit_rate_column is not None:

    sort_columns.append(
        hit_rate_column
    )

    ascending_values.append(
        False
    )


comparison = comparison.sort_values(
    by=sort_columns,
    ascending=ascending_values
).reset_index(
    drop=True
)


comparison[
    "rank"
] = comparison.index + 1


print()

print(
    comparison[
        [
            "rank",
            model_column,
            ndcg_column,
        ]
    ].to_string(
        index=False
    )
)


# ============================================================
# 9. SÉLECTION DU MEILLEUR MODÈLE
# ============================================================

print_section(
    "6. Sélection du meilleur modèle"
)


best_row = comparison.iloc[0]

best_model_name = str(
    best_row[model_column]
)

best_ndcg = float(
    best_row[ndcg_column]
)


print(
    "Meilleur modèle :",
    best_model_name
)

print(
    f"NDCG@5 : {best_ndcg:.4f}"
)


# ============================================================
# 10. RECHERCHE DU FICHIER JOBLIB
# ============================================================

print_section(
    "7. Recherche du modèle"
)


model_files = list(
    MODELS_DIR.glob("*.joblib")
)


print(
    f"{len(model_files)} modèle(s) trouvé(s)."
)


for path in model_files:

    print(
        f"  - {path.name}"
    )


def normalize_model_name(name):
    """
    Normalise un nom pour faciliter la correspondance
    entre le nom présent dans ranking_metrics.csv
    et le fichier .joblib.
    """

    name = str(name).lower().strip()

    name = name.replace(
        ".joblib",
        ""
    )

    name = name.replace(
        " ",
        "_"
    )

    name = name.replace(
        "-",
        "_"
    )

    return name


best_normalized = normalize_model_name(
    best_model_name
)


selected_model_path = None


# ------------------------------------------------------------
# Correspondance exacte
# ------------------------------------------------------------

for model_path in model_files:

    normalized_file = normalize_model_name(
        model_path.stem
    )

    if normalized_file == best_normalized:

        selected_model_path = model_path

        break


# ------------------------------------------------------------
# Correspondance partielle
# ------------------------------------------------------------

if selected_model_path is None:

    for model_path in model_files:

        normalized_file = normalize_model_name(
            model_path.stem
        )

        if (
            best_normalized in normalized_file
            or normalized_file in best_normalized
        ):

            selected_model_path = model_path

            break


# ------------------------------------------------------------
# Cas particulier baseline
# ------------------------------------------------------------

if selected_model_path is None:

    if (
        "logistic" in best_normalized
        or "baseline" in best_normalized
    ):

        baseline_path = (
            MODELS_DIR /
            "baseline_logistic_regression.joblib"
        )

        if baseline_path.exists():

            selected_model_path = (
                baseline_path
            )


if selected_model_path is None:

    raise FileNotFoundError(
        f"""
Le meilleur modèle est :

{best_model_name}

Mais aucun fichier .joblib correspondant
n'a été trouvé dans :

{MODELS_DIR}

Fichiers disponibles :

{[p.name for p in model_files]}
"""
    )


print(
    "Modèle sélectionné :",
    selected_model_path
)


# ============================================================
# 11. VÉRIFICATION DU MODÈLE
# ============================================================

print_section(
    "8. Vérification du modèle"
)


try:

    selected_model = joblib.load(
        selected_model_path
    )

except Exception as exc:

    raise RuntimeError(
        f"""
Impossible de charger le modèle :

{selected_model_path}

Erreur :
{exc}
"""
    )


print(
    "[OK] Modèle chargé avec succès."
)

print(
    "Type :",
    type(selected_model).__name__
)


# ============================================================
# 12. SAUVEGARDE DU MEILLEUR MODÈLE
# ============================================================

print_section(
    "9. Sauvegarde du meilleur modèle"
)


joblib.dump(
    selected_model,
    BEST_MODEL_PATH
)


print(
    "Meilleur modèle sauvegardé :"
)

print(
    BEST_MODEL_PATH
)


# ============================================================
# 13. SAUVEGARDE DU TABLEAU COMPARATIF
# ============================================================

print_section(
    "10. Sauvegarde de la comparaison"
)


comparison.to_csv(
    OUTPUT_COMPARISON_PATH,
    index=False
)


print(
    "Comparaison sauvegardée :"
)

print(
    OUTPUT_COMPARISON_PATH
)


# ============================================================
# 14. GRAPHIQUE DE COMPARAISON
# ============================================================

print_section(
    "11. Génération du graphique"
)


plot_data = comparison.copy()

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    plot_data[model_column].astype(str),
    plot_data[ndcg_column]
)

plt.xlabel(
    "Modèle"
)

plt.ylabel(
    "NDCG@5"
)

plt.title(
    "Comparaison des modèles — NDCG@5"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_PLOT_PATH,
    dpi=150
)

plt.close()


print(
    "Graphique sauvegardé :"
)

print(
    OUTPUT_PLOT_PATH
)


# ============================================================
# 15. RAPPORT MARKDOWN
# ============================================================

print_section(
    "12. Génération du rapport"
)


report = []

report.append(
    "# ORIENT'IA — Sélection du meilleur modèle\n\n"
)


report.append(
    "## 1. Objectif\n\n"
)

report.append(
    "Sélectionner automatiquement le meilleur modèle "
    "pour la recommandation candidat → filière.\n\n"
)


report.append(
    "## 2. Critère principal\n\n"
)

report.append(
    "**NDCG@5** a été utilisé comme critère principal.\n\n"
)

report.append(
    "NDCG@5 mesure la qualité du classement des cinq "
    "premières filières recommandées pour chaque candidat.\n\n"
)


report.append(
    "## 3. Critères secondaires\n\n"
)

if recall_column:

    report.append(
        "- Recall@5\n"
    )

if precision_column:

    report.append(
        "- Precision@5\n"
    )

if hit_rate_column:

    report.append(
        "- HitRate@5\n"
    )


report.append(
    "\n## 4. Classement des modèles\n\n"
)


table_columns = [
    "rank",
    model_column,
    ndcg_column,
]


if recall_column:

    table_columns.append(
        recall_column
    )

if precision_column:

    table_columns.append(
        precision_column
    )

if hit_rate_column:

    table_columns.append(
        hit_rate_column
    )


report.append(
    comparison[
        table_columns
    ].to_markdown(
        index=False
    )
)

report.append(
    "\n\n"
)


report.append(
    "## 5. Modèle sélectionné\n\n"
)

report.append(
    f"### {best_model_name}\n\n"
)

report.append(
    f"- NDCG@5 : **{best_ndcg:.4f}**\n"
)


if recall_column:

    report.append(
        f"- Recall@5 : "
        f"**{float(best_row[recall_column]):.4f}**\n"
    )


if precision_column:

    report.append(
        f"- Precision@5 : "
        f"**{float(best_row[precision_column]):.4f}**\n"
    )


if hit_rate_column:

    report.append(
        f"- HitRate@5 : "
        f"**{float(best_row[hit_rate_column]):.4f}**\n"
    )


report.append(
    "\n"
)


report.append(
    "## 6. Fichier du modèle\n\n"
)

report.append(
    f"`{selected_model_path.name}`\n\n"
)


report.append(
    "Le modèle sélectionné a été copié vers :\n\n"
)

report.append(
    "`ml/models/best_model.joblib`\n\n"
)


report.append(
    "## 7. Conclusion\n\n"
)

report.append(
    "Le modèle sélectionné constitue le modèle de référence "
    "pour la phase d'inférence et de recommandation.\n\n"
)


report.append(
    "## 8. Prochaine étape\n\n"
)

report.append(
    "Développer le module d'inférence permettant de recevoir "
    "le profil d'un candidat et de retourner les filières "
    "classées par score de recommandation.\n"
)


with open(
    OUTPUT_REPORT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "".join(report)
    )


print(
    "Rapport sauvegardé :"
)

print(
    OUTPUT_REPORT_PATH
)


# ============================================================
# 16. RÉSUMÉ FINAL
# ============================================================

print_section(
    "SÉLECTION DU MODÈLE TERMINÉE"
)

print(
    "Meilleur modèle :",
    best_model_name
)

print(
    f"NDCG@5 : {best_ndcg:.4f}"
)

print()
print(
    "Fichiers générés :"
)

print(
    f"  ✓ {BEST_MODEL_PATH}"
)

print(
    f"  ✓ {OUTPUT_COMPARISON_PATH}"
)

print(
    f"  ✓ {OUTPUT_REPORT_PATH}"
)

print(
    f"  ✓ {OUTPUT_PLOT_PATH}"
)

print()
print(
    "Prochaine étape :"
)


print()
print(
    "[OK] Étape 06 terminée avec succès."
)