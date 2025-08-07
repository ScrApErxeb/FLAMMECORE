# core/plugins/hello_plugin.py
from core.signal import Signal, Action

class Plugin:
    def __init__(self):
        self.name = "hello"

    def handle_signal(self, signal: Signal):
        text = signal.payload.get("text", "")
        response = f"Plugin Hello dit : {text}"
        return Action(id="action_hello_1", params={"response": response})
