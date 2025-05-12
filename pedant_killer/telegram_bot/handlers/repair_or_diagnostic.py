from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import logging
from pydantic import ValidationError
from dependency_injector.wiring import inject, Provide

from pedant_killer.schemas.order_device_service_user_schema import DeviceServiceDeviceIdAndListServiceId
from pedant_killer.schemas.order_status_schema import OrderStatusPartialDTO
from pedant_killer.schemas.manufacturer_device_type_schema import ManufacturerDeviceTypePartialDTO
from pedant_killer.schemas.device_schema import DevicePartialDTO
from pedant_killer.schemas.common_schema import BaseIdDTO
from pedant_killer.schemas.service_breaking_schema import ServicePartialDTO, BreakingPartialDTO, ServiceIdListDTO
from pedant_killer.schemas.order_device_service_user_schema import OrderPostDTO, UserPartialDTO, DeviceServicePartialDTO
from pedant_killer.schemas.yandex_map_schema import YandexMapGeo, YandexMapAddress
from pedant_killer.containers import Container
from pedant_killer.services.device_service import DeviceService
from pedant_killer.services.breaking_service import BreakingService
from pedant_killer.services.device_service_service import DeviceServiceService
from pedant_killer.services.yandex_map_service import YandexMapService
from pedant_killer.services.user_service import UserService
from pedant_killer.services.order_status_service import OrderStatusService
from pedant_killer.services.service_service import ServiceService
from pedant_killer.services.order_service import OrderService
from pedant_killer.services.order_device_service_service import OrderDeviceServiceService
from pedant_killer.services.manufacturer_service import ManufacturerService
from pedant_killer.services.device_type_service import DeviceTypeService
from pedant_killer.services.manufacturer_device_type_service import ManufacturerDeviceTypeService
from pedant_killer.telegram_bot.keyboards.question import (
    get_users_phone,
    get_city_user,
    get_yes_or_no,
    get_users_target,
    get_users_location,
    same_and_back,
    back
)
from pedant_killer.telegram_bot.keyboards.device_models import (
    manufacturer_keyboard,
    device_type_keyboard,
    device_keyboard,
    breaking_keyboard
)
from pedant_killer.telegram_bot.filters.repair import (
    FilterPhoneNumber,
    FilterYes,
    FilterNo
)
router_for_diagnostics = Router()
bot_cmd_repair_logger = logging.getLogger('bot_cmd_repair_logger')


class Repair(StatesGroup):
    model = State()
    defect = State()
    city = State()
    confirm = State()
    number = State()
    location_from = State()
    location_to = State()


page_size = 5


@router_for_diagnostics.message(StateFilter(None), F.text == 'Нужен ремонт/диагностика устройства', )
@inject
async def handle_diagnostic_start_handler(message: Message, state: FSMContext,
                                          manufacturer_service: ManufacturerService = Provide[
                                              Container.manufacturer_service
                                          ]) -> None:
    await state.set_state(Repair.model)
    data = await state.get_data()
    message_hello = data.get('message_hello')

    if message_hello:
        await message_hello.delete()
        del data['message_hello']
        bot_cmd_repair_logger.info('Удалено сообщение-знакомство')
        bot_cmd_repair_logger.info('Из state удалено сообщение-знакомство')

    manufacturer_dto = await manufacturer_service.get_all()
    manufacturer_list = [row.model_dump() for row in manufacturer_dto]
    data['manufacturer_list'] = manufacturer_list
    bot_cmd_repair_logger.info(f'В state добавлен список производителей {manufacturer_list=}')

    page_manufacturers = manufacturer_list[0:page_size]

    msg_model = await message.answer(
        text='Напишите <b>модель</b> вашего устройства 💻\n'
        'или выберите его из списка предложенных 👇',
        reply_markup=await manufacturer_keyboard(page_manufacturers=page_manufacturers, manufacturer_pages_count=0),
    )
    data['msg_model'] = msg_model
    await state.set_data(data)
    bot_cmd_repair_logger.info('В state добавлено сообщение c моделями')


@router_for_diagnostics.callback_query(Repair.model, F.data.startswith('page_manufacturer:'))
async def handle_manufacturer_pages(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    manufacturer_pages_count = int(callback.data.split(':')[1])

    manufacturer_list = data.get('manufacturer_list')
    total_pages = (len(manufacturer_list) - 1) // page_size + 1

    if manufacturer_pages_count < 0:
        manufacturer_pages_count = total_pages - 1
    elif manufacturer_pages_count >= total_pages:
        manufacturer_pages_count = 0

    start_indx = manufacturer_pages_count * page_size
    end_indx = start_indx + page_size
    page_manufacturers = manufacturer_list[start_indx:end_indx]

    try:
        await callback.message.edit_reply_markup(reply_markup=await manufacturer_keyboard(
            page_manufacturers=page_manufacturers,
            manufacturer_pages_count=manufacturer_pages_count
        )
                                                 )
        await callback.answer()

    except TelegramBadRequest as e:
        bot_cmd_repair_logger.info(f'Ошибка пагинации, на странице все объекты {e}')
        await callback.answer()


@router_for_diagnostics.callback_query(Repair.model, F.data.startswith('manufacturer:'))
@inject
async def handle_manufacturer_selected(callback: CallbackQuery, state: FSMContext,
                                       device_type_service: DeviceTypeService = Provide[
                                           Container.device_type_service
                                       ]) -> None:
    manufacturer_id = callback.data.split(':')[1]
    await state.update_data(manufacturer=manufacturer_id)
    bot_cmd_repair_logger.info(f'В state сохранен manufacturer c id:{manufacturer_id}')

    device_type_dto = await device_type_service.get_all()
    device_type_list = [row.model_dump() for row in device_type_dto]
    await state.update_data(device_type_list=device_type_list)
    page_devices_type = device_type_list[0:page_size]

    await callback.message.edit_reply_markup(reply_markup=await device_type_keyboard(
        page_devices_type=page_devices_type,
        device_type_pages_count=0
    )
                                             )
    bot_cmd_repair_logger.info(f'В state добавлен {device_type_list=}')
    await callback.answer()


@router_for_diagnostics.callback_query(Repair.model, F.data == 'exit_manufacturer')
async def handle_manufacturer_exit(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    msg_model = data.get('msg_model')
    await msg_model.delete()
    await state.clear()
    bot_cmd_repair_logger.info('state очищен')
    message_hello = await callback.message.answer(text='<b>Выберите услугу 👇</b>',
                                                  reply_markup=get_users_target(),
                                                  )
    await state.update_data(message_hello=message_hello)
    bot_cmd_repair_logger.info('В state добавлено сообщение-приветствие')


@router_for_diagnostics.callback_query(Repair.model, F.data.startswith('page_device_type:'))
async def handle_device_type_pages(callback: CallbackQuery, state: FSMContext) -> None:
    device_type_pages_count = int(callback.data.split(':')[1])
    data = await state.get_data()
    device_type_list = data.get('device_type_list')

    total_pages = (len(device_type_list) - 1) // page_size + 1

    if device_type_pages_count < 0:
        device_type_pages_count = total_pages - 1
    elif device_type_pages_count >= total_pages:
        device_type_pages_count = 0

    start_indx = device_type_pages_count * page_size
    end_indx = start_indx + page_size
    page_devices_type = device_type_list[start_indx:end_indx]

    try:
        await callback.message.edit_reply_markup(reply_markup=await device_type_keyboard(
            page_devices_type=page_devices_type,
            device_type_pages_count=device_type_pages_count
        )
                                                 )
        await callback.answer()

    except TelegramBadRequest as e:
        bot_cmd_repair_logger.info(f'Ошибка пагинации, на странице все объекты {e}')


@router_for_diagnostics.callback_query(Repair.model, F.data.startswith('device_type:'))
@inject
async def handle_device_type_selected(callback: CallbackQuery, state: FSMContext,
                                      manufacturer_device_type_service: ManufacturerDeviceTypeService = Provide[
                                          Container.manufacturer_device_type_service
                                      ],
                                      device_service: DeviceService = Provide[Container.device_service]
                                      ) -> None:
    device_type_id = callback.data.split(':')[1]
    data = await state.get_data()
    data['device_type'] = device_type_id
    bot_cmd_repair_logger.info(f'В state добавлен device_type с id: {device_type_id}')

    manufacturer = data.get('manufacturer')
    device_type = data.get('device_type')

    manufacturer_device_type_dto = ManufacturerDeviceTypePartialDTO(manufacturer_id=manufacturer,
                                                                    device_type_id=device_type
                                                                    )
    manufacturer_device_type_res = await manufacturer_device_type_service.get(
        model_dto=manufacturer_device_type_dto
    )
    device_dto = DevicePartialDTO(manufacturer_device_type_id=manufacturer_device_type_res[0].id)
    device_res = await device_service.get(model_dto=device_dto)
    device_list = [row.model_dump() for row in device_res]
    await state.update_data(device_list=device_list)
    bot_cmd_repair_logger.info(f'В state добавлен {device_list=}')

    page_devices = device_list[0:page_size]

    await callback.message.edit_reply_markup(reply_markup=await device_keyboard(
        page_devices=page_devices,
        device_pages_count=0
    )
                                             )
    await callback.answer()


@router_for_diagnostics.callback_query(Repair.model, F.data == 'exit_device_type')
async def device_type_exit(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    manufacturer_list = data.get('manufacturer_list')
    del data['device_type_list']
    await state.set_data(data)
    bot_cmd_repair_logger.info('Из state удален device_type_list')

    page_manufacturers = manufacturer_list[0:page_size]

    await callback.message.edit_reply_markup(reply_markup=await manufacturer_keyboard(
        page_manufacturers=page_manufacturers,
        manufacturer_pages_count=0
    ))


@router_for_diagnostics.callback_query(Repair.model, F.data.startswith('page_device:'))
async def device_pages(callback: CallbackQuery, state: FSMContext) -> None:
    device_pages_count = int(callback.data.split(':')[1])
    data = await state.get_data()
    device_list = data.get('device_list')

    total_pages = (len(device_list) - 1) // page_size + 1

    if device_pages_count < 0:
        device_pages_count = total_pages - 1
    elif device_pages_count >= total_pages:
        device_pages_count = 0

    start_indx = device_pages_count * page_size
    end_indx = start_indx + page_size
    page_devices = device_list[start_indx:end_indx]

    try:
        await callback.message.edit_reply_markup(reply_markup=await device_keyboard(
            page_devices=page_devices,
            device_pages_count=device_pages_count
        )
                                                 )
        await callback.answer()

    except TelegramBadRequest as e:
        bot_cmd_repair_logger.info(f'Ошибка пагинации, на странице все объекты {e}')
        await callback.answer()


@router_for_diagnostics.callback_query(Repair.model, F.data.startswith('device:'))
@inject
async def handle_device_selected(callback: CallbackQuery, state: FSMContext,
                                 device_service_service: DeviceServiceService = Provide[
                                     Container.device_service_service],
                                 service_service: ServiceService = Provide[Container.service_service]
                                 ) -> None:
    device_id = int(callback.data.split(':')[1])
    await state.update_data(device_id=device_id)
    bot_cmd_repair_logger.info(f'В state добавлен device с id: {device_id}')
    device_name = callback.data.split(':')[2]
    data = await state.get_data()
    msg_model = data.get('msg_model')

    if 'другое' in device_name.replace(' ', '').lower():
        msg_device_name = await callback.message.answer('<b>Введите название устройства 💻</b>')

        if msg_model:
            await msg_model.delete()
            del data['msg_model']
            await state.set_data(data)
            bot_cmd_repair_logger.info('Удалено сообщение с моделями')

        await state.update_data(msg_device_name=msg_device_name)
        bot_cmd_repair_logger.info(f'В state добавлено id сообщения: {msg_device_name=}')

    else:
        device_id = data.get('device_id')
        device_service_list = await device_service_service.get(
            DeviceServicePartialDTO(device_id=device_id)
        )

        service_id_list = [
            model_device_service.service.id
            for model_device_service in device_service_list
        ]

        service_breaking_dto_list = await service_service.get(
            ServiceIdListDTO(id=service_id_list)
        )
        breaking_list = list(
            {
                (res.id, res.name)
                for breaking_list in service_breaking_dto_list
                for res in breaking_list.breakings
            }
        )
        breaking_list = sorted(breaking_list, key=lambda x: x[0])

        await state.update_data(breaking_list=breaking_list)
        bot_cmd_repair_logger.info(f'В state добавлен {breaking_list=}')

        page_breakings = breaking_list[0:page_size]

        msg_breaking = await callback.message.answer('🛠Выберите <b>проблему</b> из списка\n'
                                                     'Либо опишите ее, если не нашли подходящую',
                                                     reply_markup=await breaking_keyboard(page_breakings=page_breakings,
                                                                                          breaking_pages_count=0)
                                                     )
        await state.update_data(msg_breaking=msg_breaking)
        await state.update_data(device_name=device_name)
        bot_cmd_repair_logger.info('В state добавлено сообщение поломок и название устройства')
        await callback.message.delete()
        await callback.answer()
        await state.set_state(Repair.defect)


@router_for_diagnostics.callback_query(Repair.model, F.data == 'exit_device')
async def handle_device_exit(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    del data['device_list']
    device_type_list = data.get('device_type_list')
    await state.set_data(data)
    bot_cmd_repair_logger.info('Из state удален device_list')

    page_devices_type_list = device_type_list[0:page_size]

    await callback.message.edit_reply_markup(reply_markup=await device_type_keyboard(
        page_devices_type=page_devices_type_list,
        device_type_pages_count=0
    )
                                             )
    await callback.answer()


@router_for_diagnostics.message(Repair.model)
@inject
async def handle_model_selection(message: Message, state: FSMContext,
                                 device_service: DeviceService = Provide[Container.device_service],
                                 device_service_service: DeviceServiceService = Provide[
                                     Container.device_service_service],
                                 service_service: ServiceService = Provide[Container.service_service]
                                 ) -> None:
    data = await state.get_data()
    msg_model = data.get('msg_model')
    msg_device_name = data.get('msg_device_name')
    device_id = data.get('device_id')

    await state.update_data(model=message.text)
    bot_cmd_repair_logger.info('В state добавлено сообщение поломок и название устройства')

    if msg_device_name:
        await msg_device_name.delete()
        del data['msg_device_name']
        bot_cmd_repair_logger.info('Из state удалено сообщение device_name')

    if msg_model:
        await msg_model.delete()
        del data['msg_model']
        bot_cmd_repair_logger.info('Из state удалено сообщение model')

    await state.set_data(data)

    try:
        introduced_model_dto = DevicePartialDTO(name_model=message.text)
        other_device_model_dto = DevicePartialDTO(name_model='Другое Устройство')
        device = await device_service.get_standardize(model_dto=introduced_model_dto)
        device_other = await device_service.get_standardize(model_dto=other_device_model_dto)
        bot_cmd_repair_logger.info(f'{device_other=}')
        if device:
            bot_cmd_repair_logger.info(f'Введенная модель {device[0].name_model} найдена в базе с id: {device}')
            await state.update_data(device_id=device[0].id)
            bot_cmd_repair_logger.info(f'В state добавлено устройство с id: {device[0].id}')

        else:
            bot_cmd_repair_logger.info(f'Введенная модель {message.text} не найдена в базе')
            device_id = device_id or device_other[0].id
            await state.update_data(device_description=message.text, device_id=device_id)
            bot_cmd_repair_logger.info(f'В state добавлено id устройства: {device_id} и'
                                       f' полное название введенное устройства: {message.text}')

        device_id = data.get('device_id')
        device_service_list = await device_service_service.get(
            DeviceServicePartialDTO(device_id=device_id)
        )

        service_id_list = [
            model_device_service.service.id
            for model_device_service in device_service_list
        ]

        service_breaking_dto_list = await service_service.get(
            ServiceIdListDTO(id=service_id_list)
        )
        breaking_list = list(
            {
                (res.id, res.name)
                for breaking_list in service_breaking_dto_list
                for res in breaking_list.breakings
            }
        )
        breaking_list = sorted(breaking_list, key=lambda x: x[0])

        await state.update_data(breaking_list=breaking_list)
        bot_cmd_repair_logger.info(f'В state добавлен {breaking_list=}')

        page_breakings = breaking_list[0:page_size]

        msg_breaking = await message.answer('🛠️ Выберите <b>проблему</b> из списка\n'
                                            'Либо опишите ее, если не нашли подходящую',
                                            reply_markup=await breaking_keyboard(page_breakings=page_breakings,
                                                                                 breaking_pages_count=0))
        await state.update_data(msg_breaking=msg_breaking)
        await state.update_data(device_name=message.text)
        bot_cmd_repair_logger.info('В state добавлено сообщение поломок и название устройства')
        await state.set_state(Repair.defect)

    except ValidationError as e:
        bot_cmd_repair_logger.info(f'Некорректные модель введена пользователем {message.text}: {e}')
        await message.answer('<b>Введите верную модель</b>')


@router_for_diagnostics.callback_query(Repair.defect, F.data.startswith('page_breaking:'))
async def handle_breaking_pages(callback: CallbackQuery, state: FSMContext) -> None:
    breaking_pages_count = int(callback.data.split(':')[1])
    data = await state.get_data()
    breaking_list = data.get('breaking_list')

    total_pages = (len(breaking_list) - 1) // page_size + 1

    if breaking_pages_count < 0:
        breaking_pages_count = total_pages - 1
    elif breaking_pages_count >= total_pages:
        breaking_pages_count = 0

    start_idx = breaking_pages_count * page_size
    end_idx = start_idx + page_size

    page_breakings = breaking_list[start_idx:end_idx]

    try:
        await callback.message.edit_reply_markup(reply_markup=await breaking_keyboard(
            page_breakings=page_breakings,
            breaking_pages_count=breaking_pages_count
        )
                                                 )
        await callback.answer()

    except TelegramBadRequest as e:
        bot_cmd_repair_logger.info(f'Ошибка пагинации, на странице все объекты {e}')


@router_for_diagnostics.callback_query(Repair.defect, F.data.startswith('breaking:'))
@inject
async def handle_selected_breaking(callback: CallbackQuery, state: FSMContext,
                                   breaking_service: BreakingService = Provide[Container.breaking_service],
                                   device_service_service: DeviceServiceService = Provide[Container.device_service_service]
                                   ) -> None:
    breaking_id = int(callback.data.split(':')[1])
    breaking_dto = await breaking_service.get(BaseIdDTO(id=breaking_id))
    breaking_name = breaking_dto[0].name
    await state.update_data(breaking_id=breaking_id, breaking_name=breaking_name)
    bot_cmd_repair_logger.info(f'В state добавлен {breaking_id=}, {breaking_name=}')
    data = await state.get_data()

    breaking_service_list_dto = await breaking_service.get(BaseIdDTO(id=breaking_id))
    suitable_service_list = [service.id for service in breaking_service_list_dto[0].services]
    device_service_list_dto = await device_service_service.get(
        DeviceServiceDeviceIdAndListServiceId(device_id=data['device_id'], service_id=suitable_service_list)
    )

    device_service_dict = {
        f'{device_service.service.name}': device_service.price
        for device_service in device_service_list_dto
    }
    await callback.message.delete()
    bot_cmd_repair_logger.info('Сообщение с поломками удалено')

    if data.get('msg_breaking'):
        del data['msg_breaking']
        bot_cmd_repair_logger.info('Из state удалено сообщение с поломками')

    suitable_service_text = [f'🔧 {service} - {price}\n' for service, price in device_service_dict.items()]
    msg_price = await callback.message.answer(f'<b>Список подходящих услуг под вашу проблему</b>\n'
                                              f'Это ознакомительный лист, требуется <b>бесплатная диагностика</b>\n\n'
                                              f'{"".join(suitable_service_text)}')

    await state.set_state(Repair.city)
    await callback.message.answer(text='🏙️ Выберите <b>город</b>, где вы находитесь,\n либо введите его вручную',
                                  reply_markup=get_city_user())
    await callback.answer()
    data['msg_price'] = msg_price
    await state.set_data(data)
    bot_cmd_repair_logger.info('В state добавлено сообщение с прайсом')


@router_for_diagnostics.callback_query(Repair.defect, F.data.startswith('exit_breaking'))
async def handle_exit_breaking(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    del data['breaking_list']
    del data['device_id']
    device_list = data.get('device_list')
    bot_cmd_repair_logger.info('Из state удалено breaking_list и device_id')
    device_description = data.get('device_description')
    if device_description:
        del data['device_description']
        bot_cmd_repair_logger.info('Из state удален device_description')

    await callback.message.delete()

    page_devices = device_list[0:page_size]

    msg_model = await callback.message.answer(text='Напишите <b>модель</b> вашего устройства 💻\n'
                                                   'или выберите его из списка предложенных 👇',
                                              reply_markup=await device_keyboard(
                                                  page_devices=page_devices,
                                                  device_pages_count=0
                                              )
    )
    await callback.answer()
    data['msg_model'] = msg_model
    bot_cmd_repair_logger.info('В state добавлено сообщение выбора модели')
    await state.set_data(data)
    await state.set_state(Repair.model)


@router_for_diagnostics.message(Repair.defect)
@inject
async def handle_defect_selection(message: Message, state: FSMContext,
                                  breaking_service: BreakingService = Provide[Container.breaking_service],
                                  device_service_service: DeviceServiceService = Provide[
                                      Container.device_service_service
                                  ]
                                  ) -> None:
    data = await state.get_data()
    msg_breaking = data.get('msg_breaking')
    defect_name = message.text
    breaking_dto = await breaking_service.get_breaking_standardize(BreakingPartialDTO(name=defect_name))
    breaking_dto_other = await breaking_service.get_breaking_standardize(BreakingPartialDTO(name='Другое'))

    if breaking_dto:
        breaking_id = breaking_dto[0].id
        data['breaking_id'] = breaking_id
        bot_cmd_repair_logger.info(f'В state добавлен {breaking_id=}')

        breaking_service_list_dto = await breaking_service.get(BaseIdDTO(id=breaking_id))
        suitable_service_list = [service.id for service in breaking_service_list_dto[0].services]

        device_service_list_dto = await (
            device_service_service.get(
                DeviceServiceDeviceIdAndListServiceId(device_id=data['device_id'], service_id=suitable_service_list)
            )
        )

        device_service_dict = {
            f'{device_service.service.name}': device_service.price
            for device_service in device_service_list_dto
        }

        suitable_service_text = [f'🔧 {service} - {price}\n' for service, price in device_service_dict.items()]
        msg_price = await message.answer(f'<b>Список подходящих услуг под вашу проблему</b>\n'
                                         f'Это ознакомительный лист, требуется <b>бесплатная диагностика</b>\n\n'
                                         f'{"".join(suitable_service_text)}')
        data['msg_price'] = msg_price
        bot_cmd_repair_logger.info('В state добавлено сообщение с прайсом')

    else:
        data['breaking_id'] = breaking_dto_other[0].id
        data['breaking_description'] = message.text
        bot_cmd_repair_logger.info(f'В state добавлен {data['breaking_id']=} и {data['breaking_description']=}')

    data['breaking_name'] = message.text
    bot_cmd_repair_logger.info('В state добавлено breaking_name')
    await msg_breaking.delete()
    bot_cmd_repair_logger.info('Сообщение с поломками удаленно')
    del data['msg_breaking']
    await state.set_data(data)
    await state.set_state(Repair.city)
    await message.answer(text='🏙️ Выберите <b>город</b>, где вы находитесь,\n либо введите его вручную',
                         reply_markup=get_city_user())


@router_for_diagnostics.callback_query(Repair.city, F.data == 'москва')
async def handle_select_city_moscow(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(city=callback.data)
    bot_cmd_repair_logger.info(f'В state добавлено city = {callback.data}')
    msg_confirm = await callback.message.answer(text=f'✅<b>Оформляем заказ?</b>\n\n'
                                                     f'🧰Диагностика + типовой ремонт займет около <b>1 дня</b>,\n'
                                                     f'🆓🚚Курьер заберет устройство прямо от вас',
                                                reply_markup=get_yes_or_no())
    await callback.answer()

    await callback.message.delete()
    await state.update_data(msg_confirm=msg_confirm)
    bot_cmd_repair_logger.info('В state добавлено сообщение подтверждение')
    await state.set_state(Repair.confirm)


@router_for_diagnostics.callback_query(Repair.city, F.data == 'другое')
async def handle_select_city_other(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    msg_enter_city = await callback.message.answer('🏙️<b>Введите ваш город</b>')
    await callback.answer()
    await state.update_data(msg_enter_city=msg_enter_city)
    bot_cmd_repair_logger.info('В state добавлено сообщение с вводом города')


@router_for_diagnostics.callback_query(Repair.city, F.data == 'exit_city')
async def handle_exit_city(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    msg_price = data.get('msg_price')
    breaking_description = data.get('breaking_description')
    breaking_list = data.get('breaking_list')

    if msg_price:
        await msg_price.delete()
        del data['msg_price']
        bot_cmd_repair_logger.info('Из state удалено сообщение с price')

    if breaking_description:
        del data['breaking_description']
        bot_cmd_repair_logger.info('Из state удален breaking_description')

    await callback.message.delete()

    page_breakings = breaking_list[0:page_size]

    msg_breaking = await callback.message.answer(text='🛠 Выберите <b>проблему</b> из списка\n'
                                                 'Либо опишите ее, если не нашли подходящую',
                                                 reply_markup=await breaking_keyboard(page_breakings=page_breakings,
                                                                                      breaking_pages_count=0)
                                                 )

    await callback.answer()
    data['msg_breaking'] = msg_breaking
    await state.set_data(data)
    bot_cmd_repair_logger.info('В state добавлено сообщение поломок')
    await state.set_state(Repair.defect)


@router_for_diagnostics.message(Repair.city)
async def handle_city_selection(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    data['city'] = message.text.lower()
    msg_enter_city = data.get('msg_enter_city')

    if msg_enter_city:
        await msg_enter_city.delete()
        del data['msg_enter_city']
        bot_cmd_repair_logger.info('Из state удалено сообщение ввод города')

    if message.text.lower().strip() == 'москва':
        msg_confirm = await message.answer(text=f'✅<b>Оформляем заказ?</b>\n\n'
                                                f'🧰Диагностика + типовой ремонт займет около <b>1 дня</b>,\n'
                                                f'🆓🚚Курьер заберет устройство прямо от вас',
                                           reply_markup=get_yes_or_no())

    else:
        msg_confirm = await message.answer(text=f'✅<b>Оформляем заказ?</b>\n\n'
                                                f'🧰Диагностика + типовой ремонт займет около <b>1 дня</b>,\n'
                                                f'🚚 Доставка осуществляется через CDEK от <b>1 до 6 дней</b>',
                                           reply_markup=get_yes_or_no())

    data['msg_confirm'] = msg_confirm
    await state.set_data(data)
    bot_cmd_repair_logger.info('В state добавлено сообщение подтверждение')
    await state.set_state(Repair.confirm)


@router_for_diagnostics.callback_query(Repair.confirm, F.data == 'yes')
async def handle_callback_yes(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    msg_phone_1 = await callback.message.answer(text='📞 Хорошо, введите <b>номер телефона</b> для связи',
                                                reply_markup=get_users_phone())
    msg_phone_2 = await callback.message.answer(text='Или отправьте свой контакт 👇', reply_markup=back())

    await state.update_data(msg_phone_1=msg_phone_1)
    await state.update_data(msg_phone_2=msg_phone_2)
    bot_cmd_repair_logger.info('В state добавлено сообщения с телефонами')
    await state.set_state(Repair.number)


@router_for_diagnostics.callback_query(Repair.confirm, F.data == 'no')
async def handle_callback_no(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    message_hello = await callback.message.answer(text=f'❌ <b>Отмена заказа</b>\n\n'
                                                       f'<b>Выберите услугу 👇</b>',
                                                  reply_markup=get_users_target())
    await callback.answer()
    await state.clear()
    await state.update_data(message_hello=message_hello)
    bot_cmd_repair_logger.info('state очищен, в state добавлено сообщение-приветствие')


@router_for_diagnostics.callback_query(Repair.confirm, F.data == 'exit_yes_no')
async def handle_exit_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    del data['city']
    await state.set_data(data)
    bot_cmd_repair_logger.info('Из state удален город')
    await callback.message.delete()
    await callback.message.answer(text='🏙️ Выберите <b>город</b>, где вы находитесь,\n либо введите его вручную',
                                  reply_markup=get_city_user())
    await state.set_state(Repair.city)


@router_for_diagnostics.message(FilterYes(), Repair.confirm)
async def handle_message_yes(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    msg_confirm = data.get('msg_confirm')
    await msg_confirm.delete()
    msg_phone_1 = await message.answer(text='📞 Хорошо, введите <b>номер телефона</b> для связи',
                                       reply_markup=get_users_phone())

    msg_phone_2 = await message.answer(text='Или отправьте свой контакт 👇', reply_markup=back())
    data['msg_phone_1'] = msg_phone_1
    data['msg_phone_2'] = msg_phone_2
    await state.set_data(data)
    bot_cmd_repair_logger.info('Из state удалены сообщения с телефоном')
    await state.set_state(Repair.number)


@router_for_diagnostics.message(FilterNo(), Repair.confirm)
async def handle_message_no(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    msg_confirm = data.get('msg_confirm')
    await msg_confirm.delete()
    message_hello = await message.answer(text=f'❌ <b>Отмена заказа</b>\n\n'
                                              f'<b>Выберите услугу 👇</b>',
                                         reply_markup=get_users_target())
    await state.clear()
    await state.update_data(message_hello=message_hello)
    bot_cmd_repair_logger.info('state очищен, в state добавлено сообщение-приветствие')


@router_for_diagnostics.message(Repair.number, F.contact)
async def handle_contact_selection(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    msg_phone_1 = data.get('msg_phone_1')
    msg_phone_2 = data.get('msg_phone_2')
    msg_incorrect_phone = data.get('msg_incorrect_phone')

    if msg_incorrect_phone:
        await msg_incorrect_phone.delete()
        del data['msg_incorrect_phone']
        bot_cmd_repair_logger.info('Из state удалено сообщение некорректного ввода телефона')

    if msg_phone_1:
        await msg_phone_1.delete()
        await msg_phone_2.delete()
        del data['msg_phone_1']
        del data['msg_phone_2']
        bot_cmd_repair_logger.info('Из state удалено сообщение некорректного ввода телефона')

    data['number'] = message.contact.phone_number
    bot_cmd_repair_logger.info(f'В state добавлен номер телефона: {message.contact.phone_number}')
    await state.set_state(Repair.location_from)
    msg_address_1 = await message.answer(text='🏠 Введите ваш адрес: <b>Улица, Дом</b>',
                                         reply_markup=get_users_location())

    msg_address_2 = await message.answer(text='Или отправьте свое текущее положение👇',
                                         reply_markup=back())

    data['msg_address_1'] = msg_address_1
    data['msg_address_2'] = msg_address_2
    bot_cmd_repair_logger.info('В state добавлены сообщения с адресом')
    await state.set_data(data)


@router_for_diagnostics.message(Repair.number, FilterPhoneNumber())
async def handle_number_selection(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    msg_phone_1 = data.get('msg_phone_1')
    msg_phone_2 = data.get('msg_phone_2')
    msg_incorrect_phone = data.get('msg_incorrect_phone')

    if msg_incorrect_phone:
        await msg_incorrect_phone.delete()
        del data['msg_incorrect_phone']
        bot_cmd_repair_logger.info('Из state удалено сообщение с некорректным вводом телефона')

    if msg_phone_1:
        await msg_phone_1.delete()
        await msg_phone_2.delete()
        del data['msg_phone_1']
        del data['msg_phone_2']
        bot_cmd_repair_logger.info('Из state удалены сообщения ввода телефона')

    data['number'] = message.text
    bot_cmd_repair_logger.info(f'В state добавлен номер телефона {message.text}')

    msg_address_1 = await message.answer(text='🏠 Введите ваш адрес: <b>Улица, Дом</b>',
                                         reply_markup=get_users_location())
    msg_address_2 = await message.answer(text='Или отправьте свое текущее положение👇',
                                         reply_markup=back())

    data['msg_address_1'] = msg_address_1
    data['msg_address_2'] = msg_address_2
    await state.set_data(data)
    bot_cmd_repair_logger.info(f'В state добавлены сообщения с адресом')
    await state.set_state(Repair.location_from)


@router_for_diagnostics.message(Repair.number)
async def handle_invalid_number(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    msg_incorrect_phone = data.get('msg_incorrect_phone')

    if msg_incorrect_phone:
        await msg_incorrect_phone.delete()

    msg_incorrect_phone = await message.answer(text='<b>❌ Введен некорректный номер телефона</b>',
                                               reply_markup=get_users_phone())

    await state.update_data(msg_incorrect_phone=msg_incorrect_phone)
    bot_cmd_repair_logger.info(f'В state добавлено сообщение некорректный номер телефона')


@router_for_diagnostics.callback_query(Repair.number, F.data == 'exit')
async def handle_callback_number_back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    msg_phone_1 = data.get('msg_phone_1')
    msg_phone_2 = data.get('msg_phone_2')
    msg_incorrect_phone = data.get('msg_incorrect_phone')

    if msg_incorrect_phone:
        await msg_incorrect_phone.delete()
        del data['msg_incorrect_phone']
        bot_cmd_repair_logger.info('Из state удаленно сообщение некорректного ввода номера телефона')

    if msg_phone_1:
        await msg_phone_1.delete()
        await msg_phone_2.delete()
        del data['msg_phone_1']
        del data['msg_phone_2']
        bot_cmd_repair_logger.info('Из state удалены сообщения с вводом телефона')

    if city == 'москва':
        msg_confirm = await callback.message.answer(text=f'✅<b>Оформляем заказ?</b>\n\n'
                                                         f'🧰Диагностика + типовой ремонт займет около <b>1 дня</b>,\n'
                                                         f'🆓🚚Курьер заберет устройство прямо от вас',
                                                    reply_markup=get_yes_or_no())

    else:
        msg_confirm = await callback.message.answer(text=f'✅<b>Оформляем заказ?</b>\n\n'
                                                         f'🧰Диагностика + типовой ремонт займет около <b>1 дня</b>,\n'
                                                         f'🚚 Доставка осуществляется через CDEK от <b>1 до 6 дней</b>',
                                                    reply_markup=get_yes_or_no())

    await callback.answer()
    data['msg_confirm'] = msg_confirm
    bot_cmd_repair_logger.info('В state добавлено сообщение с подтверждением')
    await state.set_data(data)
    await state.set_state(Repair.confirm)


@router_for_diagnostics.message(Repair.location_from, F.location)
@inject
async def handle_location_to(message: Message, state: FSMContext,
                             yandex_map_service: YandexMapService = Provide[Container.yandex_map_service]) -> None:
    data = await state.get_data()
    msg_address_1 = data.get('msg_address_1')
    msg_address_2 = data.get('msg_address_2')
    msg_incorrect_address = data.get('msg_incorrect_address')

    if msg_incorrect_address:
        await msg_incorrect_address.delete()
        del data['msg_incorrect_address']
        bot_cmd_repair_logger.info('Из state удалено сообщение с некорректным адресом')

    if msg_address_1:
        await msg_address_1.delete()
        await msg_address_2.delete()
        del data['msg_address_1']
        del data['msg_address_2']
        bot_cmd_repair_logger.info('Удалены сообщения с получением адреса')

    location = message.location
    lat = location.latitude
    lon = location.longitude
    bot_cmd_repair_logger.info(f'Получены координаты пользователя {lat=}, {lon=}')
    address_dto = await yandex_map_service.get_address_by_coords(YandexMapGeo(lat=lat, lon=lon))

    msg_location_from = await message.answer(
        text='🏠 Введите адрес, куда доставить: <b>Улица Дом </b>',
        reply_markup=same_and_back()
    )
    data['msg_location_from'] = msg_location_from
    address = address_dto[0].address
    data['location_first'] = address
    await state.set_data(data)
    bot_cmd_repair_logger.info(f'В state добавлен адрес {address}')
    await state.set_state(Repair.location_to)


@router_for_diagnostics.message(Repair.location_from)
@inject
async def handle_location_to(message: Message, state: FSMContext,
                             yandex_map_service: YandexMapService = Provide[Container.yandex_map_service]) -> None:
    data = await state.get_data()
    msg_address_1 = data.get('msg_address_1')
    msg_address_2 = data.get('msg_address_2')
    city = data.get('city')
    msg_incorrect_address = data.get('msg_incorrect_address')

    if msg_incorrect_address:
        await msg_incorrect_address.delete()
        del data['msg_incorrect_address']
        bot_cmd_repair_logger.info('Из state удалено сообщение об некорректном адресе')

    if msg_address_1:
        await msg_address_1.delete()
        await msg_address_2.delete()
        del data['msg_address_1']
        del data['msg_address_2']
        bot_cmd_repair_logger.info('Удалены сообщения с получением адреса')

    if await yandex_map_service.validate_address(YandexMapAddress(address=f'{city} {message.text}')):
        msg_location_from = await message.answer(
            text='🏠 Введите адрес, куда доставить: <b>Улица Дом </b>',
            reply_markup=same_and_back()
        )
        data['msg_location_from'] = msg_location_from
        data['location_first'] = f'{city.capitalize()} {message.text}'
        bot_cmd_repair_logger.info(f'В state добавлено место, откуда забрать устройство {city} {message.text}')
        await state.set_state(Repair.location_to)

    else:
        msg_incorrect_address = await message.answer(text='<b>❌ Введен некорректный адрес</b>')
        data['msg_incorrect_address'] = msg_incorrect_address
        bot_cmd_repair_logger.info('В state добавлено сообщение об некорректном адресе')

    await state.set_data(data)


@router_for_diagnostics.callback_query(Repair.location_from, F.data == 'exit')
async def handle_callback_location_to_back(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    msg_address_1 = data.get('msg_address_1')
    msg_address_2 = data.get('msg_address_2')
    msg_incorrect_address = data.get('msg_incorrect_address')

    if msg_incorrect_address:
        await msg_incorrect_address.delete()
        del data['msg_incorrect_address']
        bot_cmd_repair_logger.info('Из state удалено сообщение об некорректном адресе')

    if msg_address_1:
        await msg_address_1.delete()
        await msg_address_2.delete()
        del data['msg_address_1']
        del data['msg_address_2']
        bot_cmd_repair_logger.info('Из state удалены сообщения c адресом')

    msg_phone_1 = await callback.message.answer(text='📞 Хорошо, введите <b>номер телефона</b> для связи',
                                                reply_markup=get_users_phone())

    msg_phone_2 = await callback.message.answer(text='Или отправьте свой контакт 👇', reply_markup=back())
    data['msg_phone_1'] = msg_phone_1
    data['msg_phone_2'] = msg_phone_2
    await callback.answer()
    await state.set_data(data)
    bot_cmd_repair_logger.info('В state добавлено сообщение с телефоном')
    await state.set_state(Repair.number)


@router_for_diagnostics.callback_query(Repair.location_to, F.data == 'same')
@inject
async def handle_callback_location_from_same(callback: CallbackQuery, state: FSMContext,
                                             user_service: UserService = Provide[Container.user_service],
                                             order_status_service: OrderStatusService = Provide[
                                                 Container.order_status_service
                                             ],
                                             service_service: ServiceService = Provide[Container.service_service],
                                             device_service_service: DeviceServiceService = Provide[
                                                 Container.device_service_service
                                             ],
                                             order_service: OrderService = Provide[Container.order_service],
                                             order_device_service_service: OrderDeviceServiceService = Provide[
                                                 Container.order_device_service_service
                                             ]) -> None:
    data = await state.get_data()
    location_second = data.get('location_first')
    await callback.message.delete()
    user_dto = await user_service.get(UserPartialDTO(telegram_id=callback.from_user.id))
    user_id = user_dto[0].id
    user_full_name = user_dto[0].full_name

    order_status_dto = await order_status_service.get(OrderStatusPartialDTO(name='Новый'))
    order_status_id = order_status_dto[0].id

    city = data.get('city')
    sent_from_address = data.get('location_first')
    return_to_address = location_second
    breaking_id = data.get('breaking_id')
    breaking_name = data.get('breaking_name')
    breaking_description = data.get('breaking_description')
    device_name = data.get('device_name')
    device_description = data.get('device_description')
    device_id = data.get('device_id')
    service_dto = await service_service.get(ServicePartialDTO(name='Диагностика'))
    service_id = service_dto[0].id
    device_service_dto = await device_service_service.get(DeviceServicePartialDTO(device_id=device_id,
                                                                                  service_id=service_id))
    device_service_id = device_service_dto[0].id
    number = data.get('number')

    await user_service.update(UserPartialDTO(id=user_id, phone=number, address=sent_from_address))

    order_dto = OrderPostDTO(
        client_id=user_id,
        status_id=order_status_id,
        sent_from_address=sent_from_address,
        return_to_address=return_to_address,
        description_model_device=device_description,
        breaking_id=breaking_id,
        description_breaking=breaking_description
    )
    order_dto = await order_service.save(order_dto)
    order_id = order_dto[0].id
    await order_device_service_service.save(order_id_dto=BaseIdDTO(id=order_id),
                                            device_service_id_dto=BaseIdDTO(id=device_service_id))

    await callback.message.answer(
        text=f'🎉 <b>{user_full_name}</b>, Ваш заказ создан.\n\n'
             f'💻 <b>Модель:</b> {device_name}\n\n'
             f'🔧 <b>Дефект:</b> {breaking_name}\n\n'
             f'📞 <b>Ваш номер телефона:</b> {number}\n\n'
             f'🚚 <b>Забрать по адресу: {sent_from_address}</b>\n\n'
             f'🧑‍💼 По всем вопросам можете написать <b>менеджеру @KillerFaceID</b>',
        reply_markup=ReplyKeyboardRemove()
    )
    message_hello = await callback.message.answer(text=f'<b>Выберите услугу 👇</b>', reply_markup=get_users_target())
    await callback.answer()
    await state.clear()
    await state.update_data(message_hello=message_hello)
    bot_cmd_repair_logger.info('State очищен, в state добавлено сообщение-приветствие')


@router_for_diagnostics.callback_query(Repair.location_to, F.data == 'exit')
async def handle_callback_location_from_back(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    msg_location_from = data.get('msg_location_from')

    if msg_location_from:
        await msg_location_from.delete()
        del data['msg_location_from']
        bot_cmd_repair_logger.info('Из state удалено сообщение откуда доставить')

    msg_address_1 = await callback.message.answer(text='🏠 Введите ваш адрес: <b>Улица, Дом</b>',
                                                  reply_markup=get_users_location())
    msg_address_2 = await callback.message.answer(text='Или отправьте свое текущее положение👇',
                                                  reply_markup=back())

    await callback.answer()

    data['msg_address_1'] = msg_address_1
    data['msg_address_2'] = msg_address_2
    await state.set_data(data)
    bot_cmd_repair_logger.info('В state добавлено сообщение с адресом')
    await state.set_state(Repair.location_from)


@router_for_diagnostics.message(Repair.location_to)
@inject
async def handle_location_from(message: Message, state: FSMContext,
                               yandex_map_service: YandexMapService = Provide[Container.yandex_map_service],
                               user_service: UserService = Provide[Container.user_service],
                               order_status_service: OrderStatusService = Provide[
                                   Container.order_status_service
                               ],
                               service_service: ServiceService = Provide[Container.service_service],
                               device_service_service: DeviceServiceService = Provide[
                                   Container.device_service_service
                               ],
                               order_service: OrderService = Provide[Container.order_service],
                               order_device_service_service: OrderDeviceServiceService = Provide[
                                   Container.order_device_service_service
                               ]) -> None:
    data = await state.get_data()

    msg_location_from = data.get('msg_location_from')
    msg_incorrect_address = data.get('msg_incorrect_address')
    city = data.get('city')

    if msg_location_from:
        await msg_location_from.delete()
        del data['msg_location_from']

    if msg_incorrect_address:
        await msg_incorrect_address.delete()
        del data['msg_incorrect_address']

    if await yandex_map_service.validate_address(YandexMapAddress(address=f'{city} {message.text}')):
        user_dto = await user_service.get(UserPartialDTO(telegram_id=message.from_user.id))
        user_id = user_dto[0].id
        user_full_name = user_dto[0].full_name

        order_status_dto = await order_status_service.get(OrderStatusPartialDTO(name='Новый'))
        order_status_id = order_status_dto[0].id

        sent_from_address = data.get('location_first')
        return_to_address = f'{city} {message.text}'
        breaking_id = data.get('breaking_id')
        breaking_name = data.get('breaking_name')
        breaking_description = data.get('breaking_description')
        device_name = data.get('device_name')
        device_description = data.get('device_description')
        device_id = data.get('device_id')
        service_dto = await service_service.get(ServicePartialDTO(name='Диагностика'))
        service_id = service_dto[0].id
        device_service_dto = await device_service_service.get(DeviceServicePartialDTO(
            device_id=device_id,
            service_id=service_id))

        device_service_id = device_service_dto[0].id
        number = data.get('number')

        await user_service.update(UserPartialDTO(id=user_id, phone=number, address=sent_from_address))

        order_dto = OrderPostDTO(
            client_id=user_id,
            status_id=order_status_id,
            sent_from_address=sent_from_address,
            return_to_address=return_to_address,
            description_model_device=device_description,
            breaking_id=breaking_id,
            description_breaking=breaking_description
        )
        order_dto = await order_service.save(order_dto)
        order_id = order_dto[0].id
        await order_device_service_service.save(order_id_dto=BaseIdDTO(id=order_id),
                                                device_service_id_dto=BaseIdDTO(id=device_service_id))

        await message.answer(
            text=f'🎉 <b>{user_full_name}</b>, Ваш заказ создан.\n\n'
                 f'💻 <b>Модель:</b> {device_name}\n\n'
                 f'🔧 <b>Дефект:</b> {breaking_name}\n\n'
                 f'📞 <b>Ваш номер телефона:</b> {number}\n\n'
                 f'🚚 <b>Забрать по адресу:</b> {sent_from_address}\n\n'
                 f'🧑‍💼 По всем вопросам можете написать <b>менеджеру @KillerFaceID</b>',
            reply_markup=ReplyKeyboardRemove()
        )
        message_hello = await message.answer(text=f'<b>Выберите услугу 👇</b>', reply_markup=get_users_target())
        await state.clear()
        await state.update_data(message_hello=message_hello)
        bot_cmd_repair_logger.info('State очищен, в state добавлено сообщение-приветствие')

    else:
        msg_incorrect_address = await message.answer(text='<b>❌ Введен некорректный адрес</b>')
        data['msg_incorrect_address'] = msg_incorrect_address
        bot_cmd_repair_logger.info('В state добавлено сообщение об некорректном адресе')

    await state.set_data(data)
