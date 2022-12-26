import asyncio
from typing import AsyncGenerator

import asyncpg
from aiohttp import web

import handlers
from configuration import Urls, Config


def add_routes(app: web.Application) -> None:
    app.add_routes((
        web.get(
            Urls.RENDEZVOUS_RETRIEVAL.value.path,
            handlers.handle_rendezvous_retrieval,
            name=Urls.RENDEZVOUS_RETRIEVAL.value.pseudonym
        ),
        web.post(
            Urls.RENDEZVOUS_CREATION.value.path,
            handlers.handle_rendezvous_creation,
            name=Urls.RENDEZVOUS_CREATION.value.pseudonym
        ),
        web.patch(
            Urls.RENDEZVOUS_UPDATE.value.path,
            handlers.handle_rendezvous_update,
            name=Urls.RENDEZVOUS_UPDATE.value.pseudonym
        ),
        web.delete(
            Urls.RENDEZVOUS_DELETION.value.path,
            handlers.handle_rendezvous_deletion,
            name=Urls.RENDEZVOUS_DELETION.value.pseudonym
        )
    ))


async def add_cleanup_context(
    app: web.Application
) -> AsyncGenerator[None, None]:
    app['db_connection_pool'] = await asyncpg.create_pool(
        Config.DATABASE_URL.value
    )
    yield
    await asyncio.wait_for(
        app['db_connection_pool'].close(),
        timeout=Config.DB_CONNECTION_POOL_CLOSURE_TIMEOUT.value
    )


def configure_app(app: web.Application) -> None:
    add_routes(app)
    app.cleanup_ctx.append(add_cleanup_context)


async def create_app() -> web.Application:
    app = web.Application()
    configure_app(app)
    return app
