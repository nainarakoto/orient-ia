"""
Security guard — ORIENT'IA (§16, §21 du plan)

Filtre appliqué AVANT l'appel à l'agent (sur la question brute) et APRÈS
(sur la réponse générée), pour couvrir les scénarios de risque explicitement
testés par le jury (T26-T32) :
  - prompt injection ("ignore tes instructions...")
  - critères discriminatoires (genre, âge...)
  - profilage psychologique
  - confusion conseil / décision officielle (couverte par la mention légale,
    injectée systématiquement côté schemas.RecommendResponse)

MVP volontairement simple (mots-clés + règles). À muscler avec un vrai
classifieur ou des règles plus fines si le temps le permet.
"""
from __future__ import annotations
import re
from dataclasses import dataclass

# --- Signaux de prompt injection / tentative de contournement -------------
INJECTION_PATTERNS = [
    r"ignore\s+(tes|les)\s+instructions",
    r"ignore\s+les\s+documents",
    r"affirme\s+que",
    r"fais\s+comme\s+si",
    r"oublie\s+(tes|les)\s+r[eè]gles",
    r"tu\s+es\s+maintenant",
    r"nouvelle\s+filière",  # cf. exemple exact du sujet (robotique)
]

# --- Critères discriminatoires interdits comme base de recommandation -----
DISCRIMINATORY_PATTERNS = [
    r"selon\s+(le\s+)?sexe",
    r"selon\s+(le\s+)?genre",
    r"selon\s+l'?âge",
    r"selon\s+(l'?origine|la\s+religion|l'?ethnie)",
    r"parce\s+qu'?(elle|il)\s+est\s+(une\s+femme|un\s+homme)",
]

# --- Demandes de profilage psychologique -----------------------------------
PSYCH_PROFILING_PATTERNS = [
    r"analyse\s+ma\s+personnalit[eé]",
    r"profil\s+psychologique",
    r"d[eé]duis\s+mon\s+caract[eè]re",
    r"quel\s+type\s+de\s+personnalit[eé]",
]


@dataclass
class SecurityVerdict:
    allowed: bool
    reason: str | None = None
    category: str | None = None  # "injection" | "discrimination" | "profilage_psy"


def _matches_any(text: str, patterns: list[str]) -> bool:
    text_low = text.lower()
    return any(re.search(p, text_low) for p in patterns)


def check_input(question: str) -> SecurityVerdict:
    """Vérifie la question/l'instruction utilisateur avant de la transmettre à l'agent."""
    if _matches_any(question, INJECTION_PATTERNS):
        return SecurityVerdict(
            allowed=False,
            category="injection",
            reason=(
                "Requête refusée : je ne peux pas ignorer les documents vérifiés "
                "ni affirmer l'existence d'une formation non confirmée par le corpus."
            ),
        )
    if _matches_any(question, DISCRIMINATORY_PATTERNS):
        return SecurityVerdict(
            allowed=False,
            category="discrimination",
            reason=(
                "Je ne peux pas fonder une recommandation sur le sexe, l'âge, "
                "l'origine ou tout autre critère discriminatoire."
            ),
        )
    if _matches_any(question, PSYCH_PROFILING_PATTERNS):
        return SecurityVerdict(
            allowed=False,
            category="profilage_psy",
            reason=(
                "Je ne réalise pas de profilage psychologique. Je me base "
                "uniquement sur les matières, résultats, compétences et "
                "intérêts que vous déclarez explicitement."
            ),
        )
    return SecurityVerdict(allowed=True)


def strip_unverified_claims(generated_text: str, known_source_ids: set[str]) -> str:
    """
    Garde-fou de sortie minimal : si le texte généré ne contient aucune
    référence à une source connue alors qu'il prétend décrire une formation
    précise, on préfère renvoyer un message prudent plutôt qu'une affirmation
    non tracée. (Le vrai filtrage sémantique reste à affiner par M3/M4.)
    """
    if not known_source_ids and "parcours" in generated_text.lower():
        return (
            "Cette information n'est pas présente dans les documents "
            "disponibles. Je vous invite à contacter l'administration de "
            "l'ISPM pour confirmation."
        )
    return generated_text
