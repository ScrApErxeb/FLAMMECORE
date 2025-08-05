from core.reponse import Reponse, ReponseStorage, generate_simple_response
from core.porte import Porte
from core.gomde import Gomde

def test_reponse_storage(tmp_path):
    storage_path = tmp_path / "reponses.json"
    storage = ReponseStorage()
    storage.STORAGE_FILE = storage_path

    gomde = Gomde("test réponse")
    porte = Porte(gomde)
    reponse = generate_simple_response(porte)
    storage.save_reponse(reponse)

    reponses = storage.list_reponses()
    assert len(reponses) == 1
    assert reponses[0]["porte_id"] == porte.id

def test_generate_simple_response_keywords():
    gomde = Gomde("bonjour")
    porte = Porte(gomde)
    reponse = generate_simple_response(porte)
    assert "Salut" in reponse.content

    gomde = Gomde("Quelle heure est-il ?")
    porte = Porte(gomde)
    reponse = generate_simple_response(porte)
    assert "Il est actuellement" in reponse.content

    gomde = Gomde("bla bla")
    porte = Porte(gomde)
    reponse = generate_simple_response(porte)
    assert "je travaille dessus" in reponse.content.lower()
