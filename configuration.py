import toml

CONFIG = None

class Configuration:
    config_file = "pymips.toml"

    def __init__(self, config_file=config_file):
        if CONFIG is not None:
            raise RuntimeError("class Configuration is a singleton, cannot be instantiated twice")
        self.config_file = config_file
        self.load()

    def load(self):
        CONFIG = toml.load(self.config_file)

    def get_config(self, key):
        try:
            if key == "memory_mapped":
                return self.CONFIG["features"]["memory_mapped"]
            elif key == "end_of_instruction":
                return self.CONFIG["features"]["end_of_instruction"]
            elif key == "entry_point":
                return self.CONFIG["runner"]["entry_point"]
            
        except KeyError:
            return None

