import json
import sys


def parse_config() -> dict:
    try:
        with open("config.json") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(" [x] Error: Failed to parse config.json. Try running setup.py\n", e)
        sys.exit(-1)
    except FileNotFoundError:
        print(" [x] Error: Missing config.json. Try running setup.py")
        sys.exit(-1)
