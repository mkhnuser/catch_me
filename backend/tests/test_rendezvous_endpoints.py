import http
import uuid
import random
from typing import Callable, Mapping, AsyncGenerator

import pytest
from aiohttp.test_utils import TestClient

from logic.configuration import Config
from logic.web_app.routes import Routes
from logic.web_app.app import create_app
from logic.utils.misc import generate_pseudo_random_string
from logic.validation.validation_models import RendezvousValidationModel
from logic.db.expressions import (
    create_rendezvous_expression,
    delete_rendezvous_expression
)


@pytest.fixture
async def client(aiohttp_client: Callable) -> TestClient:
    return await aiohttp_client(await create_app())


@pytest.fixture
async def rendezvous_validation_model() -> RendezvousValidationModel:
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


@pytest.fixture
async def rendezvous_db_instance(
    client: TestClient,
    rendezvous_validation_model: RendezvousValidationModel
) -> AsyncGenerator[Mapping, None]:
    columns_to_attributes_mapping = (await client.app["db"].execute(
        create_rendezvous_expression,
        rendezvous_title=rendezvous_validation_model.title,
        rendezvous_description=rendezvous_validation_model.description,
        rendezvous_coordinates_latitude=
        rendezvous_validation_model.coordinates.latitude,
        rendezvous_coordinates_longitude=
        rendezvous_validation_model.coordinates.longitude
    )).first()._asdict()
    yield columns_to_attributes_mapping
    await client.app["db"].execute(
        delete_rendezvous_expression,
        rendezvous_id=columns_to_attributes_mapping["id"]
    )


async def test_rendezvous_retrieval(
    client: TestClient,
    rendezvous_db_instance: Mapping
) -> None:
    existing_rendezvous_id = str(rendezvous_db_instance["id"])

    response = await client.get(
        Routes.RENDEZVOUS_RETRIEVAL.value.path.format(
            rendezvous_id=existing_rendezvous_id
        )
    )
    assert response.status == http.HTTPStatus.OK.value
    response_data = await response.json()
    response_rendezvous_id = str(uuid.UUID(response_data.pop("id")))
    assert response_rendezvous_id == existing_rendezvous_id

    RendezvousValidationModel(**response_data)


async def test_rendezvous_creation(
    client: TestClient,
    rendezvous_validation_model: RendezvousValidationModel
) -> None:
    response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous_validation_model.dict()
    )
    assert response.status == http.HTTPStatus.OK.value
    response_data = await response.json()
    uuid.UUID(response_data.pop("id"))
    created_rendezvous = RendezvousValidationModel(**response_data)

    for key, value in created_rendezvous:
        assert getattr(rendezvous_validation_model, key) == value


async def test_redirection_after_rendezvous_creation(
    client: TestClient,
    rendezvous_validation_model: RendezvousValidationModel
) -> None:
    response = await client.post(
        Routes.RENDEZVOUS_CREATION.value.path,
        json=rendezvous_validation_model.dict()
    )
    response_data = await response.json()

    assert response.status == http.HTTPStatus.OK.value
    assert len(response.history) == 1
    assert response.history[-1].status == http.HTTPStatus.FOUND.value
    assert response.url.path == Routes.RENDEZVOUS_RETRIEVAL.value.path.format(
        rendezvous_id=str(uuid.UUID(response_data.pop("id")))
    )


async def test_rendezvous_update(
    client: TestClient,
    rendezvous_validation_model: RendezvousValidationModel,
    rendezvous_db_instance: Mapping
) -> None:
    existing_rendezvous_id = str(rendezvous_db_instance["id"])

    response = await client.put(
        Routes.RENDEZVOUS_UPDATE.value.path.format(
            rendezvous_id=existing_rendezvous_id
        ),
        json=rendezvous_validation_model.dict()
    )
    assert response.status == http.HTTPStatus.OK.value

    response_data = await response.json()
    updated_rendezvous_id = str(uuid.UUID(response_data.pop("id")))
    updated_rendezvous = RendezvousValidationModel(**response_data)

    assert existing_rendezvous_id == updated_rendezvous_id

    for key, value in updated_rendezvous:
        assert getattr(rendezvous_validation_model, key) == value


async def test_rendezvous_deletion(
    client: TestClient,
    rendezvous_db_instance: Mapping
) -> None:
    existing_rendezvous_id = str(rendezvous_db_instance["id"])

    response = await client.delete(
        Routes.RENDEZVOUS_DELETION.value.path.format(
            rendezvous_id=existing_rendezvous_id
        )
    )
    assert response.status == http.HTTPStatus.OK.value
