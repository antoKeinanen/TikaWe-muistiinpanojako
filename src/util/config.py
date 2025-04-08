import json
import sys
from util.logger import Logger
from typing import NoReturn


def parse_config() -> dict | NoReturn:  # noqa: RUF020
    """
    Parse the configuration file 'config.json' and returns its contents as a dictionary.

    Stops further execution on failure

    Returns:
        dict: A dictionary containing the parsed contents of 'config.json'.
    """

    try:
        with open("config.json") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        Logger.error("Failed to parse config.json. Make sure its valid json.", e)
        return sys.exit(-1)
    except FileNotFoundError:
        Logger.error("Could not find config.json. Create one with setup.py")
        return sys.exit(-1)
