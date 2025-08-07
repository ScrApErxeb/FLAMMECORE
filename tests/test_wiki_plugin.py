# tests/test_wiki_plugin.py
import pytest
from unittest.mock import patch, Mock
from core.plugins.wiki_plugin import WikiPlugin
from core.signal import Signal, Action, SignalType

def test_wiki_plugin_handle_signal_success():
    plugin = WikiPlugin()
    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"query": "Python_(langage)"})

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"extract": "Python est un langage de programmation."}

    with patch("core.plugins.wiki_plugin.requests.get", return_value=mock_response):
        action = plugin.handle_signal(signal)
        assert action is not None
        assert "Python est un langage" in action.params["summary"]

def test_wiki_plugin_handle_signal_not_found():
    plugin = WikiPlugin()
    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"query": "ArticleInexistant12345"})

    mock_response = Mock()
    mock_response.status_code = 404

    with patch("core.plugins.wiki_plugin.requests.get", return_value=mock_response):
        action = plugin.handle_signal(signal)
        assert action is not None
        assert action.params["summary"] == "Article introuvable."

def test_wiki_plugin_handle_signal_exception():
    plugin = WikiPlugin()
    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"query": "Python"})

    with patch("core.plugins.wiki_plugin.requests.get", side_effect=Exception("Erreur réseau")):
        action = plugin.handle_signal(signal)
        assert action is not None
        assert "Erreur API Wiki" in action.params["summary"]
