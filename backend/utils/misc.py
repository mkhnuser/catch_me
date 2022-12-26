import random
import string
import asyncpg
from typing import Mapping, Union


def generate_pseudo_random_string(
    min_length: int,
    max_length: int
) -> str:
    return ''.join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(min_length, max_length))
    )


def create_rendezvous_retrieval_json_payload(
    record: asyncpg.Record
) -> Mapping[str, Union[int, float, str, None]]:
    payload = dict(record)
    payload['id'] = str(payload['id'])
    payload['coordinates'] = {
        'latitude': payload.pop('latitude'),
        'longitude': payload.pop('longitude')
    }
    return payload
