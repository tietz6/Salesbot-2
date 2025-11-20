
import math

def analyze_voice(features: dict) -> dict:
    # features: {speed_wpm, pauses, energy, clarity, pitch_var, emotion_hint}
    speed = float(features.get("speed_wpm", 120) or 120)
    pauses = float(features.get("pauses", 3) or 3)
    energy = float(features.get("energy", 0.6) or 0.6)
    clarity = float(features.get("clarity", 0.7) or 0.7)
    pitch = float(features.get("pitch_var", 0.5) or 0.5)
    hint = str(features.get("emotion_hint") or "").lower()

    # scores (0..100)
    score_conf = max(0, min(100, int((energy * 55) + (clarity * 40) - (pauses * 3))))
    score_emot = max(0, min(100, int((pitch * 60) + (energy * 30))))
    score_speed = max(0, min(100, int(100 - abs(speed - 140))))

    # labels
    if "ang" in hint:
        emo = "angry"
    elif "sad" in hint:
        emo = "sad"
    elif "exc" in hint:
        emo = "excited"
    else:
        if energy > 0.7:
            emo = "positive"
        elif energy < 0.4:
            emo = "low"
        else:
            emo = "neutral"

    return {
        "confidence_score": score_conf,
        "emotion_score": score_emot,
        "speed_score": score_speed,
        "label": emo,
        "raw": {
            "speed_wpm": speed,
            "pauses": pauses,
            "energy": energy,
            "clarity": clarity,
            "pitch_var": pitch,
            "emotion_hint": hint
        }
    }
