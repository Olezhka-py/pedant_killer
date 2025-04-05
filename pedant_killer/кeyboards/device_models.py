from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def model_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
