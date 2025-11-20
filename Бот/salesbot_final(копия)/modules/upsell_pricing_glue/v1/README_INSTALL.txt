
upsell_pricing_glue/v1 — ценностная связка для Upsell
-----------------------------------------------------
Назначение:
  - Считать цену с учётом скидок, купонов, НДС, валюты
  - Собирать bundle-предложение (basic/premium/pro) из каталога
  - Генерировать аргументацию выгоды для менеджера (LLM)
  - Готовые эндпоинты и glue для modules/upsell/v3

Входные данные (пример каталога):
catalog = {
  "basic":   {"title":"Basic",   "items":[{"sku":"song","price":1200}]},
  "premium": {"title":"Premium", "items":[{"sku":"song","price":1200},{"sku":"video","price":1800}]},
  "pro":     {"title":"Pro",     "items":[{"sku":"song","price":1200},{"sku":"video","price":1800},{"sku":"story","price":900}]}
}
