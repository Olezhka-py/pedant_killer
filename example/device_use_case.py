from example import device_repository, schemas


# можно использовать название "use case" вместо service, чтобы избежать DeviceServiceService
class DeviceUseCase:
    # репозиторий передается из контейнера зависимостей
    def __init__(self, device_repository: device_repository.DeviceRepository):
        # если нужна более сложная логика, то можно добавить больше репозиториев в конструктор
        self._device_repository = device_repository

    async def create(self, create_dto: schemas.CreateDeviceDTO) -> schemas.ReadDeviceDTO:
        return await self._device_repository.create(create_dto)

    async def get(self, device_id: int) -> schemas.ReadDeviceDTO:
        return await self._device_repository.get(device_id)

    async def get_all(self) -> list[schemas.ReadDeviceDTO]:
        return await self._device_repository.get_all()

    async def update(
        self,
        device_id: int,
        update_dto: schemas.UpdateDeviceDTO,
    ) -> schemas.ReadDeviceDTO:
        return await self._device_repository.update(device_id=device_id, update_dto=update_dto)

    async def delete(self, device_id: int) -> bool:
        return await self._device_repository.delete(device_id)

