# plugins/meteo.py

def plugin_meteo(data: dict) -> str:
    location = data.get("lieu", "Ouagadougou")
    return f"Il fait 28°C à {location} 🌤️"
