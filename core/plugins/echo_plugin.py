from core.signal import Signal, Action

class Plugin:
    def __init__(self):
        self.name = "echo"

    def handle_signal(self, signal: Signal):
        msg = signal.payload.get("message", "")
        return Action(id="echo", params={"echo": msg})
