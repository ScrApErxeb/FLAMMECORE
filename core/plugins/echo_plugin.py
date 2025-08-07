from core.signal import Signal, SignalType, Action

class Plugin:
    def __init__(self):
        self.name = "echo"

    def handle_signal(self, signal: Signal):
        text = signal.payload.get("text", "")
        return Action(id="echo_action", params={"response": text})
