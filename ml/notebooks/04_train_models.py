#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ORIENT'IA
04_train_models.py

Entraînement et comparaison de plusieurs modèles ML
pour la recommandation candidat -> filière.

Modèles :
    1. Random Forest
    2. HistGradientBoosting

Objectif :
    Comparer plusieurs approches ML à la baseline
    Logistic Regression.

Entrées :
    ml/preprocessing/X_train.csv
    ml/preprocessing/X_validation.csv
    ml/preprocessing/X_test.csv
    ml/preprocessing/y_train.csv
    ml/preprocessing/y_validation.csv
    ml/preprocessing/y_test.csv

Sorties :
    ml/models/random_forest.joblib
    ml/models/hist_gradient_boosting.joblib

    reports/ml/model_comparison.csv
    reports/ml/model_comparison.md

    reports/ml/random_forest_confusion_matrix.png
    reports/ml/random_forest_roc_curve.png
    reports/ml/random_forest_pr_curve.png

    reports/ml/hist_gradient_boosting_confusion_matrix.png
    reports/ml/hist_gradient_boosting_roc_curve.png
    reports/ml/hist_gradient_boosting_pr_curve.png
"""

from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from sklearn.ensemble import (
    RandomForestClassifier,
    HistGradientBoostingClassifier
)

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
    precision_recall_curve
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


warnings.filterwarnings("ignore")


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_DATA_DIR = PROJECT_ROOT / "ml" / "preprocessing"

ML_MODELS_DIR = PROJECT_ROOT / "ml" / "models"

REPORTS_DIR = PROJECT_ROOT / "reports" / "ml"

ML_MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. UTILITAIRES
# ============================================================

def print_section(title):

    print()
    print("=" * 75)
    print(title)
    print("=" * 75)


def load_csv(path):

    if not path.exists():

        raise FileNotFoundError(
            f"\nFichier introuvable : {path}\n"
            f"Vérifie que 02_preprocessing.py a bien été exécuté."
        )

    df = pd.read_csv(path)

    print(
        f"Chargé : {path} "
        f"| Shape : {df.shape}"
    )

    return df


def normalize_target(y):

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
            "FALSE": 0
        }

        y = y.map(mapping)

    y = pd.to_numeric(
        y,
        errors="coerce"
    )

    if y.isna().any():

        raise ValueError(
            "La cible contient des valeurs invalides."
        )

    unique_values = sorted(
        y.unique()
    )

    if not set(unique_values).issubset({0, 1}):

        raise ValueError(
            f"La cible doit contenir 0 et 1. "
            f"Valeurs trouvées : {unique_values}"
        )

    return y.astype(int)


# ============================================================
# 3. MÉTRIQUES
# ============================================================

def evaluate_model(
    model,
    X,
    y
):

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)[:, 1]

    metrics = {

        "accuracy": accuracy_score(
            y,
            predictions
        ),

        "precision": precision_score(
            y,
            predictions,
            zero_division=0
        ),

        "recall": recall_score(
            y,
            predictions,
            zero_division=0
        ),

        "f1": f1_score(
            y,
            predictions,
            zero_division=0
        )
    }

    if len(np.unique(y)) == 2:

        metrics["roc_auc"] = roc_auc_score(
            y,
            probabilities
        )

        metrics["pr_auc"] = average_precision_score(
            y,
            probabilities
        )

    else:

        metrics["roc_auc"] = np.nan

        metrics["pr_auc"] = np.nan

    return (
        metrics,
        predictions,
        probabilities
    )


# ============================================================
# 4. GRAPHIQUES
# ============================================================

def save_confusion_matrix(
    y_true,
    y_pred,
    model_name
):

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    path = (
        REPORTS_DIR /
        f"{model_name}_confusion_matrix.png"
    )

    plt.figure(
        figsize=(6, 5)
    )

    plt.imshow(cm)

    plt.title(
        f"Matrice de confusion — {model_name}"
    )

    plt.xlabel(
        "Prédiction"
    )

    plt.ylabel(
        "Réalité"
    )

    plt.xticks(
        [0, 1],
        ["Non", "Oui"]
    )

    plt.yticks(
        [0, 1],
        ["Non", "Oui"]
    )

    for i in range(
        cm.shape[0]
    ):

        for j in range(
            cm.shape[1]
        ):

            plt.text(
                j,
                i,
                cm[i, j],
                ha="center",
                va="center"
            )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=150
    )

    plt.close()

    return path


def save_roc_curve(
    y_true,
    y_proba,
    model_name
):

    if len(np.unique(y_true)) < 2:

        return None

    fpr, tpr, _ = roc_curve(
        y_true,
        y_proba
    )

    auc = roc_auc_score(
        y_true,
        y_proba
    )

    path = (
        REPORTS_DIR /
        f"{model_name}_roc_curve.png"
    )

    plt.figure(
        figsize=(7, 5)
    )

    plt.plot(
        fpr,
        tpr,
        label=f"{model_name} (AUC={auc:.3f})"
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--"
    )

    plt.xlabel(
        "False Positive Rate"
    )

    plt.ylabel(
        "True Positive Rate"
    )

    plt.title(
        f"Courbe ROC — {model_name}"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=150
    )

    plt.close()

    return path


def save_pr_curve(
    y_true,
    y_proba,
    model_name
):

    if len(np.unique(y_true)) < 2:

        return None

    precision, recall, _ = precision_recall_curve(
        y_true,
        y_proba
    )

    ap = average_precision_score(
        y_true,
        y_proba
    )

    path = (
        REPORTS_DIR /
        f"{model_name}_pr_curve.png"
    )

    plt.figure(
        figsize=(7, 5)
    )

    plt.plot(
        recall,
        precision,
        label=f"{model_name} (AP={ap:.3f})"
    )

    plt.xlabel(
        "Recall"
    )

    plt.ylabel(
        "Precision"
    )

    plt.title(
        f"Precision-Recall — {model_name}"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=150
    )

    plt.close()

    return path


# ============================================================
# 5. CHARGEMENT
# ============================================================

print_section(
    "ORIENT'IA — COMPARAISON DES MODÈLES"
)

print(
    f"Projet : {PROJECT_ROOT}"
)

print_section(
    "1. Chargement des données"
)

X_train = load_csv(
    ML_DATA_DIR /
    "X_train.csv"
)

X_validation = load_csv(
    ML_DATA_DIR /
    "X_validation.csv"
)

X_test = load_csv(
    ML_DATA_DIR /
    "X_test.csv"
)

y_train = normalize_target(
    load_csv(
        ML_DATA_DIR /
        "y_train.csv"
    )
)

y_validation = normalize_target(
    load_csv(
        ML_DATA_DIR /
        "y_validation.csv"
    )
)

y_test = normalize_target(
    load_csv(
        ML_DATA_DIR /
        "y_test.csv"
    )
)


# ============================================================
# 6. VÉRIFICATION
# ============================================================

print_section(
    "2. Vérification des données"
)

if list(X_train.columns) != list(
    X_validation.columns
):

    raise ValueError(
        "X_train et X_validation "
        "n'ont pas les mêmes colonnes."
    )


if list(X_train.columns) != list(
    X_test.columns
):

    raise ValueError(
        "X_train et X_test "
        "n'ont pas les mêmes colonnes."
    )


print(
    f"Nombre de features : "
    f"{X_train.shape[1]}"
)

print(
    f"Train : {X_train.shape}"
)

print(
    f"Validation : {X_validation.shape}"
)

print(
    f"Test : {X_test.shape}"
)


# ============================================================
# 7. IDENTIFICATION DES FEATURES
# ============================================================

print_section(
    "3. Identification des variables"
)

numeric_features = X_train.select_dtypes(
    include=[
        "int64",
        "int32",
        "float64",
        "float32"
    ]
).columns.tolist()


categorical_features = X_train.select_dtypes(
    include=[
        "object",
        "category",
        "bool"
    ]
).columns.tolist()


print(
    f"Variables numériques : "
    f"{len(numeric_features)}"
)

print(
    f"Variables catégorielles : "
    f"{len(categorical_features)}"
)


# ============================================================
# 8. ENCODAGE
# ============================================================

print_section(
    "4. Construction du preprocessing"
)

numeric_pipeline = Pipeline(
    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        )
    ]
)


try:

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )

except TypeError:

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse=False
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
            encoder
        )
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
        )
    ],

    remainder="drop"
)


# ============================================================
# 9. MODÈLES
# ============================================================

print_section(
    "5. Construction des modèles"
)


random_forest = RandomForestClassifier(

    n_estimators=300,

    max_depth=None,

    min_samples_split=2,

    min_samples_leaf=1,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1
)


hist_gradient_boosting = HistGradientBoostingClassifier(

    max_iter=200,

    learning_rate=0.08,

    max_leaf_nodes=31,

    l2_regularization=1.0,

    random_state=42
)


models = {

    "random_forest":
        Pipeline(
            steps=[

                (
                    "preprocessing",
                    preprocessor
                ),

                (
                    "model",
                    random_forest
                )
            ]
        ),

    "hist_gradient_boosting":
        Pipeline(
            steps=[

                (
                    "preprocessing",
                    preprocessor
                ),

                (
                    "model",
                    hist_gradient_boosting
                )
            ]
        )
}


# ============================================================
# 10. ENTRAÎNEMENT
# ============================================================

results = []

trained_models = {}


for model_name, model in models.items():

    print_section(
        f"6. Entraînement : {model_name}"
    )

    print(
        "Début de l'entraînement..."
    )

    model.fit(
        X_train,
        y_train
    )

    print(
        "Entraînement terminé."
    )

    trained_models[
        model_name
    ] = model


    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    train_metrics, _, _ = evaluate_model(
        model,
        X_train,
        y_train
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    validation_metrics, _, _ = evaluate_model(
        model,
        X_validation,
        y_validation
    )


    # --------------------------------------------------------
    # TEST
    # --------------------------------------------------------

    test_metrics, test_pred, test_proba = evaluate_model(
        model,
        X_test,
        y_test
    )


    # --------------------------------------------------------
    # RESULTATS
    # --------------------------------------------------------

    results.append(

        {
            "model":
                model_name,

            "train_accuracy":
                train_metrics["accuracy"],

            "train_precision":
                train_metrics["precision"],

            "train_recall":
                train_metrics["recall"],

            "train_f1":
                train_metrics["f1"],

            "validation_accuracy":
                validation_metrics["accuracy"],

            "validation_precision":
                validation_metrics["precision"],

            "validation_recall":
                validation_metrics["recall"],

            "validation_f1":
                validation_metrics["f1"],

            "validation_roc_auc":
                validation_metrics["roc_auc"],

            "validation_pr_auc":
                validation_metrics["pr_auc"],

            "test_accuracy":
                test_metrics["accuracy"],

            "test_precision":
                test_metrics["precision"],

            "test_recall":
                test_metrics["recall"],

            "test_f1":
                test_metrics["f1"],

            "test_roc_auc":
                test_metrics["roc_auc"],

            "test_pr_auc":
                test_metrics["pr_auc"]
        }
    )


    # --------------------------------------------------------
    # GRAPHIQUES
    # --------------------------------------------------------

    save_confusion_matrix(
        y_test,
        test_pred,
        model_name
    )

    save_roc_curve(
        y_test,
        test_proba,
        model_name
    )

    save_pr_curve(
        y_test,
        test_proba,
        model_name
    )


    # --------------------------------------------------------
    # RAPPORT TERMINAL
    # --------------------------------------------------------

    print()

    print(
        "Résultats TEST"
    )

    print(
        f"Accuracy  : "
        f"{test_metrics['accuracy']:.4f}"
    )

    print(
        f"Precision : "
        f"{test_metrics['precision']:.4f}"
    )

    print(
        f"Recall    : "
        f"{test_metrics['recall']:.4f}"
    )

    print(
        f"F1        : "
        f"{test_metrics['f1']:.4f}"
    )

    print(
        f"ROC-AUC   : "
        f"{test_metrics['roc_auc']:.4f}"
    )

    print(
        f"PR-AUC    : "
        f"{test_metrics['pr_auc']:.4f}"
    )


    # --------------------------------------------------------
    # CLASSIFICATION REPORT
    # --------------------------------------------------------

    print()

    print(
        classification_report(
            y_test,
            test_pred,
            target_names=[
                "Non recommandée",
                "Recommandée"
            ],
            zero_division=0
        )
    )


# ============================================================
# 11. COMPARAISON
# ============================================================

print_section(
    "7. Comparaison des modèles"
)

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    by="test_f1",
    ascending=False
)


print()

print(
    results_df[
        [
            "model",
            "test_accuracy",
            "test_precision",
            "test_recall",
            "test_f1",
            "test_roc_auc",
            "test_pr_auc"
        ]
    ].to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# 12. SAUVEGARDE DES MODÈLES
# ============================================================

print_section(
    "8. Sauvegarde des modèles"
)


for model_name, model in trained_models.items():

    model_path = (
        ML_MODELS_DIR /
        f"{model_name}.joblib"
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        f"✓ {model_path}"
    )


# ============================================================
# 13. SAUVEGARDE DES MÉTRIQUES
# ============================================================

print_section(
    "9. Sauvegarde des métriques"
)


metrics_path = (
    REPORTS_DIR /
    "model_comparison.csv"
)

results_df.to_csv(
    metrics_path,
    index=False
)

print(
    f"✓ {metrics_path}"
)


# ============================================================
# 14. MEILLEUR MODÈLE
# ============================================================

best_model_row = results_df.iloc[0]

best_model_name = best_model_row[
    "model"
]

best_f1 = best_model_row[
    "test_f1"
]

best_roc_auc = best_model_row[
    "test_roc_auc"
]

best_pr_auc = best_model_row[
    "test_pr_auc"
]


# ============================================================
# 15. RAPPORT MARKDOWN
# ============================================================

print_section(
    "10. Génération du rapport"
)


report_path = (
    REPORTS_DIR /
    "model_comparison.md"
)


report = f"""# ORIENT'IA — Comparaison des modèles ML

## 1. Objectif

Comparer plusieurs modèles de classification pour le problème :

**candidat → filière recommandée**

La baseline Logistic Regression est évaluée séparément dans :

`reports/ml/baseline_report.md`

Les modèles évalués ici sont :

- Random Forest
- HistGradientBoosting

---

## 2. Données

| Dataset | Lignes |
|---|---:|
| Train | {len(X_train)} |
| Validation | {len(X_validation)} |
| Test | {len(X_test)} |

Nombre de features avant encodage :

**{X_train.shape[1]}**

---

## 3. Méthodologie

Les variables numériques sont imputées avec la médiane.

Les variables catégorielles sont :

- imputées avec la modalité la plus fréquente ;
- encodées avec OneHotEncoder ;
- les catégories inconnues sont ignorées.

Les modèles sont entraînés uniquement sur le jeu d'entraînement.

Le jeu de validation est utilisé pour comparer les performances pendant
le développement.

Le jeu de test est conservé pour l'évaluation finale.

---

## 4. Résultats

| Modèle | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
"""


for _, row in results_df.iterrows():

    report += (
        f"| {row['model']} "
        f"| {row['test_accuracy']:.4f} "
        f"| {row['test_precision']:.4f} "
        f"| {row['test_recall']:.4f} "
        f"| {row['test_f1']:.4f} "
        f"| {row['test_roc_auc']:.4f} "
        f"| {row['test_pr_auc']:.4f} |\\n"
    )


report += f"""

---

## 5. Meilleur modèle

Selon la métrique F1 sur le jeu de test :

**{best_model_name}**

F1 :

**{best_f1:.4f}**

ROC-AUC :

**{best_roc_auc:.4f}**

PR-AUC :

**{best_pr_auc:.4f}**

---

## 6. Interprétation

Le meilleur modèle selon F1 est :

**{best_model_name}**

Il devra cependant être évalué avec des métriques de ranking avant
d'être considéré comme le modèle final du système de recommandation.

La classification binaire répond à la question :

> Cette filière est-elle recommandée ou non ?

Le système ORIENT'IA devra également répondre à :

> Quelles sont les meilleures filières pour ce candidat ?

Cette deuxième question nécessite une évaluation par classement.

---

## 7. Limites

Cette comparaison porte principalement sur une classification binaire.

Elle ne suffit pas à évaluer complètement un système de recommandation.

Les prochaines étapes devront notamment mesurer :

- Precision@K
- Recall@K
- Hit Rate@K
- NDCG@K

pour plusieurs valeurs de K.

---

## 8. Fichiers générés

### Modèles

- `ml/models/random_forest.joblib`
- `ml/models/hist_gradient_boosting.joblib`

### Métriques

- `reports/ml/model_comparison.csv`
- `reports/ml/model_comparison.md`

### Visualisations

- `random_forest_confusion_matrix.png`
- `random_forest_roc_curve.png`
- `random_forest_pr_curve.png`
- `hist_gradient_boosting_confusion_matrix.png`
- `hist_gradient_boosting_roc_curve.png`
- `hist_gradient_boosting_pr_curve.png`

---

## 9. Prochaine étape

Évaluer les modèles sur le véritable objectif de recommandation :

**classer les filières pour chaque candidat.**

Les métriques principales seront :

- Precision@K
- Recall@K
- Hit Rate@K
- NDCG@K
"""


with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(report)


print(
    f"✓ {report_path}"
)


# ============================================================
# 16. FIN
# ============================================================

print_section(
    "ENTRAÎNEMENT TERMINÉ"
)

print(
    f"Meilleur modèle selon F1 : "
    f"{best_model_name}"
)

print(
    f"F1 TEST : "
    f"{best_f1:.4f}"
)

print()

print(
    "Fichiers disponibles dans :"
)

print(
    f"  {ML_MODELS_DIR}"
)

print(
    f"  {REPORTS_DIR}"
)
