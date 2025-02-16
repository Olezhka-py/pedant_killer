import asyncio
from typing import TYPE_CHECKING

from pedant_killer.schemas.manufacturer_schema import (ManufacturerPostDTO,
                                                       ManufacturerPartialDTO,
                                                       ManufacturerDTO,
                                                       BaseIdDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import ManufacturerRepository


class ManufacturerService:
    def __init__(self, repository: 'ManufacturerRepository'):
        self._repository = repository

    async def save_manufacturer(self, model_dto: ManufacturerPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_manufacturer(self, model_dto: ManufacturerPartialDTO | BaseIdDTO) -> list[ManufacturerDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_manufacturer(self) -> list[ManufacturerDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_manufacturer(self, model_dto: BaseIdDTO) -> list[ManufacturerDTO] | None:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_manufacturer(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        delete_orm = await delete_task

        if result_orm and delete_orm:
            return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_manufacturer(self, model_dto: ManufacturerPartialDTO) -> list[ManufacturerDTO] | None:
        result_orm = await self._repository.update(
                                                  instance_id=model_dto.id,
                                                  name=model_dto.name,
                                                  description=model_dto.description
                                                  )

        if result_orm:
            return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None

