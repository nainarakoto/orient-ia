"""
chunking.py (v2 — corpus réel ISPM)
--------------------------------------
Transforme une fiche parsée (parser.py) en chunks exploitables par
le RAG. Remplace la version précédente qui travaillait sur des JSON
synthétiques.

Stratégie : un chunk par section réelle du document (ex. "1. Présentation
générale", "2. Matières principales"...). Le texte complet de la section
est conservé (pas résumé), pour permettre des citations fidèles.

Fonctionne à la fois pour :
- les fiches filière (formation_id = code filière, ex. "AEE")
- les documents d'information générale (formation_id = type_document,
  ex. "admission_et_frais") — utile pour les questions hors filières
  (frais, contacts, calendrier).
"""


def chunker_fiche(fiche: dict) -> list[dict]:
    """
    Entrée : une fiche telle que produite par parser.parser_corpus()
    Sortie : liste de chunks, chacun de la forme :
        {
            "texte": "...",
            "formation_id": "AEE" | "admission_et_frais",
            "type": "filiere" | "information_generale",
            "parcours": "..." ou None,
            "section": "1. Présentation générale",
            "sources_ids": ["SRC_SITE_ISPM", ...],
            "source_id": "SRC_SITE_ISPM",   # source principale (1ère de la liste), pour compat contrat existant
        }
    """
    identifiant = fiche["identifiant"]
    type_fiche = fiche["type"]
    parcours = fiche.get("parcours")
    sources_ids = fiche.get("sources_ids", [])
    source_principale = sources_ids[0] if sources_ids else None

    chunks = []
    for titre_section, texte_section in fiche["sections"].items():
        if not texte_section.strip():
            continue

        # Préfixe de contexte : aide le modèle d'embeddings à situer le
        # passage (ex. "Filière AEE — Prérequis et profil recherché : ...")
        prefixe = f"{fiche['titre']} — {titre_section} : "

        chunks.append({
            "texte": prefixe + texte_section,
            "formation_id": identifiant,
            "type": type_fiche,
            "parcours": parcours,
            "section": titre_section,
            "sources_ids": sources_ids,
            "source_id": source_principale,
        })

    return chunks


def chunker_tout_le_corpus(fiches: list[dict]) -> list[dict]:
    """Applique chunker_fiche() à toutes les fiches et fusionne les résultats."""
    tous_chunks = []
    for fiche in fiches:
        tous_chunks.extend(chunker_fiche(fiche))
    return tous_chunks


if __name__ == "__main__":
    from parser import parser_corpus

    fiches = parser_corpus("data/corpus_ispm.md")
    chunks = chunker_tout_le_corpus(fiches)

    print(f"{len(chunks)} chunks générés à partir de {len(fiches)} fiches.\n")

    print("--- Exemple : chunks de la fiche AEE ---")
    for c in chunks:
        if c["formation_id"] == "AEE":
            print(f"[{c['section']}] ({len(c['texte'])} caractères)")
            print(f"   {c['texte'][:120]}...\n")

    print("--- Exemple : chunks d'un document d'information générale ---")
    for c in chunks:
        if c["formation_id"] == "admission_et_frais":
            print(f"[{c['section']}] ({len(c['texte'])} caractères)")
            print(f"   {c['texte'][:120]}...\n")

    print("OK — chunking sur corpus réel fonctionnel.")