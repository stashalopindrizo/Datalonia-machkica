from __future__ import annotations

import os
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .entity_manager import EntityManager
from entities import MedaEntity, GraEntity
from kvartovi.definitions import KVARTOVI
from .brain import router as brain_router # APIRouter(prefix="/api/brain")

load_dotenv()

app = FastAPI(title="Datalonija")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brain_router)

entity_manager = EntityManager()
meda = MedaEntity()
entity_manager.add_entity("meda", meda) 
gra = GraEntity ()
entity_manager .add_entity("gra", gra)

def _world_state() -> Dict[str, Any]:
    return {
        "status": "Datalonia is running",
        "entities": list(entity_manager.entities.keys()),
        "kvartovi": list(KVARTOVI.keys()) if isinstance(KVARTOVI, dict) else [],
    }

@app.get("/ping")
def ping():
    return {"message": "Pong! Datalonija je budna."}

@app.get("/")
def root():
    return _world_state() 

@app.get("/api/ping")
def api_ping():
    return {"message": "Pong! Datalonija je budna."}

@app.get("/api/")
def api_root():
    return _world_state()
