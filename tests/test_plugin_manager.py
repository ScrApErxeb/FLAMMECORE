from core.plugin_manager import PluginManager
from core.signal import Signal, SignalType

pm = PluginManager()
pm.load_plugin("core.plugins.hello_plugin")

signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "hello", "message": "Coucou"})
action = pm.handle_signal(signal)

print(action.params["response"])  # -> Plugin Hello dit : Coucou
