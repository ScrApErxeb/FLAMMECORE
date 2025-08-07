from core.signal import Signal, Action

class Plugin:
    def __init__(self):
        self.name = "math"

    def handle_signal(self, signal: Signal):
        a = signal.payload.get("a")
        b = signal.payload.get("b")
        if a is None or b is None:
            return Action(id="math_error", params={"error": "Chiffres manquants"})
        try:
            result = float(a) + float(b)
            return Action(id="math_result", params={"result": result})
        except Exception as e:
            return Action(id="math_error", params={"error": str(e)})
