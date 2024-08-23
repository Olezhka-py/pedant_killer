from random import choice
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pedant_killer.кeyboards.for_question import get_users_target

start_router_1 = Router()


@start_router_1.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        f"<b>Здравствуйте!</b> {message.from_user.first_name} {message.from_user.last_name}, " 
        f"Меня зовут <b>{choice(["Александр", "Олег"])}</b> 🧑‍💼\n\n"
        f"✅ Давайте я Вас проконсультирую\n\n"
        f"Нажмите нужную кнопку, чтобы получить быстрый ответ 👇",
        parse_mode=ParseMode.HTML,
        reply_markup=get_users_target(),
        one_time_keyboard=True
    )
