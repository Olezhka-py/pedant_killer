import asyncio
from typing import TYPE_CHECKING

from pedant_killer.database.schemas import DeviceTypeDTO, DeviceTypePostDTO, BaseIdDTO
if TYPE_CHECKING:
    from pedant_killer.database.models import DeviceTypeOrm
    from pedant_killer.database.repository import DeviceTypeRepository


class DeviceTypeService:
    def __init__(self, repository: 'DeviceTypeRepository', model_orm: 'DeviceTypeOrm'):
        self.repository = repository
        self.model_orm = model_orm

    async def save_device_type(self, model_dto: DeviceTypePostDTO) -> [BaseIdDTO | None]:
        result_orm = await self.repository.save(self.model_orm, **model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_device_type(self, model_dto: BaseIdDTO) -> [DeviceTypeDTO | None]:
        result_orm = await self.repository.get(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_device_type(self) -> [list[DeviceTypeDTO] | None]:
        result_orm = await self.repository.get_all(self.model_orm)

        if result_orm:
            return [DeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device_type(self, model_dto: BaseIdDTO) -> [DeviceTypeDTO | None]:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_device_type(model_dto))
            delete_task = tg.create_task(self.repository.delete(self.model_orm, instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [DeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_device_type(self, model_dto: DeviceTypeDTO) -> [DeviceTypeDTO | None]:
        result_orm = await self.repository.update(self.model_orm,
                                                  instance_id=model_dto.id,
                                                  name=model_dto.name,
                                                  description=model_dto.description
                                                  )

        if result_orm:
            return [DeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None
