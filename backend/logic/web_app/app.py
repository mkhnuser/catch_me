import asyncio
from typing import AsyncGenerator

from aiohttp import web

from . import handlers
from .routes import Routes
from ..db.database import Database
from ..db.metadata import metadata
from ..configuration import Config


def add_routes(app: web.Application) -> None:
    app.add_routes((
        web.get(
            Routes.RENDEZVOUS_RETRIEVAL.value.path,
            handlers.handle_rendezvous_retrieval,
            name=Routes.RENDEZVOUS_RETRIEVAL.value.pseudonym
        ),
        web.post(
            Routes.RENDEZVOUS_CREATION.value.path,
            handlers.handle_rendezvous_creation,
            name=Routes.RENDEZVOUS_CREATION.value.pseudonym
        ),
        web.put(
            Routes.RENDEZVOUS_UPDATE.value.path,
            handlers.handle_rendezvous_update,
            name=Routes.RENDEZVOUS_UPDATE.value.pseudonym
        ),
        web.delete(
            Routes.RENDEZVOUS_DELETION.value.path,
            handlers.handle_rendezvous_deletion,
            name=Routes.RENDEZVOUS_DELETION.value.pseudonym
        )
    ))


async def add_cleanup_context(app: web.Application) -> AsyncGenerator:
    app["db"] = Database(Config.DATABASE_URL.value)
    app["db"].start()
    await app["db"].init_metadata(metadata)
    yield
    await asyncio.wait_for(
        app["db"].stop(),
        timeout=Config.DB_CLOSE_TIMEOUT.value
    )


def configure_app(app: web.Application) -> None:
    add_routes(app)
    app.cleanup_ctx.append(add_cleanup_context)


async def create_app() -> web.Application:
    app = web.Application()
    configure_app(app)
    return app
