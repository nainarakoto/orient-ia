# ORIENT'IA — Rapport d'évaluation du ranking

## 1. Objectif

Évaluer la capacité des modèles à classer les filières pour chaque candidat.

Le problème est traité comme un problème de ranking :

```text
Candidat
   ↓
Score de chaque filière
   ↓
Classement
   ↓
Top-K recommandations
```

## 2. Identifiants

- Identifiant candidat : `candidat_id`
- Identifiant filière : `filiere_code`
- Variable cible : `target`

L'identifiant candidat est utilisé uniquement pour regrouper les recommandations et n'est pas utilisé comme feature ML.

## 3. Modèles évalués

- `baseline_logistic_regression`
- `best_model`
- `hist_gradient_boosting`
- `random_forest`

## 4. Métriques

- Precision@K
- Recall@K
- Hit Rate@K
- NDCG@K

## 5. Résultats

| Model | Candidates | Precision@1 | Recall@1 | HitRate@1 | NDCG@1 | Precision@3 | Recall@3 | HitRate@3 | NDCG@3 | Precision@5 | Recall@5 | HitRate@5 | NDCG@5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_logistic_regression | 750 | 0.0627 | 0.0627 | 0.0627 | 0.0627 | 0.0627 | 0.1880 | 0.1880 | 0.1335 | 0.0624 | 0.3120 | 0.3120 | 0.1843 |
| best_model | 750 | 0.9840 | 0.9840 | 0.9840 | 0.9833 | 0.3329 | 0.9987 | 0.9987 | 0.9928 | 0.2000 | 1.0000 | 1.0000 | 0.9934 |
| hist_gradient_boosting | 750 | 0.7453 | 0.7453 | 0.7453 | 0.7462 | 0.3333 | 1.0000 | 1.0000 | 0.8900 | 0.2000 | 1.0000 | 1.0000 | 0.8900 |
| random_forest | 750 | 0.9840 | 0.9840 | 0.9840 | 0.9833 | 0.3329 | 0.9987 | 0.9987 | 0.9928 | 0.2000 | 1.0000 | 1.0000 | 0.9934 |

## 6. Interprétation

Le meilleur modèle selon NDCG@5 est `best_model` avec un score de **0.9934**.

NDCG@K mesure la qualité du classement en tenant compte de la position des filières pertinentes. Une filière pertinente placée en première position est donc mieux valorisée qu'une filière pertinente placée plus bas dans le classement.

## 7. Fichiers générés

- `ranking_metrics.csv`
- `ranking_predictions.csv`
- `ranking_comparison.png`
- `ranking_report.md`
