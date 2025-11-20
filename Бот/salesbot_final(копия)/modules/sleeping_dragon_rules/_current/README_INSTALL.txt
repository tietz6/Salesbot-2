
sleeping_dragon_rules/v1 — детерминированные правила качества ответа
-------------------------------------------------------------------
Что даёт:
  - Правила (регулярки/эвристики) для мгновенного выявления ошибок
  - Комбинированный скор: RULE (0..10) + LLM (0..10) → COMBINED (0..10)
  - Готовые короткие исправления («сделай вот так») + уточняющий вопрос
  - Glue для sleeping_dragon/v4

Роуты:
  POST /sleep_dragon_rules/v1/score   {history?, reply, stage?}
  POST /sleep_dragon_rules/v1/suggest {history?, reply, stage?}
