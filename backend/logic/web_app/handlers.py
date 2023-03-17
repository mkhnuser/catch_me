import uuid
import json

from aiohttp import web
from pydantic import ValidationError

from .routes import Routes
from ..db.expressions import (
    retrieve_rendezvous_expression,
    create_rendezvous_expression,
    update_rendezvous_expression,
    delete_rendezvous_expression
)
from ..db.exceptions import DatabaseError
from ..validation.validation_models import RendezvousValidationModel
from ..utils.misc import create_rendezvous_json


async def handle_rendezvous_creation(request: web.Request) -> web.Response:
    try:
        rendezvous = RendezvousValidationModel(
            **(await request.json())
        )
    except (json.JSONDecodeError, ValidationError):
        raise web.HTTPBadRequest()

    try:
        row = (await request.app["db"].execute(
            create_rendezvous_expression,
            rendezvous_title=rendezvous.title,
            rendezvous_description=rendezvous.description,
            rendezvous_coordinates_latitude=rendezvous.coordinates.latitude,
            rendezvous_coordinates_longitude=rendezvous.coordinates.longitude
        )).first()
    except DatabaseError:
        raise web.HTTPInternalServerError()

    raise web.HTTPFound(
        request
        .app
        .router[Routes.RENDEZVOUS_RETRIEVAL.value.pseudonym]
        .url_for(rendezvous_id=str(row._asdict()["id"]))
    )


async def handle_rendezvous_update(request: web.Request) -> web.Response:
    try:
        rendezvous_id = uuid.UUID(request.match_info["rendezvous_id"])
        rendezvous = RendezvousValidationModel(
            **(await request.json())
        )
    except (ValueError, json.JSONDecodeError, ValidationError):
        raise web.HTTPBadRequest()

    try:
        row = (await request.app["db"].execute(
            update_rendezvous_expression,
            rendezvous_id=rendezvous_id,
            rendezvous_title=rendezvous.title,
            rendezvous_description=rendezvous.description,
            rendezvous_coordinates_latitude=rendezvous.coordinates.latitude,
            rendezvous_coordinates_longitude=rendezvous.coordinates.longitude
        )).first()
    except DatabaseError:
        raise web.HTTPInternalServerError()

    if row is None:
        raise web.HTTPBadRequest()

    return web.json_response(create_rendezvous_json(row._asdict()))


async def handle_rendezvous_retrieval(request: web.Request) -> web.Response:
    try:
        rendezvous_id = uuid.UUID(request.match_info["rendezvous_id"])
    except ValueError:
        raise web.HTTPBadRequest()

    try:
        row = (await request.app["db"].execute(
            retrieve_rendezvous_expression,
            rendezvous_id=rendezvous_id
        )).first()
    except DatabaseError:
        raise web.HTTPInternalServerError()

    if row is None:
        raise web.HTTPBadRequest()

    return web.json_response(create_rendezvous_json(row._asdict()))


async def handle_rendezvous_deletion(request: web.Request) -> web.Response:
    try:
        rendezvous_id = uuid.UUID(request.match_info["rendezvous_id"])
    except ValueError:
        raise web.HTTPBadRequest()

    try:
        row = (await request.app["db"].execute(
            delete_rendezvous_expression,
            rendezvous_id=rendezvous_id
        )).first()
    except DatabaseError:
        raise web.HTTPInternalServerError()

    if row is None:
        raise web.HTTPBadRequest()

    return web.Response()
