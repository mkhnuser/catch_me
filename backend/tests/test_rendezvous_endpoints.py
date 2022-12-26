import http
import uuid
import random
from typing import Callable

import pytest
from aiohttp.test_utils import TestClient

from main import create_app
from configuration import Urls, Config
from utils.misc import generate_pseudo_random_string
from utils.validation_models import RendezvousValidationModel


@pytest.fixture
async def client(aiohttp_client: Callable) -> TestClient:
    return await aiohttp_client(await create_app())


@pytest.fixture
async def rendezvous() -> RendezvousValidationModel:
    return RendezvousValidationModel(**{
        'title': generate_pseudo_random_string(
            min_length=Config.RENDEZVOUS_TITLE_MIN_LENGTH.value,
            max_length=Config.RENDEZVOUS_TITLE_MAX_LENGTH.value
        ),
        'description': generate_pseudo_random_string(
            min_length=Config.RENDEZVOUS_DESCRIPTION_MIN_LENGTH.value,
            max_length=Config.RENDEZVOUS_DESCRIPTION_MAX_LENGTH.value
        ),
        'coordinates': {
            'latitude': random.randint(-90, 90),
            'longitude': random.randint(-180, 180)
        }
    })


async def test_rendezvous_retrieval(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    post_response = await client.post(
        Urls.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    post_response_data = await post_response.json()
    post_response_rendezvous_id = str(
        uuid.UUID(post_response_data.pop('id'))
    )

    get_response = await client.get(
        Urls.RENDEZVOUS_RETRIEVAL.value.path.format(
            rendezvous_id=post_response_rendezvous_id
        )
    )
    assert get_response.status == http.HTTPStatus.OK.value
    get_response_data = await get_response.json()
    get_response_rendezvous_id = str(
        uuid.UUID(get_response_data.pop('id'))
    )
    assert get_response_rendezvous_id == post_response_rendezvous_id

    rendezvous_validation_model = RendezvousValidationModel(
        **get_response_data
    )
    for key, value in rendezvous_validation_model:
        assert getattr(rendezvous, key) == value


async def test_rendezvous_creation(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    response = await client.post(
        Urls.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    assert response.status == http.HTTPStatus.OK.value
    response_data = await response.json()
    uuid.UUID(response_data.pop('id'))
    rendezvous_validation_model = RendezvousValidationModel(**response_data)

    for key, value in rendezvous_validation_model:
        assert getattr(rendezvous, key) == value


async def test_redirection_after_rendezvous_creation(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    response = await client.post(
        Urls.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    response_data = await response.json()

    assert response.status == http.HTTPStatus.OK.value
    assert len(response.history) == 1
    assert response.history[-1].status == http.HTTPStatus.FOUND.value
    assert response.url.path == Urls.RENDEZVOUS_RETRIEVAL.value.path.format(
        rendezvous_id=str(uuid.UUID(response_data.pop('id')))
    )


async def test_rendezvous_patching(client: TestClient) -> None:
    response = await client.patch(
        Urls.RENDEZVOUS_UPDATE.value.path.format(
            rendezvous_id=str(uuid.uuid4())
        )
    )
    assert response.status == http.HTTPStatus.OK.value


async def test_rendezvous_deletion(client: TestClient) -> None:
    response = await client.delete(
        Urls.RENDEZVOUS_DELETION.value.path.format(
            rendezvous_id=str(uuid.uuid4())
        )
    )
    assert response.status == http.HTTPStatus.OK.value
