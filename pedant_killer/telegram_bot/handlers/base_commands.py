from random import choice

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pydantic import ValidationError
import logging
from dependency_injector.wiring import inject, Provide

from pedant_killer.containers import Container
from pedant_killer.telegram_bot.keyboards.question import get_users_target, agreement
from pedant_killer.services.user_service import UserService
from pedant_killer.schemas.order_device_service_user_schema import UserPostDTO, UserPartialDTO

base_router = Router()
bot_cmd_start_logger = logging.getLogger('bot_cmd_start_logger')


@base_router.message(CommandStart())
@inject
async def cmd_start(message: Message, state: FSMContext,
                    user_service: UserService = Provide[Container.user_service]) -> None:
    await state.clear()
    print('работает')
    user_get_result = await user_service.get(UserPartialDTO(telegram_id=message.from_user.id))
    if not user_get_result:
        await message.answer(
            '☑️ <b>Нажмите на кнопку "Я соглашаюсь",\n чтоб принять соглашение на обработку персональных данных</b>',
            reply_markup=agreement()
        )

    else:
        user_id = user_get_result[0].id
        await state.update_data(user_id=user_id)
        first_name = message.from_user.first_name if message.from_user.first_name is not None else ''
        last_name = message.from_user.last_name if message.from_user.last_name is not None else ''
        message_hello = await message.answer(
            text=f'<b>Здравствуйте!</b> {first_name} {last_name},\n'
            f'Меня зовут <b>{choice(["Александр", "Олег"])}</b> 🧑‍💼\n\n'
            f'✅ Давайте я Вас проконсультирую\n\n'
            f'Нажмите нужную кнопку, чтобы получить быстрый ответ 👇',
            parse_mode=ParseMode.HTML,
            reply_markup=get_users_target(),
            one_time_keyboard=True
        )
        bot_cmd_start_logger.info(f'Клиент :{message.from_user.id} есть в базе')

        await state.update_data(message_hello=message_hello)


@base_router.callback_query(F.data == 'agree')
@inject
async def handler_agree(callback: CallbackQuery, state: FSMContext,
                        user_service: UserService = Provide[Container.user_service]) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text("✅ Вы успешно приняли соглашение. Добро пожаловать!")
    bot_cmd_start_logger.info(f'Соглашение об обработке персональных данных принято клиентом {callback.from_user.id}')
    first_name = callback.from_user.first_name if callback.from_user.first_name is not None else ''
    last_name = callback.from_user.last_name if callback.from_user.last_name is not None else ''
    try:
        user_dto = UserPostDTO(access_level_id=1,
                               telegram_username=callback.from_user.username,
                               telegram_id=callback.from_user.id,
                               full_name=f'{first_name} {last_name}'.strip(),
                               )

        user_save_result = await user_service.save(user_dto)
        if user_save_result:
            user_id = user_save_result[0].id
            await state.update_data(user_id=user_id)

            message_hello = await callback.message.answer(
                text=f'<b>Здравствуйте!</b> {first_name} {last_name},\n'
                f'Меня зовут <b>{choice(["Александр", "Олег"])}</b> 🧑‍💼\n\n'
                f'✅ Давайте я Вас проконсультирую\n\n'
                f'Нажмите нужную кнопку, чтобы получить быстрый ответ 👇',
                parse_mode=ParseMode.HTML,
                reply_markup=get_users_target(),
                one_time_keyboard=True
            )
            await state.update_data(message_hello=message_hello)
    except ValidationError as e:
        bot_cmd_start_logger.warning(f'Произошла ошибка при регистрации пользователя {callback.from_user.id} в системе')
        await callback.message.answer(
            f'Произошла ошибка при регистрации пользователя: {e}',
            reply_markup=get_users_target(),
            one_time_keyboard=True
        )



