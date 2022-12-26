import uuid
import json

from aiohttp import web
from pydantic import ValidationError

from configuration import Urls
from utils.db import retrieve_rendezvous, create_rendezvous
from utils.validation_models import RendezvousValidationModel
from utils.misc import create_rendezvous_retrieval_json_payload


async def handle_rendezvous_creation(request: web.Request) -> web.Response:
    try:
        rendezvous_validation_model = RendezvousValidationModel(
            **(await request.json())
        )
    except (json.JSONDecodeError, ValidationError):
        raise web.HTTPBadRequest()

    try:
        record = await create_rendezvous(
            request.app['db_connection_pool'],
            rendezvous_validation_model
        )
    except Exception:
        raise web.HTTPInternalServerError()

    raise web.HTTPFound(
        request.app.router[Urls.RENDEZVOUS_RETRIEVAL.value.pseudonym].url_for(
            rendezvous_id=str(record['id'])
        )
    )


async def handle_rendezvous_update(request: web.Request) -> web.Response:
    try:
        rendezvous_id = uuid.UUID(request.match_info['rendezvous_id'])
    except ValueError:
        raise web.HTTPBadRequest()
    return web.json_response({'success': str(rendezvous_id)})


async def handle_rendezvous_retrieval(request: web.Request) -> web.Response:
    try:
        rendezvous_id = uuid.UUID(request.match_info['rendezvous_id'])
    except ValueError:
        raise web.HTTPBadRequest()

    try:
        record = await retrieve_rendezvous(
            request.app['db_connection_pool'],
            rendezvous_id
        )
    except Exception:
        raise web.HTTPInternalServerError()

    if record is None:
        raise web.HTTPBadRequest()

    return web.json_response(create_rendezvous_retrieval_json_payload(record))


async def handle_rendezvous_deletion(request: web.Request) -> web.Response:
    try:
        rendezvous_id = uuid.UUID(request.match_info['rendezvous_id'])
    except ValueError:
        raise web.HTTPBadRequest()
    return web.json_response({'success': str(rendezvous_id)})
