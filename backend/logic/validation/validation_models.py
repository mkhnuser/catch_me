from typing import Optional

from pydantic import BaseModel, constr, confloat, Extra

from ..configuration import Config


class CoordinatesValidationModel(BaseModel):
    latitude: confloat(
        ge=Config.LATITUDE_MIN_VALUE.value,
        le=Config.LATITUDE_MAX_VALUE.value,
        allow_inf_nan=False
    )
    longitude: confloat(
        ge=Config.LONGITUDE_MIN_VALUE.value,
        le=Config.LONGITUDE_MAX_VALUE.value,
        allow_inf_nan=False
    )

    class Config:
        extra = Extra.forbid


class RendezvousValidationModel(BaseModel):
    title: constr(
        min_length=Config.RENDEZVOUS_TITLE_MIN_LENGTH.value,
        max_length=Config.RENDEZVOUS_TITLE_MAX_LENGTH.value,
        strip_whitespace=True
    )
    description: Optional[constr(
        min_length=Config.RENDEZVOUS_DESCRIPTION_MIN_LENGTH.value,
        max_length=Config.RENDEZVOUS_DESCRIPTION_MAX_LENGTH.value,
        strip_whitespace=True
    )]
    coordinates: CoordinatesValidationModel

    class Config:
        extra = Extra.forbid
