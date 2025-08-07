from typing import List, Dict, Callable, Optional, Set
from enum import Enum

class ActionStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class Action:
    def __init__(
        self,
        id: str,
        execute: Callable[[], None],
        dependencies: Optional[List[str]] = None,
        condition: Optional[Callable[[], bool]] = None,
        wait_for_signals: Optional[Set[str]] = None,
    ):
        self.id = id
        self.execute = execute
        self.dependencies = dependencies or []
        self.condition = condition  # Fonction retournant bool
        self.wait_for_signals = wait_for_signals or set()  # IDs de signaux attendus
        self.status = ActionStatus.PENDING
        self.received_signals = set()

    def can_execute(self, plan_actions: Dict[str, "Action"]) -> bool:
        # 1. Toutes les dépendances sont DONE
        if any(plan_actions[dep].status != ActionStatus.DONE for dep in self.dependencies):
            return False
        # 2. Condition est satisfaite (ou pas de condition)
        if self.condition and not self.condition():
            return False
        # 3. Tous les signaux attendus reçus
        if not self.wait_for_signals.issubset(self.received_signals):
            return False
        return True

    def receive_signal(self, signal_id: str):
        self.received_signals.add(signal_id)

class Plan:
    def __init__(self, actions: List[Action]):
        self.actions: Dict[str, Action] = {a.id: a for a in actions}

    def all_done_or_skipped(self) -> bool:
        return all(a.status in (ActionStatus.DONE, ActionStatus.SKIPPED) for a in self.actions.values())

class PlanManager:
    def __init__(self, plan: Plan):
        self.plan = plan

    def receive_signal(self, signal_id: str):
        # Propagation aux actions en attente
        for action in self.plan.actions.values():
            if action.status == ActionStatus.PENDING:
                action.receive_signal(signal_id)

    def run(self):
        while not self.plan.all_done_or_skipped():
            progress = False
            for action in self.plan.actions.values():
                if action.status == ActionStatus.PENDING and action.can_execute(self.plan.actions):
                    action.status = ActionStatus.RUNNING
                    try:
                        action.execute()
                        action.status = ActionStatus.DONE
                        print(f"Action {action.id} terminée avec succès.")
                    except Exception as e:
                        action.status = ActionStatus.FAILED
                        print(f"Action {action.id} a échoué: {e}")
                    progress = True
            if not progress:
                # Aucune action n'a pu être lancée => deadlock ou attente signaux
                print("Plus d'actions exécutables pour le moment, attente de signaux ou conditions.")
                break
