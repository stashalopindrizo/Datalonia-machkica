from fastapi import APIRouter, Body, HTTPException
from typing import Dict, List, Any
from datetime import datetime
import uuid, re, json
from pathlib import Path

from .schemas_brain import RememberIn, MemoryItem, SearchIn, SearchOutItem, BrainStats
from entities import GraEntity


# fajl na disku gde čuvamo memoriju
MEM_FILE = Path("memory.json")

# globalni rečnik memorije u RAM-u
_MEM: Dict[str, MemoryItem] = {}


def save_mem() -> None:
    """Snimi _MEM u memory.json (datetime → string)."""
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                k: {
                    **v.dict(),
                    "created_at": v.created_at.isoformat(),
                }
                for k, v in _MEM.items()
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def load_mem() -> None:
    """Učitaj memoriju iz fajla ako postoji."""
    global _MEM
    if MEM_FILE.exists():
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        _MEM = {k: MemoryItem(**v) for k, v in data.items()}


# napravimo router i odmah probamo da učitamo stare memoare
router = APIRouter(prefix="/api/brain", tags=["brain"])
load_mem()

def _norm(txt: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9šđžčćŠĐŽČĆ]+", txt.lower())

def _jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

@router.post("/remember", response_model=MemoryItem)
def remember(payload: RememberIn):
    mid = str(uuid.uuid4())
    item = MemoryItem(
        id=mid,
        text=payload.text.strip(),
        tags=[t.strip().lower() for t in payload.tags],
        created_at=datetime.utcnow(),
    )
    _MEM[mid] = item 
    save_mem()
    return item

@router.post("/search", response_model=List[SearchOutItem])
def search(payload: SearchIn):
    qtoks = _norm(payload.query)
    scored: List[SearchOutItem] = []
    for it in _MEM.values():
        score = max(
            _jaccard(qtoks, _norm(it.text)),
            _jaccard(qtoks, it.tags),
        )
        if score > 0:
            scored.append(SearchOutItem(item=it, score=score))
    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[: max(1, min(50, payload.top_k))]

@router.get("/stats", response_model=BrainStats)
def stats():
    all_tags = set(t for it in _MEM.values() for t in it.tags)
    return BrainStats(total=len(_MEM), tags=sorted(all_tags))

@router.delete("/clear")
def clear():
    _MEM.clear()
    return {"ok": True, "cleared": True, "total": 0} 

# --- CHAT (Medina ruta) ---

gra = GraEntity() # globalna instanca

@router.post("/chat")
async def api_chat(payload: Dict[str, Any] = Body(...)):
    user_text = None

    if "messages" in payload and isinstance(payload["messages"], list) and payload["messages"]:
        user_text = payload["messages"][-1].get("content")
    elif "message" in payload:
        user_text = payload["message"]
    elif "prompt" in payload:
        user_text = payload["prompt"]

    if not user_text:
        raise HTTPException(status_code=400, detail="No user message provided")

    try:
        reply = await gra.respond(user_text, user_id="ui")
    except Exception as e:
        print("❌ /api/chat error:", e)
        raise HTTPException(status_code=500, detail="Chat failed")

    return {
        "message": {
            "role": "assistant",
            "content": reply, 
            "timestamp": datetime.now().isoformat(),
        }
    }

