from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional


class RelationshipMarker(BaseModel):

    rec_ID: int
    rec_RecTypeID: int
    rec_Title: str
    rec_URL: Optional[str]
    rec_ScratchPad: Optional[str]
    rec_OwnerUGrpID: int
    rec_NonOwnerVisibility: str
    rec_URLLastVerified: Optional[str]
    rec_URLErrorMessage: Optional[str]
    rec_Added: datetime
    rec_Modified: datetime
    rec_AddedByUGrpID: int
    rec_Hash: Optional[str]
    rec_FlagTemporary: int
    rec_RecTypeName: str
    rec_RecTypeConceptID: str
    source_record_id: int
    source_record_name: str
    source_record_type: int
    target_record_id: int
    target_record_name: str
    target_record_type: int
    relationship_term_label: str

    @model_validator(mode="before")
    @classmethod
    def parse_details(cls, data: dict) -> dict:
        d = data.pop("details")
        details = {detail["fieldName"]: detail for detail in d}
        source, target, relationship = (
            details["Source record"]["value"],
            details["Target record"]["value"],
            details["Relationship type"],
        )
        data.update(
            {
                "source_record_id": source["id"],
                "source_record_name": source["title"],
                "source_record_type": source["type"],
                "target_record_id": target["id"],
                "target_record_name": target["title"],
                "target_record_type": target["type"],
                "relationship_term_label": relationship["termLabel"],
            }
        )
        return data
