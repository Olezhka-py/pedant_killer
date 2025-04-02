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
            return [ManufacturerDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_all_manufacturer(self) -> list[ManufacturerDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [ManufacturerDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def delete_manufacturer(self, model_dto: BaseIdDTO) -> list[ManufacturerDTO] | None:
        result_dto = await self.get_manufacturer(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_manufacturer(self, model_dto: ManufacturerPartialDTO) -> list[ManufacturerDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [ManufacturerDTO.model_validate(result_orm, from_attributes=True)]

        return None
