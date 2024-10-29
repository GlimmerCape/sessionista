import yaml
from textual.binding import Binding

def load_bindings(bindings_file):
    bindings = []
    with open(bindings_file, "r") as f:
        config = yaml.safe_load(f)
        for action, key in config.get("bindings", {}).items():
            bindings.append(Binding(key, action, action.capitalize()))
    return bindings
