from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from pedant_killer.config import config

database_logger = logging.getLogger('database')
logging.basicConfig(
    filename='pedant_killer.log',
    format='%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
database_logger.propagate = True

# async_engine = create_async_engine(
#     url=config.database_url_asyncpg,
#     echo=False
# )

# async_session_factory = async_sessionmaker(async_engine)


# def connection(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
#     async def wrapper(*args, **kwargs):
#         if len(args) > 0 and hasattr(args[0], "__class__"):
#             self_or_cls = args[0]
#         else:
#             self_or_cls = None
#
#         async with async_session_factory() as session:
#             if self_or_cls:
#                 return await func(self_or_cls, session, *args[1:], **kwargs)
#             else:
#                 return await func(session, *args, **kwargs)
#
#     # Копируем имя, документацию и аннотации
#     wrapper.__name__ = func.__name__
#     wrapper.__doc__ = func.__doc__
#
#     return wrapper


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        cols = [f'{col}={getattr(self, col)}' for col in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__} {','.join(cols)}>'


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._session_factory = async_sessionmaker(self._engine)

    @asynccontextmanager
    async def session(self) -> AsyncIterator:
        async with self._session_factory() as session:
            try:
                yield session

            except Exception:
                await session.rollback()
                raise

            finally:
                await session.close()
