import logging

from aiogram import Dispatcher

from pedant_killer.telegram_bot.bot_init import bot
from pedant_killer.telegram_bot.handlers.base_commands import base_router
from pedant_killer.telegram_bot.handlers.repair_or_diagnostic import router_for_diagnostics
from pedant_killer.containers import container

bot_main_logger = logging.getLogger('bot_main_logger')

dp = Dispatcher()


async def run_bot() -> None:
    container.init_resources()
    container.wire()
    dp.include_router(base_router)
    dp.include_router(router_for_diagnostics)
    bot_main_logger.info('Bot started')
    try:
        print('бот вкл')
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
