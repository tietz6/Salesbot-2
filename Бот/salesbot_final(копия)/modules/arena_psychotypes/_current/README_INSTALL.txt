
arena_psychotypes/v1 — психотипы клиентов и уровни сложности
------------------------------------------------------------
Фичи:
  - 8 психотипов (toxic, cold, doubter, haggler, fast, closed, emotional, rational)
  - уровни: easy / medium / hard / nightmare
  - динамика эмоций (calm→neutral→annoyed→angry) и «давление»
  - реакция на ошибки менеджера: становится жёстче при плохих ответах
  - LLM-перефраз клиентских реплик под контекст (через VoicePipeline)

Эндпоинты:
  POST /arena_psy/v1/spawn  {difficulty?, type?, context?}
  POST /arena_psy/v1/step   {state, manager_reply}
  GET  /arena_psy/v1/health
