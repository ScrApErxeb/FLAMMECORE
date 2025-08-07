from core.signal import Signal, Action
from datetime import datetime

class Plugin:
    def __init__(self):
        self.name = "time"

    def handle_signal(self, signal: Signal):
        now = datetime.now().strftime("%H:%M:%S")
        return Action(id="time_info", params={"time": now})
