
payments/v2 — платежный модуль
-------------------------------
Функции:
  - создание счета (invoice)
  - генерация payment_id + redirect_url
  - webhook обновляет статус (paid/failed)
  - синхронизация с CRM через crm_sync/v1
  - события → timeline (оплата успешна/неуспешна)

Роуты:
  POST /payments/v2/invoice/{deal_id}
  POST /payments/v2/webhook
  GET  /payments/v2/status/{deal_id}
