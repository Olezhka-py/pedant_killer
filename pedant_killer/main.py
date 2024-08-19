import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers.common import rt_1
from handlers.repair_or_diagnostic import rt_2
from config_reader import config
import logging


bot = Bot(
    config.TG_API_DIGIT_SPACE_BOT.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


async def main() -> None:
    dp.include_router(rt_1)
    dp.include_router(rt_2)
    logger.info("Starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger = logging.getLogger()
    logging.basicConfig(
        filename="/Users/olezhka/PycharmProjects/pedant_killer/pedant_killer.log",  # Установи свой путь
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exit")
