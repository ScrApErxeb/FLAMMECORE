from datetime import datetime, timezone
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

class ActionExecutor:
    def __init__(self, max_workers=4):
        self.results = []
        self.before_hooks = []
        self.after_hooks = []
        self.max_workers = max_workers

    def register_before_hook(self, hook_func):
        """Ajouter une fonction à exécuter avant chaque action"""
        self.before_hooks.append(hook_func)

    def register_after_hook(self, hook_func):
        """Ajouter une fonction à exécuter après chaque action"""
        self.after_hooks.append(hook_func)

    def execute(self, actions: list[dict]) -> list[dict]:
        """Exécution parallèle des actions"""
        self.results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._execute_single_action, action): action for action in actions}
            for future in as_completed(futures):
                result_entry = future.result()
                self.results.append(result_entry)
        return self.results

    def _execute_single_action(self, action: dict):
        for hook in self.before_hooks:
            hook(action)

        # Gestion du délai (en secondes) si spécifié
        delay = action.get("delay", 0)
        if delay > 0:
            time.sleep(delay)

        start_time = datetime.now(timezone.utc).isoformat()
        start_perf = time.perf_counter()

        result_entry = {
            "action": action,
            "status": "pending",
            "result": None,
            "error": None,
            "start_time": start_time,
            "end_time": None,
            "duration_ms": None,
        }

        try:
            result = self._execute_action(action)
            result_entry["result"] = result
            result_entry["status"] = "success"
        except Exception as e:
            result_entry["status"] = "failed"
            result_entry["error"] = str(e)

        end_perf = time.perf_counter()
        result_entry["end_time"] = datetime.now(timezone.utc).isoformat()
        result_entry["duration_ms"] = round((end_perf - start_perf) * 1000, 3)

        for hook in self.after_hooks:
            hook(action, result_entry)

        return result_entry

    def _execute_action(self, action: dict):
        if action["type"] == "echo":
            return action.get("message", "")
        elif action["type"] == "add":
            return action["a"] + action["b"]
        else:
            raise ValueError(f"Action inconnue: {action['type']}")

    def export_logs(self, filepath: str):
        """Export des logs d'exécution au format JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
