from core.planner import Planner
from core.signal import Signal, SignalType

def test_plan_creation_from_plugin_signal():
    planner = Planner()
    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "wiki", "query": "FlammeCore"})
    plan = planner.plan_actions(signal)
    assert len(plan.actions) == 1
    assert plan.actions[0].target == "plugin_manager"
