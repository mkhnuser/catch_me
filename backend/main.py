from aiohttp import web

import handlers
from configuration import Urls


def configure_app(app: web.Application) -> None:
    app.add_routes((
        web.get(Urls.RENDEZVOUS_RETRIEVAL.value, handlers.retrieve_rendezvous),
        web.post(Urls.RENDEZVOUS_CREATION.value, handlers.create_rendezvous),
        web.patch(Urls.RENDEZVOUS_PATCHING.value, handlers.update_rendezvous),
        web.delete(Urls.RENDEZVOUS_DELETION.value, handlers.delete_rendezvous)
    ))


async def create_app() -> web.Application:
    app = web.Application()
    configure_app(app)
    return app
