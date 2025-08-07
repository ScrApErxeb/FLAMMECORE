# tests/test_wikipedia_plugin.py
import pytest
from core.plugins.wiki_plugin import WikipediaPlugin
from core.signal import Signal, SignalType

def test_wikipedia_plugin_handle_signal():
    plugin = WikipediaPlugin()

    signal = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "wikipedia", "query": "Python"})
    action = plugin.handle_signal(signal)

    assert action is not None
    assert "Résumé Wikipédia" in action.params.get("summary", "")

    # Test sans query (erreur)
    signal_empty = Signal(type=SignalType.PLUGIN_CALL, payload={"plugin_name": "wikipedia"})
    action_err = plugin.handle_signal(signal_empty)

    assert action_err.id == "wiki_error"
    assert "Aucune requête" in action_err.params.get("error", "")
