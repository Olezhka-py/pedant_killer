import asyncio
from typing import TYPE_CHECKING

from pedant_killer.schemas.device_schema import (DevicePostDTO,
                                                 DeviceDTO,
                                                 DeviceManufacturerDeviceTypeRelDTO,
                                                 DevicePartialDTO,
                                                 BaseIdDTO
                                                 )
if TYPE_CHECKING:
    from pedant_killer.database.repository import DeviceRepository


class DeviceService:
    def __init__(self, repository: 'DeviceRepository'):
        self._repository = repository

    async def save_device(self, model_dto: DevicePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    # async def save_manufacturer_device_type(self, manufacturer_device_type_dto: BaseIdDTO,
    #                                  name_model: str) -> BaseIdDTO | None:
    #     manufacturer_device_type = ManufacturerDeviceTypeService()
    #     manufacturer_device_type_id_dto = await manufacturer_device_type.save_and_create_manufacturer_device_type(
    #         manufacturer_dto,
    #         device_type_dto
    #     )  # TODO: переделать на уровне выше
    #
    #     if manufacturer_device_type_id_dto:
    #         result = await self.save_device(
    #             DevicePostDTO(
    #                 manufacturer_device_type_id=manufacturer_device_type_id_dto.id,
    #                 name_model=name_model
    #             )
    #         )
    #
    #         return result
    #
    #     return None

    async def get_device(self, model_dto: DevicePartialDTO | BaseIdDTO) -> list[DeviceDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [DeviceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer_device_type(self, model_dto: BaseIdDTO
                                                        ) -> list[DeviceManufacturerDeviceTypeRelDTO] | None:
        result_orm = await self._repository.get_manufacturer_device_type(instance_id=model_dto.id)

        if result_orm:
            return [DeviceManufacturerDeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_device(self) -> list[DeviceDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [DeviceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device(self, model_dto: BaseIdDTO) -> list[DeviceDTO] | None:

        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_device(model_dto))
            delete_task = tg.create_task(self._repository.delete(instance_id=model_dto.id))

        result_orm = await instance_task
        delete_orm = await delete_task

        if result_orm and delete_orm:
            return [DeviceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_device(self, model_dto: DevicePartialDTO) -> list[DeviceDTO] | None:
        result_orm = await self._repository.update(instance_id=model_dto.id,
                                                   manufacturer_device_type_id=model_dto.manufacturer_device_type_id,
                                                   name_model=model_dto.name_model)

        if result_orm:
            return [DeviceDTO.model_validate(result_orm, from_attributes=True)]

        return None

