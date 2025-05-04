import asyncio
from pedant_killer.containers import container
from pedant_killer.schemas.common_schema import BaseModel, BaseIdDTO
from pedant_killer.schemas.access_level_schema import AccessLevelPartialDTO
from pedant_killer import config
from pydantic import ValidationError


async def ggvp():
    m = container.manufacturer_service()
    breaking_id = BaseIdDTO(id=3)
    service_id = BaseIdDTO(id=1)
    g = await m.get_all_manufacturer()
    # m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    print(g)

asyncio.run(ggvp())

