import pytest
from unittest.mock import AsyncMock, MagicMock

from pedant_killer.database.models.device_orm import DeviceOrm
from pedant_killer.database.repository.device_repository import DeviceRepository
from pedant_killer.services.device_service import DeviceService
from pedant_killer.schemas.device_schema import (DevicePostDTO, DeviceDTO,
                                                 DeviceManufacturerDeviceTypeRelDTO,
                                                 DevicePartialDTO, BaseIdDTO)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=DeviceRepository)


@pytest.fixture(scope='function')
def service(repository) -> DeviceService:
    return DeviceService(repository)


async def test_save_device(service: DeviceService, repository: AsyncMock) -> None:
    model_dto = DevicePostDTO(name_model='test_device', manufacturer_device_type_id=1)
    repository.save.return_value = 1
    result = await service.save(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(name_model=model_dto.name_model, manufacturer_device_type_id=model_dto.manufacturer_device_type_id)


async def test_get_device(service: DeviceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = DeviceOrm(id=model_dto.id, name_model="test_device", manufacturer_device_type_id=1)

    result = await service.get(model_dto)

    assert result == [DeviceDTO(id=model_dto.id, name_model="test_device", manufacturer_device_type_id=1)]
    repository.get.assert_called_once_with(id=model_dto.id)


async def test_get_all_device(service: DeviceService, repository: AsyncMock) -> None:
    repository.get.return_value = [DeviceOrm(id=1, name_model="test_device", manufacturer_device_type_id=1)]

    result = await service.get_all()

    assert result == [DeviceDTO(id=1, name_model="test_device", manufacturer_device_type_id=1)]
    repository.get.assert_called_once_with()


async def test_get_relationship_manufacturer_device_type(service: DeviceService, repository: AsyncMock) -> None:
    manufacturer_mock = MagicMock()
    manufacturer_mock.id = 2
    manufacturer_mock.name = "Test Manufacturer"
    manufacturer_mock.description = "Some description"

    device_type_mock = MagicMock()
    device_type_mock.id = 3
    device_type_mock.name = "Test Device Type"
    device_type_mock.description = "Some device type"

    manufacturer_device_type_mock = MagicMock()
    manufacturer_device_type_mock.id = 1
    manufacturer_device_type_mock.manufacturer = manufacturer_mock
    manufacturer_device_type_mock.device_type = device_type_mock

    result_orm_mock = MagicMock()
    result_orm_mock.id = 10
    result_orm_mock.manufacturer_device_type_id = 1
    result_orm_mock.name_model = "Test Model"
    result_orm_mock.manufacturer_device_type = manufacturer_device_type_mock

    model_dto = BaseIdDTO(id=1)

    repository.get_manufacturer_device_type.return_value = result_orm_mock

    expected_result = [DeviceManufacturerDeviceTypeRelDTO.model_validate(result_orm_mock, from_attributes=True)]
    result = await service.get_relationship_manufacturer_device_type(model_dto)

    assert result == expected_result
    repository.get_manufacturer_device_type.assert_called_once_with(instance_id=model_dto.id)


async def test_delete_device(service: DeviceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = DeviceOrm(id=model_dto.id, name_model="test_device", manufacturer_device_type_id=1)
    repository.delete.return_value = True

    result = await service.delete(model_dto)

    assert result == [DeviceDTO(id=model_dto.id, name_model="test_device", manufacturer_device_type_id=1)]
    repository.get.assert_called_once_with(id=model_dto.id)
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_device(service: DeviceService, repository: AsyncMock) -> None:
    model_dto = DevicePartialDTO(id=1, name_model="updated_device", manufacturer_device_type_id=1)
    repository.update.return_value = DeviceOrm(id=model_dto.id, name_model=model_dto.name_model,
                                               manufacturer_device_type_id=model_dto.manufacturer_device_type_id)

    result = await service.update(model_dto)

    assert result == [DeviceDTO(id=model_dto.id, name_model=model_dto.name_model,
                                manufacturer_device_type_id=model_dto.manufacturer_device_type_id)]
    repository.update.assert_called_once_with(id=model_dto.id, name_model=model_dto.name_model,
                                              manufacturer_device_type_id=model_dto.manufacturer_device_type_id)
