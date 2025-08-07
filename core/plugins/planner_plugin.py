from core.signal import Signal, Action
from typing import List, Dict, Optional

class Plugin:
    def __init__(self):
        self.name = "planner"

    def handle_signal(self, signal: Signal) -> List[Action]:
        steps = signal.payload.get("steps", [])
        if not steps:
            return [Action(id="planner_empty", params={"info": "Aucune étape fournie."})]

        # Trier les étapes selon la priorité (plus petit = plus prioritaire)
        steps_sorted = sorted(steps, key=lambda s: s.get("priority", 100))

        actions: List[Action] = []
        completed_ids = set()

        for step in steps_sorted:
            deps = step.get("depends_on", [])
            # Vérifier que toutes les dépendances sont dans completed_ids
            if all(dep in completed_ids for dep in deps):
                # TODO: appeler plugin adapté à type ici, mais on simule
                action_id = step.get("id", f"step_{len(actions)+1}")
                actions.append(Action(id=action_id, params={"info": f"Étape {action_id} exécutée"}))
                completed_ids.add(action_id)
            else:
                # Si dépendances non satisfaites, on pourrait différer, ici on ignore
                actions.append(Action(id=f"{step.get('id', 'unknown')}_skipped", params={"info": "Dépendances non satisfaites"}))

        return actions
