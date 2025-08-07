from core.signal import Signal, SignalType
from core.plugin_manager import PluginManager
from core.plugins.weather_plugin import WeatherPlugin

plugin_manager = PluginManager()
weather_plugin = WeatherPlugin()
plugin_manager.register_plugin(weather_plugin)

def handle_signal(signal):
    action = plugin_manager.handle_signal(signal)
    if action:
        print(f"Action reçue : {action.params['weather']}")
    else:
        print("Aucun plugin ne gère ce signal.")

if __name__ == "__main__":
    # On simule un signal PLUGIN_CALL vers weather pour Lyon
    signal = Signal(
        type=SignalType.PLUGIN_CALL,
        payload={"plugin_name": "weather", "location": "Lyon"}
    )
    handle_signal(signal)
