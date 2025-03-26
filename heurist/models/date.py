from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated

from heurist.converters.date_handler import HeuristDateHandler

PROFILE_MAP = {"0": "flat", "1": "central", "2": "slowStart", "3": "slowFinish"}
DETERMINATION_MAP = {
    "0": "unknown",
    "1": "attested",
    "2": "conjecture",
    "3": "measurement",
}


def parse_date(value) -> datetime:
    return HeuristDateHandler.parse(value)


def parse_profile(value) -> str | None:
    if PROFILE_MAP.get(value):
        return PROFILE_MAP[value]


def parse_determination(value) -> str | None:
    if DETERMINATION_MAP.get(value):
        return DETERMINATION_MAP[value]


HeuristDate = Annotated[datetime, BeforeValidator(parse_date)]
HeuristProfile = Annotated[str, BeforeValidator(parse_profile)]
HeuristDetermination = Annotated[str, BeforeValidator(parse_determination)]


class DateLimit(BaseModel):
    earliest: Optional[HeuristDate] = Field(default=None)
    latest: Optional[HeuristDate] = Field(default=None)
    estProfile: Optional[HeuristProfile] = Field(
        default=None, validation_alias="profile"
    )
    estDetermination: Optional[HeuristDetermination] = Field(
        default=None, validation_alias="determination"
    )


class Timestamp(BaseModel):
    inYear: Optional[HeuristDate] = Field(default=None, alias="in")
    typeTime: Optional[str] = Field(default=None, alias="type")
    circa: Optional[bool] = Field(default=None)


class TemporalObject(BaseModel):
    start: Optional[DateLimit] = Field(default=None)
    end: Optional[DateLimit] = Field(default=None)
    estDetermination: Optional[HeuristDetermination] = Field(
        default=None, validation_alias="determination"
    )
    estProfile: Optional[HeuristProfile] = Field(
        default=None, validation_alias="profile"
    )
    timestamp: Optional[Timestamp] = Field(default=None)
    estMinDate: Optional[HeuristDate] = Field(default=None)
    estMaxDate: Optional[HeuristDate] = Field(default=None)
