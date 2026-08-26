"""
chunking.py
-----------
Transforme une fiche formation (JSON de M1) en plusieurs petits blocs de texte
(chunks), chacun avec ses métadonnées (source_id, formation_id, section).

Stratégie choisie : un chunk par section logique (matières, compétences,
prérequis, débouchés) plutôt qu'un découpage aveugle par nombre de caractères.
C'est plus lisible, plus pertinent pour des fiches courtes comme des formations,
et ça facilite les citations précises.
"""


def chunker_formation(formation: dict) -> list[dict]:
    """
    Entrée : une fiche formation (dict, format livré par M1)
    Sortie : liste de chunks, chacun de la forme :
        {
            "texte": "...",
            "formation_id": "...",
            "source_id": "...",
            "section": "..."
        }
    """
    formation_id = formation.get("id", "inconnu")
    sources = formation.get("sources", [])
    source_id = sources[0] if sources else None  # simplification : 1ère source associée

    nom = formation.get("nom", "")
    niveau = formation.get("niveau", "")
    diplome = formation.get("diplome", "")

    chunks = []

    # Chunk 1 — informations générales
    chunks.append({
        "texte": f"{nom} ({niveau}, {diplome}), mention {formation.get('mention', '')}.",
        "formation_id": formation_id,
        "source_id": source_id,
        "section": "generalites",
    })

    # Chunk 2 — matières
    matieres = formation.get("matieres", [])
    if matieres:
        chunks.append({
            "texte": f"Matières enseignées en {nom} : {', '.join(matieres)}.",
            "formation_id": formation_id,
            "source_id": source_id,
            "section": "matieres",
        })

    # Chunk 3 — compétences
    competences = formation.get("competences", [])
    if competences:
        chunks.append({
            "texte": f"Compétences développées en {nom} : {', '.join(competences)}.",
            "formation_id": formation_id,
            "source_id": source_id,
            "section": "competences",
        })

    # Chunk 4 — prérequis
    prerequis = formation.get("prerequis", [])
    if prerequis:
        chunks.append({
            "texte": f"Prérequis pour intégrer {nom} : {', '.join(prerequis)}.",
            "formation_id": formation_id,
            "source_id": source_id,
            "section": "prerequis",
        })

    # Chunk 5 — débouchés et métiers
    debouches = formation.get("debouches", [])
    metiers = formation.get("metiers_associes", [])
    if debouches or metiers:
        infos = debouches + metiers
        chunks.append({
            "texte": f"Débouchés et métiers pour {nom} : {', '.join(infos)}.",
            "formation_id": formation_id,
            "source_id": source_id,
            "section": "debouches",
        })

    # Chunk 6 — passerelles (optionnel, seulement si renseigné)
    passerelles = formation.get("passerelles", [])
    if passerelles:
        chunks.append({
            "texte": f"Passerelles possibles après {nom} : {', '.join(passerelles)}.",
            "formation_id": formation_id,
            "source_id": source_id,
            "section": "passerelles",
        })

    return chunks


def chunker_toutes_formations(formations: list[dict]) -> list[dict]:
    """Applique chunker_formation() à une liste de formations et fusionne les résultats."""
    tous_chunks = []
    for f in formations:
        tous_chunks.extend(chunker_formation(f))
    return tous_chunks


if __name__ == "__main__":
    # Test rapide avec une fiche fictive
    formation_test = {
        "id": "info-l3",
        "nom": "Licence Informatique",
        "mention": "Informatique",
        "niveau": "Licence 3",
        "diplome": "Licence",
        "matieres": ["Algorithmique", "Bases de données", "Réseaux"],
        "competences": ["Programmation Python", "Gestion de projet"],
        "prerequis": ["Bases en mathématiques", "Notions de programmation"],
        "debouches": ["Développeur", "Analyste de données"],
        "metiers_associes": ["Développeur logiciel", "Data analyst"],
        "passerelles": ["Master Informatique"],
        "sources": ["src-test-01"],
    }

    chunks = chunker_formation(formation_test)
    print(f"{len(chunks)} chunks générés :\n")
    for c in chunks:
        print(f"[{c['section']}] {c['texte']}")
    print("\nOK — le module chunking fonctionne.")