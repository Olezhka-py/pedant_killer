from datetime import datetime

import pytest
from unittest.mock import AsyncMock, MagicMock

from pedant_killer.database.models.order_orm import OrderOrm
from pedant_killer.database.repository.order_repository import OrderRepository
from pedant_killer.services.order_service import OrderService
from pedant_killer.schemas.order_schema import (
    OrderPostDTO, BaseIdDTO, OrderDTO, OrderPartialDTO, OrderDeviceServiceRelDTO, OrderClientRelDTO,
    OrderMasterRelDTO, OrderOrderStatusRelDTO
)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=OrderRepository)


@pytest.fixture(scope='function')
def service(repository) -> OrderService:
    return OrderService(repository)


async def test_save_order(service: OrderService, repository: AsyncMock) -> None:
    model_dto = OrderPostDTO(client_id=1,
                             master_id=1,
                             status_id=1,
                             created_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                             status_updated_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

    repository.save.return_value = 1
    result = await service.save(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(**model_dto.model_dump(exclude_none=True))


async def test_save_relationship_order_device_service(service: OrderService, repository: AsyncMock) -> None:
    order_id_dto = BaseIdDTO(id=1)
    device_service_id_dto = BaseIdDTO(id=1)

    repository.save_order_device_service.return_value = 1
    result = await service.save_relationship_order_device_service(order_id=order_id_dto,
                                                                  device_service_id=device_service_id_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save_order_device_service.assert_called_once_with(order_id=order_id_dto.id,
                                                                 device_service_id=device_service_id_dto.id)


async def test_get_order(service: OrderService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = OrderOrm(id=model_dto.id,
                                           client_id=1,
                                           master_id=1,
                                           status_id=1,
                                           created_at='2023-01-01 00:00:00',
                                           status_updated_at='2023-01-01 00:00:00')

    result = await service.get(model_dto)

    assert result == [OrderDTO(id=model_dto.id,
                               client_id=1,
                               master_id=1,
                               status_id=1,
                               created_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                               status_updated_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                               )]

    repository.get.assert_called_once_with(**model_dto.model_dump(exclude_none=True))


async def test_get_relationship_device_service(service: OrderService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    device_service_mock = MagicMock()
    device_service_mock.id = 1
    device_service_mock.device_id = 1
    device_service_mock.service_id = 1
    device_service_mock.price = 100
    device_service_mock.work_duration = 10

    order_mock = MagicMock()
    order_mock.id = 1
    order_mock.client_id = 1
    order_mock.master_id = 1
    order_mock.status_id = 1
    order_mock.created_at = '2023-01-01 00:00:00',
    order_mock.status_updated_at = '2023-01-01 00:00:00'

    result = await service.get_relationship_device_service(model_dto)

    assert result == [OrderDeviceServiceRelDTO.model_validate(order_mock, from_attributes=True)]
    repository.get_order_device_service.assert_called_once_with(instance_id=model_dto.id)


async def test_get_all_orders(service: OrderService, repository: AsyncMock) -> None:
    repository.get.return_value = [OrderOrm(id=1,
                                            client_id=1,
                                            master_id=1,
                                            status_id=1,
                                            created_at='2023-01-01 00:00:00',
                                            status_updated_at='2023-01-01 00:00:00')]

    result = await service.get_all()

    assert result == [OrderDTO(id=1,
                               client_id=1,
                               master_id=1,
                               status_id=1,
                               created_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                               status_updated_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))]
    repository.get.assert_called_once_with()


async def test_delete_order(service: OrderService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = OrderOrm(id=model_dto.id,
                                           client_id=1,
                                           master_id=1,
                                           status_id=1,
                                           created_at='2023-01-01 00:00:00',
                                           status_updated_at='2023-01-01 00:00:00')
    repository.delete.return_value = True

    result = await service.delete(model_dto)

    assert result == [OrderDTO(id=model_dto.id,
                               client_id=1,
                               master_id=1,
                               status_id=1,
                               created_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                               status_updated_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_order(service: OrderService, repository: AsyncMock) -> None:
    model_dto = OrderPartialDTO(id=2,
                                client_id=1,
                                master_id=1,
                                status_id=1,
                                created_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                status_updated_at=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
    repository.update.return_value = OrderOrm(id=model_dto.id,
                                              client_id=model_dto.client_id,
                                              master_id=model_dto.master_id,
                                              status_id=model_dto.status_id,
                                              created_at=model_dto.created_at,
                                              status_updated_at=model_dto.status_updated_at)

    result = await service.update(model_dto)

    assert result == [OrderDTO(id=model_dto.id,
                               client_id=model_dto.client_id,
                               master_id=model_dto.master_id,
                               status_id=model_dto.status_id,
                               created_at=model_dto.created_at,
                               status_updated_at=model_dto.status_updated_at)]
    repository.update.assert_called_once_with(**model_dto.model_dump(exclude_none=True))
