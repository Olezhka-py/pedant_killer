from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from pedant_killer.кeyboards.for_question import (
    get_users_phone,
    get_users_city,
    get_yes_or_no,
    back
)
from pedant_killer.handlers.common import cmd_start
from pedant_killer.filters.filters_for_repair import (
    FilterNumber,
    FilterYesNo
)

rt_2 = Router()


class Repair(StatesGroup):
    model = State()
    defect = State()
    city = State()
    yes = State()
    number = State()
    location_first = State()
    location_second = State()


@rt_2.message(StateFilter(None), F.text == "Нужен ремонт/диагностика устройства")
async def handle_repair_1(message: Message, state: FSMContext) -> None:
    await state.set_state(Repair.model)
    await message.answer(
        "💻 Напишите модель вашего устройства или выберите его из списка предложенных",
        reply_markup=back()
    )  # Здесь дописать клавиатуру с моделями устройств


@rt_2.message(Repair.model)  # Нужно сделать фильтр-проверку введеной модели
async def handle_repair_2(message: Message, state: FSMContext) -> None:
    await state.update_data(model=message.text)
    await state.set_state(Repair.defect)
    await message.answer("🛠️ Опишите проблему", reply_markup=back())  # Здесь дописать клавиатуру с неисправностями


@rt_2.message(Repair.defect)  # Нужно сделать фильтр-проверку введенной неисправности
async def handle_repair_3(message: Message, state: FSMContext) -> None:
    await state.update_data(defect=message.text)
    await state.set_state(Repair.city)
    await message.answer("Укажите город, где вы находитесь", reply_markup=get_users_city())


@rt_2.message(Repair.city)  # Нужно сделать фильтр-проверку города
async def handle_repair_4(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text.lower())
    await state.set_state(Repair.yes)
    await message.answer(
        "💵 Цена ремонта вашего устройства с доставкой составляет ...\n\n"
        "✅ Оформляю заказ?",
        reply_markup=get_yes_or_no()
    )  # Здесь будет выводиться цена ремонта с доставкой


@rt_2.message(FilterYesNo(), Repair.yes)
async def handle_repair_5(message: Message, state: FSMContext) -> None:
    if message.text.lower() == "да":
        await state.update_data(yes=True)
        await message.answer("📞 Хорошо, введите номер телефона для связи", reply_markup=get_users_phone())
        await state.set_state(Repair.number)

    elif message.text.lower() == "нет":
        await message.answer("❌ <b>Отмена заказа</b>. Вы можете начать заново")
        await state.clear()
        await state.set_data({})
        await cmd_start(message, state)


@rt_2.message(Repair.yes)
async def handle_repair_5_1(message: Message) -> None:
    await message.answer("<b>Оформляю заказ?</b>", reply_markup=get_yes_or_no())


@rt_2.message(FilterNumber(), Repair.number)
async def handle_repair_6(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    if message.text is None:
        await state.update_data(number=message.contact.phone_number)
    else:
        await state.update_data(number=message.text)

    if data['city'] == "москва":
        await message.answer("Введите ваш адрес: <b>Улица, Дом, Квартира</b>")
    else:
        await message.answer("Введите ваш адрес: <b>Город, Улица, Дом, Квартира</b>")

    await state.set_state(Repair.location_first)


@rt_2.message(Repair.number)
async def handle_repair_6_1(message: Message) -> None:
    await message.answer("<b>❌ Введен некорректный номер телефона</b>", reply_markup=get_users_phone())


@rt_2.message(Repair.location_first)
async def handle_repair_7(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(location_first=message.text)
    await state.set_state(Repair.location_second)
    if data["city"] == "москва":
        await message.answer(
            "Введите адрес, куда доставить: <b>Улица, Дом, Квартира</b>",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Введите адрес, куда доставить: <b>Город, Улица, Дом, Квартира</b>",
            reply_markup=ReplyKeyboardRemove()  # Реализовать кнопку "Тот же адрес"
        )


@rt_2.message(Repair.location_second)
async def handle_repair_8(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(
        f'🎉 <b>{message.from_user.full_name}</b>, Ваш заказ создан.\n\n'
        f'💻 <b>Модель:</b> {data["model"]}\n\n'
        f'🔧 <b>Дефект:</b> {data["defect"]}\n\n'
        f'📞 <b>Номер телефона:</b> {data["number"]}',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    await cmd_start(message, state)
