import pytest
from unittest.mock import AsyncMock

from pedant_killer.database.models.order_status_orm import OrderStatusOrm
from pedant_killer.database.repository.order_status_repository import OrderStatusRepository
from pedant_killer.services.order_status_service import OrderStatusService
from pedant_killer.schemas.order_status_schema import (
    OrderStatusPostDTO, BaseIdDTO, OrderStatusDTO, OrderStatusPartialDTO
)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=OrderStatusRepository)


@pytest.fixture(scope='function')
def service(repository) -> OrderStatusService:
    return OrderStatusService(repository)


async def test_save_order_status(service: OrderStatusService, repository: AsyncMock) -> None:
    model_dto = OrderStatusPostDTO(name='test', description='test_description')
    repository.save.return_value = 1
    result = await service.save_order_status(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(**model_dto.model_dump(exclude_none=True))


async def test_get_order_status(service: OrderStatusService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = OrderStatusOrm(id=model_dto.id, name="test", description='test_description')

    result = await service.get_order_status(model_dto)

    assert result == [OrderStatusDTO(id=model_dto.id, name="test", description='test_description')]
    repository.get.assert_called_once_with(**model_dto.model_dump(exclude_none=True))


async def test_get_all_order_status(service: OrderStatusService, repository: AsyncMock) -> None:
    repository.get.return_value = [OrderStatusOrm(id=1, name="test", description='test_description')]

    result = await service.get_all_order_status()

    assert result == [OrderStatusDTO(id=1, name="test", description='test_description')]
    repository.get.assert_called_once_with()


async def test_delete_order_status(service: OrderStatusService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = OrderStatusOrm(id=model_dto.id, name="test", description='test_description')
    repository.delete.return_value = True

    result = await service.delete_order_status(model_dto)

    assert result == [OrderStatusDTO(id=model_dto.id, name="test", description='test_description')]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_order_status(service: OrderStatusService, repository: AsyncMock) -> None:
    model_dto = OrderStatusPartialDTO(id=2, name="updated_2", description='updated_description')
    repository.update.return_value = OrderStatusOrm(id=model_dto.id, name=model_dto.name, description=model_dto.description)

    result = await service.update_access_level(model_dto)

    assert result == [OrderStatusDTO(id=model_dto.id, name=model_dto.name, description=model_dto.description)]
    repository.update.assert_called_once_with(**model_dto.model_dump(exclude_none=True))