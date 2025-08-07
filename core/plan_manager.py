import time
import threading
import heapq
from typing import List, Optional, Callable, Dict, Any
from core.signal import Signal, Action
from core.signal_manager import SignalManager

class Action:
    def __init__(
        self,
        id: str,
        func: Callable[..., bool],
        params: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: int = 5,
        dependencies: Optional[List[str]] = None,
        condition: Optional[Callable[[], bool]] = None,
        priority: int = 10
    ):
        self.id = id
        self.func = func
        self.params = params or {}
        self.max_retries = max_retries
        self.timeout = timeout
        self.dependencies = dependencies or []
        self.condition = condition or (lambda: True)
        self.priority = priority

        self.status = "PENDING"  # PENDING, RUNNING, DONE, FAILED
        self.retry_count = 0
        self.next_run_time = 0  # timestamp pour backoff retry

    def ready(self, plan: "Plan") -> bool:
        # Vérifie dépendances terminées
        deps_done = all(plan.actions[dep].status == "DONE" for dep in self.dependencies)
        cond_ok = self.condition()
        retry_ok = time.time() >= self.next_run_time
        return self.status == "PENDING" and deps_done and cond_ok and retry_ok

class Plan:
    def __init__(self, id: str, actions: List[Action]):
        self.id = id
        self.actions: Dict[str, Action] = {a.id: a for a in actions}
        self.status = "RUNNING"  # RUNNING, DONE, FAILED

    def all_done(self):
        return all(a.status == "DONE" for a in self.actions.values())

class PlanManager(threading.Thread):
    def __init__(self, signal_manager: SignalManager):
        super().__init__()
        self.plans: List[Plan] = []
        self.signal_manager = signal_manager
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def add_plan(self, plan: Plan):
        with self._lock:
            self.plans.append(plan)

    def run(self):
        while not self.stop_event.is_set():
            for plan in self.plans:
                for action in plan.actions.values():
                    if action.status == "PENDING" and self._dependencies_done(action, plan):
                        if action.condition and not action.condition():
                            print(f"[PlanManager] Condition non satisfaite pour action {action.id}, on skip.")
                            continue
                        self._execute_action(action)
            time.sleep(0.1)


    def _execute_action(self, action: Action, plan: Plan):
        action.status = "RUNNING"
        print(f"[PlanManager] Exécution action {action.id} (tentative {action.retry_count+1})")

        timer = threading.Timer(action.timeout, lambda: self._timeout_action(action))
        timer.start()

        try:
            success = action.func(**action.params)
        except Exception as e:
            print(f"[PlanManager] Exception action {action.id}: {e}")
            success = False

        timer.cancel()

        if success:
            action.status = "DONE"
            print(f"[PlanManager] Action {action.id} réussie")
            self.signal_manager.enqueue_signal(Signal(payload={"action_id": action.id, "status": "done"}))
        else:
            action.retry_count += 1
            if action.retry_count > action.max_retries:
                action.status = "FAILED"
                print(f"[PlanManager] Action {action.id} a échoué après {action.retry_count} tentatives")
                self._handle_failure(action, plan)
            else:
                # backoff exponentiel (en secondes)
                backoff = 2 ** (action.retry_count - 1)
                action.next_run_time = time.time() + backoff
                action.status = "PENDING"
                print(f"[PlanManager] Retry action {action.id} dans {backoff}s")

    def _timeout_action(self, action: Action):
        if action.status == "RUNNING":
            print(f"[PlanManager] Timeout pour action {action.id}")
            action.status = "FAILED"

    def _handle_failure(self, action: Action, plan: Plan):
        print(f"[PlanManager] Gestion échec action {action.id} du plan {plan.id}")
        # Ici tu peux notifier, logger, déclencher autre chose

    def stop(self):
        self._stop_event.set()
        self.join()
