# core/plugins/wiki_plugin.py
from core.signal import Signal, SignalType, Action
import requests

class WikiPlugin:
    def __init__(self):
        self.name = "wiki"

    def handle_signal(self, signal: Signal):
        query = signal.payload.get("query", "")
        if not query:
            return None

        url = f"https://fr.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                summary = data.get("extract", "Pas de résumé disponible.")
                return Action(id="action_wiki_1", params={"summary": summary})
            else:
                return Action(id="action_wiki_1", params={"summary": "Article introuvable."})
        except Exception as e:
            return Action(id="action_wiki_1", params={"summary": f"Erreur API Wiki: {str(e)}"})
