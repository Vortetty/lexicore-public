import json

def loadConfig():
    config = json.loads(open("lexicore/config/config.json", "r").read())
    return config
