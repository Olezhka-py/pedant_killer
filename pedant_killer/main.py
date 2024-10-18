import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from pedant_killer.handlers.base_commands import base_router
from pedant_killer.handlers.repair_or_diagnostic import router_for_diagnostics
from pedant_killer.config import config
from pedant_killer.database.database import database_logger


base_logger = logging.getLogger()
logging.basicConfig(
    filename='pedant_killer.log',
    format='%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot = Bot(
    config.TG_API_DIGIT_SPACE_BOT.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


async def run() -> None:
    dp.include_router(base_router)
    dp.include_router(router_for_diagnostics)
    base_logger.info('Bot started')
    await dp.start_polling(bot)


try:
    asyncio.run(run())
except KeyboardInterrupt:
    base_logger.info('Exit')
