import pytest
from unittest.mock import AsyncMock, MagicMock

from pedant_killer.database.models.manufacturer_device_type_orm import ManufacturerDeviceTypeOrm
from pedant_killer.database.repository.manufacturer_device_type_repository import ManufacturerDeviceTypeRepository
from pedant_killer.services.manufacturer_device_type_service import ManufacturerDeviceTypeService
from pedant_killer.schemas.manufacturer_device_type_schema import (
    ManufacturerDeviceTypePostDTO, BaseIdDTO, ManufacturerDeviceTypeDTO, ManufacturerDeviceTypePartialDTO,
    ManufacturerRelDTO, DeviceTypeRelDTO, ManufacturerDeviceTypeRelDTO
)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=ManufacturerDeviceTypeRepository)


@pytest.fixture(scope='function')
def service(repository) -> ManufacturerDeviceTypeService:
    return ManufacturerDeviceTypeService(repository)


async def test_save_manufacturer_device_type(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    model_dto = ManufacturerDeviceTypePostDTO(manufacturer_id=1, device_type_id=2)
    repository.save.return_value = 1
    result = await service.save(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(manufacturer_id=1, device_type_id=2)


async def test_get_manufacturer_device_type(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = ManufacturerDeviceTypeOrm(id=model_dto.id, manufacturer_id=1, device_type_id=2)

    result = await service.get(model_dto)

    assert result == [ManufacturerDeviceTypeDTO(id=model_dto.id, manufacturer_id=1, device_type_id=2)]
    repository.get.assert_called_once_with(id=model_dto.id)


async def test_get_all_manufacturer_device_types(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    repository.get.return_value = [ManufacturerDeviceTypeOrm(id=1, manufacturer_id=1, device_type_id=2)]

    result = await service.get_all()

    assert result == [ManufacturerDeviceTypeDTO(id=1, manufacturer_id=1, device_type_id=2)]
    repository.get.assert_called_once_with()


async def test_delete_manufacturer_device_type(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = ManufacturerDeviceTypeOrm(id=model_dto.id, manufacturer_id=1, device_type_id=1)
    repository.delete.return_value = True

    result = await service.delete(model_dto)

    assert result == [ManufacturerDeviceTypeDTO(id=model_dto.id, manufacturer_id=1, device_type_id=1)]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_manufacturer_device_type(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    model_dto = ManufacturerDeviceTypePartialDTO(id=2, manufacturer_id=1, device_type_id=1)
    repository.update.return_value = ManufacturerDeviceTypeOrm(id=model_dto.id,
                                                               manufacturer_id=model_dto.manufacturer_id,
                                                               device_type_id=model_dto.device_type_id)

    result = await service.update(model_dto)

    assert result == [ManufacturerDeviceTypeDTO(id=model_dto.id, manufacturer_id=1, device_type_id=1)]
    repository.update.assert_called_once_with(id=model_dto.id, manufacturer_id=model_dto.manufacturer_id,
                                              device_type_id=model_dto.device_type_id)


async def test_get_relationship_manufacturer(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    manufacturer_mock = MagicMock()
    manufacturer_mock.id = 1
    manufacturer_mock.name = "test"
    manufacturer_mock.description = "test_description"
    repository.get_manufacturer.return_value = ManufacturerDeviceTypeOrm()

    manufacturer_device_type_mock = MagicMock()
    manufacturer_device_type_mock.id = 1
    manufacturer_device_type_mock.manufacturer_id = 1
    manufacturer_device_type_mock.device_type_id = 1
    manufacturer_device_type_mock.manufacturer = manufacturer_mock

    repository.get_manufacturer.return_value = manufacturer_device_type_mock
    expected_result = [ManufacturerRelDTO.model_validate(manufacturer_device_type_mock, from_attributes=True)]
    result = await service.get_relationship_manufacturer(model_dto)
    assert result == expected_result
    repository.get_manufacturer.assert_called_once_with(instance_id=model_dto.id)


async def test_get_relationship_device_type(service: ManufacturerDeviceTypeService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    device_type_mock = MagicMock()
    device_type_mock.id = 1
    device_type_mock.name = "test"
    device_type_mock.description = "test_description"
    repository.get_device_type.return_value = ManufacturerDeviceTypeOrm()

    manufacturer_device_type_mock = MagicMock()
    manufacturer_device_type_mock.id = 1
    manufacturer_device_type_mock.manufacturer_id = 1
    manufacturer_device_type_mock.device_type_id = 1
    manufacturer_device_type_mock.device_type = device_type_mock

    repository.get_device_type.return_value = manufacturer_device_type_mock
    expected_result = [DeviceTypeRelDTO.model_validate(manufacturer_device_type_mock, from_attributes=True)]
    result = await service.get_relationship_device_type(model_dto)
    assert result == expected_result
    repository.get_device_type.assert_called_once_with(instance_id=model_dto.id)


async def test_get_relationship_manufacturer_device_type(service: ManufacturerDeviceTypeService, repository: AsyncMock
                                                         ) -> None:
    model_dto = BaseIdDTO(id=1)
    manufacturer_mock = MagicMock()
    manufacturer_mock.id = 1
    manufacturer_mock.name = "test"
    manufacturer_mock.description = "test_description"

    device_type_mock = MagicMock()
    device_type_mock.id = 1
    device_type_mock.name = "test"
    device_type_mock.description = "test_description"

    manufacturer_device_type_mock = MagicMock()
    manufacturer_device_type_mock.id = 1
    manufacturer_device_type_mock.manufacturer_id = 1
    manufacturer_device_type_mock.device_type_id = 1
    manufacturer_device_type_mock.manufacturer = manufacturer_mock
    manufacturer_device_type_mock.device_type = device_type_mock

    repository.get_manufacturer_device_type.return_value = manufacturer_device_type_mock
    expected_result = [ManufacturerDeviceTypeRelDTO.model_validate(manufacturer_device_type_mock, from_attributes=True)]
    result = await service.get_relationship_manufacturer_device_type(model_dto)
    assert result == expected_result
    repository.get_manufacturer_device_type.assert_called_once_with(instance_id=model_dto.id)
