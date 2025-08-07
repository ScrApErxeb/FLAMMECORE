import time
from threading import Timer, Event
from typing import List, Optional

from core.signal import Signal
from core.signal_manager import SignalManager

class Action:
    def __init__(self, id: str, func, params=None, max_retries=3, timeout=5, dependencies=None):
        self.id = id
        self.func = func  # fonction à exécuter (callable)
        self.params = params or {}
        self.max_retries = max_retries
        self.timeout = timeout
        self.dependencies = dependencies or []  # Liste d'IDs actions à terminer avant
        self.status = "PENDING"
        self.retry_count = 0

class Plan:
    def __init__(self, id: str, actions: List[Action]):
        self.id = id
        self.actions = {a.id: a for a in actions}  # Accès rapide par ID

class PlanManager:
    def __init__(self, signal_manager: SignalManager):
        self.plans = []
        self.signal_manager = signal_manager
        self.stop_event = Event()

    def add_plan(self, plan: Plan):
        self.plans.append(plan)

    def run(self):
        while not self.stop_event.is_set():
            for plan in self.plans:
                for action in plan.actions.values():
                    if action.status == "PENDING" and self._dependencies_done(action, plan):
                        self._execute_action(action)
            time.sleep(0.1)  # éviter 100% CPU

    def _dependencies_done(self, action: Action, plan: Plan) -> bool:
        # Toutes les dépendances doivent être DONE
        return all(plan.actions[dep_id].status == "DONE" for dep_id in action.dependencies)

    def _execute_action(self, action: Action):
        print(f"[PlanManager] Exécution action {action.id} (tentative {action.retry_count+1})")

        def timeout_handler():
            print(f"[PlanManager] Timeout pour action {action.id}")
            action.status = "FAILED"
            self._handle_failure(action)

        timer = Timer(action.timeout, timeout_handler)
        timer.start()

        success = False
        try:
            # Appel fonction métier avec params
            success = action.func(**action.params)
        except Exception as e:
            print(f"[PlanManager] Exception action {action.id} : {e}")

        timer.cancel()

        if success:
            action.status = "DONE"
            print(f"[PlanManager] Action {action.id} réussie")
            # Optionnel : émettre un signal
            self.signal_manager.enqueue_signal(Signal(payload={"action_id": action.id, "status": "done"}))
        else:
            action.retry_count += 1
            if action.retry_count > action.max_retries:
                action.status = "FAILED"
                print(f"[PlanManager] Action {action.id} a échoué après {action.retry_count} tentatives")
                self._handle_failure(action)
            else:
                print(f"[PlanManager] Retry action {action.id}")
                # Remettre à PENDING pour réessayer plus tard
                action.status = "PENDING"

    def _handle_failure(self, action: Action):
        # Exemple de callback ou log
        print(f"[PlanManager] Gestion échec action {action.id}")
        # Ici tu peux notifier un Signal, logger, ou autre

    def stop(self):
        self.stop_event.set()
