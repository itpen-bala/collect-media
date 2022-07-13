from asyncio import current_task
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger

CONN_KWARGS = {
    "pool_size": 5,
    "max_overflow": 5,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo_pool": True,
}


class Database:
    def __init__(
            self,
            db_url: str,
            conn_kwargs: dict[str, Any]
    ):
        self.url = db_url
        self._async_engine = create_async_engine(url=self.url, **conn_kwargs, echo=True)
        self._async_session = async_scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                class_=AsyncSession,
                expire_on_commit=False,
                bind=self._async_engine,
            ),
            scopefunc=current_task,
        )

    async def create_tables(self, base: declarative_base) -> None:
        async with self._async_engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[Session, None]:
        session: Session = self._async_session()
        try:
            yield session
        except Exception as e:
            logger.exception("Session rollback")
            await session.rollback()
            raise e
        finally:
            await session.close()
            await self._async_session.remove()

    async def disconnect(self) -> None:
        logger.info(f"Disconnecting from database: {self.url}")
        await self._async_engine.dispose()
