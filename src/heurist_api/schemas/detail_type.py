from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional
import re


def split_arg(input) -> List:
    f = []
    if isinstance(input, str):
        s = re.sub(r"\\\"", "", input)
        l = re.sub("[\[|\]]", "", s)
        g = l.split(",")
        for i in g:
            if i == "":
                i = None
            f.append(i)
    return f


class DetailType(BaseModel):
    dty_ID: int
    dty_Name: str
    dty_Documentation: Optional[str] = None
    dty_Type: str
    dty_HelpText: Optional[str] = None
    dty_ExtendedDescription: Optional[str] = None
    dty_EntryMask: Optional[str] = None
    dty_Status: str
    dty_OriginatingDBID: int
    dty_NameInOriginatingDB: Optional[str] = None
    dty_IDInOriginatingDB: int
    dty_DetailTypeGroupID: int
    dty_OrderInGroup: int
    dty_JsonTermIDTree: Optional[int] = None
    dty_TermIDTreeNonSelectableIDs: List[Optional[int]] = []
    dty_PtrTargetRectypeIDs: List[Optional[int]] = []
    dty_FieldSetRectypeID: Optional[int] = None
    dty_ShowInLists: bool
    dty_NonOwnerVisibility: str
    dty_Modified: datetime
    dty_LocallyModified: bool
    dty_SemanticReferenceURL: Optional[str] = None

    @field_validator("dty_TermIDTreeNonSelectableIDs", mode="before")
    @classmethod
    def validate_selectable_ids(cls, raw: str | None) -> List:
        return split_arg(raw)

    @field_validator("dty_PtrTargetRectypeIDs", mode="before")
    @classmethod
    def validate_rectype_ids(cls, raw: str | None) -> List:
        return split_arg(raw)
