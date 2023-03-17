import uuid

from sqlalchemy import MetaData, Table, Column, String, CheckConstraint, Float
from sqlalchemy.dialects.postgresql import UUID

from ..configuration import Config


metadata = MetaData()

rendezvous_table = Table(
    "rendezvous",
    metadata,
    Column("id", UUID, default=uuid.uuid4, primary_key=True),
    Column(
        "title",
        String(Config.RENDEZVOUS_TITLE_MAX_LENGTH.value),
        CheckConstraint(
            f"{Config.RENDEZVOUS_TITLE_MIN_LENGTH.value} <= char_length(title)"
        ),
        nullable=False,
    ),
    Column(
        "description",
        String(Config.RENDEZVOUS_DESCRIPTION_MAX_LENGTH.value),
        CheckConstraint(
            f"{Config.RENDEZVOUS_DESCRIPTION_MIN_LENGTH.value}"
            " <= char_length(title)"
        )
    ),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
)
