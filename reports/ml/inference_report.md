# ORIENT'IA — Rapport d'inférence

## 1. Objectif

Produire un classement des filières les plus adaptées
à un candidat à partir du modèle ML sélectionné.

## 2. Modèle

Modèle utilisé :

`best_model.joblib`

## 3. Candidat

Identifiant :

`STD_2026_0001`

## 4. Nombre de filières évaluées

16

## 5. Nombre de recommandations

Top-5

## 6. Résultats

| Rang | Filière | Score |
|---:|---|---:|
| 1 | Industrie Agroalimentaire (IAA) | 1.0000 |
| 2 | Agriculture et Élevage (AEE) | 0.1267 |
| 3 | Informatique Statistique Appliquée et Intelligence Artificielle (ISAIA) | 0.1033 |
| 4 | Pharmacologie et Industries Pharmaceutiques (PIP) | 0.0867 |
| 5 | Électro-Mécanique et Informatique Industrielle (EMII) | 0.0633 |


## 7. Meilleure recommandation

La filière classée première possède un score de :

**1.0000**

## 8. Interprétation

Le score représente la probabilité estimée par le modèle
que la paire candidat-filière corresponde à la classe
`Recommandée`.

Les filières sont ensuite classées par ordre décroissant
de ce score.

## 9. Fichier généré

`reports/ml/inference_predictions.csv`

## 10. Prochaine étape

Intégrer cette fonction d'inférence dans le backend/API
d'ORIENT'IA afin de permettre à l'application de recevoir
un profil candidat et de retourner dynamiquement ses
recommandations.
