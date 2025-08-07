from core.plugin_manager import PluginManager
from core.signal import Signal, SignalType

def test_math_plugin():
    pm = PluginManager(local_plugins=["math"])
    pm.load_plugin("core.plugins.math_plugin")

    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "math", "a": 5, "b": 3})
    action = pm.handle_signal(signal)

    assert action is not None
    assert action.params["result"] == 8.0
