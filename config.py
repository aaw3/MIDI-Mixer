import pyaml
from pyaml import yaml
class Config:
    def __init__(self):
        self.config = None
        self.read_config()

    def read_config(self):
        """Read the config file and store the contents in the config attribute."""
        try:
            with open("config.yaml", "r") as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            self.config = {}

    def get_saved_input(self):
        """Get the saved MIDI input port name from the config file."""
        if "input" in self.config:
            return self.config["input"]
        return None


    def save_input(self, port_name):
        """Save the MIDI input port name to the config file."""
        self.config["input"] = port_name

        with open("config.yaml", "w") as file:
            pyaml.dump(self.config, file)