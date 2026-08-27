# ORIENT'IA — Comparaison des modèles ML

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
| Train | 8400 |
| Validation | 1792 |
| Test | 1808 |

Nombre de features avant encodage :

**15**

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
| random_forest | 0.9806 | 1.0000 | 0.6903 | 0.8168 | 1.0000 | 0.9997 |\n| hist_gradient_boosting | 0.9486 | 1.0000 | 0.1770 | 0.3008 | 0.9603 | 0.6809 |\n

---

## 5. Meilleur modèle

Selon la métrique F1 sur le jeu de test :

**random_forest**

F1 :

**0.8168**

ROC-AUC :

**1.0000**

PR-AUC :

**0.9997**

---

## 6. Interprétation

Le meilleur modèle selon F1 est :

**random_forest**

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
