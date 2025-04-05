from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

database_logger = logging.getLogger("database_logger")


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        cols = [f'{col}={getattr(self, col)}' for col in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__} {','.join(cols)}>'


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._session_factory = async_sessionmaker(self._engine)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session

            except Exception:
                await session.rollback()
                raise

            finally:
                await session.close()
