
exam_autocheck/v2 — full automatic exam evaluator
-------------------------------------------------
Функции:
  - проверка 4 модулей: master_path, objections, upsell, arena
  - DeepSeek анализ каждого ответа
  - итоговый балл 0–100
  - детальный отчёт: ошибки, советы, лучшие моменты
  - конфигурация весов по этапам
  - интеграция с sleeping_dragon/v4 для ошибок

Роуты:
  POST /exam/v2/start/{sid}
  POST /exam/v2/answer/{sid}
  GET  /exam/v2/result/{sid}
