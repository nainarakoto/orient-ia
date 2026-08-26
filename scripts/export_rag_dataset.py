import json
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "../data/formations/mentions_parcours.json")
OUTPUT_JSONL = os.path.join(BASE_DIR, "../data/processed/orientia_rag_dataset.jsonl")
OUTPUT_CSV_M2 = os.path.join(BASE_DIR, "../data/processed/dataset_orientation_m2.csv")

def exporter_donnees():
    print("🚀 Exportation des datasets M1 vers M2 et M3...\n")

    if not os.path.exists(JSON_PATH):
        print(f"❌ Fichier introuvable : {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        formations = json.load(f)

    # --- 1. Génération JSONL pour M3 (RAG) ---
    jsonl_records = []
    for f in formations:
        texte = (
            f"Parcours: {f['parcours']} ({f['mention']} - {f['niveau']}).\n"
            f"Description: {f['description']}\n"
            f"Matières clés: {', '.join(f['matieres_principales'])}.\n"
            f"Compétences: {', '.join(f['competences_developpees'])}.\n"
            f"Prérequis: {', '.join(f['prerequis'])}.\n"
            f"Débouchés: {', '.join(f['debouches'])}."
        )
        jsonl_records.append({
            "id": f["id_parcours"],
            "source_id": f["source_id"],
            "text": texte,
            "metadata": {
                "mention": f["mention"],
                "niveau": f["niveau"],
                "parcours": f["parcours"]
            }
        })

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f_out:
        for rec in jsonl_records:
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"✅ Corpus RAG (M3) généré -> {OUTPUT_JSONL}")

    # --- 2. Génération CSV pour M2 (ML) ---
    m2_rows = []
    for f in formations:
        m2_rows.append({
            "id_parcours": f["id_parcours"],
            "parcours": f["parcours"],
            "mention": f["mention"],
            "matieres": " | ".join(f["matieres_principales"]),
            "competences": " | ".join(f["competences_developpees"]),
            "prerequis": " | ".join(f["prerequis"]),
            "debouches": " | ".join(f["debouches"])
        })

    df = pd.DataFrame(m2_rows)
    df.to_csv(OUTPUT_CSV_M2, index=False, encoding="utf-8")
    print(f"✅ Catalogue M2 (ML) généré -> {OUTPUT_CSV_M2}")

if __name__ == "__main__":
    exporter_donnees()
