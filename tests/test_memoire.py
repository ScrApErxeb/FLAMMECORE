import pytest
from core.plugins.memoire_plugin import Plugin as MemoirePlugin
from core.memoire import MemoireStorage, Memoire
from core.signal import Signal

@pytest.fixture
def memoire_plugin():
    # On vide la mémoire avant chaque test pour être clean
    storage = MemoireStorage()
    storage.STORAGE_FILE.unlink(missing_ok=True)
    return MemoirePlugin()

def test_add_memory_with_context(memoire_plugin):
    signal = Signal(
        name="test_add",
        payload={
            "action": "add_memory",
            "vector": [1, 2, 3],
            "response_id": "resp_123",
            "context_id": "ctx_abc"
        }
    )
    action = memoire_plugin.handle_signal(signal)
    assert action.id == "memoire_added"
    assert "id" in action.params

def test_search_memory_with_context(memoire_plugin):
    # Ajout d’une mémoire avec context_id
    add_signal = Signal(
        name="test_add",
        payload={
            "action": "add_memory",
            "vector": [1, 2, 3],
            "response_id": "resp_456",
            "context_id": "ctx_xyz"
        }
    )
    memoire_plugin.handle_signal(add_signal)

    # Recherche avec le même context_id : doit trouver la mémoire
    search_signal = Signal(
        name="test_search",
        payload={
            "action": "search_memory",
            "vector": [1, 2, 3],
            "context_id": "ctx_xyz"
        }
    )
    action = memoire_plugin.handle_signal(search_signal)
    assert action.id == "memoire_search_result"
    assert action.params["response_id"] == "resp_456"
    assert action.params["context_id"] == "ctx_xyz"

def test_search_memory_with_different_context_returns_empty(memoire_plugin):
    # Ajout d’une mémoire avec un context_id donné
    add_signal = Signal(
        name="test_add",
        payload={
            "action": "add_memory",
            "vector": [1, 2, 3],
            "response_id": "resp_789",
            "context_id": "ctx_111"
        }
    )
    memoire_plugin.handle_signal(add_signal)

    # Recherche avec un context_id différent : ne doit rien trouver
    search_signal = Signal(
        name="test_search",
        payload={
            "action": "search_memory",
            "vector": [1, 2, 3],
            "context_id": "ctx_222"
        }
    )
    action = memoire_plugin.handle_signal(search_signal)
    assert action.id == "memoire_empty"

def test_unknown_action_returns_error(memoire_plugin):
    signal = Signal(
        name="test_unknown",
        payload={"action": "foo_bar"}
    )
    action = memoire_plugin.handle_signal(signal)
    assert action.id == "memoire_error"
