from typing import TYPE_CHECKING

from pedant_killer.schemas.device_service_schema import (DeviceServiceOrderRelDTO,
                                                         DeviceServicePartialDTO,
                                                         DeviceServicePostDTO,
                                                         DeviceServiceDTO,
                                                         DeviceServiceDeviceRelDTO,
                                                         DeviceServiceServiceRelDTO,
                                                         DeviceServiceRelDTO,
                                                         BaseIdDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import DeviceServiceRepository


class DeviceServiceService:
    def __init__(self, repository: 'DeviceServiceRepository'):
        self._repository = repository

    async def save_device_service(self, model_dto: DeviceServicePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def save_relationship_device_service_order(self, device_service_id_dto: BaseIdDTO, order_id_dto: BaseIdDTO
                                               ) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save_device_service_order(
            order_id=order_id_dto.id,
            device_service_id=device_service_id_dto.id
            )

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_relationship_order(self, model_dto: BaseIdDTO) -> list[DeviceServiceOrderRelDTO] | None:
        result_orm = await self._repository.get_order(instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceOrderRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_device_service(self, model_dto: DeviceServicePartialDTO | BaseIdDTO) -> list[DeviceServiceDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [DeviceServiceDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_relationship_device(self, model_dto: BaseIdDTO) -> list[DeviceServiceDeviceRelDTO] | None:
        result_orm = await self._repository.get_device(instance_id=model_dto.id)

        if result_orm:
            return [DeviceServiceDeviceRelDTO.model_validate(res, from_attributes=True) for res in result_orm]

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
        result_orm = await self._repository.get()

        if result_orm:
            return [DeviceServiceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device_service(self, model_dto: BaseIdDTO) -> list[DeviceServiceDTO] | None:
        result_dto = await self.get_device_service(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_device_service(self, model_dto: DeviceServicePartialDTO) -> list[DeviceServiceDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [DeviceServiceDTO.model_validate(result_orm, from_attributes=True)]

        return None
