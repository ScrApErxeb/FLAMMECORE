from typing import Optional, Callable

class Action:
    def __init__(self, id: str, func: Callable, dependencies=None, condition: Optional[Callable] = None, max_retries=0):
        self.id = id
        self.func = func
        self.dependencies = dependencies or []
        self.condition = condition
        self.max_retries = max_retries
        self.retry_count = 0
        self.status = "PENDING"  # PENDING, RUNNING, DONE, FAILED, SKIPPED

    def can_run(self, plan) -> bool:
        # Toutes dépendances DONE ?
        if not all(plan.actions[dep_id].status == "DONE" for dep_id in self.dependencies):
            return False
        # Condition personnalisée, si définie
        if self.condition:
            return self.condition(plan)
        return True
