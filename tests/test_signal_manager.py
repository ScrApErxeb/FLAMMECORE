import time
import pytest
from core.signal import Signal, SignalType
from core.signal_manager import SignalManager


def test_signal_manager_processing_order():
    # Liste pour capturer l’ordre des signaux traités
    processed_signals = []

    # Handler de test : ajoute l'ID du signal traité dans une liste
    def test_handler(signal):
        processed_signals.append((signal.payload["name"]))

    manager = SignalManager(handler=test_handler)

    # Création de signaux avec des priorités variées
    low_priority = Signal(type=SignalType.USER_INPUT, payload={"name": "low"})
    high_priority = Signal(type=SignalType.PLUGIN_CALL, payload={"name": "high"})
    medium_priority = Signal(type=SignalType.SYSTEM_EVENT, payload={"name": "medium"})

    # Envoi des signaux (ordre volontairement mélangé)
    manager.send_signal(low_priority, priority=10)
    manager.send_signal(high_priority, priority=1)
    manager.send_signal(medium_priority, priority=5)

    # Attendre que tous les signaux soient traités
    time.sleep(0.5)

    # Stopper proprement le manager
    manager.stop()

    # Vérifier que les signaux ont été traités dans le bon ordre de priorité
    assert processed_signals == ["high", "medium", "low"]
