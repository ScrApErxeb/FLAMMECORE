from core.plugin_manager import PluginManager
from core.signal import Signal, SignalType
from core.plugins.planner_plugin import Plugin as PlannerPlugin
from core.plugins.echo_plugin import Plugin as EchoPlugin
from core.plugins.math_plugin import Plugin as MathPlugin

def test_planner_multiple_steps():
    local_plugins = ["echo", "math", "planner"]  # Tous les plugins locaux
    pm = PluginManager(local_plugins=local_plugins)

    echo = EchoPlugin()
    math = MathPlugin()
    planner = PlannerPlugin(plugin_manager=pm)

    pm.register_plugin(echo)
    pm.register_plugin(math)
    pm.register_plugin(planner)

    planner.plugin_manager = pm

    signal = Signal(type=SignalType.PLUGIN_CALL, payload={
        "plugin_name": "planner",
        "steps": [
            {"type": "echo", "text": "Bonjour"},
            {"type": "math", "operation": "add", "a": 5, "b": 7}
        ]
    })

    actions = planner.handle_signal(signal)
    assert isinstance(actions, list)
    assert any(action.params.get("response") == "Bonjour" for action in actions)
    assert any(action.params.get("result") == 12.0 for action in actions)
