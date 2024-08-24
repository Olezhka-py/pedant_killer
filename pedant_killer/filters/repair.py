import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


class FilterYesNo(BaseFilter):
    async def __call__(self, message: Message) -> bool:  # Если убираю try except, то отправляя контакт бот стопариться
        text = getattr(message, 'text', None)
        return text is not None and text.lower() in ('да', 'нет')


class FilterPhoneNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if getattr(message.contact, 'phone_number', None) is not None:
            return True
        else:
            phone_number_pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
            return bool(re.match(phone_number_pattern, message.text))

