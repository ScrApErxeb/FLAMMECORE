import pytest
from core.signal import Signal
from core.planner import Planner

class FakeMemoirePlugin:
    def handle_signal(self, signal):
        # Simule un résultat mémoire si le vecteur contient 1, sinon rien
        if signal.payload.get("vector") and 1 in signal.payload["vector"]:
            return type("Action", (), {
                "id": "memoire_search_result",
                "params": {"response_id": "fake123", "score": 0.9}
            })()
        else:
            return type("Action", (), {
                "id": "memoire_error",
                "params": {}
            })()

@pytest.fixture
def planner():
    p = Planner()
    p.memoire_plugin = FakeMemoirePlugin()
    return p

def test_enrich_signal_with_memory_found(planner):
    signal = Signal(name="test", payload={"vector": [0,1,2]}, context=None)
    enriched = planner.enrich_signal_with_memory(signal)
    assert "memory" in enriched.context
    assert enriched.context["memory"] is not None
    assert enriched.context["memory"]["response_id"] == "fake123"

def test_enrich_signal_with_memory_empty(planner):
    signal = Signal(name="test", payload={"vector": [0, 2, 3]}, context=None)
    enriched = planner.enrich_signal_with_memory(signal)
    assert "memory" in enriched.context
    assert enriched.context["memory"] is None

def test_enrich_signal_creates_context(planner):
    signal = Signal(name="test", payload={"vector": [1]})
    signal.context = None
    enriched = planner.enrich_signal_with_memory(signal)
    assert enriched.context is not None

def test_merge_contexts_merges_dicts(planner):
    base = {"memory": {"response_id": "old"}, "other": 123}
    update = {"memory": {"score": 0.8}, "newkey": "val"}
    merged = planner.merge_contexts(base, update)
    assert merged["memory"]["response_id"] == "old"
    assert merged["memory"]["score"] == 0.8
    assert merged["other"] == 123
    assert merged["newkey"] == "val"
