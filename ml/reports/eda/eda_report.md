# ORIENT'IA — Rapport EDA

Analyse exploratoire des données synthétiques destinées au système de recommandation.

## 1. Vue générale

- Nombre de datasets : **13**
- Nombre total de lignes : **14522**
- Nombre total de colonnes : **121**
- Cellules manquantes : **0**
- Doublons : **0**

## 2. Datasets analysés

| dataset                             |   rows |   columns |   missing_cells |   missing_percentage |   duplicates |   memory_mb |
|:------------------------------------|-------:|----------:|----------------:|---------------------:|-------------:|------------:|
| admission_requirements              |     16 |         5 |               0 |                    0 |            0 |        0.01 |
| candidat_filiere                    |  12000 |         6 |               0 |                    0 |            0 |        3.2  |
| competences                         |     64 |         4 |               0 |                    0 |            0 |        0.02 |
| formations_etablissement            |     16 |        11 |               0 |                    0 |            0 |        0.03 |
| metiers                             |     64 |         4 |               0 |                    0 |            0 |        0.02 |
| professional_validation             |    250 |         6 |               0 |                    0 |            0 |        0.08 |
| profils_etudiants_synthetiques      |    750 |        19 |               0 |                    0 |            0 |        1.45 |
| profils_professionnels_synthetiques |    250 |        16 |               0 |                    0 |            0 |        0.31 |
| profils_synthetiques                |   1000 |         9 |               0 |                    0 |            0 |        0.57 |
| serie_filiere_matrix                |      9 |        17 |               0 |                    0 |            0 |        0.01 |
| sources                             |      2 |         4 |               0 |                    0 |            0 |        0    |
| subject_filiere_matrix              |     22 |        17 |               0 |                    0 |            0 |        0.02 |
| terminal_subjects                   |     79 |         3 |               0 |                    0 |            0 |        0.01 |

## 3. Valeurs manquantes

Aucune valeur manquante détectée.

## 4. Doublons

| dataset                             |   rows |   duplicates |   duplicate_percentage |
|:------------------------------------|-------:|-------------:|-----------------------:|
| admission_requirements              |     16 |            0 |                      0 |
| candidat_filiere                    |  12000 |            0 |                      0 |
| competences                         |     64 |            0 |                      0 |
| formations_etablissement            |     16 |            0 |                      0 |
| metiers                             |     64 |            0 |                      0 |
| professional_validation             |    250 |            0 |                      0 |
| profils_etudiants_synthetiques      |    750 |            0 |                      0 |
| profils_professionnels_synthetiques |    250 |            0 |                      0 |
| profils_synthetiques                |   1000 |            0 |                      0 |
| serie_filiere_matrix                |      9 |            0 |                      0 |
| sources                             |      2 |            0 |                      0 |
| subject_filiere_matrix              |     22 |            0 |                      0 |
| terminal_subjects                   |     79 |            0 |                      0 |

## 5. Variables numériques

| dataset                             | column                            |   count |       mean |       std |     min |       q1 |   median |        q3 |     max |
|:------------------------------------|:----------------------------------|--------:|-----------:|----------:|--------:|---------:|---------:|----------:|--------:|
| admission_requirements              | note_minimale_requise             |      16 |   10       |  0        |   10    |   10     |   10     |   10      |   10    |
| candidat_filiere                    | score_compatibilite               |   12000 |   67.1695  | 15.135    |   22.42 |   52.21  |   72.93  |   79.61   |  100    |
| professional_validation             | adequation_score                  |     250 |   84.3208  |  8.58062  |   70.04 |   76.7   |   84.475 |   92.0625 |   98.88 |
| profils_etudiants_synthetiques      | age                               |     750 |   18.4987  |  1.75217  |   16    |   17     |   19     |   20      |   21    |
| profils_etudiants_synthetiques      | moyenne_generale                  |     750 |   13.0375  |  0.988707 |   10.08 |   12.34  |   13.06  |   13.6475 |   15.99 |
| profils_etudiants_synthetiques      | score_compatibilite               |     750 |   67.3098  | 15.119    |   28.15 |   52.95  |   72.605 |   79.535  |   98.14 |
| profils_professionnels_synthetiques | age                               |     250 |   36.264   |  7.91891  |   23    |   30     |   36.5   |   42.75   |   50    |
| profils_professionnels_synthetiques | annee_obtention                   |     250 | 2015.38    |  5.75369  | 2006    | 2011     | 2015     | 2020      | 2025    |
| profils_professionnels_synthetiques | annees_experience                 |     250 |   10.616   |  5.75369  |    1    |    6     |   11     |   15      |   20    |
| profils_professionnels_synthetiques | adequation_formation_metier_score |     250 |   84.3208  |  8.58062  |   70.04 |   76.7   |   84.475 |   92.0625 |   98.88 |
| profils_synthetiques                | age                               |    1000 |   22.94    |  8.78451  |   16    |   17     |   20     |   21.5    |   50    |
| profils_synthetiques                | score_adéquation_global           |    1000 |   71.5626  | 15.6219   |   28.15 |   57.515 |   75.68  |   82.3625 |   98.88 |
| terminal_subjects                   | coefficient                       |      79 |    3.39241 |  1.47124  |    2    |    2     |    3     |    4.5    |    7    |

## 6. Variables catégorielles

| dataset                             | column                 |   unique_values | most_frequent                                                                                                                                                              |   most_frequent_count |
|:------------------------------------|:-----------------------|----------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------:|
| admission_requirements              | filiere_code           |              16 | AEE                                                                                                                                                                        |                     1 |
| admission_requirements              | series_autorisees      |              14 | A; A1; A2; L; G; D                                                                                                                                                         |                     2 |
| admission_requirements              | matieres_obligatoires  |               5 | Mathématiques                                                                                                                                                              |                     7 |
| admission_requirements              | prerequis_detail       |              16 | Aisance en langues, sensibilité écologique et ouverture culturelle.                                                                                                        |                     1 |
| candidat_filiere                    | candidat_id            |             750 | STD_2026_0001                                                                                                                                                              |                    16 |
| candidat_filiere                    | filiere_code           |              16 | AEE                                                                                                                                                                        |                   750 |
| candidat_filiere                    | parcours_id            |               5 | P3                                                                                                                                                                         |                  3000 |
| candidat_filiere                    | est_admissible         |               3 | Oui                                                                                                                                                                        |                  5223 |
| candidat_filiere                    | est_recommandee        |               2 | Non                                                                                                                                                                        |                 11250 |
| competences                         | competence_id          |              64 | COMP_001                                                                                                                                                                   |                     1 |
| competences                         | nom_competence         |              64 | Agronomie                                                                                                                                                                  |                     1 |
| competences                         | filiere_code           |              16 | AEE                                                                                                                                                                        |                     4 |
| competences                         | secteur                |              16 | Agriculture / Agronomie                                                                                                                                                    |                     4 |
| formations_etablissement            | code_filiere           |              16 | AEE                                                                                                                                                                        |                     1 |
| formations_etablissement            | nom_complet            |              16 | Agriculture et Élevage                                                                                                                                                     |                     1 |
| formations_etablissement            | parcours_id            |               5 | P3                                                                                                                                                                         |                     4 |
| formations_etablissement            | parcours_nom           |               5 | Informatique et Télécommunication                                                                                                                                          |                     4 |
| formations_etablissement            | description            |              16 | Analyse conjoncturelle, pilotage budgétaire, évaluation d'impact et méthodologies de gestion de projets complexes.                                                         |                     1 |
| formations_etablissement            | matieres_principales   |              13 | Mathématiques; Mathématiques appliquées; Sciences Physiques, Chimiques et Technologie (SPCT); Sciences Physiques et Chimiques; Physique appliquée / Technologie; Anglais   |                     2 |
| formations_etablissement            | competences_visees     |              16 | Agronomie; Zootechnie; Analyse des sols; Gestion d'exploitation                                                                                                            |                     1 |
| formations_etablissement            | prerequis              |              16 | Aisance en langues, sensibilité écologique et ouverture culturelle.                                                                                                        |                     1 |
| formations_etablissement            | series_admissibles     |              14 | A; A1; A2; L; G; D                                                                                                                                                         |                     2 |
| formations_etablissement            | metiers_accessibles    |              16 | Agronome; Conseiller agricole; Chef d'exploitation; Responsable d'élevage                                                                                                  |                     1 |
| formations_etablissement            | secteur_professionnel  |              16 | Agriculture / Agronomie                                                                                                                                                    |                     1 |
| metiers                             | metier_id              |              64 | MET_001                                                                                                                                                                    |                     1 |
| metiers                             | intitule_metier        |              64 | Administrateur Réseaux & TIC                                                                                                                                               |                     1 |
| metiers                             | filiere_code           |              16 | AEE                                                                                                                                                                        |                     4 |
| metiers                             | parcours_nom           |               5 | Informatique et Télécommunication                                                                                                                                          |                    16 |
| professional_validation             | professional_id        |             250 | PRO_2026_0001                                                                                                                                                              |                     1 |
| professional_validation             | filiere_etudiee        |              16 | EMII                                                                                                                                                                       |                    16 |
| professional_validation             | parcours_id            |               5 | P3                                                                                                                                                                         |                    64 |
| professional_validation             | metier_exerce          |              61 | Data Analyst                                                                                                                                                               |                     9 |
| professional_validation             | parcours_valide        |               1 | Oui                                                                                                                                                                        |                   250 |
| profils_etudiants_synthetiques      | student_id             |             750 | STD_2026_0001                                                                                                                                                              |                     1 |
| profils_etudiants_synthetiques      | nom_complet            |             194 | Nary Rabenjamina                                                                                                                                                           |                    10 |
| profils_etudiants_synthetiques      | sexe                   |               2 | M                                                                                                                                                                          |                   389 |
| profils_etudiants_synthetiques      | serie                  |               9 | A1                                                                                                                                                                         |                    84 |
| profils_etudiants_synthetiques      | notes_detaillees       |             750 | Mathématiques appliquées:10.38; Physique appliquée / Technologie:16.64; Dessin technique:10.14; Français:12.51; Anglais:9.66; Philosophie:8.41; EPS:10.85                  |                     1 |
| profils_etudiants_synthetiques      | matieres_fortes        |             169 | Philosophie; LV2                                                                                                                                                           |                    30 |
| profils_etudiants_synthetiques      | matieres_faibles       |             107 | SVT / Sciences humaines; Mathématiques                                                                                                                                     |                    32 |
| profils_etudiants_synthetiques      | centres_interet        |              90 | Jeux de Stratégie; Musique                                                                                                                                                 |                    16 |
| profils_etudiants_synthetiques      | competences            |             190 | Développement Web/Mobile; Infographie & 3D; Résolution de problèmes                                                                                                        |                    11 |
| profils_etudiants_synthetiques      | preferences_env        |               5 | Laboratoire & R&D                                                                                                                                                          |                   162 |
| profils_etudiants_synthetiques      | objectif_professionnel |              64 | Data Scientist                                                                                                                                                             |                    21 |
| profils_etudiants_synthetiques      | filieres_compatibles   |             660 | DTJA; ESIIA; CAA                                                                                                                                                           |                     3 |
| profils_etudiants_synthetiques      | filiere_recommandee    |              16 | CAA                                                                                                                                                                        |                    47 |
| profils_etudiants_synthetiques      | parcours_recommande    |               5 | Informatique et Télécommunication                                                                                                                                          |                   188 |
| profils_etudiants_synthetiques      | niveau_confiance       |               3 | Élevé                                                                                                                                                                      |                   322 |
| profils_etudiants_synthetiques      | justification          |             725 | Excellente adéquation avec la série D et bonnes notes en SVT, Sciences Physiques, Chimiques et Technologie (SPCT). Profil aligné avec l'objectif de Responsable d'élevage. |                     3 |
| profils_professionnels_synthetiques | professional_id        |             250 | PRO_2026_0001                                                                                                                                                              |                     1 |
| profils_professionnels_synthetiques | nom_complet            |             148 | Nomena Andriantsitohaina                                                                                                                                                   |                     6 |
| profils_professionnels_synthetiques | sexe                   |               2 | M                                                                                                                                                                          |                   135 |
| profils_professionnels_synthetiques | a_etudie_ispm          |               1 | Oui                                                                                                                                                                        |                   250 |
| profils_professionnels_synthetiques | formation_suivie       |              16 | Diplôme ISPM - Electronique Système Informatique et Intelligence Artificielle                                                                                              |                    16 |
| profils_professionnels_synthetiques | parcours_ispm          |               5 | Informatique et Télécommunication                                                                                                                                          |                    64 |
| profils_professionnels_synthetiques | filiere_etudiee        |              16 | EMII                                                                                                                                                                       |                    16 |
| profils_professionnels_synthetiques | competences            |             142 | C/C++ embarqué; Électronique numérique; Gestion de projet; Leadership                                                                                                      |                     5 |
| profils_professionnels_synthetiques | specialisation         |              16 | Electronique Système Informatique et Intelligence Artificielle                                                                                                             |                    16 |
| profils_professionnels_synthetiques | metier_actuel          |              61 | Data Analyst                                                                                                                                                               |                     9 |
| profils_professionnels_synthetiques | secteur_professionnel  |              16 | Bâtiment et Travaux Publics (BTP)                                                                                                                                          |                    16 |
| profils_professionnels_synthetiques | matieres_cles_retenues |              11 | Mathématiques; Mathématiques appliquées; Sciences Physiques, Chimiques et Technologie (SPCT)                                                                               |                    48 |
| profils_synthetiques                | profile_id             |            1000 | PRO_2026_0001                                                                                                                                                              |                     1 |
| profils_synthetiques                | type_profil            |               2 | Étudiant                                                                                                                                                                   |                   750 |
| profils_synthetiques                | sexe                   |               2 | M                                                                                                                                                                          |                   524 |
| profils_synthetiques                | serie_ou_filiere       |              25 | A1                                                                                                                                                                         |                    84 |
| profils_synthetiques                | competences_clefs      |             332 | Développement Web/Mobile; Infographie & 3D; Résolution de problèmes                                                                                                        |                    11 |
| profils_synthetiques                | objectif_ou_metier     |              64 | Data Scientist                                                                                                                                                             |                    24 |
| profils_synthetiques                | filiere_associee       |              16 | EMII                                                                                                                                                                       |                    63 |
| serie_filiere_matrix                | serie                  |               9 | A                                                                                                                                                                          |                     1 |
| serie_filiere_matrix                | AEE                    |               2 | Compatible                                                                                                                                                                 |                     6 |
| serie_filiere_matrix                | IAA                    |               2 | Non Compatible                                                                                                                                                             |                     5 |
| serie_filiere_matrix                | PIP                    |               2 | Non Compatible                                                                                                                                                             |                     6 |
| serie_filiere_matrix                | EMII                   |               2 | Non Compatible                                                                                                                                                             |                     5 |
| serie_filiere_matrix                | GCA                    |               2 | Non Compatible                                                                                                                                                             |                     5 |
| serie_filiere_matrix                | ICMP                   |               2 | Non Compatible                                                                                                                                                             |                     5 |
| serie_filiere_matrix                | ESIIA                  |               2 | Non Compatible                                                                                                                                                             |                     6 |
| serie_filiere_matrix                | IGGLIA                 |               2 | Compatible                                                                                                                                                                 |                     8 |
| serie_filiere_matrix                | IMTICIA                |               1 | Compatible                                                                                                                                                                 |                     9 |
| serie_filiere_matrix                | ISAIA                  |               2 | Non Compatible                                                                                                                                                             |                     5 |
| serie_filiere_matrix                | TEE                    |               2 | Compatible                                                                                                                                                                 |                     7 |
| serie_filiere_matrix                | TEH                    |               2 | Compatible                                                                                                                                                                 |                     6 |
| serie_filiere_matrix                | CAA                    |               2 | Compatible                                                                                                                                                                 |                     8 |
| serie_filiere_matrix                | DTJA                   |               2 | Compatible                                                                                                                                                                 |                     6 |
| serie_filiere_matrix                | EMP                    |               2 | Compatible                                                                                                                                                                 |                     7 |
| serie_filiere_matrix                | FIC                    |               2 | Non Compatible                                                                                                                                                             |                     5 |
| sources                             | source_id              |               2 | SRC_01                                                                                                                                                                     |                     1 |
| sources                             | nom                    |               2 | Base Données Baccalauréat                                                                                                                                                  |                     1 |
| sources                             | type                   |               2 | Officiel                                                                                                                                                                   |                     1 |
| sources                             | description            |               2 | Référentiel officiel des 5 parcours et 16 filières.                                                                                                                        |                     1 |
| subject_filiere_matrix              | matiere                |              22 | Anglais                                                                                                                                                                    |                     1 |
| subject_filiere_matrix              | AEE                    |               2 | Faible                                                                                                                                                                     |                    11 |
| subject_filiere_matrix              | IAA                    |               2 | Faible                                                                                                                                                                     |                    11 |
| subject_filiere_matrix              | PIP                    |               2 | Faible                                                                                                                                                                     |                    11 |
| subject_filiere_matrix              | EMII                   |               2 | Faible                                                                                                                                                                     |                    15 |
| subject_filiere_matrix              | GCA                    |               2 | Faible                                                                                                                                                                     |                    15 |
| subject_filiere_matrix              | ICMP                   |               2 | Faible                                                                                                                                                                     |                    14 |
| subject_filiere_matrix              | ESIIA                  |               2 | Faible                                                                                                                                                                     |                    15 |
| subject_filiere_matrix              | IGGLIA                 |               2 | Faible                                                                                                                                                                     |                    16 |
| subject_filiere_matrix              | IMTICIA                |               2 | Faible                                                                                                                                                                     |                    14 |
| subject_filiere_matrix              | ISAIA                  |               2 | Faible                                                                                                                                                                     |                    16 |
| subject_filiere_matrix              | TEE                    |               2 | Faible                                                                                                                                                                     |                    14 |
| subject_filiere_matrix              | TEH                    |               2 | Faible                                                                                                                                                                     |                    16 |
| subject_filiere_matrix              | CAA                    |               2 | Faible                                                                                                                                                                     |                    14 |
| subject_filiere_matrix              | DTJA                   |               2 | Faible                                                                                                                                                                     |                    16 |
| subject_filiere_matrix              | EMP                    |               2 | Faible                                                                                                                                                                     |                    15 |
| subject_filiere_matrix              | FIC                    |               2 | Faible                                                                                                                                                                     |                    15 |
| terminal_subjects                   | serie                  |               9 | L                                                                                                                                                                          |                    10 |
| terminal_subjects                   | matiere                |              22 | Anglais                                                                                                                                                                    |                     9 |

## 7. Valeurs aberrantes

| dataset                             | column                            |   outliers |   percentage |
|:------------------------------------|:----------------------------------|-----------:|-------------:|
| profils_synthetiques                | age                               |        199 |        19.9  |
| profils_etudiants_synthetiques      | moyenne_generale                  |          5 |         0.67 |
| admission_requirements              | note_minimale_requise             |          0 |         0    |
| professional_validation             | adequation_score                  |          0 |         0    |
| candidat_filiere                    | score_compatibilite               |          0 |         0    |
| profils_etudiants_synthetiques      | age                               |          0 |         0    |
| profils_etudiants_synthetiques      | score_compatibilite               |          0 |         0    |
| profils_professionnels_synthetiques | annee_obtention                   |          0 |         0    |
| profils_professionnels_synthetiques | age                               |          0 |         0    |
| profils_professionnels_synthetiques | annees_experience                 |          0 |         0    |
| profils_professionnels_synthetiques | adequation_formation_metier_score |          0 |         0    |
| profils_synthetiques                | score_adéquation_global           |          0 |         0    |
| terminal_subjects                   | coefficient                       |          0 |         0    |

## 8. Conclusion EDA

L'EDA doit être utilisée pour décider :

1. quelles variables conserver ;
2. quelles variables nettoyer ;
3. quelles variables encoder ;
4. quelles variables normaliser ;
5. quelles variables utiliser pour le ML ;
6. quelle variable représente la cible ;
7. quelles variables pourraient créer un biais ou une fuite de données.
