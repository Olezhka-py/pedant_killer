import logging

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from pedant_killer.config import config

bot = Bot(
    config.TG_API_DIGIT_SPACE_BOT.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

