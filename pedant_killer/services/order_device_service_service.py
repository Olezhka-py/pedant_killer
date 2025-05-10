from pedant_killer.database.repository.order_device_service_repository import OrderDeviceServiceRepository
from pedant_killer.schemas.common_schema import BaseIdDTO


class OrderDeviceServiceService:
    def __init__(self, repository: OrderDeviceServiceRepository) -> None:
        self._repository = repository

    async def save(self, device_service_id_dto: BaseIdDTO, order_id_dto: BaseIdDTO) -> list[BaseIdDTO] | None:
        result_orm = await self._repository.save(
            order_id=order_id_dto.id,
            device_service_id=device_service_id_dto.id
        )

        if result_orm:
            return [BaseIdDTO(id=result_orm)]

        return None
