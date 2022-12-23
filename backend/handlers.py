import uuid

from aiohttp import web


async def create_rendezvous(request: web.Request) -> web.Response:
    return web.json_response({'success': True})


async def update_rendezvous(request: web.Request) -> web.Response:
    try:
        rendezvous_identifier = uuid.UUID(request.match_info['uuid'])
    except ValueError:
        raise web.HTTPBadRequest()
    return web.json_response({'success': str(rendezvous_identifier)})


async def retrieve_rendezvous(request: web.Request) -> web.Response:
    try:
        rendezvous_identifier = uuid.UUID(request.match_info['uuid'])
    except ValueError:
        raise web.HTTPBadRequest()
    return web.json_response({'success': str(rendezvous_identifier)})


async def delete_rendezvous(request: web.Request) -> web.Response:
    try:
        rendezvous_identifier = uuid.UUID(request.match_info['uuid'])
    except ValueError:
        raise web.HTTPBadRequest()
    return web.json_response({'success': str(rendezvous_identifier)})
