import json
import os
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "../data/formations/mentions_parcours.json")
CSV_SOURCES_PATH = os.path.join(BASE_DIR, "../data/sources/registre_sources.csv")

def valider_donnees():
    print("🔍 Validation du corpus M1 en cours...\n")
    erreurs = 0

    if not os.path.exists(JSON_PATH):
        print(f"❌ Erreur : Fichier introuvable -> {JSON_PATH}")
        sys.exit(1)

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            formations = json.load(f)
        print(f"✅ JSON valide : {len(formations)} parcours recensés.")
    except Exception as e:
        print(f"❌ Erreur de lecture du JSON : {e}")
        sys.exit(1)

    if not os.path.exists(CSV_SOURCES_PATH):
        print(f"❌ Erreur : Fichier introuvable -> {CSV_SOURCES_PATH}")
        sys.exit(1)

    try:
        df_sources = pd.read_csv(CSV_SOURCES_PATH)
        sources_ids = set(df_sources["id"].tolist())
        print(f"✅ CSV Registre valide : {len(df_sources)} sources enregistrées.")
    except Exception as e:
        print(f"❌ Erreur de lecture du CSV sources : {e}")
        sys.exit(1)

    print("\n--- Contrôle de Traçabilité ---")
    champs_obligatoires = [
        "id_parcours", "mention", "parcours", "niveau",
        "matieres_principales", "competences_developpees",
        "prerequis", "debouches", "source_id"
    ]

    for item in formations:
        parcours_id = item.get("id_parcours", "INCONNU")
        
        for champ in champs_obligatoires:
            if champ not in item or not item[champ]:
                print(f"⚠️ Champ manquant ou vide '{champ}' pour : {parcours_id}")
                erreurs += 1

        s_id = item.get("source_id")
        if s_id not in sources_ids:
            print(f"❌ Source non référencée '{s_id}' pour le parcours : {parcours_id}")
            erreurs += 1
        else:
            print(f"  -> {parcours_id} [OK] (Lié à {s_id})")

    print("\n-------------------------------")
    if erreurs == 0:
        print("🎉 Validation réussie ! Les fichiers sont conformes et prêts pour M2, M3 et M4.")
    else:
        print(f"❌ Validation échouée avec {erreurs} anomalie(s) à corriger.")
        sys.exit(1)

if __name__ == "__main__":
    valider_donnees()
