# core/plugin_manager.py (début de fichier)
from core.logging_utils import get_logger
logger = get_logger("PluginManager")

import time

import importlib
import traceback
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
            logger.info(f"[PluginManager] Plugin '{plugin_instance.name}' chargé.")
            return plugin_instance.name

        except Exception as e:
            logger.info(f"[PluginManager] Erreur chargement plugin {module_path}: {e}")
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
        Route un signal vers le plugin adéquat, avec gestion avancée des erreurs
        """
        plugin_name = signal.payload.get("plugin_name")
        if not plugin_name:
            logger.info("[PluginManager] Signal sans plugin_name")
            return Action(id="plugin_error", params={"error": "Nom du plugin manquant dans le signal."})

        # Utilise le balancer pour décider où router (local ou cloud)
        route = self.balancer.route(plugin_name)

        if route == "local" and plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]

            if "handle_signal" in self.allowed_methods and hasattr(plugin, "handle_signal"):
                return self.safe_handle_signal(plugin, signal)
            else:
                logger.info(f"[PluginManager] Méthode handle_signal non autorisée pour plugin '{plugin_name}'")
                return Action(id="plugin_error", params={"error": f"Méthode non autorisée pour '{plugin_name}'"})

        elif route == "cloud":
            return self.call_cloud_api(signal)

        else:
            logger.info(f"[PluginManager] Plugin '{plugin_name}' non trouvé ou route inconnue")
            return Action(id="plugin_error", params={"error": f"Plugin '{plugin_name}' non disponible"})

    def safe_handle_signal(self, plugin, signal: Signal, retries=3, retry_delay=1) -> Action:
        """
        Enveloppe la méthode handle_signal d’un plugin avec gestion d’erreurs, retries et retour propre
        """
        for attempt in range(1, retries + 1):
            try:
                result = plugin.handle_signal(signal)
                if result is None:
                    raise ValueError(f"Plugin '{plugin.name}' n'a rien retourné.")
                return result
            except Exception as e:
                error_msg = f"Erreur dans plugin '{plugin.name}', tentative {attempt} : {str(e)}"
                logger.error(error_msg)
                if attempt < retries:
                    time.sleep(retry_delay)
                else:
                    logger.error(f"[PluginManager] Échec après {retries} tentatives.")
                    return Action(id="plugin_error", params={
                        "error": error_msg,
                        "plugin": plugin.name,
                        "retries": retries
                    })

    def call_cloud_api(self, signal: Signal) -> Optional[Action]:
        # Simulation d’appel cloud (à remplacer par un vrai appel)
        return Action(
            id="cloud_action_1",
            params={"info": f"Réponse cloud pour {signal.payload.get('plugin_name', '')}"}
        )
