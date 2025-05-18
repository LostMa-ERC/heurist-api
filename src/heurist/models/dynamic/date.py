from datetime import datetime
from typing import Annotated, Optional

from heurist.validators import parse_heurist_date
from pydantic import BaseModel, BeforeValidator, Field

PROFILE_MAP = {"0": "flat", "1": "central", "2": "slowStart", "3": "slowFinish"}
DETERMINATION_MAP = {
    "0": "unknown",
    "1": "attested",
    "2": "conjecture",
    "3": "measurement",
}


def parse_profile(value) -> str | None:
    if PROFILE_MAP.get(value):
        return PROFILE_MAP[value]


def parse_determination(value) -> str | None:
    if DETERMINATION_MAP.get(value):
        return DETERMINATION_MAP[value]


HeuristDate = Annotated[datetime, BeforeValidator(parse_heurist_date)]
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
    circa: Optional[bool] = Field(default=False)


class TemporalObject(BaseModel):
    comment: Optional[str] = Field(default=None)
    value: Optional[HeuristDate] = Field(default=None)
    start: Optional[DateLimit] = Field(default=DateLimit(**{}))
    end: Optional[DateLimit] = Field(default=DateLimit(**{}))
    estDetermination: Optional[HeuristDetermination] = Field(
        default=None, validation_alias="determination"
    )
    estProfile: Optional[HeuristProfile] = Field(
        default=None, validation_alias="profile"
    )
    timestamp: Optional[Timestamp] = Field(default=Timestamp(**{}))
    estMinDate: Optional[HeuristDate] = Field(default=None)
    estMaxDate: Optional[HeuristDate] = Field(default=None)
