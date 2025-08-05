import uuid
from datetime import datetime, timezone
import json
from pathlib import Path
from core.porte import Porte

class Reponse:
    def __init__(self, porte: Porte, content: str, mode: str = "text", confidence: float = 1.0, source: str = "local"):
        self.id = str(uuid.uuid4())
        self.porte_id = porte.id
        self.content = content
        self.mode = mode
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.confidence = confidence
        self.source = source

    def to_dict(self):
        return {
            "id": self.id,
            "porte_id": self.porte_id,
            "content": self.content,
            "mode": self.mode,
            "timestamp": self.timestamp,
            "confidence": self.confidence,
            "source": self.source
        }

class ReponseStorage:
    STORAGE_FILE = Path("data/reponses.json")

    def __init__(self):
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)

    def save_reponse(self, reponse: Reponse):
        self.STORAGE_FILE.parent.mkdir(exist_ok=True)
        if self.STORAGE_FILE.exists():
            data = json.loads(self.STORAGE_FILE.read_text())
        else:
            data = []
        data.append(reponse.to_dict())
        self.STORAGE_FILE.write_text(json.dumps(data, indent=2))

    def list_reponses(self):
        if not self.STORAGE_FILE.exists():
            return []
        return json.loads(self.STORAGE_FILE.read_text())

def generate_simple_response(porte: Porte) -> Reponse:
    content_text = "".join([chr(c) for c in porte.encoding]) if porte.format == "text" else ""
    content_lower = content_text.lower()

    if "bonjour" in content_lower:
        reply = "Salut ! Comment puis-je t’aider ?"
    elif "heure" in content_lower:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        reply = f"Il est actuellement {now}."
    else:
        reply = "Je ne comprends pas encore, mais je travaille dessus !"

    return Reponse(porte, content=reply)

if __name__ == "__main__":
    from core.porte import PorteStorage
    store_porte = PorteStorage()
    portes = store_porte.list_portes()
    if not portes:
        print("Pas de porte disponible pour réponse")
    else:
        first_porte_dict = portes[0]
        porte = Porte(
            gomde=None,
            encoding=first_porte_dict["encoding"],
            format_type=first_porte_dict["format"]
        )
        porte.id = first_porte_dict["id"]
        porte.gomde_id = first_porte_dict["gomde_id"]
        porte.meta = first_porte_dict.get("meta", {})
        porte.timestamp = first_porte_dict["timestamp"]

        response = generate_simple_response(porte)
        store_response = ReponseStorage()
        store_response.save_reponse(response)
        print(store_response.list_reponses())
