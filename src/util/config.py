import json
import sys
from util.logger import Logger


def parse_config() -> dict:
    """
    Parse the configuration file 'config.json' and returns its contents as a dictionary.

    This function attempts to open and read 'config.json' file from the current
    directory. If the file is not found or contains invalid JSON, appropriate error
    messages are logged and the program exits with a status code of -1.

    Returns:
        dict: A dictionary containing the parsed contents of 'config.json'.
    """

    try:
        with open("config.json") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        Logger.error("Failed to parse config.json. Make sure its valid json.", e)
        sys.exit(-1)
    except FileNotFoundError:
        Logger.error("Could not find config.json. Create one with setup.py")
        sys.exit(-1)
