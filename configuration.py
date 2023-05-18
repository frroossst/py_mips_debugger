import toml

class Configuration:
    config = None
    config_file = "pymips.toml"

    def __init__(self, config_file=config_file):
        self.config_file = config_file

    def load(self):
        self.config = toml.load(self.config_file)

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

