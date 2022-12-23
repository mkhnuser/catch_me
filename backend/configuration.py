import enum


class Urls(enum.Enum):
    ROOT = '/api/v1'
    RENDEZVOUS_RETRIEVAL = ROOT + '/rendezvous/{uuid}'
    RENDEZVOUS_CREATION = ROOT + '/rendezvous/'
    RENDEZVOUS_PATCHING = ROOT + '/rendezvous/{uuid}'
    RENDEZVOUS_DELETION = ROOT + '/rendezvous/{uuid}'
