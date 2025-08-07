import time
import threading
import pytest

from core.plan_manager import PlanManager, Plan, Action
from core.signal import Signal
from core.signal_manager import SignalManager

class DummySignalManager(SignalManager):
    def __init__(self):
        super().__init__(handler=lambda signal: None)  # handler factice
        self.signals = []

    def enqueue_signal(self, signal: Signal):
        self.signals.append(signal)


def always_success(**kwargs):
    return True

def fail_then_succeed_factory(fail_times=2):
    count = {"calls": 0}
    def func(**kwargs):
        if count["calls"] < fail_times:
            count["calls"] += 1
            return False
        return True
    return func

def test_plan_manager_execution():
    signal_manager = DummySignalManager()
    plan_manager = PlanManager(signal_manager)

    # Actions
    action1 = Action(id="a1", func=always_success)
    action2 = Action(id="a2", func=fail_then_succeed_factory(1), max_retries=3, dependencies=["a1"])
    action3 = Action(id="a3", func=always_success, dependencies=["a2"])

    plan = Plan(id="p1", actions=[action1, action2, action3])
    plan_manager.add_plan(plan)

    # Run plan_manager in a thread to not block
    t = threading.Thread(target=plan_manager.run)
    t.start()

    # Wait for plan to complete: max 5 seconds (arbitraire)
    timeout = time.time() + 5
    while not all(a.status == "DONE" for a in plan.actions.values()):
        if time.time() > timeout:
            break
        time.sleep(0.1)

    plan_manager.stop()
    t.join()

    # Assertions
    assert action1.status == "DONE"
    assert action2.status == "DONE"
    assert action2.retry_count == 1
    assert action3.status == "DONE"

    # Signal manager should have received signals for done actions
    done_signals = [s for s in signal_manager.signals if s.payload.get("status") == "done"]
    assert len(done_signals) == 3

