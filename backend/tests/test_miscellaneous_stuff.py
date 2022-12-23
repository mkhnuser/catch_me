import http
from typing import Callable

import pytest
from aiohttp.test_utils import TestClient

from main import create_app
from configuration import Urls


@pytest.fixture
async def client(aiohttp_client: Callable) -> TestClient:
    return await aiohttp_client(await create_app())


async def test_root(client: TestClient) -> None:
    response = await client.get(Urls.ROOT.value)
    assert response.status == http.HTTPStatus.NOT_FOUND.value
