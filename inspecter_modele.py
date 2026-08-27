import joblib

model = joblib.load("ml/models/best_model.joblib")

print("Type du modèle :", type(model))
print()

preprocessing = model.named_steps["preprocessing"]
print("Transformers du ColumnTransformer 'preprocessing' :")
for nom_t, transfo, colonnes in preprocessing.transformers_:
    print(f"\n--- Transformer '{nom_t}' sur colonnes {colonnes} ---")
    print("  Type :", type(transfo))

    # Cas 1 : le transformer a directement categories_ (OneHotEncoder direct)
    if hasattr(transfo, "categories_"):
        for col, cats in zip(colonnes, transfo.categories_):
            print(f"    Colonne '{col}' -> catégories : {list(cats)}")

    # Cas 2 : c'est un Pipeline (ex: Imputer + OneHotEncoder) -> on descend dans les steps
    elif hasattr(transfo, "named_steps"):
        print("    C'est un sous-Pipeline, étapes :", list(transfo.named_steps.keys()))
        for sous_nom, sous_etape in transfo.named_steps.items():
            print(f"    Étape '{sous_nom}' :", type(sous_etape))
            if hasattr(sous_etape, "categories_"):
                for col, cats in zip(colonnes, sous_etape.categories_):
                    print(f"      Colonne '{col}' -> catégories : {list(cats)}")
            if hasattr(sous_etape, "statistics_"):
                print(f"      Valeurs de remplissage (imputer) : {sous_etape.statistics_}")

    else:
        print("    (pas de categories_ ni de sous-pipeline trouvé - à inspecter manuellement)")

print()
print("=== Statistiques du bloc numérique (pour calibrer les valeurs par défaut) ===")
numeric_transfo = None
for nom_t, transfo, colonnes in preprocessing.transformers_:
    if nom_t == "numeric":
        numeric_transfo = transfo
        numeric_colonnes = colonnes

if numeric_transfo is not None:
    if hasattr(numeric_transfo, "named_steps"):
        for sous_nom, sous_etape in numeric_transfo.named_steps.items():
            if hasattr(sous_etape, "mean_"):
                print("Moyennes (scaler) :", dict(zip(numeric_colonnes, sous_etape.mean_)))
            if hasattr(sous_etape, "statistics_"):
                print("Valeurs de remplissage (imputer) :", dict(zip(numeric_colonnes, sous_etape.statistics_)))
    else:
        if hasattr(numeric_transfo, "mean_"):
            print("Moyennes (scaler) :", dict(zip(numeric_colonnes, numeric_transfo.mean_)))