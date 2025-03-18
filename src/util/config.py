import json
import sys
from util.logger import Logger


def parse_config() -> dict:
    try:
        with open("config.json") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        Logger.error("Failed to parse config.json. Make sure its valid json.", e)
        sys.exit(-1)
    except FileNotFoundError:
        Logger.error("Could not find config.json. Create one with setup.py")
        sys.exit(-1)
