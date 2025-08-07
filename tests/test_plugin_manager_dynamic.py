# tests/test_plugin_manager_dynamic.py
import pytest
from core.signal import Signal, SignalType
from core.plugin_manager import PluginManager

def test_dynamic_load_unload():
    pm = PluginManager(local_plugins=[])

    # Charger un plugin test (supposons qu’il existe core.plugins.weather_plugin avec classe Plugin)
    plugin_name = pm.load_plugin("core.plugins.weather_plugin")
    assert plugin_name == "weather"
    assert "weather" in pm.plugins

    # Tester handle_signal
    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "weather", "location": "Paris"})
    action = pm.handle_signal(signal)
    assert action is not None
    assert "weather" in action.params.get("weather", "")

    # Décharger le plugin
    pm.unload_plugin("weather")
    assert "weather" not in pm.plugins

    # Maintenant handle_signal doit retourner None
    action2 = pm.handle_signal(signal)
    assert action2 is None
