import asyncio
from typing import TYPE_CHECKING

from pedant_killer.schemas.access_level_schema import (AccessLevelPostDTO,
                                                       AccessLevelDTO, AccessLevelPartialDTO, BaseIdDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository.access_level_repository import AccessLevelRepository


class AccessLevelService:
    def __init__(self, repository: 'AccessLevelRepository'):
        self._repository = repository

    async def save_access_level(self, model_dto: AccessLevelPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_access_level(self, model_dto: AccessLevelPartialDTO | BaseIdDTO) -> list[AccessLevelDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def get_all_access_level(self) -> list[AccessLevelDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_access_level(self, model_dto: BaseIdDTO) -> list[AccessLevelDTO] | None:
        # result_orm = await self.get_access_level(model_dto)
        # if result_orm:
        delete_result = await self._repository.delete(instance_id=model_dto.id)
        return delete_result
        # return delete_result
        #     if delete_result:
        #         return [AccessLevelDTO.model_validate(row, from_attributes=True) for row in result_orm]

