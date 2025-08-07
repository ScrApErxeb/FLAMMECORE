# tests/test_planner_plugin.py
import pytest
from core.signal import Signal, Action
from core.plugins.planner_plugin import Plugin

def test_planner_handle_signal():
    plugin = Plugin()

    # Cas vide
    signal_empty = Signal(type="plugin_call", payload={"steps": []})
    result_empty = plugin.handle_signal(signal_empty)
    assert isinstance(result_empty, list)
    assert result_empty[0].id == "planner_empty"

    # Cas simple avec 3 étapes, priorités et dépendances
    steps = [
        {"id": "step1", "priority": 2, "depends_on": []},
        {"id": "step2", "priority": 1, "depends_on": []},
        {"id": "step3", "priority": 3, "depends_on": ["step1"]},
    ]
    signal = Signal(type="plugin_call", payload={"steps": steps})
    results = plugin.handle_signal(signal)

    assert len(results) == 3
    # step2 a priorité 1, doit être traité avant step1
    assert results[0].id == "step2"
    assert results[1].id == "step1"
    # step3 dépend de step1 donc traité après
    assert results[2].id == "step3"

    # step3 est bien exécuté (pas skip)
    assert "exécutée" in results[2].params.get("info", "")
