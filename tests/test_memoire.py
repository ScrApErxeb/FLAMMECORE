from core.memoire import Memoire, MemoireStorage

def test_memoire_storage(tmp_path):
    storage_path = tmp_path / "memoire.json"
    storage = MemoireStorage()
    storage.STORAGE_FILE = storage_path

    memoire = Memoire(vector=[1, 2, 3], response_id="test-response-id")
    storage.save_memoire(memoire)

    memoires = storage.list_memoires()
    assert len(memoires) == 1
    assert memoires[0]["response_id"] == "test-response-id"
