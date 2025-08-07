import time
from core.plan_manager import PlanManager, Plan, Action
from core.signal_manager import SignalManager
from core.signal import Signal


class DummySignalManager(SignalManager):
    def __init__(self):
        super().__init__()
        self.signals = []

    def enqueue_signal(self, signal: Signal):
        self.signals.append(signal)


def always_success():
    return True

def fail_once_then_success_factory():
    state = {"called": 0}
    def func():
        if state["called"] == 0:
            state["called"] += 1
            return False
        return True
    return func

def test_plan_manager_advanced():
    signal_manager = SignalManager()
    plan_manager = PlanManager(signal_manager)

    action1 = Action(id="a1", func=always_success, priority=5)
    action2 = Action(id="a2", func=fail_once_then_success_factory(), max_retries=3, priority=1, dependencies=["a1"])
    action3 = Action(id="a3", func=always_success, dependencies=["a2"], priority=10,
                     condition=lambda: True)

    plan = Plan(id="p1", actions=[action1, action2, action3])
    plan_manager.add_plan(plan)

    plan_manager.start()

    # Timeout raisonnable
    timeout = time.time() + 10
    while plan.status != "DONE" and time.time() < timeout:
        time.sleep(0.1)

    plan_manager.stop()

    assert action1.status == "DONE"
    assert action2.status == "DONE"
    assert action3.status == "DONE"
    assert action2.retry_count == 1


def test_plan_manager_condition():
    def always_true():
        return True

    def always_false():
        return False

    def dummy_func():
        return True

    action1 = Action(id="a1", func=dummy_func, condition=always_false)
    action2 = Action(id="a2", func=dummy_func, condition=always_true)

    plan = Plan(id="p_cond", actions=[action1, action2])
    pm = PlanManager(signal_manager=DummySignalManager())
    pm.add_plan(plan)

    # On simule une exécution simple (pas besoin de thread)
    for action in plan.actions.values():
        if action.status == "PENDING" and (not action.condition or action.condition()):
            pm._execute_action(action)

    assert action1.status == "PENDING"  # condition false => pas exécuté
    assert action2.status == "DONE"     # condition true => exécuté
