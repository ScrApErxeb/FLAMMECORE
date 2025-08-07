# core/plugin_manager.py
import importlib
from typing import Optional
from core.signal import Signal, Action
from core.balancer import Balancer  # si tu as un système de routage, sinon à supprimer

class PluginManager:
    def __init__(self, local_plugins=None, plugin_init_args=None, allowed_methods=None):
        # dictionnaire plugins chargés : nom -> instance
        self.plugins = {}

        # instancie le balancer si besoin, sinon supprimer
        self.balancer = Balancer(local_plugins or [])

        # dict d’arguments pour instanciation plugins
        self.plugin_init_args = plugin_init_args or {}

        # méthodes autorisées à appeler sur plugins (ex: handle_signal)
        self.allowed_methods = allowed_methods or {"handle_signal"}

    def load_plugin(self, module_path: str) -> Optional[str]:
        """
        Charge un plugin dynamique à partir d’un module_path type "core.plugins.hello_plugin"
        Le plugin doit contenir une classe `Plugin` avec un attribut .name
        """
        try:
            module = importlib.import_module(module_path)
            plugin_class = getattr(module, "Plugin")

            # récupère args init ou {} si pas d’args pour ce plugin
            init_args = self.plugin_init_args.get(plugin_class.__name__, {})

            plugin_instance = plugin_class(**init_args)
            self.register_plugin(plugin_instance)
            print(f"[PluginManager] Plugin '{plugin_instance.name}' chargé.")
            return plugin_instance.name

        except Exception as e:
            print(f"[PluginManager] Erreur chargement plugin {module_path}: {e}")
            return None

    def register_plugin(self, plugin_instance):
        """
        Enregistre un plugin dans le manager
        """
        self.plugins[plugin_instance.name] = plugin_instance

    def unregister_plugin(self, plugin_name: str):
        """
        Désenregistre un plugin
        """
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]

    def handle_signal(self, signal: Signal) -> Optional[Action]:
        """
        Route un signal vers le plugin adéquat
        """
        plugin_name = signal.payload.get("plugin_name")
        if not plugin_name:
            print("[PluginManager] Signal sans plugin_name")
            return None

        # Utilise le balancer pour décider où router (local ou cloud)
        route = self.balancer.route(plugin_name)

        if route == "local" and plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]

            try:
                if "handle_signal" in self.allowed_methods and hasattr(plugin, "handle_signal"):
                    return plugin.handle_signal(signal)
                else:
                    print(f"[PluginManager] Méthode handle_signal non autorisée pour plugin '{plugin_name}'")
                    return None
            except Exception as e:
                print(f"[PluginManager] Erreur dans plugin '{plugin_name}': {e}")
                return None

        elif route == "cloud":
            # Si t'as une API cloud, gère ici, sinon renvoie None ou simule
            return self.call_cloud_api(signal)

        else:
            print(f"[PluginManager] Plugin '{plugin_name}' non trouvé ou route inconnue")
            return None

    def call_cloud_api(self, signal: Signal) -> Optional[Action]:
        # Simulation d’appel cloud (à remplacer par un vrai appel)
        return Action(
            id="cloud_action_1",
            params={"info": f"Réponse cloud pour {signal.payload.get('plugin_name', '')}"}
        )
