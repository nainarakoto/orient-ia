"""
ORIENT'IA — Backend API (M5)

Démarrage local :
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Docs interactives : http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_store import load_formations
from routers import profile, recommend, chat, formations, evaluate, traces

app = FastAPI(
    title="ORIENT'IA API",
    description=(
        "Assistant virtuel d'orientation ISPM. Cet outil constitue une aide "
        "à l'orientation et ne remplace ni l'avis d'un conseiller pédagogique "
        "ni une décision officielle d'admission."
    ),
    version="0.1.0",
)

# CORS ouvert pour le hackathon (frontend séparé) — à restreindre si besoin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    load_formations()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(profile.router)
app.include_router(recommend.router)
app.include_router(chat.router)
app.include_router(formations.router)
app.include_router(evaluate.router)
app.include_router(traces.router)
