"""
parser.py
---------
Transforme le fichier corpus brut (Markdown avec plusieurs fiches séparées
par des en-têtes YAML) en une liste de "fiches" structurées (dicts Python),
exploitables ensuite par chunking.py.

Format attendu du fichier source (voir data/corpus_ispm.md) :

    ---
    titre: "Fiche Filière AEE"
    parcours: "Biotechnologie et Agronomie"
    filiere: "AEE"
    sources_ids:
      - "SRC_SITE_ISPM"
      - "SRC_SITE_TOROHAY"
    ---

    # Parcours : Biotechnologie et Agronomie
    ## Filière : AEE (...)

    ### 1. Présentation générale
    Texte...

    ### 2. Matières principales
    - Item 1
    - Item 2
    ...

Deux types de fiches sont gérés :
- fiches "filiere" (métadonnées : parcours, filiere)
- fiches "information_generale" (métadonnées : categorie, type_document)

Chaque fiche parsée a la forme :
{
    "type": "filiere" | "information_generale",
    "titre": "...",
    "identifiant": "AEE" | "admission_et_frais",   # utilisé comme formation_id
    "parcours": "..." (optionnel, seulement pour type="filiere"),
    "sources_ids": ["SRC_SITE_ISPM", ...],
    "sections": {
        "1. Présentation générale": "texte complet de la section...",
        "2. Matières principales": "texte complet (avec puces)...",
        ...
    }
}
"""

import re
import yaml


def _parser_yaml(bloc_yaml: str) -> dict:
    """Parse un bloc d'en-tête YAML (entre les deux premiers ---)."""
    return yaml.safe_load(bloc_yaml) or {}


def _parser_sections(corps_markdown: str) -> dict:
    """
    Découpe le corps Markdown d'une fiche en sections, à partir des
    titres de niveau 3 (### 1. ..., ### 2. ..., etc.).
    Les titres de niveau 1 (#) et 2 (##) sont ignorés (ce sont juste
    des titres de présentation, pas des sections de contenu utile).

    Retourne un dict {titre_section: texte_section}.
    """
    sections = {}

    # Découpe sur les lignes commençant par "### "
    morceaux = re.split(r"(?m)^###\s+", corps_markdown)

    for morceau in morceaux[1:]:  # le 1er morceau (avant le 1er ###) est ignoré (titres # et ##)
        lignes = morceau.strip().split("\n", 1)
        titre_section = lignes[0].strip()
        texte_section = lignes[1].strip() if len(lignes) > 1 else ""
        # Nettoyage : on garde le texte tel quel (utile pour la lisibilité
        # des extraits cités), on retire juste les espaces superflus
        texte_section = re.sub(r"\n{3,}", "\n\n", texte_section)
        if texte_section:
            sections[titre_section] = texte_section

    return sections


def parser_corpus(chemin_fichier: str) -> list[dict]:
    """
    Point d'entrée : lit le fichier corpus et retourne la liste des fiches
    structurées.
    """
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Le fichier alterne : (vide), yaml1, corps1, yaml2, corps2, ...
    segments = re.split(r"(?m)^---\s*$", contenu)
    segments = [s for s in segments if s.strip() != ""]

    if len(segments) % 2 != 0:
        raise ValueError(
            f"Nombre de segments impair ({len(segments)}) après découpage sur '---'. "
            f"Le fichier corpus semble mal formé (frontmatter YAML incomplet quelque part)."
        )

    fiches = []
    for i in range(0, len(segments), 2):
        bloc_yaml = segments[i]
        corps = segments[i + 1]

        meta = _parser_yaml(bloc_yaml)
        sections = _parser_sections(corps)

        if not sections:
            # Aucune section trouvée : probablement un souci de format, on prévient
            print(f"[parser] ATTENTION : aucune section détectée pour la fiche '{meta.get('titre', '?')}'")

        sources_ids = meta.get("sources_ids", [])
        if isinstance(sources_ids, str):
            sources_ids = [sources_ids]

        if "filiere" in meta:
            # Fiche filière
            fiche = {
                "type": "filiere",
                "titre": meta.get("titre", ""),
                "identifiant": meta.get("filiere", ""),
                "parcours": meta.get("parcours", ""),
                "sources_ids": sources_ids,
                "sections": sections,
            }
        else:
            # Document d'information générale (contacts, admissions, calendrier...)
            fiche = {
                "type": "information_generale",
                "titre": meta.get("titre", ""),
                "identifiant": meta.get("type_document", meta.get("titre", "info")),
                "parcours": None,
                "sources_ids": sources_ids,
                "sections": sections,
            }

        fiches.append(fiche)

    return fiches


if __name__ == "__main__":
    import sys
    import json

    chemin = sys.argv[1] if len(sys.argv) > 1 else "data/corpus_ispm.md"
    fiches = parser_corpus(chemin)

    print(f"{len(fiches)} fiche(s) trouvée(s) :\n")
    for f in fiches:
        nb_sections = len(f["sections"])
        print(f"- [{f['type']}] {f['identifiant']} — {f['titre']} ({nb_sections} sections, {len(f['sources_ids'])} source(s))")

    print("\n--- Exemple détaillé de la 1ère fiche ---")
    print(json.dumps(fiches[0], ensure_ascii=False, indent=2)[:1500])