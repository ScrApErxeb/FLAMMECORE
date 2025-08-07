import requests
from core.signal import Signal, Action

class Plugin:
    def __init__(self):
        self.name = "meteo"

    def handle_signal(self, signal: Signal):
        city = signal.payload.get("lieu", "Ouagadougou")
        api_key = "TA_CLE_API_OPENWEATHER"  # idéalement injectée via plugin_init_args ou config

        if not api_key:
            return Action(id="meteo_error", params={"error": "Clé API manquante."})

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr"
        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                message = data.get("message", "Erreur inconnue")
                return Action(id="meteo_error", params={"error": f"API OpenWeather: {message}"})

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            meteo_str = f"Il fait {temp}°C à {city}, {desc}"
            return Action(id="meteo_ok", params={"meteo": meteo_str})

        except Exception as e:
            return Action(id="meteo_error", params={"error": str(e)})
