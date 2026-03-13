import configparser
from pathlib import Path

CONFIG_FILE = Path("config.ini")

DEFAULT_CONFIG = """[Settings]
# The language used for Random Words generation.
# Supported languages: english, portuguese
language = english

# Default time limit in minutes (if not specified via -t in CLI)
default_time = 10

[StandardMode]
# Modes that will be randomly shuffled during a 'standard' session.
# Available options: random_drill, palace_rush, palace_rush_reverse, even_run, odd_run
included_modes = random_drill, palace_rush, palace_rush_reverse, even_run, odd_run
"""

def load_config():
    """Loads the config.ini file, creating it with defaults if missing."""
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    return config
