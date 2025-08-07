from core.plugin_manager import PluginManager
from core.signal import Signal, SignalType

def test_time_plugin():
    pm = PluginManager(local_plugins=["time"])
    pm.load_plugin("core.plugins.time_plugin")

    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "time"})
    action = pm.handle_signal(signal)

    assert action is not None
    assert "time" in action.params
