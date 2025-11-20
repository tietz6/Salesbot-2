# Пример шаблона для модуля upsell v3
# Сохраните бизнес-логику прежней; ниже — только регистрация телеграм-хэндлеров.

from aiogram import types
from aiogram.dispatcher import Dispatcher

# Здесь — импорт бизнес-функций модуля (ленивый внутри хэндлера, чтобы избежать циклов)
def register_telegram(dp: Dispatcher, registry):
    """
    Регистрируем все телеграм-хэндлеры, которые относятся к этому модулю.
    Вызывается автозагрузчиком telegram/autoload.py.
    """
    @dp.message_handler(commands=["upsell"])
    async def _cmd_upsell(message: types.Message):
        # ленивый импорт бизнес-логики
        try:
            from .service import start_upsell_session  # пример
        except Exception:
            # если нет service — используем заглушку
            async def start_upsell_session(user_id):
                return {"ok": True, "note": "stub"}

        user_id = message.from_user.id
        result = start_upsell_session(user_id)
        # Если result — coroutine, await it
        if hasattr(result, "__await__"):
            result = await result
        await message.reply(f"Upsell started: {result}")