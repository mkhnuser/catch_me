import uuid
from typing import Optional

import asyncpg

from utils.validation_models import RendezvousValidationModel


async def retrieve_rendezvous(
    db_connection_pool: asyncpg.Pool,
    rendezvous_identifier: uuid.UUID
) -> Optional[asyncpg.Record]:
    async with db_connection_pool.acquire() as connection:
        return await connection.fetchrow(
            """
            SELECT id, title, description, latitude, longitude FROM rendezvous
            WHERE rendezvous.id = $1
            """,
            str(rendezvous_identifier)
        )


async def create_rendezvous(
    db_connection_pool: asyncpg.Pool,
    rendezvous: RendezvousValidationModel
) -> asyncpg.Record:
    async with db_connection_pool.acquire() as connection:
        return await connection.fetchrow(
            """
            INSERT INTO rendezvous(title, description, latitude, longitude)
            VALUES($1, $2, $3, $4) RETURNING *;
            """,
            rendezvous.title,
            rendezvous.description,
            rendezvous.coordinates.latitude,
            rendezvous.coordinates.longitude
        )
