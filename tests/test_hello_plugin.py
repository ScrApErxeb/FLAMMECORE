import pytest
from core.plugin_manager import PluginManager
from core.signal import Signal, SignalType

def test_hello_plugin():
    pm = PluginManager(local_plugins=[])
    plugin_name = pm.load_plugin("core.plugins.hello_plugin")
    assert plugin_name == "hello"

    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "hello", "text": "Coucou"})
    action = pm.handle_signal(signal)

    assert action is not None
    assert action.params["response"] == "Plugin Hello dit : Coucou"
