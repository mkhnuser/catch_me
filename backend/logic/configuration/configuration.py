import os
import enum


class Config(enum.Enum):
    RENDEZVOUS_TITLE_MIN_LENGTH = int(
        os.environ["RENDEZVOUS_TITLE_MIN_LENGTH"]
    )
    RENDEZVOUS_TITLE_MAX_LENGTH = int(
        os.environ["RENDEZVOUS_TITLE_MAX_LENGTH"]
    )
    RENDEZVOUS_DESCRIPTION_MIN_LENGTH = int(
        os.environ["RENDEZVOUS_DESCRIPTION_MIN_LENGTH"]
    )
    RENDEZVOUS_DESCRIPTION_MAX_LENGTH = int(
        os.environ["RENDEZVOUS_DESCRIPTION_MAX_LENGTH"]
    )
    LATITUDE_MIN_VALUE = int(os.environ["LATITUDE_MIN_VALUE"])
    LATITUDE_MAX_VALUE = int(os.environ["LATITUDE_MAX_VALUE"])
    LONGITUDE_MIN_VALUE = int(os.environ["LONGITUDE_MIN_VALUE"])
    LONGITUDE_MAX_VALUE = int(os.environ["LONGITUDE_MAX_VALUE"])
    DATABASE_URL = os.environ["DATABASE_URL"]
    DB_CLOSE_TIMEOUT = int(os.environ["DB_CLOSE_TIMEOUT"])
