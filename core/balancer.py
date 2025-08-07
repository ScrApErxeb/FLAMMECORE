# core/balancer.py

class Balancer:
    def __init__(self, local_plugins):
        # local_plugins : liste ou set des noms de plugins dispo en local
        self.local_plugins = set(local_plugins)

    def route(self, plugin_name):
        if plugin_name in self.local_plugins:
            return "local"
        else:
            return "cloud"
