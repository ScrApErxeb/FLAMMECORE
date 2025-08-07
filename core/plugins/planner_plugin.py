from core.signal import Signal, SignalType, Action
from core.plugin_manager import PluginManager

class Plugin:
    def __init__(self, plugin_manager: PluginManager):
        self.name = "planner"
        self.plugin_manager = plugin_manager

    def handle_signal(self, signal: Signal):
        steps = signal.payload.get("steps", [])
        if not steps:
            return [Action(id="planner_empty", params={"info": "Aucune étape à traiter."})]

        actions = []
        for idx, step in enumerate(steps):
            plugin_name = step.get("type")
            step_payload = dict(step)  # Copie pour ne pas muter l'original
            step_payload["plugin_name"] = plugin_name

            sub_signal = Signal(type=SignalType.PLUGIN_CALL, payload=step_payload)
            action = self.plugin_manager.handle_signal(sub_signal)
            if action:
                # Ajouter un identifiant unique par étape
                action.id = f"step_{idx+1}_{plugin_name}"
                actions.append(action)
            else:
                actions.append(Action(id=f"step_{idx+1}_{plugin_name}_failed", params={"error": f"Échec du plugin {plugin_name}"}))

        return actions
