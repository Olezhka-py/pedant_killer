import asyncio
from pedant_killer.containers import Container
from pedant_killer.database.schemas import AccessLevelPostDTO, ManufacturerPostDTO, ManufacturerDeviceTypePostDTO, ManufacturerDeviceTypeDTO, BaseIdDTO, DeviceTypePostDTO, DeviceTypePostDTO, DeviceTypeDTO, DeviceServiceDTO
from pedant_killer import config
from pydantic import ValidationError


async def ggvp():
    container = Container()
    container.config.from_pydantic(config.Config())
    m = container.access_level_service()
    try:
        access_level_dto = AccessLevelPostDTO(name='dfd', importance=2)
    except ValidationError:
        return None
    g = await m.save_access_level(access_level_dto)
    # m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    print(g)

asyncio.run(ggvp())

