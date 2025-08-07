import pytest
import time
import os
import json
import tempfile
from core.executor import ActionExecutor

def test_execute_echo():
    executor = ActionExecutor()
    actions = [{"type": "echo", "message": "Hello FlammeCore"}]
    results = executor.execute(actions)
    assert results[0]["result"] == "Hello FlammeCore"
    assert results[0]["status"] == "success"
    assert results[0]["error"] is None

def test_execute_add():
    executor = ActionExecutor()
    actions = [{"type": "add", "a": 2, "b": 3}]
    results = executor.execute(actions)
    assert results[0]["result"] == 5
    assert results[0]["status"] == "success"
    assert results[0]["error"] is None

def test_execute_unknown_action():
    executor = ActionExecutor()
    actions = [{"type": "multiply", "a": 2, "b": 3}]
    results = executor.execute(actions)
    assert results[0]["status"] == "failed"
    assert results[0]["result"] is None
    assert "Action inconnue" in results[0]["error"]

def test_execute_broken_action():
    executor = ActionExecutor()
    actions = [{"type": "add", "a": 2}]  # manque "b"
    results = executor.execute(actions)
    assert results[0]["status"] == "failed"
    assert results[0]["result"] is None
    assert "b" in results[0]["error"]

def test_hooks_are_called():
    executor = ActionExecutor()
    called = {"before": False, "after": False}

    def before_hook(action):
        called["before"] = True
        assert "type" in action

    def after_hook(action, result):
        called["after"] = True
        assert "status" in result
        assert "result" in result

    executor.register_before_hook(before_hook)
    executor.register_after_hook(after_hook)

    actions = [{"type": "echo", "message": "hook test"}]
    executor.execute(actions)

    assert called["before"] is True
    assert called["after"] is True

def test_parallel_execution_time():
    executor = ActionExecutor(max_workers=2)
    actions = [
        {"type": "echo", "message": "action 1", "delay": 2},
        {"type": "echo", "message": "action 2", "delay": 2},
    ]

    start = time.perf_counter()
    results = executor.execute(actions)
    duration = time.perf_counter() - start

    # En mode séquentiel, ça serait 4s, là ça doit être moins (environ 2s)
    assert duration < 3
    assert all(r["status"] == "success" for r in results)

def test_export_logs():
    executor = ActionExecutor()
    actions = [{"type": "echo", "message": "test export"}]
    executor.execute(actions)

    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmp_path = tmpfile.name

    executor.export_logs(tmp_path)

    with open(tmp_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert data[0]["action"]["type"] == "echo"
    assert "start_time" in data[0]
    os.remove(tmp_path)
