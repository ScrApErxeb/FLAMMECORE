# tests/test_sentiment_plugin.py
from core.plugins.sentiment_plugin import SentimentPlugin
from core.signal import Signal, SignalType

def test_sentiment_plugin():
    plugin = SentimentPlugin()

    signal_pos = Signal(type=SignalType.PLUGIN_CALL, payload={"text": "J'adore ce projet!"})
    action_pos = plugin.handle_signal(signal_pos)
    assert action_pos is not None
    assert action_pos.params["sentiment"] == "positif"

    signal_neg = Signal(type=SignalType.PLUGIN_CALL, payload={"text": "Je déteste ce bug."})
    action_neg = plugin.handle_signal(signal_neg)
    assert action_neg is not None
    assert action_neg.params["sentiment"] == "negatif"
