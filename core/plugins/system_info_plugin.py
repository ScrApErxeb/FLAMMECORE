# core/plugins/system_info_plugin.py
from core.signal import Signal, SignalType, Action
import platform
import psutil

class SystemInfoPlugin:
    def __init__(self):
        self.name = "system_info"

    def handle_signal(self, signal: Signal):
        try:
            cpu = platform.processor()
            ram = psutil.virtual_memory().percent
            os_info = platform.system() + " " + platform.release()
            info = f"CPU: {cpu}, RAM utilisée: {ram}%, OS: {os_info}"
            return Action(id="action_sysinfo_1", params={"system_info": info})
        except Exception as e:
            return Action(id="action_sysinfo_1", params={"system_info": f"Erreur récupération info système: {str(e)}"})
