from contextlib import asynccontextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()


# взял из примера в документации
class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._session_factory = async_sessionmaker(self._engine)

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @asynccontextmanager
    async def session(self) -> ...:
        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                logger.exception("Session rollback because of exception")
                session.rollback()
                raise
            finally:
                session.close()
