import pytest
from unittest.mock import AsyncMock
from pedant_killer.database.repository.core_repository import CoreRepository


@pytest.fixture
def session_mock():
    mock_ = AsyncMock(spec=CoreRepository)
