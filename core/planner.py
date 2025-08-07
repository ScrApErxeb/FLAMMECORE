from copy import deepcopy
from core.signal import Signal
from core.plugins.memoire_plugin import Plugin as MemoirePlugin

class Planner:
    def __init__(self):
        self.memoire_plugin = MemoirePlugin()

    def merge_contexts(self, base: dict, update: dict) -> dict:
        """Fusion récursive des dicts pour ne pas écraser des sous-contextes."""
        result = deepcopy(base)
        for k, v in update.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = self.merge_contexts(result[k], v)
            else:
                result[k] = v
        return result

    def enrich_signal_with_memory(self, signal: Signal, context_id: str = None) -> Signal:
        if not hasattr(signal, "context") or signal.context is None:
            signal.context = {}

        vector = signal.payload.get("vector")
        if not vector:
            return signal

        mem_payload = {
            "action": "search_memory",
            "vector": vector,
        }
        if context_id is not None:
            mem_payload["context_id"] = context_id

        memory_response = self.memoire_plugin.handle_signal(
            Signal(name="memoire", payload=mem_payload)
        )

        mem_ctx = memory_response.params if memory_response.id == "memoire_search_result" else None
        signal.context = self.merge_contexts(signal.context, {"memory": mem_ctx})
        return signal

    # Tu peux ensuite rajouter d'autres méthodes d'enrichissement, ex :
    def enrich_signal_with_history(self, signal: Signal, history: dict) -> Signal:
        if not hasattr(signal, "context") or signal.context is None:
            signal.context = {}

        signal.context = self.merge_contexts(signal.context, {"history": history})
        return signal
