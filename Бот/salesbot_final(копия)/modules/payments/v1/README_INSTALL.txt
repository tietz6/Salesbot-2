
Payments v1 — FakeProvider (training/offline)

Что входит:
  - PaymentsEngine: создание инвойса, смена статусов, генерация webhook
  - FakeProvider: эмуляция онлайн-оплаты
  - FastAPI маршруты /payments/*
  - Таймлайн статусов (SQLite через core/db)

Статусы:
  pending -> paid / failed -> refunded (опционально)

Использование:
  1) POST /payments/invoice  {amount, currency, deal_id?}
  2) POST /payments/pay/{invoice_id}
  3) GET  /payments/status/{invoice_id}
