import pytest
from unittest.mock import AsyncMock

from pedant_killer.database.models.device_type_orm import DeviceTypeOrm
from pedant_killer.database.repository.device_type_repository import DeviceTypeRepository
from pedant_killer.services.device_type_service import DeviceTypeService
from pedant_killer.schemas.device_type_schema import (DeviceTypePostDTO, BaseIdDTO, DeviceTypeDTO, DeviceTypePartialDTO)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=DeviceTypeRepository)


@pytest.fixture(scope='function')
def service(repository) -> DeviceTypeService:
    return DeviceTypeService(repository)


async def test_save_device_type(service: DeviceTypeService, repository: AsyncMock) -> None:
    model_dto = DeviceTypePostDTO(name='test', description='test_description')
    repository.save.return_value = 1
    result = await service.save(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(name=model_dto.name, description=model_dto.description)


async def test_get_device_type(service: DeviceTypeService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = DeviceTypeOrm(id=model_dto.id, name="test", description='test_description')

    result = await service.get(model_dto)

    assert result == [DeviceTypeDTO(id=model_dto.id, name="test", description='test_description')]
    repository.get.assert_called_once_with(id=model_dto.id)


async def test_get_all_device_type(service: DeviceTypeService, repository: AsyncMock) -> None:
    repository.get.return_value = [DeviceTypeOrm(id=1, name="test")]

    result = await service.get_all()

    assert result == [DeviceTypeDTO(id=1, name="test")]
    repository.get.assert_called_once_with()


async def test_delete_device_type(service: DeviceTypeService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = DeviceTypeOrm(id=model_dto.id, name="test")
    repository.delete.return_value = True

    result = await service.delete(model_dto)

    assert result == [DeviceTypeDTO(id=model_dto.id, name="test")]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_device_type(service: DeviceTypeService, repository: AsyncMock) -> None:
    model_dto = DeviceTypePartialDTO(id=2, name="updated_2")
    repository.update.return_value = DeviceTypeOrm(id=model_dto.id, name=model_dto.name)

    result = await service.update(model_dto)

    assert result == [DeviceTypeDTO(id=model_dto.id, name=model_dto.name)]
    repository.update.assert_called_once_with(id=model_dto.id, name=model_dto.name)