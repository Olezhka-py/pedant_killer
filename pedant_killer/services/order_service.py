from pedant_killer.schemas.order_device_service_user_schema import (BaseIdDTO,
                                                                    OrderDTO,
                                                                    OrderRelDTO,
                                                                    OrderPostDTO,
                                                                    OrderPartialDTO)

from pedant_killer.database.repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    async def save(self, model_dto: OrderPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

    async def get(self, model_dto: OrderPartialDTO | BaseIdDTO) -> list[OrderRelDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [OrderRelDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_all(self) -> list[OrderDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [OrderDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete(self, model_dto: BaseIdDTO) -> list[OrderDTO] | None:
        result_dto = await self.get(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update(self, model_dto: OrderPartialDTO) -> list[OrderDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None
