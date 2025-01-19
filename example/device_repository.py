from sqlalchemy.ext.asyncio import AsyncSession

from example import core_repository, models, schemas


class DeviceRepository(core_repository.CoreRepository):
    # сессия передается из контейнера зависимостей
    def __init__(self, session: AsyncSession):
        # указываем нужную модель прямо в конструкторе
        super().__init__(session=session, model_class=models.DeviceORM)

    async def create(self, create_dto: schemas.CreateDeviceDTO) -> schemas.ReadDeviceDTO:
        created_model = await super().create(create_dto)
        return schemas.ReadDeviceDTO.model_validate(created_model, from_attributes=True)

    async def get(self, device_id: int) -> schemas.ReadDeviceDTO:
        found_model = await super().get(device_id)

        if found_model is None:
            raise ValueError(f"Device with id {device_id} not found")

        return schemas.ReadDeviceDTO.model_validate(found_model, from_attributes=True)

    async def get_all(self) -> list[schemas.ReadDeviceDTO]:
        found_models = await super().get_all()
        dto_list = [
            schemas.ReadDeviceDTO.model_validate(found_model, from_attributes=True)
            for found_model in found_models
        ]
        return dto_list

    async def update(
        self,
        device_id: int,
        update_dto: schemas.UpdateDeviceDTO,
    ) -> schemas.ReadDeviceDTO:
        updated_model = await super().update(instance_id=device_id, update_dto=update_dto)
        return schemas.ReadDeviceDTO.model_validate(updated_model, from_attributes=True)

    async def delete(self, device_id: int) -> bool:
        return await super().delete(device_id)
