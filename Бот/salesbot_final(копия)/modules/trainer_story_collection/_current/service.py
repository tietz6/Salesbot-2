
import json, os
BASE = os.path.dirname(__file__)
CHK = os.path.join(BASE,"data","checklist.json")

def load():
    return json.load(open(CHK,"r",encoding="utf-8"))

def evaluate_story(payload: dict)->dict:
    data = load()
    text = (payload or {}).get("text","").lower()
    missing = [k for k in data["required"] if k not in text]
    score = max(0, 100 - len(missing)*15)
    return {"score": score, "missing": missing, "warm_questions": data["warm_questions"]}
