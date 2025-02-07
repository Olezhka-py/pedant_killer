import asyncio
from typing import TYPE_CHECKING

from pedant_killer.database.schemas import ManufacturerPostDTO, ManufacturerDTO, BaseIdDTO
if TYPE_CHECKING:
    from pedant_killer.database.repository import ManufacturerRepository


class ManufacturerService:
    def __init__(self, repository: 'ManufacturerRepository'):
        self._repository = repository

    async def save_manufacturer(self, model_dto: ManufacturerPostDTO) -> [BaseIdDTO | None]:
        result_orm = await self._repository.save(**model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_manufacturer(self, model_dto: BaseIdDTO) -> [ManufacturerDTO | None]:
        result_orm = await self._repository.get(instance_id=model_dto.id)

        if result_orm:
            return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_manufacturer(self) -> [list[ManufacturerDTO] | None]:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_manufacturer(self, model_dto: BaseIdDTO) -> [ManufacturerDTO | None]:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_manufacturer(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [ManufacturerDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_manufacturer(self, model_dto: ManufacturerDTO) -> [ManufacturerDTO | None]:
        result_orm = await self._repository.update(
                                                  instance_id=model_dto.id,
                                                  name=model_dto.name,
                                                  description=model_dto.description
                                                  )

        if result_orm:
            return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None

