import asyncio
from typing import TYPE_CHECKING

from pedant_killer.database.schemas import (DeviceServiceOrderRelDTO,
                                            BaseIdDTO,
                                            DeviceServicePostDTO,
                                            DeviceServiceDTO,
                                            DeviceServiceDeviceRelDTO,
                                            DeviceServiceServiceRelDTO,
                                            DeviceServiceRelDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import DeviceServiceRepository


class DeviceServiceService:
    def __init__(self, repository: 'DeviceServiceRepository'):
        self._repository = repository

    async def save_device_service(self, model_dto: DeviceServicePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def save_relationship_device_service(self, device_service_id_dto: BaseIdDTO, order_id_dto: BaseIdDTO
                                               ) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save_device_service_order(
            order_id=order_id_dto.id,
            device_service_id=device_service_id_dto.id
            )

        if result_orm:  # TODO: Сделать проверку метода
            return [DeviceServiceOrderRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_order(self, device_service_id_dto: BaseIdDTO) -> list[DeviceServiceOrderRelDTO] | None:
        result_orm = await self._repository.get_order(instance_id=device_service_id_dto.id)

        if result_orm:
            return [DeviceServiceOrderRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_device_service(self, model_dto: BaseIdDTO) -> list[DeviceServiceDTO] | None:
        result_orm = await self._repository.get(instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device(self, model_dto: BaseIdDTO) -> list[DeviceServiceDeviceRelDTO] | None:
        result_orm = await self._repository.get_device(instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceDeviceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_service(self, model_dto: BaseIdDTO) -> list[DeviceServiceServiceRelDTO] | None:
        result_orm = await self._repository.get_service(instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device_service(self, model_dto: BaseIdDTO) -> list[DeviceServiceRelDTO] | None:
        result_orm = await self._repository.get_device_service(instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_device_service(self) -> list[DeviceServiceDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device_service(self, model_dto: BaseIdDTO) -> list[DeviceServiceDTO] | None:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_device_service(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        await delete_task

        if result_orm:
            return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_device_service(self, model_dto: DeviceServiceDTO) -> list[DeviceServiceDTO] | None:

        result_orm = await self._repository.update(
                                                instance_id=model_dto.id,
                                                service_id=model_dto.service_id,
                                                device_id=model_dto.device_id,
                                                work_duration=model_dto.work_duration
                                                )

        if result_orm:
            return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None
