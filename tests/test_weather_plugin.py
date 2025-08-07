# tests/test_weather_plugin.py
import pytest
from unittest.mock import patch, Mock
from core.signal import Signal, SignalType
from core.plugin_manager import PluginManager

@patch("core.plugins.weather_plugin.requests.get")
def test_weather_plugin(mock_get):
    # Prépare la réponse mockée
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"description": "ensoleillé"}],
        "main": {"temp": 25}
    }
    mock_get.return_value = mock_response

    # Instancie PluginManager avec un dict args pour le plugin weather
    pm = PluginManager(local_plugins=[], plugin_init_args={"Plugin": {"api_key": "fake_api_key"}})
    
    # Charge dynamiquement le plugin météo
    plugin_name = pm.load_plugin("core.plugins.weather_plugin")
    assert plugin_name == "weather"
    
    # Crée un signal météo
    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "weather", "location": "Lyon"})
    
    # Handle le signal via PluginManager
    action = pm.handle_signal(signal)

    # Vérifie qu'on a bien une action et le texte attendu
    assert action is not None
    assert "Le temps à Lyon est ensoleillé avec 25°C." == action.params["weather"]
