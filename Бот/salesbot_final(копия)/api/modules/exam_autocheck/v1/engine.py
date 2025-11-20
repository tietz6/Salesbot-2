
from .rules import check_rules
from core.voice_gateway.v1 import VoicePipeline

class ExamAutoCheck:
    def __init__(self):
        # optional LLM-based checking
        try:
            self.llm = VoicePipeline().llm
        except Exception:
            self.llm = None

    def evaluate(self, transcript: str)->dict:
        rule_score, details = check_rules(transcript)
        llm_score = None
        llm_feedback = None

        if self.llm:
            try:
                msg = [
                    {"role":"system","content":"You are an exam evaluator for sales scripts. Score from 1 to 10."},
                    {"role":"user","content":transcript}
                ]
                ans = self.llm.chat(msg)
                llm_score = 7
                llm_feedback = ans
            except Exception:
                pass

        final_score = rule_score + (llm_score or 0)
        return {
            "ok": True,
            "rule_score": rule_score,
            "details": details,
            "llm_score": llm_score,
            "llm_feedback": llm_feedback,
            "final_score": final_score
        }
