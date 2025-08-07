import uuid
from datetime import datetime, timezone
import json
from pathlib import Path
from threading import Lock
from typing import List, Dict, Optional
import math

class Memoire:
    def __init__(self, vector: list, response_id: str, context_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.vector = vector
        self.response_id = response_id
        self.context_id = context_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        d = {
            "id": self.id,
            "vector": self.vector,
            "response_id": self.response_id,
            "timestamp": self.timestamp,
        }
        if self.context_id is not None:
            d["context_id"] = self.context_id
        return d

class MemoireStorage:
    STORAGE_FILE = Path("data/memoire.json")

    def __init__(self):
        self.lock = Lock()
        self.STORAGE_FILE.parent.mkdir(exist_ok=True, parents=True)

    def save_memoire(self, memoire: Memoire) -> None:
        with self.lock:
            if self.STORAGE_FILE.exists():
                try:
                    data = json.loads(self.STORAGE_FILE.read_text())
                except json.JSONDecodeError:
                    data = []
            else:
                data = []
            data.append(memoire.to_dict())
            self.STORAGE_FILE.write_text(json.dumps(data, indent=2))

    def list_memoires(self) -> List[Dict]:
        if not self.STORAGE_FILE.exists():
            return []
        try:
            return json.loads(self.STORAGE_FILE.read_text())
        except json.JSONDecodeError:
            return []

    def delete_memoire(self, memoire_id: str) -> bool:
        with self.lock:
            data = self.list_memoires()
            new_data = [m for m in data if m.get("id") != memoire_id]
            if len(new_data) == len(data):
                return False
            self.STORAGE_FILE.write_text(json.dumps(new_data, indent=2))
            return True

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query_vector: List[float], threshold: float = 0.75, context_id: Optional[str] = None) -> List[Dict]:
        """
        Recherche les mémoires dont la similarité cosinus dépasse le seuil.
        Filtre sur context_id si fourni.
        Retourne la liste des mémoires correspondantes avec leur score.
        """
        results = []
        memoires = self.list_memoires()
        for memoire in memoires:
            if context_id is not None and memoire.get("context_id") != context_id:
                continue
            stored_vec = memoire.get("vector", [])
            sim = self.cosine_similarity(query_vector, stored_vec)
            if sim >= threshold:
                memoire_with_score = memoire.copy()
                memoire_with_score["similarity"] = sim
                results.append(memoire_with_score)
        return results

if __name__ == "__main__":
    storage = MemoireStorage()
    memoire1 = Memoire(vector=[1, 2, 3], response_id="test123", context_id="ctxA")
    storage.save_memoire(memoire1)

    query = [1, 2, 3]
    matches = storage.search(query_vector=query, threshold=0.9, context_id="ctxA")
    print("Matches trouvés:", matches)
