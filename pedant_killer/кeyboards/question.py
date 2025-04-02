from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_users_city() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Москва')
    kb.button(text='Другой город')
    kb.button(text='Назад')
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите нужный вариант',
        one_time_keyboard=True
    )


def get_users_target() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Нужен ремонт/диагностика устройства')
    kb.button(text='Отследить статус заказа')
    kb.button(text='Нужен аксессуар')
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите нужный вариант',
        one_time_keyboard=True
    )


def get_users_phone() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Отправить номер телефона', request_contact=True),
        KeyboardButton(text='Назад')
    )
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_yes_or_no() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Да')
    kb.button(text='Нет')
    kb.button(text='Назад')
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите вариант'
    )


def get_users_location() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text='Отправить моё местоположение', request_location=True))
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите вариант'
    )


def back() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Назад')
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def same() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Тот же')
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def agreement() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(
        text='Ознакомиться с политикой 📋',
        url='https://pedant.ru/pravila-lno/'
    ))

    kb.add(InlineKeyboardButton(
        text='Я соглашаюсь ✍️',
        callback_data='agree'
    ))

    return kb.as_markup()
