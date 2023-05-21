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
        try:
            return toml.load(self.config_file)
        except FileNotFoundError:
            print("Configuration file not found, generating default configuration file")
            self.generate_default_config()

    def generate_default_config(self):
        default_config = {
            "features": {
                "memory_mapped": False,
                "end_of_instruction": True
            },
            "runner": {
                "entry_point": "main",
                "file_to_run": "hello.asm"
            },
            "debugger" : {
                "breakpoints": [],
                "watchpoints": []
            }
        }
        with open(self.config_file, "w") as f:
            toml.dump(default_config, f)

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

