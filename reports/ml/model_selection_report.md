# ORIENT'IA — Sélection du meilleur modèle

## 1. Objectif

Sélectionner automatiquement le meilleur modèle pour la recommandation candidat → filière.

## 2. Critère principal

**NDCG@5** a été utilisé comme critère principal.

NDCG@5 mesure la qualité du classement des cinq premières filières recommandées pour chaque candidat.

## 3. Critères secondaires

- Recall@5
- Precision@5
- HitRate@5

## 4. Classement des modèles

|   rank | model                        |   ndcg@5 |   recall@5 |   precision@5 |   hit_rate@5 |
|-------:|:-----------------------------|---------:|-----------:|--------------:|-------------:|
|      1 | random_forest                | 0.993407 |      1     |        0.2    |        1     |
|      2 | hist_gradient_boosting       | 0.889987 |      1     |        0.2    |        1     |
|      3 | baseline_logistic_regression | 0.184254 |      0.312 |        0.0624 |        0.312 |

## 5. Modèle sélectionné

### 🏆 random_forest

- NDCG@5 : **0.9934**
- Recall@5 : **1.0000**
- Precision@5 : **0.2000**
- HitRate@5 : **1.0000**

## 6. Fichier du modèle

`random_forest.joblib`

Le modèle sélectionné a été copié vers :

`ml/models/best_model.joblib`

## 7. Conclusion

Le modèle sélectionné constitue le modèle de référence pour la phase d'inférence et de recommandation.

## 8. Prochaine étape

Développer le module d'inférence permettant de recevoir le profil d'un candidat et de retourner les filières classées par score de recommandation.
