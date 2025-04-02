import pytest
from unittest.mock import AsyncMock

from pedant_killer.database.models.manufacturer_orm import ManufacturerOrm
from pedant_killer.database.repository.manufacturer_repository import ManufacturerRepository
from pedant_killer.services.manufacturer_service import ManufacturerService
from pedant_killer.schemas.manufacturer_schema import (
    ManufacturerPostDTO, BaseIdDTO, ManufacturerDTO, ManufacturerPartialDTO
)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=ManufacturerRepository)


@pytest.fixture(scope='function')
def service(repository) -> ManufacturerService:
    return ManufacturerService(repository)


async def test_save_manufacturer(service: ManufacturerService, repository: AsyncMock) -> None:
    model_dto = ManufacturerPostDTO(name='test', description='test_description')
    repository.save.return_value = 1
    result = await service.save_manufacturer(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(name=model_dto.name, description=model_dto.description)


async def test_get_manufacturer(service: ManufacturerService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = ManufacturerOrm(id=model_dto.id, name="test", description='test_description')

    result = await service.get_manufacturer(model_dto)

    assert result == [ManufacturerDTO(id=model_dto.id, name="test", description='test_description')]
    repository.get.assert_called_once_with(id=model_dto.id)


async def test_get_all_manufacturer(service: ManufacturerService, repository: AsyncMock) -> None:
    repository.get.return_value = [ManufacturerOrm(id=1, name="test")]

    result = await service.get_all_manufacturer()

    assert result == [ManufacturerDTO(id=1, name="test")]
    repository.get.assert_called_once_with()


async def test_delete_manufacturer(service: ManufacturerService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = ManufacturerOrm(id=model_dto.id, name="test")
    repository.delete.return_value = True

    result = await service.delete_manufacturer(model_dto)

    assert result == [ManufacturerDTO(id=model_dto.id, name="test")]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_manufacturer(service: ManufacturerService, repository: AsyncMock) -> None:
    model_dto = ManufacturerPartialDTO(id=2, name="updated_2")
    repository.update.return_value = ManufacturerOrm(id=model_dto.id, name=model_dto.name)

    result = await service.update_manufacturer(model_dto)

    assert result == [ManufacturerDTO(id=model_dto.id, name=model_dto.name)]
    repository.update.assert_called_once_with(id=model_dto.id, name=model_dto.name)
