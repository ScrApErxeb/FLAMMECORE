# core/plugins/memoire_plugin.py
from core.signal import Signal, Action
from core.memoire import Memoire, MemoireStorage
import numpy as np

class Plugin:
    def __init__(self):
        self.name = "memoire"
        self.storage = MemoireStorage()

    def handle_signal(self, signal: Signal):
        action_type = signal.payload.get("action")
        context_id = signal.payload.get("context_id")  # Nouveau paramètre facultatif

        if action_type == "add_memory":
            vector = signal.payload.get("vector")
            response_id = signal.payload.get("response_id", "unknown")
            if not vector:
                return Action(id="memoire_error", params={"error": "Vecteur manquant"})
            memoire = Memoire(vector=vector, response_id=response_id, context_id=context_id)
            self.storage.save_memoire(memoire)
            return Action(id="memoire_added", params={"id": memoire.id})

        elif action_type == "search_memory":
            query_vector = signal.payload.get("vector")
            threshold = signal.payload.get("threshold", 0.75)
            if not query_vector:
                return Action(id="memoire_error", params={"error": "Vecteur de recherche manquant"})

            memories = self.storage.search(query_vector=query_vector, threshold=threshold, context_id=context_id)
            if not memories:
                return Action(id="memoire_empty", params={"info": "Aucune mémoire trouvée"})

            # Renvoie la meilleure correspondance
            best_match = max(memories, key=lambda m: m["similarity"])

            return Action(
                id="memoire_search_result",
                params={
                    "best_match_id": best_match["id"],
                    "response_id": best_match["response_id"],
                    "score": best_match["similarity"],
                    "timestamp": best_match["timestamp"],
                    "context_id": best_match.get("context_id")
                }
            )
        else:
            return Action(id="memoire_error", params={"error": f"Action inconnue: {action_type}"})
