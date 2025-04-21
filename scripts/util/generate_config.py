import json
import secrets
from pathlib import Path


def generate_config():
    config_path = Path("config.json")
    config_path.unlink(missing_ok=True)

    with config_path.open("w") as file:
        config = {
            "csrf_secret": secrets.token_urlsafe(32),
            "csrf_enabled": True,
        }
        json.dump(config, file)
