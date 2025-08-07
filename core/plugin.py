# core/plugin.py

from typing import Callable, Dict

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        if name in self.plugins:
            raise ValueError(f"Plugin '{name}' is déjà enregistré.")
        self.plugins[name] = func

    def call(self, name: str, data: dict = {}) -> str:
        if name not in self.plugins:
            raise ValueError(f"Plugin '{name}' introuvable.")
        return self.plugins[name](data)
