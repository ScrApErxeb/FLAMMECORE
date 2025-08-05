import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))



from core.gomde import GomdeStorage, Gomde
from core.porte import PorteStorage, Porte
from core.reponse import ReponseStorage, Reponse, generate_simple_response
from core.memoire import MemoireStorage, Memoire

def test_full_pipeline(tmp_path):
    # Setup stockage temporaire
    gomde_storage = GomdeStorage()
    gomde_storage.STORAGE_FILE = tmp_path / "gomdes.json"
    porte_storage = PorteStorage()
    porte_storage.STORAGE_FILE = tmp_path / "portes.json"
    reponse_storage = ReponseStorage()
    reponse_storage.STORAGE_FILE = tmp_path / "reponses.json"
    memoire_storage = MemoireStorage()
    memoire_storage.STORAGE_FILE = tmp_path / "memoire.json"

    # 1. Création d'un Gomde
    gomde = Gomde("bonjour agent FlammeCore")
    gomde_storage.save_gomde(gomde)

    # 2. Transformation en Porte
    porte = Porte(gomde)
    porte_storage.save_porte(porte)

    # 3. Génération de la Réponse
    reponse = generate_simple_response(porte)
    reponse_storage.save_reponse(reponse)

    # 4. Stockage dans la mémoire
    memoire = Memoire(vector=porte.encoding, response_id=reponse.id)
    memoire_storage.save_memoire(memoire)

    # Vérifications
    gomdes = gomde_storage.list_gomdes()
    portes = porte_storage.list_portes()
    reponses = reponse_storage.list_reponses()
    memoires = memoire_storage.list_memoires()

    assert len(gomdes) == 1
    assert len(portes) == 1
    assert len(reponses) == 1
    assert len(memoires) == 1

    assert portes[0]["gomde_id"] == gomdes[0]["id"]
    assert reponses[0]["porte_id"] == portes[0]["id"]
    assert memoires[0]["response_id"] == reponses[0]["id"]
