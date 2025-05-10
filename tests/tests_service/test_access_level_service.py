import pytest
from unittest.mock import AsyncMock

from pedant_killer.database.models.access_level_orm import AccessLevelOrm
from pedant_killer.database.repository.access_level_repository import AccessLevelRepository
from pedant_killer.services.access_level_service import AccessLevelService
from pedant_killer.schemas.access_level_schema import (AccessLevelPostDTO, BaseIdDTO,
                                                       AccessLevelDTO, AccessLevelPartialDTO)


@pytest.fixture(scope='function')
def repository() -> AsyncMock:
    return AsyncMock(spec=AccessLevelRepository)


@pytest.fixture(scope='function')
def service(repository) -> AccessLevelService:
    return AccessLevelService(repository)


async def test_save_access_level(service: AccessLevelService, repository: AsyncMock) -> None:
    model_dto = AccessLevelPostDTO(name='test', importance=5)
    repository.save.return_value = 1
    result = await service.save(model_dto)

    assert result == [BaseIdDTO(id=1)]
    repository.save.assert_called_once_with(name=model_dto.name, importance=model_dto.importance)


async def test_get_access_level(service: AccessLevelService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = [AccessLevelOrm(id=model_dto.id, name="test", importance=5)]

    result = await service.get(model_dto)

    assert result == [AccessLevelDTO(id=model_dto.id, name="test", importance=5)]
    repository.get.assert_called_once_with(id=model_dto.id)


async def test_get_all_access_level(service: AccessLevelService, repository: AsyncMock) -> None:
    repository.get.return_value = [AccessLevelOrm(id=1, name="test", importance=5)]

    result = await service.get_all()

    assert result == [AccessLevelDTO(id=1, name="test", importance=5)]
    repository.get.assert_called_once_with()


async def test_delete_access_level(service: AccessLevelService, repository: AsyncMock) -> None:
    model_dto = BaseIdDTO(id=1)
    repository.get.return_value = [AccessLevelOrm(id=model_dto.id, name="test", importance=5)]
    repository.delete.return_value = True

    result = await service.delete(model_dto)

    assert result == [AccessLevelDTO(id=model_dto.id, name="test", importance=5)]
    repository.delete.assert_called_once_with(id=model_dto.id)


async def test_update_access_level(service: AccessLevelService, repository: AsyncMock) -> None:
    model_dto = AccessLevelPartialDTO(id=2, name="updated_2", importance=20)
    repository.update.return_value = AccessLevelOrm(id=model_dto.id, name=model_dto.name, importance=model_dto.importance)

    result = await service.update(model_dto)

    assert result == [AccessLevelDTO(id=model_dto.id, name=model_dto.name, importance=model_dto.importance)]
    repository.update.assert_called_once_with(id=model_dto.id, name=model_dto.name, importance=model_dto.importance)
