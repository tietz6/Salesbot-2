
import json, os
BASE = os.path.dirname(__file__)
RUB = os.path.join(BASE,"data","rubric.json")

def grade(session_report: dict)->dict:
    r = json.load(open(RUB,"r",encoding="utf-8"))
    w = r["weights"]
    s = session_report.get("scores",{})
    total = int(
        (s.get("warmth",0)*w["warmth"]) +
        (s.get("empathy",0)*w["empathy"]) +
        (s.get("questions",0)*w["questions"]) +
        (s.get("payment",0)*w["payment"]) +
        (s.get("upsell",0)*w["upsell"])
    )
    verdict = "fail"
    if total >= r["thresholds"]["excellent"]:
        verdict = "excellent"
    elif total >= r["thresholds"]["pass"]:
        verdict = "pass"
    return {"total": total, "verdict": verdict}
