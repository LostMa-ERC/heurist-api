from typing import Optional

from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


def convert_duckdb_json(d: dict) -> dict:
    return {k: v for k, v in zip(d["key"], d["value"])}


def convert_vocab_dict(v: dict | None) -> list:
    l = []
    if v:
        d = convert_duckdb_json(v)
        for k, v in d.items():
            nd = {"label": k} | v
            l.append(nd)
    return l


VocabTerms = Annotated[list, BeforeValidator(convert_vocab_dict)]


class DTY(BaseModel):
    rst_DisplayName: str
    rst_DisplayHelpText: str
    dty_ID: int
    dty_Type: str
    dty_SemanticReferenceURL: Optional[str]
    trm_TreeID: Optional[int]
    trm_Label: Optional[str]
    trm_Description: Optional[str]
    vocabTerms: Optional[VocabTerms]


class RTY(BaseModel):
    rty_ID: int
    rty_Name: str
    rty_Description: str
    rty_TitleMask: str
    rty_ReferenceURL: Optional[str]
