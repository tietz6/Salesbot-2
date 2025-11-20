
import json, random
from dataclasses import dataclass, asdict
from core.state.v1 import StateStore
from core.voice_gateway.v1 import VoicePipeline

MODULES = ["master_path","objections","upsell","arena"]

@dataclass
class ExamState:
    module: str
    answers: list
    score: int
    done: bool
    report: dict
    def to_dict(self): return asdict(self)

class ExamAutoCheck:
    def __init__(self, sid:str):
        self.sid=f"exam:{sid}"
        self.store=StateStore("salesbot.db")
        raw=self.store.get(self.sid)
        if raw:
            try:
                d=json.loads(raw)
                self.state=ExamState(**d)
            except:
                self._reset()
        else:
            self._reset()
        try: self.llm=VoicePipeline().llm
        except: self.llm=None

    def _reset(self):
        self.state = ExamState(
            module=random.choice(MODULES),
            answers=[],
            score=0,
            done=False,
            report={}
        )
        self._save()

    def _save(self):
        self.store.set(self.sid, json.dumps(self.state.to_dict(), ensure_ascii=False))

    def start(self):
        self._reset()
        return {"ok":True, "module":self.state.module}

    def answer(self, text:str)->dict:
        if self.state.done:
            return {"error":"exam finished"}

        self.state.answers.append(text)

        partial_score=0
        feedback=None
        if self.llm:
            try:
                msg=[
                  {"role":"system","content":f"Ты экзаменатор. Модуль: {self.state.module}. Оцени ответ 0-5 и дай обратную связь."},
                  {"role":"user","content":text}
                ]
                feedback=self.llm.chat(msg)
                if any(s in feedback.lower() for s in ["5","отлично","идеально"]):
                    partial_score=5
                elif any(s in feedback.lower() for s in ["4"]):
                    partial_score=4
                elif any(s in feedback.lower() for s in ["3"]):
                    partial_score=3
                elif any(s in feedback.lower() for s in ["2"]):
                    partial_score=2
                else:
                    partial_score=1
            except:
                partial_score=random.randint(1,5)

        self.state.score += partial_score
        self._save()

        if len(self.state.answers)>=5:
            self.state.done=True
            self.state.report={
                "module":self.state.module,
                "total_score":self.state.score,
                "answers":self.state.answers
            }
            self._save()
            return {
                "done":True,
                "score":self.state.score,
                "report":self.state.report
            }

        return {
            "done":False,
            "current_score":self.state.score,
            "feedback":feedback
        }

    def result(self):
        if not self.state.done:
            return {"error":"not finished"}
        return self.state.report
