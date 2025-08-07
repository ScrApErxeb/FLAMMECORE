# core/planner.py
from typing import List, Optional
from core.signal import Signal, SignalType
from core.action import Action

class Planner:
    def __init__(self):
        pass

    def plan(self, signal: Signal) -> Optional[Action]:
        if signal.type != SignalType.PLANNING_REQUEST:
            return None

        # TODO: logiques plus complexes à venir ici
        return Action(id="plan_action_1", params={"info": "Planificateur activé pour: " + str(signal.payload)})
