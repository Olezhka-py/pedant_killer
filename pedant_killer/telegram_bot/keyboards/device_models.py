import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

bot_keyboard_device_model_logger = logging.getLogger('bot_keyboard_device_model_logger')


async def manufacturer_keyboard(page_manufacturers: list[dict[str, str | int]], manufacturer_pages_count: int = 0
                                ) -> InlineKeyboardMarkup:

    navigation_kb = InlineKeyboardBuilder()
    manufacturer_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row['name'], callback_data=f'manufacturer:{row['id']}')]
        for row in page_manufacturers
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_manufacturer:{manufacturer_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_manufacturer'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_manufacturer:{manufacturer_pages_count + 1}')
    )
    manufacturer_kb.attach(navigation_kb)
    return manufacturer_kb.as_markup()


async def device_type_keyboard(page_devices_type: list[dict[str, str | int]], device_type_pages_count: int = 0,
                               ) -> InlineKeyboardMarkup:

    navigation_kb = InlineKeyboardBuilder()
    device_type_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row['name'], callback_data=f'device_type:{row['id']}')]
        for row in page_devices_type
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_device_type:{device_type_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_device_type'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_device_type:{device_type_pages_count + 1}')
    )
    device_type_kb.attach(navigation_kb)
    return device_type_kb.as_markup()


async def device_keyboard(page_devices: list[dict[str, str | int]], device_pages_count: int = 0) -> InlineKeyboardMarkup:

    navigation_kb = InlineKeyboardBuilder()
    device_type_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row['name_model'], callback_data=f'device:{row['id']}:{row['name_model']}')]
        for row in page_devices
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_device:{device_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_device'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_device:{device_pages_count + 1}')
    )
    device_type_kb.attach(navigation_kb)
    return device_type_kb.as_markup()


async def breaking_keyboard(page_breakings: list[tuple[int, str]], breaking_pages_count: int = 0
                            ) -> InlineKeyboardMarkup:

    navigation_kb = InlineKeyboardBuilder()
    breaking_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row[1], callback_data=f'breaking:{row[0]}')]
        for row in page_breakings
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_breaking:{breaking_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_breaking'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_breaking:{breaking_pages_count + 1}')
    )
    breaking_kb.attach(navigation_kb)

    return breaking_kb.as_markup()
