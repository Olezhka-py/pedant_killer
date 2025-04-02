from typing import TYPE_CHECKING

from pedant_killer.schemas.order_schema import (BaseIdDTO,
                                                OrderDTO,
                                                OrderDeviceServiceRelDTO,
                                                OrderClientRelDTO,
                                                OrderMasterRelDTO,
                                                OrderOrderStatusRelDTO,
                                                OrderPostDTO,
                                                OrderPartialDTO)
if TYPE_CHECKING:
    from pedant_killer.database.repository import OrderRepository


class OrderService:
    def __init__(self, repository: 'OrderRepository') -> None:
        self._repository = repository

    async def save_order(self, model_dto: OrderPostDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

    async def save_relationship_order_device_service(self, order_id: BaseIdDTO,
                                                     device_service_id: BaseIdDTO
                                                     ) -> list[BaseIdDTO] | None:

        result_orm = await self._repository.save_order_device_service(order_id=order_id.id,
                                                                      device_service_id=device_service_id.id)

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None

    async def get_order(self, model_dto: OrderPartialDTO | BaseIdDTO) -> list[OrderDTO] | None:
        result_orm = await self._repository.get(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [OrderDTO.model_validate(res, from_attributes=True) for res in result_orm]

        return None

    async def get_relationship_device_service(self, model_dto: BaseIdDTO) -> list[OrderDeviceServiceRelDTO] | None:
        result_orm = await self._repository.get_order_device_service(instance_id=model_dto.id)

        if result_orm:
            return [OrderDeviceServiceRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_client(self, model_dto: BaseIdDTO) -> list[OrderClientRelDTO] | None:
        result_orm = await self._repository.get_client(instance_id=model_dto.id)

        if result_orm:
            return [OrderClientRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_master(self, model_dto: BaseIdDTO) -> list[OrderMasterRelDTO] | None:
        result_orm = await self._repository.get_master(instance_id=model_dto.id)

        if result_orm:
            return [OrderMasterRelDTO.model_validate(result_orm, from_attributes=True)]

        return None

    async def get_relationship_status(self, model_dto: BaseIdDTO) -> list[OrderOrderStatusRelDTO] | None:
        result_orm = await self._repository.get_status(instance_id=model_dto.id)

        if result_orm:
            return [OrderOrderStatusRelDTO.model_validate(result_orm, from_attributes=True)]

    async def get_all_orders(self) -> list[OrderDTO] | None:
        result_orm = await self._repository.get()

        if result_orm:
            return [OrderDTO.model_validate(row, from_attributes=True) for row in result_orm]

        return None

    async def delete_order(self, model_dto: BaseIdDTO) -> list[OrderDTO] | None:
        result_dto = await self.get_order(model_dto)

        if result_dto:
            delete_result = await self._repository.delete(id=model_dto.id)

            if delete_result:
                return result_dto

        return None

    async def update_order(self, model_dto: OrderPartialDTO) -> list[OrderDTO] | None:
        result_orm = await self._repository.update(**model_dto.model_dump(exclude_none=True))

        if result_orm:
            return [OrderDTO.model_validate(result_orm, from_attributes=True)]

        return None
