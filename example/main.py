import asyncio

import dependency_injector.wiring as di_wiring

from example import containers
from example.device_use_case import DeviceUseCase
from pedant_killer import config


@di_wiring.inject  # помечаем функцию, в которую нужно внедрить зависимости из контейнера
async def example_message_handler(
    message,  # имитируем сообщение от телеграма
    # внедряем зависимость из контейнера
    device_use_case: DeviceUseCase = di_wiring.Provide[containers.Container.device_use_case],
):
    # пример логики хендлера
    device_id = message["..."]["message_text"]

    found_device = await device_use_case.get(device_id=device_id)

    if found_device is None:
        message.respond("Устройство не найдено")
    else:
        message.respond("Устройство успешно найдено")


async def main():
    container = containers.Container()
    # передаем наши настройки в контейнер для того, чтобы их можно было использовать при сборке зависимостей
    container.config.from_pydantic(config.Config)


if __name__ == "__main__":
    asyncio.run(main())
