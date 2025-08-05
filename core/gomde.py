import uuid
from datetime import datetime, timezone
import json
from pathlib import Path

class Gomde:
    def __init__(self, content: str, input_type: str = "text", source: str = "user"):
        self.id = str(uuid.uuid4())
        self.type = input_type
        self.content = content
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.source = source

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "timestamp": self.timestamp,
            "source": self.source,
        }

class GomdeStorage:
    STORAGE_FILE = Path("data/gomdes.json")

    def __init__(self):
        # On laisse ce mkdir ici pour les usages standards
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)

    def save_gomde(self, gomde: Gomde):
        # On recrée le dossier à chaque save au cas où STORAGE_FILE a changé
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)
        if self.STORAGE_FILE.exists():
            data = json.loads(self.STORAGE_FILE.read_text())
        else:
            data = []
        data.append(gomde.to_dict())
        self.STORAGE_FILE.write_text(json.dumps(data, indent=2))

    def list_gomdes(self):
        if not self.STORAGE_FILE.exists():
            return []
        return json.loads(self.STORAGE_FILE.read_text())

if __name__ == "__main__":
    # Exemple simple d'utilisation
    store = GomdeStorage()
    gomde = Gomde("Salut Flamme, c'est le début de FlammeCore !")
    store.save_gomde(gomde)
    print(store.list_gomdes())
