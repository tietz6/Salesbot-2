
import json, os, random
BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data", "scenarios.json")

def load():
    with open(DATA,"r",encoding="utf-8") as f:
        return json.load(f)

def list_scenarios():
    return load()["catalog"]

def random_scenario():
    return random.choice(list_scenarios())

def rubric():
    return load()["rubric"]
