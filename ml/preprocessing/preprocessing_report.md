# ORIENT'IA — Rapport de préprocessing
## 1. Objectif

Préparer les données synthétiques pour l'entraînement du système de recommandation de filières.
## 2. Problème ML

Le problème est formulé comme une recommandation candidat → filière.
Chaque ligne représente une paire candidat-filière.
## 3. Cible

`target = est_recommandee`

La cible est encodée :

- Oui → 1
- Non → 0
## 4. Prévention de la fuite de données

Les variables suivantes ont été exclues du modèle car elles peuvent être directement liées à la génération de la recommandation :

- `nom_complet`
- `est_recommandee`
- `score_compatibilite_cf`
- `est_admissible`
- `filiere_recommandee`
- `justification`

## 5. Feature engineering

- `nombre_competences`
- `nombre_matieres_fortes`
- `nombre_matieres_faibles`
- `nombre_centres_interet`

## 6. Séparation des données

- Train : 8400 lignes
- Validation : 1792 lignes
- Test : 1808 lignes

La séparation est effectuée par groupe de candidat afin d'éviter qu'un même candidat apparaisse dans plusieurs ensembles.

## 7. Features finales

- `parcours_id`
- `age`
- `sexe`
- `serie`
- `moyenne_generale`
- `preferences_env`
- `objectif_professionnel`
- `filieres_compatibles`
- `parcours_recommande`
- `score_compatibilite_student`
- `niveau_confiance`
- `filiere_nom`
- `filiere_parcours_id`
- `filiere_parcours_nom`
- `filiere_secteur`
- `nombre_competences`
- `nombre_matieres_fortes`
- `nombre_matieres_faibles`
- `nombre_centres_interet`

## 8. Fichiers produits

- `ml_dataset.csv`
- `X_train.csv`
- `X_validation.csv`
- `X_test.csv`
- `y_train.csv`
- `y_validation.csv`
- `y_test.csv`
- `feature_columns.txt`
- `preprocessing_report.md`
