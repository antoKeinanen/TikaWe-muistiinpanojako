import json

def parse_config():
    try:
        with open("config.json") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(" [x] Error: Failed to parse config.json. Try running setup.py\n", e)
        exit(-1)
    except FileNotFoundError:
        print(" [x] Error: Missing config.json. Try running setup.py")
        exit(-1)
    
