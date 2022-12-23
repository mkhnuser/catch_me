import http
import uuid
import string
from typing import Callable

import pytest
from aiohttp.test_utils import TestClient

from main import create_app
from configuration import Urls


@pytest.fixture
async def client(aiohttp_client: Callable) -> TestClient:
    return await aiohttp_client(await create_app())


async def test_rendezvous_retrieval(client: TestClient) -> None:
    UUID = str(uuid.uuid4())

    response = await client.get(
        Urls.RENDEZVOUS_RETRIEVAL.value.format(uuid=UUID)
    )
    assert response.status == http.HTTPStatus.OK.value


async def test_rendezvous_creation(client: TestClient) -> None:
    response = await client.post(Urls.RENDEZVOUS_CREATION.value)
    assert response.status == http.HTTPStatus.OK.value


async def test_rendezvous_patching(client: TestClient) -> None:
    UUID = str(uuid.uuid4())

    response = await client.patch(
        Urls.RENDEZVOUS_PATCHING.value.format(uuid=UUID)
    )
    assert response.status == http.HTTPStatus.OK.value


async def test_rendezvous_deletion(client: TestClient) -> None:
    UUID = str(uuid.uuid4())

    response = await client.delete(
        Urls.RENDEZVOUS_DELETION.value.format(uuid=UUID)
    )
    assert response.status == http.HTTPStatus.OK.value


async def test_rendezvous_retrieval_sending_invalid_uuid(
    client: TestClient
) -> None:
    INVALID_UUID = string.ascii_letters

    response = await client.get(
        Urls.RENDEZVOUS_RETRIEVAL.value.format(uuid=INVALID_UUID)
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST.value


async def test_rendezvous_patching_sending_invalid_uuid(
    client: TestClient
) -> None:
    INVALID_UUID = string.ascii_letters

    response = await client.patch(
        Urls.RENDEZVOUS_PATCHING.value.format(uuid=INVALID_UUID)
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST.value


async def test_rendezvous_deletion_sending_invalid_uuid(
    client: TestClient
) -> None:
    INVALID_UUID = string.ascii_letters

    response = await client.delete(
        Urls.RENDEZVOUS_DELETION.value.format(uuid=INVALID_UUID)
    )
    assert response.status == http.HTTPStatus.BAD_REQUEST.value
