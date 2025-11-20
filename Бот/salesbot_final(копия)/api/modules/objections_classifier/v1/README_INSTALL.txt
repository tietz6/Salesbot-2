
objections_classifier/v1 — классификатор и обработчик возражений (жёсткий режим)
-------------------------------------------------------------------------------
Функции:
  - classify(utterance, history=None) -> {type, confidence, reasons[], advice}
  - apply_patterns(obj_type, history, last_reply) -> {template, coach_reply}
  - score_response(last_reply) -> {penalties[], score_delta}

Типы возражений: price, trust, need, timing, doubts, competing

Роуты:
  POST /objections_classifier/v1/classify
  POST /objections_classifier/v1/patterns
  POST /objections_classifier/v1/score
