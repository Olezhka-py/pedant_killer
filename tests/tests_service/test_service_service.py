import pytest
from unittest.mock import AsyncMock

from pedant_killer.database.models.service_orm import ServiceOrm
from pedant_killer.database.repository.service_repository import ServiceRepository
from pedant_killer.services.service_service import ServiceService
from pedant_killer.schemas.service_schema import (
    ServicePostDTO, BaseIdDTO, ServiceDTO, ServicePartialDTO
)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=ServiceRepository)


@pytest.fixture(scope='function')
def service(repository) -> ServiceService:
    return ServiceService(repository)


async def test_save_service(service: ServiceService, repository: AsyncMock) -> None:
    model_dto = ServicePostDTO(name='test_service', description='test_description')
    repository.save.return_value = 1
    result = await service.save(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(**model_dto.model_dump(exclude_none=True))


async def test_get_service(service: ServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = ServiceOrm(id=model_dto.id, name="test_service", description='test_description')

    result = await service.get(model_dto)

    assert result == [ServiceDTO(id=model_dto.id, name="test_service", description='test_description')]
    repository.get.assert_called_once_with(**model_dto.model_dump(exclude_none=True))


async def test_get_all_services(service: ServiceService, repository: AsyncMock) -> None:
    repository.get.return_value = [ServiceOrm(id=1, name="test_service", description='test_description')]

    result = await service.get_all()

    assert result == [ServiceDTO(id=1, name="test_service", description='test_description')]
    repository.get.assert_called_once_with()


async def test_delete_service(service: ServiceService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = ServiceOrm(id=model_dto.id, name="test_service", description='test_description')
    repository.delete.return_value = True

    result = await service.delete(model_dto)

    assert result == [ServiceDTO(id=model_dto.id, name="test_service", description='test_description')]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_service(service: ServiceService, repository: AsyncMock) -> None:
    model_dto = ServicePartialDTO(id=2, name="updated_service", description='updated_description')
    repository.update.return_value = ServiceOrm(id=model_dto.id, name=model_dto.name, description=model_dto.description)

    result = await service.update(model_dto)

    assert result == [ServiceDTO(id=model_dto.id, name=model_dto.name, description=model_dto.description)]
    repository.update.assert_called_once_with(**model_dto.model_dump(exclude_none=True))
