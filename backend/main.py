from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    resultat = agent.executer_dialogue(request.message)
    return resultat