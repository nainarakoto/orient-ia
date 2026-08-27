#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ORIENT'IA
03_baseline.py

Baseline ML pour le système de recommandation candidat -> filière.

Modèle :
    Logistic Regression

Objectif :
    Construire un modèle simple, interprétable et reproductible
    servant de référence pour les futurs modèles.

Entrées :
    ml/preprocessing/X_train.csv
    ml/preprocessing/X_validation.csv
    ml/preprocessing/X_test.csv
    ml/preprocessing/y_train.csv
    ml/preprocessing/y_validation.csv
    ml/preprocessing/y_test.csv

Sorties :
    reports/ml/baseline_metrics.csv
    reports/ml/baseline_report.md
    reports/ml/confusion_matrix_baseline.png
    reports/ml/roc_curve_baseline.png
    reports/ml/pr_curve_baseline.png
    ml/models/baseline_logistic_regression.joblib
"""

from pathlib import Path
import sys
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import matplotlib.pyplot as plt


warnings.filterwarnings("ignore")


# ============================================================
# 1. CONFIGURATION DES CHEMINS
# ============================================================

# ml/notebooks/03_baseline.py
# parents[0] = notebooks
# parents[1] = ml
# parents[2] = orientia
PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_DATA_DIR = PROJECT_ROOT / "ml" / "preprocessing"
ML_MODELS_DIR = PROJECT_ROOT / "ml" / "models"
REPORTS_DIR = PROJECT_ROOT / "reports" / "ml"

ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. FONCTIONS UTILITAIRES
# ============================================================

def print_section(title):
    """Affiche une section lisible dans le terminal."""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def load_csv(path):
    """Charge un fichier CSV et vérifie son existence."""
    if not path.exists():
        raise FileNotFoundError(
            f"\nFichier introuvable : {path}\n"
            f"Vérifie que 02_preprocessing.py a bien été exécuté."
        )

    df = pd.read_csv(path)

    print(f"Chargé : {path}")
    print(f"Shape   : {df.shape}")

    return df


def normalize_target(y):
    """
    Convertit la cible en 0/1.

    Accepte :
        Oui / Non
        1 / 0
        True / False
    """

    if isinstance(y, pd.DataFrame):
        y = y.iloc[:, 0]

    y = y.copy()

    if y.dtype == object:
        mapping = {
            "Oui": 1,
            "oui": 1,
            "OUI": 1,
            "Yes": 1,
            "yes": 1,
            "YES": 1,
            "True": 1,
            "true": 1,
            "TRUE": 1,
            "Non": 0,
            "non": 0,
            "NON": 0,
            "No": 0,
            "no": 0,
            "NO": 0,
            "False": 0,
            "false": 0,
            "FALSE": 0,
        }

        y = y.map(mapping)

    y = pd.to_numeric(y, errors="coerce")

    if y.isna().any():
        raise ValueError(
            "La variable cible contient des valeurs qui ne peuvent "
            "pas être converties en 0/1."
        )

    unique_values = sorted(y.unique())

    if not set(unique_values).issubset({0, 1}):
        raise ValueError(
            f"La cible doit contenir uniquement 0 et 1. "
            f"Valeurs trouvées : {unique_values}"
        )

    return y.astype(int)


def evaluate_classification(y_true, y_pred, y_proba):
    """Calcule les principales métriques de classification."""

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(
            y_true,
            y_pred,
            zero_division=0
        ),
        "recall": recall_score(
            y_true,
            y_pred,
            zero_division=0
        ),
        "f1": f1_score(
            y_true,
            y_pred,
            zero_division=0
        ),
    }

    # ROC-AUC nécessite les deux classes.
    if len(np.unique(y_true)) == 2:
        metrics["roc_auc"] = roc_auc_score(
            y_true,
            y_proba
        )

        metrics["pr_auc"] = average_precision_score(
            y_true,
            y_proba
        )
    else:
        metrics["roc_auc"] = np.nan
        metrics["pr_auc"] = np.nan

    return metrics


def save_confusion_matrix(y_true, y_pred, output_path):
    """Sauvegarde la matrice de confusion."""

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(6, 5))

    plt.imshow(cm)

    plt.title("Matrice de confusion — Baseline")
    plt.xlabel("Prédiction")
    plt.ylabel("Réalité")

    plt.xticks([0, 1], ["Non", "Oui"])
    plt.yticks([0, 1], ["Non", "Oui"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j,
                i,
                cm[i, j],
                ha="center",
                va="center"
            )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_roc_curve(y_true, y_proba, output_path):
    """Sauvegarde la courbe ROC."""

    if len(np.unique(y_true)) < 2:
        return

    fpr, tpr, _ = roc_curve(
        y_true,
        y_proba
    )

    auc = roc_auc_score(
        y_true,
        y_proba
    )

    plt.figure(figsize=(7, 5))

    plt.plot(
        fpr,
        tpr,
        label=f"Logistic Regression (AUC = {auc:.3f})"
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--"
    )

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")

    plt.title("Courbe ROC — Baseline")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=150
    )

    plt.close()


def save_pr_curve(y_true, y_proba, output_path):
    """Sauvegarde la courbe Precision-Recall."""

    if len(np.unique(y_true)) < 2:
        return

    precision, recall, _ = precision_recall_curve(
        y_true,
        y_proba
    )

    ap = average_precision_score(
        y_true,
        y_proba
    )

    plt.figure(figsize=(7, 5))

    plt.plot(
        recall,
        precision,
        label=f"Baseline (AP = {ap:.3f})"
    )

    plt.xlabel("Recall")
    plt.ylabel("Precision")

    plt.title(
        "Courbe Precision-Recall — Baseline"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=150
    )

    plt.close()


# ============================================================
# 3. CHARGEMENT DES DONNÉES
# ============================================================

print_section("ORIENT'IA — BASELINE ML")

print("Projet :", PROJECT_ROOT)

print_section("1. Chargement des données")

X_train = load_csv(
    ML_DATA_DIR / "X_train.csv"
)

X_validation = load_csv(
    ML_DATA_DIR / "X_validation.csv"
)

X_test = load_csv(
    ML_DATA_DIR / "X_test.csv"
)

y_train = load_csv(
    ML_DATA_DIR / "y_train.csv"
)

y_validation = load_csv(
    ML_DATA_DIR / "y_validation.csv"
)

y_test = load_csv(
    ML_DATA_DIR / "y_test.csv"
)


# ============================================================
# 4. PRÉPARATION DE LA CIBLE
# ============================================================

print_section("2. Préparation de la cible")

y_train = normalize_target(y_train)
y_validation = normalize_target(y_validation)
y_test = normalize_target(y_test)

print("\nDistribution TRAIN :")
print(y_train.value_counts().sort_index())

print("\nDistribution VALIDATION :")
print(y_validation.value_counts().sort_index())

print("\nDistribution TEST :")
print(y_test.value_counts().sort_index())


# ============================================================
# 5. VÉRIFICATION DES FEATURES
# ============================================================

print_section("3. Vérification des features")

print(f"Nombre de features : {X_train.shape[1]}")

print("\nFeatures utilisées :")

for column in X_train.columns:
    print(f"  - {column}")


# Vérification de cohérence
if list(X_train.columns) != list(X_validation.columns):
    raise ValueError(
        "Les colonnes de X_train et X_validation sont différentes."
    )

if list(X_train.columns) != list(X_test.columns):
    raise ValueError(
        "Les colonnes de X_train et X_test sont différentes."
    )


# ============================================================
# 6. IDENTIFICATION DES TYPES DE VARIABLES
# ============================================================

print_section("4. Identification des variables")

numeric_features = X_train.select_dtypes(
    include=["int64", "int32", "float64", "float32"]
).columns.tolist()

categorical_features = X_train.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nVariables numériques :")

for column in numeric_features:
    print(f"  - {column}")

print("\nVariables catégorielles :")

for column in categorical_features:
    print(f"  - {column}")


# ============================================================
# 7. PREPROCESSING POUR LA BASELINE
# ============================================================

print_section("5. Construction du preprocessing")

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        ),
        (
            "scaler",
            StandardScaler()
        ),
    ]
)


# Compatibilité avec différentes versions de sklearn
try:

    categorical_encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=True
    )

except TypeError:

    categorical_encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse=True
    )


categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "encoder",
            categorical_encoder
        ),
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        ),
    ],
    remainder="drop"
)


# ============================================================
# 8. MODÈLE BASELINE
# ============================================================

print_section("6. Construction du modèle")

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)


baseline_pipeline = Pipeline(
    steps=[
        (
            "preprocessing",
            preprocessor
        ),
        (
            "model",
            model
        ),
    ]
)


print("Modèle : Logistic Regression")
print("max_iter : 2000")
print("class_weight : balanced")
print("random_state : 42")


# ============================================================
# 9. ENTRAÎNEMENT
# ============================================================

print_section("7. Entraînement")

baseline_pipeline.fit(
    X_train,
    y_train
)

print("Entraînement terminé.")


# ============================================================
# 10. PRÉDICTIONS
# ============================================================

print_section("8. Prédictions")

y_train_pred = baseline_pipeline.predict(
    X_train
)

y_validation_pred = baseline_pipeline.predict(
    X_validation
)

y_test_pred = baseline_pipeline.predict(
    X_test
)


y_train_proba = baseline_pipeline.predict_proba(
    X_train
)[:, 1]

y_validation_proba = baseline_pipeline.predict_proba(
    X_validation
)[:, 1]

y_test_proba = baseline_pipeline.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 11. ÉVALUATION
# ============================================================

print_section("9. Évaluation du modèle")


train_metrics = evaluate_classification(
    y_train,
    y_train_pred,
    y_train_proba
)

validation_metrics = evaluate_classification(
    y_validation,
    y_validation_pred,
    y_validation_proba
)

test_metrics = evaluate_classification(
    y_test,
    y_test_pred,
    y_test_proba
)


metrics_df = pd.DataFrame(
    [
        {
            "dataset": "train",
            **train_metrics
        },
        {
            "dataset": "validation",
            **validation_metrics
        },
        {
            "dataset": "test",
            **test_metrics
        },
    ]
)


print("\nRésultats :\n")

print(
    metrics_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# 12. RAPPORT DE CLASSIFICATION
# ============================================================

print_section("10. Rapport de classification")

print("\nTEST :\n")

print(
    classification_report(
        y_test,
        y_test_pred,
        target_names=[
            "Non recommandée",
            "Recommandée"
        ],
        zero_division=0
    )
)


# ============================================================
# 13. MATRICE DE CONFUSION
# ============================================================

print_section("11. Matrice de confusion")

confusion_path = (
    REPORTS_DIR /
    "confusion_matrix_baseline.png"
)

save_confusion_matrix(
    y_test,
    y_test_pred,
    confusion_path
)

print(
    f"Matrice sauvegardée : {confusion_path}"
)


# ============================================================
# 14. COURBE ROC
# ============================================================

print_section("12. Courbe ROC")

roc_path = (
    REPORTS_DIR /
    "roc_curve_baseline.png"
)

save_roc_curve(
    y_test,
    y_test_proba,
    roc_path
)

print(
    f"Courbe ROC sauvegardée : {roc_path}"
)


# ============================================================
# 15. COURBE PRECISION-RECALL
# ============================================================

print_section("13. Courbe Precision-Recall")

pr_path = (
    REPORTS_DIR /
    "pr_curve_baseline.png"
)

save_pr_curve(
    y_test,
    y_test_proba,
    pr_path
)

print(
    f"Courbe PR sauvegardée : {pr_path}"
)


# ============================================================
# 16. SAUVEGARDE DES MÉTRIQUES
# ============================================================

print_section("14. Sauvegarde des métriques")

metrics_path = (
    REPORTS_DIR /
    "baseline_metrics.csv"
)

metrics_df.to_csv(
    metrics_path,
    index=False
)

print(
    f"Métriques sauvegardées : {metrics_path}"
)


# ============================================================
# 17. SAUVEGARDE DU MODÈLE
# ============================================================

print_section("15. Sauvegarde du modèle")

model_path = (
    ML_MODELS_DIR /
    "baseline_logistic_regression.joblib"
)

joblib.dump(
    baseline_pipeline,
    model_path
)

print(
    f"Modèle sauvegardé : {model_path}"
)


# ============================================================
# 18. RAPPORT MARKDOWN
# ============================================================

print_section("16. Génération du rapport")

report_path = (
    REPORTS_DIR /
    "baseline_report.md"
)


best_test_metric = test_metrics["f1"]


report_content = f"""# ORIENT'IA — Rapport Baseline ML

## 1. Objectif

Construire un premier modèle de référence pour le système
de recommandation candidat → filière.

Cette baseline servira de référence pour comparer les modèles
ML plus avancés.

## 2. Modèle

**Logistic Regression**

Paramètres principaux :

- `max_iter = 2000`
- `class_weight = balanced`
- `random_state = 42`

## 3. Données

### Train

- Nombre de lignes : {len(X_train)}

### Validation

- Nombre de lignes : {len(X_validation)}

### Test

- Nombre de lignes : {len(X_test)}

### Nombre de features

{X_train.shape[1]}

## 4. Cible

La variable cible est :

`est_recommandee`

Encodage :

- `Oui → 1`
- `Non → 0`

## 5. Préprocessing

### Variables numériques

Les variables numériques sont :

- imputées par la médiane si nécessaire ;
- standardisées avec `StandardScaler`.

### Variables catégorielles

Les variables catégorielles sont :

- imputées avec la modalité la plus fréquente ;
- encodées avec `OneHotEncoder`.

Les catégories inconnues sont ignorées avec :

`handle_unknown="ignore"`

## 6. Résultats

| Dataset | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Train | {train_metrics["accuracy"]:.4f} | {train_metrics["precision"]:.4f} | {train_metrics["recall"]:.4f} | {train_metrics["f1"]:.4f} | {train_metrics["roc_auc"]:.4f} | {train_metrics["pr_auc"]:.4f} |
| Validation | {validation_metrics["accuracy"]:.4f} | {validation_metrics["precision"]:.4f} | {validation_metrics["recall"]:.4f} | {validation_metrics["f1"]:.4f} | {validation_metrics["roc_auc"]:.4f} | {validation_metrics["pr_auc"]:.4f} |
| Test | {test_metrics["accuracy"]:.4f} | {test_metrics["precision"]:.4f} | {test_metrics["recall"]:.4f} | {test_metrics["f1"]:.4f} | {test_metrics["roc_auc"]:.4f} | {test_metrics["pr_auc"]:.4f} |

## 7. Interprétation

Le modèle baseline constitue le point de référence pour les
prochains modèles.

La métrique F1 sur le jeu de test est :

**{best_test_metric:.4f}**

Les performances des prochains modèles devront être comparées
à cette baseline.

## 8. Fichiers générés

- `ml/models/baseline_logistic_regression.joblib`
- `reports/ml/baseline_metrics.csv`
- `reports/ml/confusion_matrix_baseline.png`
- `reports/ml/roc_curve_baseline.png`
- `reports/ml/pr_curve_baseline.png`
- `reports/ml/baseline_report.md`

## 9. Limite importante

Cette baseline est une première formulation du problème en
classification binaire.

Pour une recommandation réelle de plusieurs filières, les
performances de ranking devront également être évaluées avec
des métriques telles que :

- Precision@K
- Recall@K
- Hit Rate@K
- NDCG@K

Ces métriques nécessitent de conserver l'identifiant du candidat
et de pouvoir regrouper les prédictions par candidat.

## 10. Prochaine étape

Comparer cette baseline avec deux approches ML plus adaptées
au problème de recommandation.

"""

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(report_content)


print(
    f"Rapport sauvegardé : {report_path}"
)


# ============================================================
# 19. RÉSUMÉ FINAL
# ============================================================

print_section("BASELINE TERMINÉE")

print("Modèle entraîné : Logistic Regression")

print()
print("Fichiers générés :")

print(f"  ✓ {model_path}")
print(f"  ✓ {metrics_path}")
print(f"  ✓ {report_path}")
print(f"  ✓ {confusion_path}")
print(f"  ✓ {roc_path}")
print(f"  ✓ {pr_path}")

print()
print("Baseline ML terminée avec succès.")