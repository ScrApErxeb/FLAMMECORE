# api/memoire_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.memoire import MemoireStorage, Memoire

router = APIRouter()
storage = MemoireStorage()

class MemoireIn(BaseModel):
    vector: List[float]
    response_id: str

class MemoireSearchIn(BaseModel):
    vector: List[float]

@router.post("/add")
def add_memory(memoire_in: MemoireIn):
    memoire = Memoire(vector=memoire_in.vector, response_id=memoire_in.response_id)
    storage.save_memoire(memoire)
    return {"status": "success", "id": memoire.id}

@router.post("/search")
def search_memory(search_in: MemoireSearchIn):
    memories = storage.list_memoires()
    if not memories:
        raise HTTPException(status_code=404, detail="Aucune mémoire trouvée")

    import numpy as np
    qv = np.array(search_in.vector)
    best_match = None
    best_score = -1
    for mem in memories:
        mv = np.array(mem["vector"])
        score = np.dot(qv, mv) / (np.linalg.norm(qv) * np.linalg.norm(mv) + 1e-10)
        if score > best_score:
            best_score = score
            best_match = mem

    return {"best_match": best_match, "score": best_score}

@router.get("/list")
def list_memories():
    return storage.list_memoires()

@router.delete("/delete/{memoire_id}")
def delete_memory(memoire_id: str):
    success = storage.delete_memoire(memoire_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mémoire non trouvée")
    return {"status": "deleted"}
