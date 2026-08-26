from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.orchestrator import OrientIAAgent

app = FastAPI(title="Orient'IA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines pour le dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = OrientIAAgent()

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