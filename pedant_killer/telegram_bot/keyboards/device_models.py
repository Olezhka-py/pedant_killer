import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dependency_injector.wiring import inject, Provide

from pedant_killer.containers import Container

from pedant_killer.schemas.manufacturer_device_type_schema import ManufacturerDeviceTypePartialDTO
from pedant_killer.schemas.device_schema import DevicePartialDTO
from pedant_killer.schemas.order_device_service_user_schema import DeviceServicePartialDTO
from pedant_killer.schemas.service_breaking_schema import ServiceIdListDTO
from pedant_killer.services.manufacturer_service import ManufacturerService
from pedant_killer.services.device_type_service import DeviceTypeService
from pedant_killer.services.manufacturer_device_type_service import ManufacturerDeviceTypeService
from pedant_killer.services.device_service import DeviceService
from pedant_killer.services.device_service_service import DeviceServiceService
from pedant_killer.services.service_service import ServiceService

bot_keyboard_device_model_logger = logging.getLogger('bot_keyboard_device_model_logger')


@inject
async def manufacturer_keyboard(state: FSMContext, manufacturer_pages_count: int = 0,
                                manufacturer_service: ManufacturerService = Provide[Container.manufacturer_service]
                                ) -> InlineKeyboardMarkup:
    models_per_page = 5

    data = await state.get_data()
    manufacturer_list = data.get('manufacturer_list')

    if not manufacturer_list:
        manufacturer_dto = await manufacturer_service.get_all()
        manufacturer_list = [row.model_dump() for row in manufacturer_dto]
        await state.update_data(manufacturer_list=manufacturer_list)
        bot_keyboard_device_model_logger.info(f'В state добавлено {manufacturer_list=}')

    total_pages = (len(manufacturer_list) - 1) // models_per_page + 1

    if manufacturer_pages_count < 0:
        manufacturer_pages_count = total_pages - 1
    elif manufacturer_pages_count >= total_pages:
        manufacturer_pages_count = 0

    start_indx = manufacturer_pages_count * models_per_page
    end_indx = start_indx + models_per_page
    page_models = manufacturer_list[start_indx:end_indx]

    navigation_kb = InlineKeyboardBuilder()
    manufacturer_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row['name'], callback_data=f'manufacturer:{row['id']}')]
        for row in page_models
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_manufacturer:{manufacturer_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_manufacturer'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_manufacturer:{manufacturer_pages_count + 1}')
    )
    manufacturer_kb.attach(navigation_kb)
    return manufacturer_kb.as_markup()


@inject
async def device_type_keyboard(state: FSMContext, device_type_pages_count: int = 0,
                               device_type_service: DeviceTypeService = Provide[Container.device_type_service]
                               ) -> InlineKeyboardMarkup:
    device_type_per_page = 5

    data = await state.get_data()
    device_type_list = data.get('device_type_list')

    if not device_type_list:
        device_type_dto = await device_type_service.get_all()
        device_type_list = [row.model_dump() for row in device_type_dto]
        await state.update_data(device_type_list=device_type_list)
        bot_keyboard_device_model_logger.info(f'В state добавлен {device_type_list=}')

    total_pages = (len(device_type_list) - 1) // device_type_per_page + 1

    if device_type_pages_count < 0:
        device_type_pages_count = total_pages - 1
    elif device_type_pages_count >= total_pages:
        device_type_pages_count = 0

    start_indx = device_type_pages_count * device_type_per_page
    end_indx = start_indx + device_type_per_page
    page_models = device_type_list[start_indx:end_indx]

    navigation_kb = InlineKeyboardBuilder()
    device_type_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row['name'], callback_data=f'device_type:{row['id']}')]
        for row in page_models
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_device_type:{device_type_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_device_type'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_device_type:{device_type_pages_count + 1}')
    )
    device_type_kb.attach(navigation_kb)
    return device_type_kb.as_markup()


@inject
async def device_keyboard(state: FSMContext, device_pages_count: int = 0,
                          manufacturer_device_type_service: ManufacturerDeviceTypeService = Provide[
                              Container.manufacturer_device_type_service
                          ],
                          device_service: DeviceService = Provide[Container.device_service]
                          ) -> InlineKeyboardMarkup:
    device_per_page = 5

    data = await state.get_data()
    device_list = data.get('device_list')

    if not device_list:
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
        bot_keyboard_device_model_logger.info(f'В state добавлен {device_list=}')

    total_pages = (len(device_list) - 1) // device_per_page + 1

    if device_pages_count < 0:
        device_pages_count = total_pages - 1
    elif device_pages_count >= total_pages:
        device_pages_count = 0

    start_indx = device_pages_count * device_per_page
    end_indx = start_indx + device_per_page
    page_models = device_list[start_indx:end_indx]

    navigation_kb = InlineKeyboardBuilder()
    device_type_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row['name_model'], callback_data=f'device:{row['id']}:{row['name_model']}')]
        for row in page_models
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_device:{device_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_device'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_device:{device_pages_count + 1}')
    )
    device_type_kb.attach(navigation_kb)
    return device_type_kb.as_markup()


@inject
async def breaking_keyboard(state: FSMContext, breaking_pages_count: int = 0,
                            device_service_service: DeviceServiceService = Provide[Container.device_service_service],
                            service_service: ServiceService = Provide[Container.service_service]
                            ) -> InlineKeyboardMarkup:
    breaking_per_page = 5
    data = await state.get_data()
    breaking_list = data.get('breaking_list')

    if not breaking_list:
        device_id = data.get('device_id')
        device_service_list = await device_service_service.get(
            DeviceServicePartialDTO(device_id=device_id)
        )

        service_id_list = [
            model_device_service.service.id
            for model_device_service in device_service_list
        ]

        bot_keyboard_device_model_logger.info(f'{type(service_id_list[0])}{service_id_list=}')

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
        bot_keyboard_device_model_logger.info(f'В state добавлен {breaking_list=}')

    total_pages = (len(breaking_list) - 1) // breaking_per_page + 1

    if breaking_pages_count < 0:
        breaking_pages_count = total_pages - 1
    elif breaking_pages_count >= total_pages:
        breaking_pages_count = 0

    start_idx = breaking_pages_count * breaking_per_page
    end_idx = start_idx + breaking_per_page

    page_breaking = breaking_list[start_idx:end_idx]

    navigation_kb = InlineKeyboardBuilder()
    breaking_kb = InlineKeyboardBuilder([
        [InlineKeyboardButton(text=row[1], callback_data=f'breaking:{row[0]}')]
        for row in page_breaking
    ])

    navigation_kb.row(
        InlineKeyboardButton(text='⬅️', callback_data=f'page_breaking:{breaking_pages_count - 1}'),
        InlineKeyboardButton(text='Назад', callback_data=f'exit_breaking'),
        InlineKeyboardButton(text='➡️', callback_data=f'page_breaking:{breaking_pages_count + 1}')
    )
    breaking_kb.attach(navigation_kb)

    return breaking_kb.as_markup()
