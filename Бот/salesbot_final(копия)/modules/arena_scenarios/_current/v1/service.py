
import json, os, random
BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data", "scenarios.json")

def list_scenarios():
    with open(DATA,"r",encoding="utf-8") as f:
        return json.load(f)

def random_scenario():
    import random
    return random.choice(list_scenarios())
