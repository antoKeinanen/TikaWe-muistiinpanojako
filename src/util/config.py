import json
import sys
from util.logger import Logger
from models.config import Config


def parse_config() -> Config:
    """
    Parse the configuration file 'config.json' and returns its contents as a dictionary.

    Stops further execution on failure

    Returns:
        Config: An instance of the Config class if parsing is successful.
        NoReturn: Terminates the program if parsing fails.
    """

    try:
        with open("config.json") as file:
            data = json.load(file)
            try:
                return Config(**data)
            except TypeError as e:
                Logger.error("config.json does not match the expected structure.", e)
                return sys.exit(-1)
    except json.JSONDecodeError as e:
        Logger.error("Failed to parse config.json. Make sure its valid json.", e)
        return sys.exit(-1)
    except FileNotFoundError:
        Logger.error("Could not find config.json. Create one with setup.py")
        return sys.exit(-1)


config = parse_config()
