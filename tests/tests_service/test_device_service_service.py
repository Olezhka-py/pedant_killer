import pytest
from unittest.mock import AsyncMock, MagicMock

from pedant_killer.database.models.device_service_orm import DeviceServiceOrm
from pedant_killer.database.repository.device_service_repository import DeviceServiceRepository
from pedant_killer.services.device_service_service import DeviceServiceService
from pedant_killer.schemas.device_service_schema import (DeviceServicePostDTO, DeviceServiceDTO,
                                                         DeviceServiceOrderRelDTO,
                                                         DeviceServicePartialDTO, BaseIdDTO,
                                                         DeviceServiceDeviceRelDTO,
                                                         DeviceServiceServiceRelDTO, DeviceServiceRelDTO)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=DeviceServiceRepository)


@pytest.fixture(scope='function')
def service(repository) -> DeviceServiceService:
    return DeviceServiceService(repository)


async def test_save_device(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = DeviceServicePostDTO(device_id=1, service_id=1, price=100, work_duration=10)
    repository.save.return_value = 1
    result = await service.save_device_service(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(device_id=model_dto.device_id,
                                            service_id=model_dto.service_id,
                                            price=model_dto.price,
                                            work_duration=model_dto.work_duration)


async def test_save_relationship_device_service_order(service: DeviceServiceService, repository: AsyncMock) -> None:
    device_service_id_dto = BaseIdDTO(id=1)
    order_id_dto = BaseIdDTO(id=2)

    repository.save_device_service_order.return_value = 1
    result = await service.save_relationship_device_service_order(device_service_id_dto=device_service_id_dto,
                                                                  order_id_dto=order_id_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save_device_service_order.assert_called_once_with(device_service_id=device_service_id_dto.id,
                                                                 order_id=order_id_dto.id)


async def test_get_device_service(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = DeviceServiceOrm(id=model_dto.id,
                                                   device_id=1,
                                                   service_id=1,
                                                   price=100,
                                                   work_duration=10)

    result = await service.get_device_service(model_dto)

    assert result == [DeviceServiceDTO(id=model_dto.id, device_id=1, service_id=1, price=100, work_duration=10)]
    repository.get.assert_called_once_with(id=model_dto.id)


async def test_get_all_device_service(service: DeviceServiceService, repository: AsyncMock) -> None:
    repository.get.return_value = [DeviceServiceOrm(id=1, device_id=1, service_id=1, price=100, work_duration=10)]

    result = await service.get_all_device_service()

    assert result == [DeviceServiceDTO(id=1, device_id=1, service_id=1, price=100, work_duration=10)]
    repository.get.assert_called_once_with()


async def test_get_relationship_order(service: DeviceServiceService, repository: AsyncMock) -> None:

    order_mock = MagicMock()
    order_mock.id = 1
    order_mock.client_id = 1
    order_mock.master_id = 1
    order_mock.status_id = 1
    order_mock.created_at = "2021-01-01 00:00:00"
    order_mock.status_updated_at = "2021-01-01 00:00:00"
    order_mock.sent_from_address = "Test address"
    order_mock.return_to_address = "Test address"
    order_mock.comment = "Test comment"
    order_mock.rating = 5

    device_service_mock = MagicMock()
    device_service_mock.id = 10
    device_service_mock.device_id = 1
    device_service_mock.service_id = 1
    device_service_mock.price = 100
    device_service_mock.work_duration = 10
    device_service_mock.order = [order_mock]

    model_dto = BaseIdDTO(id=1)

    expected_result = [DeviceServiceOrderRelDTO.model_validate(device_service_mock, from_attributes=True)]
    repository.get_order.return_value = device_service_mock
    result = await service.get_relationship_order(model_dto)
    assert result == expected_result
    repository.get_order.assert_called_once_with(instance_id=model_dto.id)


async def test_get_relationship_device(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)

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

    device_orm_mock = MagicMock()
    device_orm_mock.id = 10
    device_orm_mock.manufacturer_device_type_id = 1
    device_orm_mock.name_model = "Test Model"
    device_orm_mock.manufacturer_device_type = manufacturer_device_type_mock

    result_orm_mock = MagicMock()
    result_orm_mock.id = 1
    result_orm_mock.device_id = 10
    result_orm_mock.service_id = 1
    result_orm_mock.price = 100
    result_orm_mock.work_duration = 10
    result_orm_mock.device = device_orm_mock

    expected_result = [DeviceServiceDeviceRelDTO.model_validate(result_orm_mock, from_attributes=True)]
    repository.get_device.return_value = expected_result
    result = await service.get_relationship_device(model_dto)
    assert result == expected_result
    repository.get_device.assert_called_once_with(instance_id=model_dto.id)


async def test_get_relationship_service(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)

    service_mock = MagicMock()
    service_mock.id = 1
    service_mock.name = "Test Service"
    service_mock.description = "Some description"

    result_orm_mock = MagicMock()
    result_orm_mock.id = 1
    result_orm_mock.device_id = 1
    result_orm_mock.service_id = 1
    result_orm_mock.price = 100
    result_orm_mock.work_duration = 10
    result_orm_mock.service = service_mock

    expected_result = [DeviceServiceServiceRelDTO.model_validate(result_orm_mock, from_attributes=True)]
    repository.get_service.return_value = result_orm_mock
    result = await service.get_relationship_service(model_dto)
    assert result == expected_result
    repository.get_service.assert_called_once_with(instance_id=model_dto.id)


async def test_get_relationship_device_service(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)

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

    device_orm_mock = MagicMock()
    device_orm_mock.id = 10
    device_orm_mock.manufacturer_device_type_id = 1
    device_orm_mock.name_model = "Test Model"
    device_orm_mock.manufacturer_device_type = manufacturer_device_type_mock

    service_mock = MagicMock()
    service_mock.id = 1
    service_mock.name = "Test Service"
    service_mock.description = "Some description"

    result_orm_mock = MagicMock()
    result_orm_mock.id = 1
    result_orm_mock.device_id = 10
    result_orm_mock.service_id = 1
    result_orm_mock.price = 100
    result_orm_mock.work_duration = 10
    result_orm_mock.device = device_orm_mock
    result_orm_mock.service = service_mock

    expected_result = [DeviceServiceRelDTO.model_validate(result_orm_mock, from_attributes=True)]
    repository.get_device_service.return_value = result_orm_mock
    result = await service.get_relationship_device_service(model_dto)
    assert result == expected_result
    repository.get_device_service.assert_called_once_with(instance_id=model_dto.id)


async def test_delete_device(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = DeviceServiceOrm(id=1, device_id=1, service_id=1, price=100, work_duration=10)
    repository.delete.return_value = True

    result = await service.delete_device_service(model_dto)

    assert result == [DeviceServiceDTO(id=1, device_id=1, service_id=1, price=100, work_duration=10)]
    repository.get.assert_called_once_with(id=model_dto.id)
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_device(service: DeviceServiceService, repository: AsyncMock) -> None:
    model_dto = DeviceServicePartialDTO(id=1, device_id=1, service_id=1, price=100, work_duration=10)
    repository.update.return_value = DeviceServiceOrm(id=1, device_id=1, service_id=1, price=100, work_duration=10)

    result = await service.update_device_service(model_dto)

    assert result == [DeviceServiceDTO(id=1, device_id=1, service_id=1, price=100, work_duration=10)]
    repository.update.assert_called_once_with(id=1, device_id=1, service_id=1, price=100, work_duration=10)
