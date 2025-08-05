import uuid
from datetime import datetime, timezone
import json
from pathlib import Path

class Memoire:
    def __init__(self, vector, response_id: str):
        self.id = str(uuid.uuid4())
        self.vector = vector  # typiquement un vecteur encodé
        self.response_id = response_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "vector": self.vector,
            "response_id": self.response_id,
            "timestamp": self.timestamp,
        }

class MemoireStorage:
    STORAGE_FILE = Path("data/memoire.json")

    def __init__(self):
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)

    def save_memoire(self, memoire: Memoire):
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)
        if self.STORAGE_FILE.exists():
            data = json.loads(self.STORAGE_FILE.read_text())
        else:
            data = []
        data.append(memoire.to_dict())
        self.STORAGE_FILE.write_text(json.dumps(data, indent=2))

    def list_memoires(self):
        if not self.STORAGE_FILE.exists():
            return []
        return json.loads(self.STORAGE_FILE.read_text())

if __name__ == "__main__":
    memoire = Memoire(vector=[1,2,3], response_id="test")
    storage = MemoireStorage()
    storage.save_memoire(memoire)
    print(storage.list_memoires())
