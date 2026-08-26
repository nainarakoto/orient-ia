"""
Schémas Pydantic — ORIENT'IA
Reprend le modèle de données de la section 5 du plan (Profil, Formation, Trace...).
"""
from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
import uuid
import time


# ---------------------------------------------------------------------------
# Profil utilisateur
# ---------------------------------------------------------------------------

class Profile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    matieres_preferees: list[str] = Field(default_factory=list)
    resultats: Optional[dict[str, float]] = None  # ex: {"maths": 15.5}
    competences_declarees: list[str] = Field(default_factory=list)
    interets: list[str] = Field(default_factory=list)
    projets: list[str] = Field(default_factory=list)
    preferences_professionnelles: Optional[str] = None
    environnement_travail_recherche: Optional[str] = None
    origine: Literal["utilisateur", "synthetique", "enquete_etudiant", "enquete_professionnel"] = "utilisateur"

    def is_complete_enough_for_recommendation(self) -> bool:
        """Garde-fou simple : on évite une recommandation prématurée (§10 workflow)."""
        return bool(self.matieres_preferees or self.interets or self.competences_declarees)


class ProfileUpdateRequest(BaseModel):
    profile_id: Optional[str] = None  # si None -> nouveau profil
    matieres_preferees: Optional[list[str]] = None
    resultats: Optional[dict[str, float]] = None
    competences_declarees: Optional[list[str]] = None
    interets: Optional[list[str]] = None
    projets: Optional[list[str]] = None
    preferences_professionnelles: Optional[str] = None
    environnement_travail_recherche: Optional[str] = None


# ---------------------------------------------------------------------------
# Formations
# ---------------------------------------------------------------------------

class Source(BaseModel):
    id: str
    titre: str
    origine_url: Optional[str] = None
    date_consultation: Optional[str] = None
    statut: Literal["officiel", "institutionnel", "externe"] = "externe"
    limites_incertitudes: Optional[str] = None


class Formation(BaseModel):
    id: str
    mention: str
    parcours: str
    niveau: Optional[str] = None
    diplome: Optional[str] = None
    description: Optional[str] = None
    matieres: list[str] = Field(default_factory=list)
    competences: list[str] = Field(default_factory=list)
    prerequis: list[str] = Field(default_factory=list)
    debouches: list[str] = Field(default_factory=list)
    passerelles: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Recommandation / explication (sortie exigée par §1 : recommandation +
# explication + sources + incertitude + refus d'inventer)
# ---------------------------------------------------------------------------

class ScoreParcours(BaseModel):
    parcours_id: str
    score_ml: float
    prerequis_ok: bool
    prerequis_manquants: list[str] = Field(default_factory=list)


class CitedPassage(BaseModel):
    source_id: str
    extrait: str
    score_recherche: Optional[float] = None


class RecommendationExplanation(BaseModel):
    """Distingue explicitement ML / documents / règles / LLM (exigence §8/§12)."""
    facteurs_ml: list[ScoreParcours] = Field(default_factory=list)
    facteurs_documentaires: list[CitedPassage] = Field(default_factory=list)
    regles_appliquees: list[str] = Field(default_factory=list)
    texte_genere: str = ""
    incertitude: Optional[str] = None


class RecommendRequest(BaseModel):
    profile: Profile
    question: Optional[str] = None


class RecommendResponse(BaseModel):
    trace_id: str
    parcours_recommandes: list[str]
    explication: RecommendationExplanation
    mention_legale: str = (
        "ORIENT'IA constitue un outil d'aide à l'orientation. Ses recommandations "
        "ne remplacent ni l'avis d'un conseiller pédagogique ni une décision "
        "officielle d'admission."
    )
    refus: Optional[str] = None  # rempli si la sécurité a bloqué la requête


# ---------------------------------------------------------------------------
# Chat conversationnel libre (agent)
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    profile_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    trace_id: str
    reponse: str
    outils_appeles: list[str] = Field(default_factory=list)
    refus: Optional[str] = None


# ---------------------------------------------------------------------------
# Trace / observabilité (§15, §20)
# ---------------------------------------------------------------------------

class ToolCallTrace(BaseModel):
    nom: str
    input: dict
    output: dict


class Trace(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    question: Optional[str] = None
    profil: Optional[dict] = None
    passages_recuperes: list[CitedPassage] = Field(default_factory=list)
    outils_appeles: list[ToolCallTrace] = Field(default_factory=list)
    reponse_finale: Optional[str] = None
    latence_ms: Optional[float] = None
    erreurs_refus: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Évaluation (32 cas de test, §13/§19)
# ---------------------------------------------------------------------------

class TestCase(BaseModel):
    id: str
    categorie: str
    question_ou_profil: str
    resultat_attendu: str
    composant_teste: str
    metrique: Optional[str] = None


class TestResult(BaseModel):
    test_id: str
    resultat_obtenu: str
    reussi: bool
    details: Optional[str] = None
