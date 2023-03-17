import http
import uuid
import random
from typing import Callable

import pytest
from aiohttp.test_utils import TestClient

from logic.configuration import Config
from logic.web_app.routes import Routes
from logic.web_app.app import create_app
from logic.utils.misc import generate_pseudo_random_string
from logic.validation.validation_models import (
    RendezvousValidationModel
)


@pytest.fixture
async def client(aiohttp_client: Callable) -> TestClient:
    return await aiohttp_client(await create_app())


@pytest.fixture
async def rendezvous() -> RendezvousValidationModel:
    return RendezvousValidationModel(**{
        "title": generate_pseudo_random_string(
            min_length=Config.RENDEZVOUS_TITLE_MIN_LENGTH.value,
            max_length=Config.RENDEZVOUS_TITLE_MAX_LENGTH.value
        ),
        "description": generate_pseudo_random_string(
            min_length=Config.RENDEZVOUS_DESCRIPTION_MIN_LENGTH.value,
            max_length=Config.RENDEZVOUS_DESCRIPTION_MAX_LENGTH.value
        ),
        "coordinates": {
            "latitude": random.randint(-90, 90),
            "longitude": random.randint(-180, 180)
        }
    })


async def test_rendezvous_retrieval(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    post_response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    post_response_data = await post_response.json()
    post_response_rendezvous_id = str(
        uuid.UUID(post_response_data.pop("id"))
    )

    get_response = await client.get(
        Routes.RENDEZVOUS_RETRIEVAL.value.path.format(
            rendezvous_id=post_response_rendezvous_id
        )
    )
    assert get_response.status == http.HTTPStatus.OK.value
    get_response_data = await get_response.json()
    get_response_rendezvous_id = str(
        uuid.UUID(get_response_data.pop("id"))
    )
    assert get_response_rendezvous_id == post_response_rendezvous_id

    retrieved_rendezvous = RendezvousValidationModel(**get_response_data)
    for key, value in retrieved_rendezvous:
        assert getattr(rendezvous, key) == value


async def test_rendezvous_creation(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    assert response.status == http.HTTPStatus.OK.value
    response_data = await response.json()
    uuid.UUID(response_data.pop("id"))
    created_rendezvous = RendezvousValidationModel(**response_data)

    for key, value in created_rendezvous:
        assert getattr(rendezvous, key) == value


async def test_redirection_after_rendezvous_creation(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    response_data = await response.json()

    assert response.status == http.HTTPStatus.OK.value
    assert len(response.history) == 1
    assert response.history[-1].status == http.HTTPStatus.FOUND.value
    assert response.url.path == Routes.RENDEZVOUS_RETRIEVAL.value.path.format(
        rendezvous_id=str(uuid.UUID(response_data.pop("id")))
    )


# Allow two random rendezvous to be passed as parameters.
rendezvous_update = rendezvous


async def test_rendezvous_update(
    client: TestClient,
    rendezvous: RendezvousValidationModel,
    rendezvous_update: RendezvousValidationModel
) -> None:
    post_response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    post_response_data = await post_response.json()
    created_rendezvous_id = uuid.UUID(post_response_data.pop("id"))

    put_response = await client.put(
        Routes.RENDEZVOUS_UPDATE.value.path.format(
            rendezvous_id=str(created_rendezvous_id)
        ),
        json=rendezvous_update.dict()
    )
    assert put_response.status == http.HTTPStatus.OK.value

    put_response_data = await put_response.json()
    updated_rendezvous_id = uuid.UUID(put_response_data.pop("id"))
    updated_rendezvous = RendezvousValidationModel(**put_response_data)

    assert created_rendezvous_id == updated_rendezvous_id

    for key, value in updated_rendezvous:
        assert getattr(rendezvous_update, key) == value


async def test_rendezvous_deletion(
    client: TestClient,
    rendezvous: RendezvousValidationModel
) -> None:
    post_response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous.dict()
    )
    created_rendezvous_id = uuid.UUID((await post_response.json()).pop("id"))

    delete_response = await client.delete(
        Routes.RENDEZVOUS_DELETION.value.path.format(
            rendezvous_id=str(created_rendezvous_id)
        )
    )

    assert delete_response.status == http.HTTPStatus.OK.value
