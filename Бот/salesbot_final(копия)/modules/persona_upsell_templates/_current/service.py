
import json, os, random
from typing import Dict, Any, List

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data", "persona.json")

def load()->Dict[str, Any]:
    with open(DATA,"r",encoding="utf-8") as f:
        return json.load(f)

def sample(key: str)->str:
    p = load()
    if key == "gentle_answers":
        import random
        return random.choice(p["templates"]["gentle_answers"])
    return p["templates"].get(key,"")
