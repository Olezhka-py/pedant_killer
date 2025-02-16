import asyncio
from typing import TYPE_CHECKING
from pedant_killer.schemas.manufacturer_device_type_schema import (ManufacturerDeviceTypeDTO,
                                                                   ManufacturerDeviceTypePostDTO,
                                                                   ManufacturerDeviceTypePartialDTO,
                                                                   ManufacturerRelDTO,
                                                                   DeviceTypeRelDTO,
                                                                   ManufacturerDeviceTypeRelDTO,
                                                                   BaseIdDTO
                                                                   )

if TYPE_CHECKING:
    from pedant_killer.database.repository import ManufacturerDeviceTypeRepository


class ManufacturerDeviceTypeService:
    def __init__(self, repository: 'ManufacturerDeviceTypeRepository') -> None:
        self._repository = repository

    async def save_manufacturer_device_type(self, model_dto: ManufacturerDeviceTypePostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    # async def save_and_create_manufacturer_device_type(self, manufacturer_dto: ManufacturerPostDTO,
    #                                                    device_type_dto: DeviceTypePostDTO) -> [BaseIdDTO | None]:
    #
    #     async with asyncio.TaskGroup() as tg:
    #         manufacturer_task = tg.create_task(self.manufacturer_service.save_manufacturer(manufacturer_dto))
    #         device_type_task = tg.create_task(self.device_type_service.save_device_type(device_type_dto))
    #
    #     result_orm = await self.repository.save(
    #         self.model_orm,
    #         manufacturer_id=manufacturer_task.result()[0].id,
    #         device_type_id=device_type_task.result()[0].id
    #     ) # TODO: Сделать на уровне выше
    #
    #     if result_orm:
    #         return [BaseIdDTO(id=result_orm)]
    #
    #     return None

    async def get_manufacturer_device_type(self, model_dto: ManufacturerDeviceTypePartialDTO | BaseIdDTO
                                           ) -> list[ManufacturerDeviceTypeDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer(self, model_dto: BaseIdDTO) -> list[ManufacturerRelDTO] | None:
        result_orm = await self._repository.get_manufacturer(instance_id=model_dto.id)

        if result_orm:
            return [ManufacturerRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_device_type(self, model_dto: BaseIdDTO) -> list[DeviceTypeRelDTO] | None:
        result_orm = await self._repository.get_device_type(instance_id=model_dto.id)

        if result_orm:
            return [DeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer_device_type(self, model_dto: BaseIdDTO
                                                        ) -> list[ManufacturerDeviceTypeRelDTO] | None:
        result_orm = await self._repository.get_manufacturer_device_type(instance_id=model_dto.id)

        if result_orm:
            return [ManufacturerDeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_manufacturer_device_types(self) -> list[ManufacturerDeviceTypeDTO] | None:
        result_orm = await self._repository.get_all()

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_manufacturer_device_type(self, model_dto: BaseIdDTO) -> list[ManufacturerDeviceTypeDTO] | None:
        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_manufacturer_device_type(model_dto))
            delete_task = tg.create_task(self._repository.delete(model_dto.id))

        result_orm = await instance_task
        delete_orm = await delete_task

        if result_orm and delete_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def update_manufacturer_device_type_id(self, model_dto: ManufacturerDeviceTypePartialDTO
                                                 ) -> list[ManufacturerDeviceTypeDTO] | None:
        result_orm = await self._repository.update(
            instance_id=model_dto.id,
            manufacturer_id=model_dto.manufacturer_id,
            device_type_id=model_dto.device_type_id
        )

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None
