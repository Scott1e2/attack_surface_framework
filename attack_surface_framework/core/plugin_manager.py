import os
import importlib
import inspect


class PluginManager:
    """
    Manages the dynamic loading and execution of plugins for threat detection.
    """

    def __init__(self, plugin_dir="plugins"):
        """
        Initialize the plugin manager with the specified directory.
        """
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        """
        Dynamically loads all plugins from the specified directory.
        """
        print("Scanning for plugins...")
        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = f"{self.plugin_dir}.{file[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for _, cls in inspect.getmembers(module, inspect.isclass):
                        if hasattr(cls, "run") and callable(cls.run):
                            self.plugins.append(cls())
                            print(f"Loaded plugin: {cls.__name__}")
                except Exception as e:
                    print(f"Failed to load plugin {file}: {e}")

    def execute_plugins(self, assets):
        """
        Executes all loaded plugins on the provided assets.
        """
        if not self.plugins:
            print("No plugins loaded.")
            return []

        results = []
        print("Executing plugins...")
        for plugin in self.plugins:
            try:
                print(f"Running {plugin.__class__.__name__}...")
                result = plugin.run(assets)
                results.append({
                    "plugin": plugin.__class__.__name__,
                    "result": result
                })
            except Exception as e:
                print(f"Error executing {plugin.__class__.__name__}: {e}")
        return results

    def get_plugin_list(self):
        """
        Returns a list of loaded plugins.
        """
        return [plugin.__class__.__name__ for plugin in self.plugins]
