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

    async def get_manufacturer_device_type(self, model_dto: (ManufacturerDeviceTypePartialDTO
                                                             | BaseIdDTO
                                                             | ManufacturerDeviceTypePostDTO)
                                           ) -> list[ManufacturerDeviceTypeDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(res, from_attributes=True) for res in result_orm]

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
        result_orm = await self._repository.get()

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_manufacturer_device_type(self, model_dto: BaseIdDTO) -> list[ManufacturerDeviceTypeDTO] | None:
        result_dto = await self.get_manufacturer_device_type(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_manufacturer_device_type_id(self, model_dto: ManufacturerDeviceTypePartialDTO
                                                 ) -> list[ManufacturerDeviceTypeDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ManufacturerDeviceTypeDTO.model_validate(result_orm, from_attributes=True)]

        return None
