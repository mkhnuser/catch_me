import enum
from typing import NamedTuple


class Route(NamedTuple):
    path: str
    pseudonym: str


class Routes(enum.Enum):
    ROOT = Route(path="/api/v1", pseudonym="root")
    RENDEZVOUS_RETRIEVAL = Route(
        path="/api/v1/rendezvous/{rendezvous_id}",
        pseudonym="rendezvous-retrieval"
    )
    RENDEZVOUS_CREATION = Route(
        path="/api/v1/rendezvous",
        pseudonym="rendezvous-creation"
    )
    RENDEZVOUS_UPDATE = Route(
        path="/api/v1/rendezvous/{rendezvous_id}",
        pseudonym="rendezvous-update"
    )
    RENDEZVOUS_DELETION = Route(
        path="/api/v1/rendezvous/{rendezvous_id}",
        pseudonym="rendezvous-deletion"
    )
