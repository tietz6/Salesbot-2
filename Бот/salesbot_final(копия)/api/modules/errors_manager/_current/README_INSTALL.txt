
errors_manager/v1 — централизованный сбор ошибок
------------------------------------------------
Функции:
  - track_error(module, context, exc, level='error', push_to_crm=False)
  - get_errors(prefix='err:', limit=200)
  - clear_errors(prefix='err:')

Хранилище:
  - core/state/v1 (таблица kv), ключи: err:<ts>:<module>

Интеграции:
  - bridges.crm_sync.v1 (опционально) → timeline (event='error')

Роуты:
  GET  /errors/v1/health
  GET  /errors/v1/list?limit=200
  POST /errors/v1/clear
  POST /errors/v1/track
