import asyncio
from pedant_killer.containers import Container
from pedant_killer.schemas.common_schema import BaseModel, BaseIdDTO
from pedant_killer.schemas.access_level_schema import AccessLevelPartialDTO
from pedant_killer import config
from pydantic import ValidationError


async def ggvp():
    container = Container()
    container.config.from_pydantic(config.Config())
    m = container.access_level_service()
    access_level_dto = BaseIdDTO(id=11)
    g = await m.delete_access_level(access_level_dto)
    # m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    print(g)

asyncio.run(ggvp())

