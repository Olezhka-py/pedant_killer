from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class FilterYesNo(BaseFilter):
    async def __call__(self, message: Message) -> bool:  # Если убираю try except, то отправляя контакт бот стопариться
        try:
            if message.text.lower() == 'да' or message.text.lower() == 'нет':
                return True
        except AttributeError:
            return False


class FilterNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            if message.contact.phone_number is not None:
                return True
        except AttributeError:
            pass

        phone_number_pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
        if bool(re.match(phone_number_pattern, message.text)) is True:
            return True

        return False
