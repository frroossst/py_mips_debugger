import toml

class Configuration:
    config_file = "pymips.toml"

    config = None

    def __init__(self, config_file=config_file):
        if self.config is not None:
            raise RuntimeError("class Configuration is a singleton, cannot be instantiated twice")
        self.config_file = config_file
        self.config = self.load()

    def load(self):
        return toml.load(self.config_file)

    def get_config(self, key):
        try:
            if key == "memory_mapped":
                return self.config["features"]["memory_mapped"]
            elif key == "end_of_instruction":
                return self.config["features"]["end_of_instruction"]
            elif key == "entry_point":
                return self.config["runner"]["entry_point"]
            
        except KeyError:
            return None

