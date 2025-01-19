import asyncio
from typing import TYPE_CHECKING

from pedant_killer.services.manufacturer_device_type_service import ManufacturerDeviceTypeService
from pedant_killer.database.schemas import (DevicePostDTO,
                                            DeviceDTO,
                                            DeviceManufacturerDeviceTypeRelDTO,
                                            BaseIdDTO,
                                            ManufacturerPostDTO,
                                            DeviceTypePostDTO)
if TYPE_CHECKING:
    from pedant_killer.database.models import DeviceOrm
    from pedant_killer.database.repository import DeviceRepository


class DeviceService:
    def __init__(self, repository: 'DeviceRepository', model_orm: 'DeviceOrm'):
        self.repository = repository
        self.model_orm = model_orm

    async def save_device(self, model_dto: DevicePostDTO) -> [BaseIdDTO | None]:
        result_orm = await self.repository.save(self.model_orm, **model_dto.dict())

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def save_and_create_device(self, manufacturer_dto: ManufacturerPostDTO, device_type_dto: DeviceTypePostDTO,
                                     name_model: str) -> [BaseIdDTO | None]:
        manufacturer_device_type = ManufacturerDeviceTypeService()
        manufacturer_device_type_id_dto = await manufacturer_device_type.save_and_create_manufacturer_device_type(
            manufacturer_dto,
            device_type_dto
        )  # TODO: проверить работоспособность

        if manufacturer_device_type_id_dto:
            result = await self.save_device(
                DevicePostDTO(
                    manufacturer_device_type_id=manufacturer_device_type_id_dto.id,
                    name_model=name_model
                )
            )

            return result

        return None

    async def get_device(self, model_dto: BaseIdDTO) -> [DeviceDTO | None]:
        result_orm = await self.repository.get(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_manufacturer_device_type(self, model_dto: BaseIdDTO
                                                        ) -> [DeviceManufacturerDeviceTypeRelDTO | None]:
        result_orm = await self.repository.get_manufacturer_device_type(self.model_orm, instance_id=model_dto.id)

        if result_orm:
            return [DeviceManufacturerDeviceTypeRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_all_device(self) -> [list[DeviceDTO] | None]:
        result_orm = await self.repository.get_all(self.model_orm)

        if result_orm:
            return [DeviceDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_device(self, model_dto: BaseIdDTO) -> [DeviceDTO | None]:

        async with asyncio.TaskGroup() as tg:
            instance_task = tg.create_task(self.get_device(model_dto))
            delete_task = tg.create_task(self.repository.delete(self.model_orm, model_dto.id))

        instance = await instance_task
        await delete_task

        if instance:
            return [DeviceDTO.model_validate(row, from_attributes=True) for row in instance]

        return None

    async def update_device(self, model_dto: DeviceDTO) -> [DeviceDTO | None]:
        result_orm = await self.repository.update(self.model_orm, instance_id=model_dto.id,
                                                  manufacturer_device_type_id=model_dto.manufacturer_device_type_id,
                                                  name_model=model_dto.name_model)

        if result_orm:
            return [DeviceDTO.model_validate(result_orm, from_attributes=True)]

        return None

