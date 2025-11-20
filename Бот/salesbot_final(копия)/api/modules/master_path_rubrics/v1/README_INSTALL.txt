
master_path_rubrics/v1 — весовые рубрики оценки «Путь Мастера»
---------------------------------------------------------------
Этапы: greeting, qualification, support, offer, demo, final

Функции:
  - score_dialog(history) -> {stage_scores, total, issues[], tips[]}
  - rubric_summary() -> вернуть текущую рубрику

Роуты:
  POST /master_path_rubrics/v1/score  {history:[{role,content,stage}]}
  GET  /master_path_rubrics/v1/rubric
