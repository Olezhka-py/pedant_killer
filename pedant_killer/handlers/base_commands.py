from random import choice

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pydantic import ValidationError
import logging

from pedant_killer.кeyboards.question import get_users_target, agreement
from pedant_killer.containers import container
from pedant_killer.schemas.user_schema import UserPostDTO, UserPartialDTO

base_router = Router()
user = container.user_service()
bot_cmd_start_logger = logging.getLogger('bot_cmd_start_logger')


@base_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_get_result = await user.get_user(UserPartialDTO(telegram_id=message.from_user.id))
    if not user_get_result:
        await message.answer(
            '☑️ <b>Нажмите на кнопку "Я соглашаюсь",\n чтоб принять соглашение на обработку персональных данных</b>',
            reply_markup=agreement()
        )

    else:
        await message.answer(
            f'<b>Здравствуйте!</b> {message.from_user.first_name} {message.from_user.last_name}, '
            f'Меня зовут <b>{choice(["Александр", "Олег"])}</b> 🧑‍💼\n\n'
            f'✅ Давайте я Вас проконсультирую\n\n'
            f'Нажмите нужную кнопку, чтобы получить быстрый ответ 👇',
            parse_mode=ParseMode.HTML,
            reply_markup=get_users_target(),
            one_time_keyboard=True
        )
        bot_cmd_start_logger.info(f'Клиент :{message.from_user.id} есть в базе')


@base_router.callback_query(F.data == 'agree')
async def handler_agree(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text("✅ Вы успешно приняли соглашение. Добро пожаловать!")
    bot_cmd_start_logger.info(f'Соглашение об обработке персональных данных принято клиентом {callback.from_user.id}')

    try:
        user_dto = UserPostDTO(access_level_id=1,
                               telegram_username=callback.from_user.username,
                               telegram_id=callback.from_user.id,
                               full_name=callback.from_user.full_name,
                               )

        user_save_result = await user.save_user(user_dto)
        if user_save_result:

            await callback.message.answer(
                f'<b>Здравствуйте!</b> {callback.from_user.first_name} {callback.from_user.last_name}, '
                f'Меня зовут <b>{choice(["Александр", "Олег"])}</b> 🧑‍💼\n\n'
                f'✅ Давайте я Вас проконсультирую\n\n'
                f'Нажмите нужную кнопку, чтобы получить быстрый ответ 👇',
                parse_mode=ParseMode.HTML,
                reply_markup=get_users_target(),
                one_time_keyboard=True
            )

    except ValidationError as e:
        bot_cmd_start_logger.info(f'Произошла ошибка при регистрации пользователя {callback.from_user.id} в системе')
        await callback.message.answer(
            f'Произошла ошибка при регистрации пользователя: {e}',
            reply_markup=get_users_target(),
            one_time_keyboard=True
        )



