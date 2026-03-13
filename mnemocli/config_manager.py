import configparser
from pathlib import Path

# Move config to the hidden home directory
CONFIG_DIR = Path.home() / ".mnemocli"
CONFIG_FILE = CONFIG_DIR / "config.ini"

DEFAULT_CONFIG = """[Settings]
# The language used for Random Words generation.
# Supported languages: english, portuguese
language = portuguese

# Default time limit in minutes (if not specified via -t in CLI)
default_time = 10

[StandardMode]
# Modes that will be randomly shuffled during a 'standard' session.
included_modes = random_drill, palace_rush, palace_rush_reverse, even_run, odd_run, middle_out
"""

def load_config():
    """Loads the config.ini file from the user's home directory."""
    # Ensure the directory exists
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    return config
