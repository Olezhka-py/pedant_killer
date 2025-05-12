from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import logging
from pydantic import ValidationError

router_for_status_order = Router()
bot_cmd_status_logger = logging.getLogger('bot_cmd_status_logger')


@router_for_status_order.message(StateFilter(None), F.text == 'Отследить статус заказа')
async def handle_status_order_start(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
