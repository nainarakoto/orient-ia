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
| baseline_logistic_regression | 750 | 0.0627 | 0.0627 | 0.0627 | 0.0627 | 0.0627 | 0.1880 | 0.1880 | 0.1335 | 0.0627 | 0.3133 | 0.3133 | 0.1848 |
| hist_gradient_boosting | 750 | 0.7040 | 0.7040 | 0.7040 | 0.7053 | 0.2804 | 0.8413 | 0.8413 | 0.7838 | 0.1936 | 0.9680 | 0.9680 | 0.8350 |
| random_forest | 750 | 1.0000 | 1.0000 | 1.0000 | 0.9993 | 0.3333 | 1.0000 | 1.0000 | 0.9998 | 0.2000 | 1.0000 | 1.0000 | 0.9998 |

## 6. Interprétation

Le meilleur modèle selon NDCG@5 est `random_forest` avec un score de **0.9998**.

NDCG@K mesure la qualité du classement en tenant compte de la position des filières pertinentes. Une filière pertinente placée en première position est donc mieux valorisée qu'une filière pertinente placée plus bas dans le classement.

## 7. Fichiers générés

- `ranking_metrics.csv`
- `ranking_predictions.csv`
- `ranking_comparison.png`
- `ranking_report.md`
