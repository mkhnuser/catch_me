from typing import Optional, Mapping

from sqlalchemy import MetaData, Executable, Result
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.exc import SQLAlchemyError

from .exceptions import DatabaseError


class Database:
    def __init__(self, url: str) -> None:
        self.url = url
        self.engine: Optional[AsyncEngine] = None

    async def init_metadata(self, metadata: MetaData) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    def start(self) -> None:
        self.engine = create_async_engine(self.url)

    async def stop(self) -> None:
        await self.engine.dispose()
        self.engine = None

    async def execute(
        self,
        statement: Executable,
        execution_options: Optional[Mapping] = None,
        **parameters
    ) -> Result:
        try:
            async with self.engine.begin() as connection:
                return await connection.execute(
                    statement,
                    parameters,
                    execution_options=execution_options
                )
        except SQLAlchemyError as e:
            raise DatabaseError from e
