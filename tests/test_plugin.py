# tests/test_plugin.py

from core.plugin import PluginManager
from core.plugins.meteo import plugin_meteo

def test_plugin_call():
    manager = PluginManager()
    manager.register("meteo", plugin_meteo)

    result = manager.call("meteo", {"lieu": "Paris"})
    assert "Paris" in result
    assert "28" in result
