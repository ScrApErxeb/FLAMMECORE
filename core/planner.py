from core.signal import Signal, SignalType, Action
from core.plan import Plan

class Planner:
    def __init__(self):
        pass

    def plan_actions(self, signal: Signal) -> Plan:
        if signal.type == SignalType.PLUGIN_CALL:
            # Exemple basique : créer un plan avec une seule action
            action = Action(target="plugin_manager", params=signal.payload)
            return Plan(actions=[action])
        else:
            # Si le signal n’est pas gérable, retourner un plan vide
            return Plan(actions=[])
