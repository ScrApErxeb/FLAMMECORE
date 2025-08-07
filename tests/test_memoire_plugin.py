import pytest
from core.signal import Signal
from core.plugins.memoire_plugin import Plugin

@pytest.fixture
def mem_plugin():
    return Plugin()

def test_add_memory(mem_plugin):
    signal = Signal(type=None, payload={"action": "add_memory", "vector": [1, 0, 0], "response_id": "r1"})
    action = mem_plugin.handle_signal(signal)
    assert action.id == "memoire_added"
    assert "id" in action.params

def test_add_memory_no_vector(mem_plugin):
    signal = Signal(type=None, payload={"action": "add_memory"})
    action = mem_plugin.handle_signal(signal)
    assert action.id == "memoire_error"
    assert "Vecteur manquant" in action.params.get("error", "")

def test_search_memory_no_vector(mem_plugin):
    signal = Signal(type=None, payload={"action": "search_memory"})
    action = mem_plugin.handle_signal(signal)
    assert action.id == "memoire_error"
    assert "Vecteur de recherche manquant" in action.params.get("error", "")

def test_search_memory_empty(mem_plugin):
    # Clear storage before test
    mem_plugin.storage.STORAGE_FILE.unlink(missing_ok=True)

    signal = Signal(type=None, payload={"action": "search_memory", "vector": [1, 0, 0]})
    action = mem_plugin.handle_signal(signal)
    assert action.id == "memoire_empty"

def test_search_memory_found(mem_plugin):
    # Ajouter une mémoire
    add_signal = Signal(type=None, payload={"action": "add_memory", "vector": [1, 0, 0], "response_id": "r1"})
    mem_plugin.handle_signal(add_signal)

    search_signal = Signal(type=None, payload={"action": "search_memory", "vector": [1, 0, 0]})
    action = mem_plugin.handle_signal(search_signal)
    assert action.id == "memoire_search_result"
    assert "score" in action.params
    assert action.params["score"] > 0.9
