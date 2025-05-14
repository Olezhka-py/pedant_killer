import asyncio
import logging

from pedant_killer.telegram_bot.main_bot import run_bot

base_logger = logging.getLogger()
logging.basicConfig(
    filename='pedant_killer.log',
    format='%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main() -> None:
    print('старт бота')
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        base_logger.info('Exit')
