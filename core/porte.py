import uuid
from datetime import datetime, timezone
import json
from pathlib import Path
from core.gomde import Gomde

class Porte:
    def __init__(self, gomde: Gomde, encoding=None, format_type="text"):
        self.id = str(uuid.uuid4())
        self.gomde_id = gomde.id if gomde else None
        self.encoding = encoding if encoding is not None else self.encode(gomde)
        self.format = format_type
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.meta = {}

    def encode(self, gomde: Gomde):
        # Encodage simple : conversion en liste de codes ASCII
        if gomde and gomde.type == "text":
            return [ord(c) for c in gomde.content]
        return []

    def to_dict(self):
        return {
            "id": self.id,
            "gomde_id": self.gomde_id,
            "encoding": self.encoding,
            "format": self.format,
            "timestamp": self.timestamp,
            "meta": self.meta,
        }

class PorteStorage:
    STORAGE_FILE = Path("data/portes.json")

    def __init__(self):
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)

    def save_porte(self, porte: Porte):
        # Création dossier au cas où
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)
        if self.STORAGE_FILE.exists():
            data = json.loads(self.STORAGE_FILE.read_text())
        else:
            data = []
        data.append(porte.to_dict())
        self.STORAGE_FILE.write_text(json.dumps(data, indent=2))

    def list_portes(self):
        if not self.STORAGE_FILE.exists():
            return []
        return json.loads(self.STORAGE_FILE.read_text())

if __name__ == "__main__":
    gomde_example = Gomde("Test encodage porte")
    porte = Porte(gomde_example)
    store = PorteStorage()
    store.save_porte(porte)
    print(store.list_portes())
