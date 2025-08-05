from core.gomde import Gomde, GomdeStorage
import os

def test_gomde_storage(tmp_path):
    storage_path = tmp_path / "gomdes.json"
    storage = GomdeStorage()
    storage.STORAGE_FILE = storage_path

    gomde = Gomde("test unitaire")
    storage.save_gomde(gomde)

    gomdes = storage.list_gomdes()
    assert len(gomdes) == 1
    assert gomdes[0]["content"] == "test unitaire"
