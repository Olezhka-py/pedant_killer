import asyncio
from typing import TYPE_CHECKING

from pedant_killer.database.models import OrderOrm
from pedant_killer.database.schemas import (DeviceServiceOrderRelDTO,
                                            BaseIdDTO,
                                            DeviceServicePostDTO,
                                            DeviceServiceDTO,
                                            DeviceServiceDeviceRelDTO,
                                            DeviceServiceServiceRelDTO,
                                            DeviceServiceRelDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import DeviceServiceRepository
    from pedant_killer.database.models import DeviceServiceOrm


class DeviceServiceService:
    def __init__(self, repository: 'DeviceServiceRepository', model_orm: 'DeviceServiceOrm'):
        self.repository = repository
        self.model_orm = model_orm

    async def save_device_service(self, model_dto: DeviceServicePostDTO) -> [BaseIdDTO | None]:
        result_orm = await self.repository.save(self.model_orm, **model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def save_relationship_device_service(self, device_service_id_dto: BaseIdDTO, order_id_dto: BaseIdDTO
                                               ) -> [BaseIdDTO | None]:
        result_orm = await self.repository.save_device_service_order(OrderOrm,
                                                                     self.model_orm,
                                                                     order_id=order_id_dto.id,
                                                                     device_service_id=device_service_id_dto.id
                                                                     )

        if result_orm:  # TODO: Сделать проверку метода
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_relationship_order(self, device_service_id_dto: BaseIdDTO) -> [DeviceServiceOrderRelDTO | None]:
        result_orm = await self.repository.get_order(self.model_orm, instance_id=device_service_id_dto.id)

        if result_orm:
            return [DeviceServiceOrderRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_device_service(self, model_dto: BaseIdDTO) -> [DeviceServiceDTO | None]:
        result_orm = await self.repository.get(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device(self, model_dto: BaseIdDTO) -> [DeviceServiceDeviceRelDTO | None]:
        result_orm = await self.repository.get_device(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceDeviceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_service(self, model_dto: BaseIdDTO) -> [DeviceServiceServiceRelDTO | None]:
        result_orm = await self.repository.get_service(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device_service(self, model_dto: BaseIdDTO) -> [DeviceServiceRelDTO | None]:
        result_orm = await self.repository.get_device_service(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_device_service(self) -> [list[DeviceServiceDTO] | None]:
        result_orm = await self.repository.get_all(self.model_orm)

        if result_orm:
            return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device_service(self, model_dto: BaseIdDTO) -> [DeviceServiceDTO | None]:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_device_service(model_dto))
            delete_task = tg.create_task(self.repository.delete(self.model_orm, instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_device_service(self, model_dto: DeviceServiceDTO) -> [DeviceServiceDTO | None]:

        result_orm = await self.repository.update(self.model_orm,
                                                  instance_id=model_dto.id,
                                                  service_id=model_dto.service_id,
                                                  device_id=model_dto.device_id,
                                                  work_duration=model_dto.work_duration
                                                  )

        if result_orm:
            return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None
