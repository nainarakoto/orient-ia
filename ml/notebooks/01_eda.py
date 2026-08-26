"""
ORIENT'IA - Exploratory Data Analysis (EDA)

Objectif :
    - Explorer les datasets synthétiques
    - Vérifier leur qualité
    - Identifier les valeurs manquantes
    - Identifier les doublons
    - Examiner les distributions
    - Détecter les valeurs aberrantes
    - Examiner les variables catégorielles
    - Identifier les variables utiles pour le ML
    - Générer automatiquement des rapports et graphiques

Entrée :
    data/synthetic/*.csv

Sortie :
    ml/reports/eda/
        ├── csv_summary.csv
        ├── missing_values.csv
        ├── duplicates.csv
        ├── numeric_summary.csv
        ├── categorical_summary.csv
        ├── correlations.csv
        ├── target_candidates.csv
        └── figures/
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "synthetic"

REPORT_DIR = PROJECT_ROOT / "ml" / "reports" / "eda"

FIGURE_DIR = REPORT_DIR / "figures"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# UTILITAIRES
# ============================================================

def print_title(title):
    """Affiche un titre lisible dans le terminal."""
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def load_csv_files():
    """Charge tous les CSV du dossier synthetic."""

    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"Aucun fichier CSV trouvé dans : {DATA_DIR}"
        )

    datasets = {}

    print_title("CHARGEMENT DES DATASETS")

    for file in csv_files:
        try:
            df = pd.read_csv(file)

            datasets[file.stem] = df

            print(
                f"[OK] {file.name:<40} "
                f"{df.shape[0]:>6} lignes x {df.shape[1]:>4} colonnes"
            )

        except Exception as e:
            print(f"[ERREUR] {file.name}: {e}")

    return datasets


# ============================================================
# 1. VUE GENERALE
# ============================================================

def generate_dataset_summary(datasets):
    """Résumé global de tous les datasets."""

    print_title("1. RESUME DES DATASETS")

    rows = []

    for name, df in datasets.items():

        rows.append({
            "dataset": name,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_cells": int(df.isna().sum().sum()),
            "missing_percentage": round(
                df.isna().sum().sum()
                / (df.shape[0] * df.shape[1]) * 100,
                2
            ),
            "duplicates": int(df.duplicated().sum()),
            "memory_mb": round(
                df.memory_usage(deep=True).sum() / 1024**2,
                2
            )
        })

    summary = pd.DataFrame(rows)

    print(summary.to_string(index=False))

    summary.to_csv(
        REPORT_DIR / "csv_summary.csv",
        index=False
    )

    return summary


# ============================================================
# 2. STRUCTURE DES COLONNES
# ============================================================

def analyze_columns(datasets):
    """Analyse les types de colonnes."""

    print_title("2. TYPES DE VARIABLES")

    rows = []

    for name, df in datasets.items():

        for column in df.columns:

            rows.append({
                "dataset": name,
                "column": column,
                "dtype": str(df[column].dtype),
                "unique_values": df[column].nunique(dropna=True),
                "missing": int(df[column].isna().sum()),
                "missing_percentage": round(
                    df[column].isna().mean() * 100,
                    2
                )
            })

    result = pd.DataFrame(rows)

    result.to_csv(
        REPORT_DIR / "columns_summary.csv",
        index=False
    )

    print(result.head(50).to_string(index=False))

    return result


# ============================================================
# 3. VALEURS MANQUANTES
# ============================================================

def analyze_missing_values(datasets):
    """Analyse les valeurs manquantes."""

    print_title("3. VALEURS MANQUANTES")

    rows = []

    for name, df in datasets.items():

        for column in df.columns:

            missing = df[column].isna().sum()

            rows.append({
                "dataset": name,
                "column": column,
                "missing_count": int(missing),
                "total": len(df),
                "missing_percentage": round(
                    missing / len(df) * 100,
                    2
                )
            })

    result = pd.DataFrame(rows)

    result = result.sort_values(
        "missing_percentage",
        ascending=False
    )

    result.to_csv(
        REPORT_DIR / "missing_values.csv",
        index=False
    )

    missing_only = result[result["missing_count"] > 0]

    if missing_only.empty:
        print("[OK] Aucune valeur manquante détectée.")
    else:
        print(missing_only.to_string(index=False))

    return result


# ============================================================
# 4. DOUBLONS
# ============================================================

def analyze_duplicates(datasets):
    """Analyse les lignes dupliquées."""

    print_title("4. DOUBLONS")

    rows = []

    for name, df in datasets.items():

        duplicate_count = df.duplicated().sum()

        rows.append({
            "dataset": name,
            "rows": len(df),
            "duplicates": int(duplicate_count),
            "duplicate_percentage": round(
                duplicate_count / len(df) * 100,
                2
            )
        })

    result = pd.DataFrame(rows)

    result.to_csv(
        REPORT_DIR / "duplicates.csv",
        index=False
    )

    print(result.to_string(index=False))

    return result


# ============================================================
# 5. STATISTIQUES NUMERIQUES
# ============================================================

def analyze_numeric_variables(datasets):
    """Analyse des variables numériques."""

    print_title("5. VARIABLES NUMERIQUES")

    rows = []

    for name, df in datasets.items():

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:

            series = df[column]

            rows.append({
                "dataset": name,
                "column": column,
                "count": int(series.count()),
                "mean": series.mean(),
                "std": series.std(),
                "min": series.min(),
                "q1": series.quantile(0.25),
                "median": series.median(),
                "q3": series.quantile(0.75),
                "max": series.max()
            })

    result = pd.DataFrame(rows)

    if not result.empty:

        result.to_csv(
            REPORT_DIR / "numeric_summary.csv",
            index=False
        )

        print(result.to_string(index=False))

    else:

        print("Aucune variable numérique trouvée.")

    return result


# ============================================================
# 6. VARIABLES CATEGORIELLES
# ============================================================

def analyze_categorical_variables(datasets):
    """Analyse des variables catégorielles."""

    print_title("6. VARIABLES CATEGORIELLES")

    rows = []

    for name, df in datasets.items():

        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns

        for column in categorical_columns:

            series = df[column]

            rows.append({
                "dataset": name,
                "column": column,
                "unique_values": series.nunique(dropna=True),
                "most_frequent": (
                    series.mode().iloc[0]
                    if not series.mode().empty
                    else None
                ),
                "most_frequent_count": (
                    int(series.value_counts().iloc[0])
                    if not series.value_counts().empty
                    else 0
                )
            })

    result = pd.DataFrame(rows)

    if not result.empty:

        result.to_csv(
            REPORT_DIR / "categorical_summary.csv",
            index=False
        )

        print(result.to_string(index=False))

    else:

        print("Aucune variable catégorielle trouvée.")

    return result


# ============================================================
# 7. DISTRIBUTIONS NUMERIQUES
# ============================================================

def generate_numeric_histograms(datasets):
    """Génère des histogrammes pour les variables numériques."""

    print_title("7. DISTRIBUTIONS NUMERIQUES")

    for name, df in datasets.items():

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:

            if df[column].nunique() <= 1:
                continue

            plt.figure(figsize=(8, 5))

            df[column].dropna().hist(
                bins=20
            )

            plt.title(
                f"Distribution - {name} - {column}"
            )

            plt.xlabel(column)
            plt.ylabel("Nombre d'observations")

            plt.tight_layout()

            filename = (
                f"{name}__{column}"
                .replace("/", "_")
                .replace(" ", "_")
            )

            plt.savefig(
                FIGURE_DIR / f"{filename}_hist.png",
                dpi=150
            )

            plt.close()

    print(
        f"[OK] Histogrammes générés dans : {FIGURE_DIR}"
    )


# ============================================================
# 8. DISTRIBUTIONS CATEGORIELLES
# ============================================================

def generate_categorical_charts(datasets):
    """Génère les graphiques des variables catégorielles."""

    print_title("8. DISTRIBUTIONS CATEGORIELLES")

    for name, df in datasets.items():

        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns

        for column in categorical_columns:

            unique_count = df[column].nunique(dropna=True)

            # Évite les graphiques illisibles
            if unique_count == 0 or unique_count > 20:
                continue

            counts = (
                df[column]
                .value_counts(dropna=False)
                .head(20)
            )

            plt.figure(figsize=(10, 5))

            counts.plot(kind="bar")

            plt.title(
                f"Distribution - {name} - {column}"
            )

            plt.xlabel(column)
            plt.ylabel("Nombre")

            plt.xticks(rotation=45, ha="right")

            plt.tight_layout()

            filename = (
                f"{name}__{column}"
                .replace("/", "_")
                .replace(" ", "_")
            )

            plt.savefig(
                FIGURE_DIR / f"{filename}_bar.png",
                dpi=150
            )

            plt.close()

    print(
        f"[OK] Graphiques catégoriels générés dans : {FIGURE_DIR}"
    )


# ============================================================
# 9. CORRELATIONS
# ============================================================

def analyze_correlations(datasets):
    """Analyse les corrélations entre variables numériques."""

    print_title("9. CORRELATIONS")

    all_results = []

    for name, df in datasets.items():

        numeric_df = df.select_dtypes(
            include=np.number
        )

        if numeric_df.shape[1] < 2:
            continue

        correlation = numeric_df.corr()

        correlation.to_csv(
            REPORT_DIR / f"correlations_{name}.csv"
        )

        # Extraction des corrélations fortes
        columns = correlation.columns

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                value = correlation.iloc[i, j]

                if pd.isna(value):
                    continue

                all_results.append({
                    "dataset": name,
                    "variable_1": columns[i],
                    "variable_2": columns[j],
                    "correlation": round(value, 4),
                    "absolute_correlation": abs(value)
                })

        # Heatmap
        plt.figure(
            figsize=(
                max(8, len(columns) * 0.8),
                max(6, len(columns) * 0.6)
            )
        )

        plt.imshow(
            correlation,
            aspect="auto"
        )

        plt.colorbar()

        plt.xticks(
            range(len(columns)),
            columns,
            rotation=90
        )

        plt.yticks(
            range(len(columns)),
            columns
        )

        plt.title(
            f"Matrice de corrélation - {name}"
        )

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / f"{name}_correlation.png",
            dpi=150
        )

        plt.close()

    result = pd.DataFrame(all_results)

    if not result.empty:

        result = result.sort_values(
            "absolute_correlation",
            ascending=False
        )

        result.to_csv(
            REPORT_DIR / "correlations.csv",
            index=False
        )

        print(
            result.head(30).to_string(index=False)
        )

    return result


# ============================================================
# 10. DETECTION DES VALEURS ABERRANTES
# ============================================================

def detect_outliers(datasets):
    """Détection simple par méthode IQR."""

    print_title("10. VALEURS ABERRANTES")

    rows = []

    for name, df in datasets.items():

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) < 4:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            if iqr == 0:
                outlier_count = 0
            else:

                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr

                outlier_count = (
                    (series < lower) |
                    (series > upper)
                ).sum()

            rows.append({
                "dataset": name,
                "column": column,
                "outliers": int(outlier_count),
                "percentage": round(
                    outlier_count / len(series) * 100,
                    2
                )
            })

    result = pd.DataFrame(rows)

    if not result.empty:

        result = result.sort_values(
            "percentage",
            ascending=False
        )

        result.to_csv(
            REPORT_DIR / "outliers.csv",
            index=False
        )

        print(result.to_string(index=False))

    return result


# ============================================================
# 11. IDENTIFICATION DES VARIABLES POTENTIELLEMENT CIBLES
# ============================================================

def identify_target_candidates(datasets):
    """
    Identifie les colonnes qui pourraient être des variables
    cibles pour le futur modèle de recommandation.

    ATTENTION :
    Cette fonction ne choisit PAS automatiquement le target final.
    La cible doit être définie selon le fonctionnement réel
    du système ORIENT'IA.
    """

    print_title("11. CIBLES POTENTIELLES POUR LE ML")

    keywords = [
        "filiere",
        "formation",
        "metier",
        "recommandation",
        "label",
        "target",
        "classe",
        "choix",
        "orientation"
    ]

    rows = []

    for name, df in datasets.items():

        for column in df.columns:

            column_lower = column.lower()

            score = sum(
                keyword in column_lower
                for keyword in keywords
            )

            if score > 0:

                rows.append({
                    "dataset": name,
                    "column": column,
                    "keyword_score": score,
                    "unique_values": df[column].nunique(
                        dropna=True
                    )
                })

    result = pd.DataFrame(rows)

    if not result.empty:

        result = result.sort_values(
            "keyword_score",
            ascending=False
        )

        result.to_csv(
            REPORT_DIR / "target_candidates.csv",
            index=False
        )

        print(result.to_string(index=False))

    else:

        print(
            "Aucune cible évidente détectée automatiquement."
        )

    return result


# ============================================================
# 12. RAPPORT TEXTUEL
# ============================================================

def generate_text_report(
    datasets,
    summary,
    missing,
    duplicates,
    numeric,
    categorical,
    outliers
):
    """Génère un rapport Markdown synthétique."""

    print_title("12. GENERATION DU RAPPORT")

    report_path = REPORT_DIR / "eda_report.md"

    total_rows = sum(
        len(df)
        for df in datasets.values()
    )

    total_columns = sum(
        len(df.columns)
        for df in datasets.values()
    )

    total_missing = sum(
        df.isna().sum().sum()
        for df in datasets.values()
    )

    total_duplicates = sum(
        df.duplicated().sum()
        for df in datasets.values()
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("# ORIENT'IA — Rapport EDA\n\n")

        f.write(
            "Analyse exploratoire des données synthétiques "
            "destinées au système de recommandation.\n\n"
        )

        f.write("## 1. Vue générale\n\n")

        f.write(
            f"- Nombre de datasets : **{len(datasets)}**\n"
        )

        f.write(
            f"- Nombre total de lignes : **{total_rows}**\n"
        )

        f.write(
            f"- Nombre total de colonnes : **{total_columns}**\n"
        )

        f.write(
            f"- Cellules manquantes : **{total_missing}**\n"
        )

        f.write(
            f"- Doublons : **{total_duplicates}**\n\n"
        )

        f.write("## 2. Datasets analysés\n\n")

        f.write(
            summary.to_markdown(index=False)
        )

        f.write("\n\n")

        f.write("## 3. Valeurs manquantes\n\n")

        missing_problem = missing[
            missing["missing_count"] > 0
        ]

        if missing_problem.empty:

            f.write(
                "Aucune valeur manquante détectée.\n\n"
            )

        else:

            f.write(
                missing_problem.to_markdown(
                    index=False
                )
            )

            f.write("\n\n")

        f.write("## 4. Doublons\n\n")

        f.write(
            duplicates.to_markdown(index=False)
        )

        f.write("\n\n")

        f.write("## 5. Variables numériques\n\n")

        if numeric.empty:

            f.write(
                "Aucune variable numérique détectée.\n\n"
            )

        else:

            f.write(
                numeric.to_markdown(index=False)
            )

            f.write("\n\n")

        f.write("## 6. Variables catégorielles\n\n")

        if categorical.empty:

            f.write(
                "Aucune variable catégorielle détectée.\n\n"
            )

        else:

            f.write(
                categorical.to_markdown(index=False)
            )

            f.write("\n\n")

        f.write("## 7. Valeurs aberrantes\n\n")

        if outliers.empty:

            f.write(
                "Aucune variable numérique exploitable "
                "pour la détection des valeurs aberrantes.\n\n"
            )

        else:

            f.write(
                outliers.to_markdown(index=False)
            )

            f.write("\n\n")

        f.write("## 8. Conclusion EDA\n\n")

        f.write(
            "L'EDA doit être utilisée pour décider :\n\n"
        )

        f.write(
            "1. quelles variables conserver ;\n"
            "2. quelles variables nettoyer ;\n"
            "3. quelles variables encoder ;\n"
            "4. quelles variables normaliser ;\n"
            "5. quelles variables utiliser pour le ML ;\n"
            "6. quelle variable représente la cible ;\n"
            "7. quelles variables pourraient créer un biais ou une fuite de données.\n"
        )

    print(
        f"[OK] Rapport créé : {report_path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 80)
    print("ORIENT'IA — EXPLORATORY DATA ANALYSIS")
    print("=" * 80)

    print(f"Projet : {PROJECT_ROOT}")
    print(f"Données : {DATA_DIR}")
    print(f"Rapports : {REPORT_DIR}")

    # Chargement
    datasets = load_csv_files()

    # Analyses
    summary = generate_dataset_summary(
        datasets
    )

    analyze_columns(
        datasets
    )

    missing = analyze_missing_values(
        datasets
    )

    duplicates = analyze_duplicates(
        datasets
    )

    numeric = analyze_numeric_variables(
        datasets
    )

    categorical = analyze_categorical_variables(
        datasets
    )

    generate_numeric_histograms(
        datasets
    )

    generate_categorical_charts(
        datasets
    )

    analyze_correlations(
        datasets
    )

    outliers = detect_outliers(
        datasets
    )

    identify_target_candidates(
        datasets
    )

    generate_text_report(
        datasets,
        summary,
        missing,
        duplicates,
        numeric,
        categorical,
        outliers
    )

    print_title("EDA TERMINEE")

    print(
        f"""
Les résultats sont disponibles dans :

    {REPORT_DIR}

Fichiers principaux :

    csv_summary.csv
    columns_summary.csv
    missing_values.csv
    duplicates.csv
    numeric_summary.csv
    categorical_summary.csv
    correlations.csv
    outliers.csv
    target_candidates.csv
    eda_report.md

Graphiques :

    {FIGURE_DIR}
"""
    )


if __name__ == "__main__":
    main()