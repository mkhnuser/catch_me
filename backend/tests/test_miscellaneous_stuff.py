import http
from typing import Callable

import pytest
from aiohttp.test_utils import TestClient

from logic.web_app.app import create_app
from logic.web_app.routes import Routes


@pytest.fixture
async def client(aiohttp_client: Callable) -> TestClient:
    return await aiohttp_client(await create_app())


async def test_root(client: TestClient) -> None:
    response = await client.get(Routes.ROOT.value.path)
    assert response.status == http.HTTPStatus.NOT_FOUND.value
