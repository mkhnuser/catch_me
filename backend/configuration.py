import os
import enum
from typing import NamedTuple


class Url(NamedTuple):
    path: str
    pseudonym: str


class Urls(enum.Enum):
    ROOT = Url(path='/api/v1', pseudonym='root')
    RENDEZVOUS_RETRIEVAL = Url(
        path='/api/v1/rendezvous/{rendezvous_id}',
        pseudonym='rendezvous-retrieval'
    )
    RENDEZVOUS_CREATION = Url(
        path='/api/v1/rendezvous',
        pseudonym='rendezvous-creation'
    )
    RENDEZVOUS_UPDATE = Url(
        path='/api/v1/rendezvous/{rendezvous_id}',
        pseudonym='rendezvous-update'
    )
    RENDEZVOUS_DELETION = Url(
        path='/api/v1/rendezvous/{rendezvous_id}',
        pseudonym='rendezvous-deletion'
    )


class Config(enum.Enum):
    RENDEZVOUS_TITLE_MIN_LENGTH = int(
        os.environ['RENDEZVOUS_TITLE_MIN_LENGTH']
    )
    RENDEZVOUS_TITLE_MAX_LENGTH = int(
        os.environ['RENDEZVOUS_TITLE_MAX_LENGTH']
    )
    RENDEZVOUS_DESCRIPTION_MIN_LENGTH = int(
        os.environ['RENDEZVOUS_DESCRIPTION_MIN_LENGTH']
    )
    RENDEZVOUS_DESCRIPTION_MAX_LENGTH = int(
        os.environ['RENDEZVOUS_DESCRIPTION_MAX_LENGTH']
    )
    LATITUDE_MIN_VALUE = int(os.environ['LATITUDE_MIN_VALUE'])
    LATITUDE_MAX_VALUE = int(os.environ['LATITUDE_MAX_VALUE'])
    LONGITUDE_MIN_VALUE = int(os.environ['LONGITUDE_MIN_VALUE'])
    LONGITUDE_MAX_VALUE = int(os.environ['LONGITUDE_MAX_VALUE'])
    DATABASE_URL = os.environ['DATABASE_URL']
    DB_CONNECTION_POOL_CLOSURE_TIMEOUT = int(
        os.environ['DB_CONNECTION_POOL_CLOSURE_TIMEOUT']
    )
