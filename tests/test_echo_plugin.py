from core.plugin_manager import PluginManager
from core.signal import Signal, SignalType

def test_echo_plugin():
    pm = PluginManager(local_plugins=["echo"])
    pm.load_plugin("core.plugins.echo_plugin")

    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "echo", "message": "Salut Flamme"})
    action = pm.handle_signal(signal)

    assert action is not None
    assert action.params["echo"] == "Salut Flamme"
