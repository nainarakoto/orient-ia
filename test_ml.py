from ml.service import recommander_parcours_ml, normaliser_objectif_professionnel

# Test 1 : vérifier le mapping en isolation
print("=== Test du normaliseur ===")
print(normaliser_objectif_professionnel("Ingénieur"))
print(normaliser_objectif_professionnel("je veux bosser dans la tech"))
print(normaliser_objectif_professionnel("un métier scientifique"))
print()

# Test 2 : pipeline complet avec un objectif vague (comme un vrai utilisateur)
print("=== Recommandations avec objectif vague ===")
resultats = recommander_parcours_ml(
    age=18,
    sexe="M",
    serie="C",
    moyenne_generale=14.0,
    preferences_env="Laboratoire & R&D",
    objectif_professionnel="je veux travailler dans la tech",
    matieres_fortes=["Mathématiques", "Physique"],
    matieres_faibles=["Anglais", "LV2"],
    centres_interet=["Programmation & Code"],
    competences=["Python", "Statistiques"],
    top_k=5,
)
for r in resultats:
    print(r)