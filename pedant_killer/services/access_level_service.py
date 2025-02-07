import asyncio
from typing import TYPE_CHECKING

from pedant_killer.database.schemas import AccessLevelPostDTO, BaseIdDTO, AccessLevelDTO
if TYPE_CHECKING:
    from pedant_killer.database.repository.access_level_repository import AccessLevelRepository


class AccessLevelService:
    def __init__(self, repository: 'AccessLevelRepository'):
        self._repository = repository

    async def save_access_level(self, model_dto: AccessLevelPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_access_level(self, model_dto: BaseIdDTO) -> list[AccessLevelDTO] | None:
        result_orm = await self._repository.get(instance_id=model_dto.id)

        if result_orm:
            return [AccessLevelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_access_level(self) -> list[AccessLevelDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_access_level(self, model_dto: BaseIdDTO) -> list[AccessLevelDTO] | None:

        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_access_level(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None
