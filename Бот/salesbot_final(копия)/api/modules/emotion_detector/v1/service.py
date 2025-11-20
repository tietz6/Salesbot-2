
from .analysis import analyze_voice

def detect(payload: dict) -> dict:
    """
    payload may include raw ASR meta (optional)
    structure: {speed_wpm, pauses, energy, clarity, pitch_var, emotion_hint}
    """
    payload = payload or {}
    return analyze_voice(payload)
