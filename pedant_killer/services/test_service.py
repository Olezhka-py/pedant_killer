import asyncio
from pedant_killer.containers import container
from pedant_killer.schemas import DevicePostDTO, DeviceDTO, ServicePartialDTO, ManufacturerDeviceTypePartialDTO, \
    DevicePartialDTO, BreakingPartialDTO
from pedant_killer.schemas.common_schema import BaseModel, BaseIdDTO
from pedant_killer.schemas.access_level_schema import AccessLevelPartialDTO
from pedant_killer import config
from pydantic import ValidationError
from pedant_killer.schemas.order_device_service_user_schema import DeviceServicePartialDTO


class ManufacturerDeviceTypeServicePartialDTO:
    pass


async def ggvp():
    m = container.user_service()
    dto = BaseIdDTO(id=1)
    g = await m.get(dto)
    # m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    print(g)

asyncio.run(ggvp())

