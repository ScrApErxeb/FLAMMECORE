# core/plugins/weather_plugin.py
from core.signal import Signal, SignalType, Action
import requests

class Plugin:
    def __init__(self, api_key: str):
        self.name = "weather"
        self.api_key = api_key

    def handle_signal(self, signal: Signal):
        location = signal.payload.get("location", "")
        if not location:
            return None
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric&lang=fr"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                report = f"Le temps à {location} est {weather} avec {temp}°C."
                return Action(id="action_weather_1", params={"weather": report})
            else:
                return Action(id="action_weather_1", params={"weather": "Ville introuvable."})
        except Exception as e:
            return Action(id="action_weather_1", params={"weather": f"Erreur API météo: {str(e)}"})
