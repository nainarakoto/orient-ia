from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ProfilUtilisateur(BaseModel):
    notes: Optional[Dict[str, float]] = Field(default_factory=dict)
    competences: Optional[List[str]] = Field(default_factory=list)
    matieres_preferees: Optional[List[str]] = Field(default_factory=list)

class ChatRequest(BaseModel):
    message: str = Field(..., description="Le message ou la question de l'utilisateur")
    profil: Optional[ProfilUtilisateur] = Field(None, description="Le profil de l'étudiant s'il est connecté")

class ChatResponse(BaseModel):
    reponse: str = Field(..., description="La réponse générée par l'agent")
    sources: List[str] = Field(default_factory=list, description="IDs des sources documentaires utilisées")
    outils_appeles: List[str] = Field(default_factory=list, description="Outils mobilisés pour répondre")
    avertissements: List[str] = Field(default_factory=list, description="Avertissements éventuels (ex: mode dégradé)")
    request_id: str = Field(..., description="Identifiant unique de la requête")