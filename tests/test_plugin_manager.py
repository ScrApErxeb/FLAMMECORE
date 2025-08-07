import pytest
from unittest.mock import MagicMock
from core.signal import Signal, Action
from core.plugin_manager import PluginManager

class DummyPlugin:
    def __init__(self, name, fail_times=0):
        self.name = name
        self.calls = 0
        self.fail_times = fail_times

    def handle_signal(self, signal):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise Exception("Simulated failure")
        return Action(id="success_action", params={"msg": "ok"})

def test_safe_handle_signal_retries_success():
    pm = PluginManager()
    plugin = DummyPlugin("dummy", fail_times=2)
    signal = Signal(type=None, payload={"plugin_name": "dummy"})

    result = pm.safe_handle_signal(plugin, signal, retries=3, retry_delay=0)
    assert result.id == "success_action"
    assert plugin.calls == 3  # 2 fails + 1 success

def test_safe_handle_signal_retries_failure():
    pm = PluginManager()
    plugin = DummyPlugin("dummy", fail_times=5)
    signal = Signal(type=None, payload={"plugin_name": "dummy"})

    result = pm.safe_handle_signal(plugin, signal, retries=3, retry_delay=0)
    assert result.id == "plugin_error"
    assert plugin.calls == 3  # tried 3 times and failed

