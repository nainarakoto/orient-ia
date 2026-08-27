from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.orchestrator import OrientIAAgent
from ml.service import recommander_parcours_ml, obtenir_schema_ml

app = FastAPI(title="Orient'IA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines pour le dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = OrientIAAgent()

# Valeur neutre envoyée au modèle ML pour le champ 'sexe'. Ce champ n'est
# jamais collecté auprès de l'utilisateur (cf. mention affichée sur la page
# "Mon Profil" : aucune caractéristique personnelle sensible n'est demandée).
# 'M' correspond exactement à la valeur que l'imputer du pipeline utilise
# déjà par défaut en cas de donnée manquante à l'entraînement - on l'envoie
# donc explicitement, la même pour tout le monde, pour ne jamais faire
# dépendre une recommandation du sexe d'un utilisateur.
SEXE_NEUTRE = "M"


class ChatRequest(BaseModel):
    message: str


# --- ROUTE CLASSIQUE (synchrone / asynchrone blocante) ---
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    resultat = await agent.executer_dialogue(request.message)
    return resultat


# --- NOUVELLE ROUTE : STREAMING (Effet machine à écrire) ---
@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Endpoint dédié au streaming de la réponse de l'agent pour le Frontend."""
    return StreamingResponse(
        agent.executer_dialogue_stream(request.message),
        media_type="text/plain"
    )


# --- ROUTE ATTENDUE PAR LE FRONTEND STREAMLIT (services/api_client.py) ---
class AgentChatRequest(BaseModel):
    historique: List[dict] = []
    message: str
    profil: Optional[dict] = None


class AgentChatResponse(BaseModel):
    reponse: str
    sources: List[str] = []
    outils_appeles: List[str] = []


@app.post("/agent/chat", response_model=AgentChatResponse)
async def agent_chat_endpoint(request: AgentChatRequest):
    """
    Route consommée par le frontend (services/api_client.py ->
    envoyer_message_assistant). Le contrat de sortie (reponse, sources,
    outils_appeles) est fixé par le frontend et ne doit pas changer.

    Limitations actuelles (à lever plus tard si besoin) :
    - `historique` est accepté mais pas encore transmis à l'agent :
      OrientIAAgent.executer_dialogue() ne gère pas encore le multi-tours.
    - `sources` est toujours vide : les outils RAG renvoient des
      source_id en interne, mais l'orchestrateur ne les remonte pas
      encore dans son résultat final.
    """
    resultat = await agent.executer_dialogue(request.message)

    outils_appeles = [
        appel["outil"] for appel in resultat["traces"].get("outils_executes", [])
    ]

    return AgentChatResponse(
        reponse=resultat["reponse_finale"],
        sources=[],
        outils_appeles=outils_appeles,
    )


# --- ROUTE SCHEMA ML : catégories exactes attendues par le modèle ---
@app.get("/ml/schema")
async def ml_schema_endpoint():
    """
    Renvoie les catégories exactes (série du bac, préférence d'environnement
    de travail, objectifs professionnels connus) attendues par le pipeline
    scikit-learn. Le frontend s'en sert pour peupler ses menus déroulants,
    afin qu'une valeur envoyée au modèle ne soit jamais une catégorie
    inconnue de lui.
    """
    return obtenir_schema_ml()


# --- ROUTE RECOMMANDATION ML (attendue par services/api_client.py -> obtenir_recommandation) ---
class ProfilRequest(BaseModel):
    matieres_preferees: List[str] = []
    matieres_faibles: List[str] = []
    resultats_scolaires: str = ""
    competences: List[str] = []
    centres_interet: str = ""
    activites_projets: str = ""
    preferences_professionnelles: List[str] = []
    environnement_travail: str = ""
    age: Optional[int] = None
    serie: Optional[str] = None
    moyenne_generale: Optional[float] = None
    objectif_professionnel: Optional[str] = None


class ResultatRecommandation(BaseModel):
    parcours: str
    score_adequation: float
    facteurs: List[str]
    sources: List[str]


class RecommandationResponse(BaseModel):
    origine: str
    resultats: List[ResultatRecommandation]
    incertitude: str


@app.post("/agent/recommander", response_model=RecommandationResponse)
async def agent_recommander_endpoint(profil: ProfilRequest):
    """
    Route consommée par le frontend (services/api_client.py ->
    obtenir_recommandation), appelée depuis pages/3_Recommandation.py.

    Valeurs par défaut utilisées quand un champ n'est pas renseigné :
    - age -> 19, moyenne_generale -> 13.03 : ce sont exactement les valeurs
      que l'imputer du pipeline utilise déjà en cas de donnée manquante à
      l'entraînement, donc aucun écart de comportement introduit.
    - sexe -> toujours SEXE_NEUTRE ('M'), jamais collecté auprès de
      l'utilisateur (voir commentaire plus haut).
    """
    # centres_interet est un champ texte libre côté frontend (pas une liste) ;
    # on approxime le nombre de centres d'intérêt en comptant les éléments
    # séparés par des virgules, sans changer l'UI existante.
    centres_interet_liste = [c.strip() for c in profil.centres_interet.split(",") if c.strip()]

    resultats_bruts = recommander_parcours_ml(
        age=profil.age if profil.age is not None else 19,
        sexe=SEXE_NEUTRE,
        serie=profil.serie or "",
        moyenne_generale=profil.moyenne_generale if profil.moyenne_generale is not None else 13.03,
        preferences_env=profil.environnement_travail or "",
        objectif_professionnel=profil.objectif_professionnel or "",
        matieres_fortes=profil.matieres_preferees,
        matieres_faibles=profil.matieres_faibles,
        centres_interet=centres_interet_liste,
        competences=profil.competences,
        top_k=5,
    )

    facteurs_communs = []
    if profil.serie:
        facteurs_communs.append(f"Série du bac : {profil.serie}")
    if profil.moyenne_generale is not None:
        facteurs_communs.append(f"Moyenne générale : {profil.moyenne_generale}")
    if profil.matieres_preferees:
        facteurs_communs.append("Matières fortes : " + ", ".join(profil.matieres_preferees))
    if profil.competences:
        facteurs_communs.append("Compétences : " + ", ".join(profil.competences))
    if profil.objectif_professionnel:
        facteurs_communs.append(f"Objectif professionnel déclaré : {profil.objectif_professionnel}")

    if not facteurs_communs:
        facteurs_communs = ["Profil partiellement renseigné - recommandation basée sur des valeurs par défaut"]

    resultats = [
        ResultatRecommandation(
            parcours=r["filiere_nom"],
            score_adequation=r["score"],
            facteurs=facteurs_communs,
            sources=["Modèle de Machine Learning entraîné sur les profils ISPM"],
        )
        for r in resultats_bruts
    ]

    return RecommandationResponse(
        origine="Machine Learning (scikit-learn)",
        resultats=resultats,
        incertitude=(
            "Cette recommandation est générée automatiquement à partir des informations "
            "que vous avez renseignées. Elle ne remplace pas l'avis d'un conseiller pédagogique "
            "ni une décision officielle d'admission."
        ),
    )