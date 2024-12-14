import json
import importlib


def load_config(config_file="config.json"):
    """
    Loads the discovery configuration from a JSON file.
    """
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Failed to load configuration file: {e}")
        return {}


def execute_discovery_methods(config):
    """
    Dynamically loads and executes discovery methods based on the configuration.
    """
    all_assets = []

    for method_config in config.get("discovery_methods", []):
        module_name = method_config.get("module")
        function_name = method_config.get("function")
        enabled = method_config.get("enabled", False)

        if not enabled:
            continue

        try:
            # Dynamically import the module and function
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)

            # Execute the discovery function and collect assets
            print(f"Executing discovery method: {function_name} from {module_name}")
            assets = func(**method_config.get("parameters", {}))
            all_assets.extend(assets)
        except Exception as e:
            print(f"Error executing {function_name} in {module_name}: {e}")

    print(f"Total discovered assets: {len(all_assets)}")
    return all_assets


def discover_assets():
    """
    High-level function to control the asset discovery process.
    """
    print("Loading discovery configuration...")
    config = load_config()
    return execute_discovery_methods(config)
