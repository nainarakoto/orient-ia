# ORIENT'IA — Rapport Baseline ML

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

- Nombre de lignes : 8400

### Validation

- Nombre de lignes : 1792

### Test

- Nombre de lignes : 1808

### Nombre de features

15

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
| Train | 0.5020 | 0.0741 | 0.6057 | 0.1320 | 0.5395 | 0.0610 |
| Validation | 0.4219 | 0.0558 | 0.5179 | 0.1007 | 0.4007 | 0.0480 |
| Test | 0.4198 | 0.0447 | 0.4071 | 0.0806 | 0.4077 | 0.0483 |

## 7. Interprétation

Le modèle baseline constitue le point de référence pour les
prochains modèles.

La métrique F1 sur le jeu de test est :

**0.0806**

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

