import asyncio
from pedant_killer.containers import Container
from pedant_killer.database.schemas import ManufacturerPostDTO, ManufacturerDeviceTypePostDTO, ManufacturerDeviceTypeDTO, BaseIdDTO, DeviceTypePostDTO, DeviceTypePostDTO, DeviceTypeDTO, DeviceServiceDTO

from pydantic import ValidationError


async def ggvp():
    container = Container()
    m = container.manufacturer_device_type_service()
    try:
        manufacturer = BaseIdDTO(id=17)
    except ValidationError:
        return None
    g = await m.delete_manufacturer_device_type(manufacturer)
    # m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    print(g)

asyncio.run(ggvp())

