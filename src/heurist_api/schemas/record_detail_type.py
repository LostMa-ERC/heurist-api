from pydantic import BaseModel, computed_field
import re
from datetime import datetime
from typing import Optional, List


class RecordField(BaseModel):

    dty_ID: int
    dty_Name: str
    dty_Type: str
    rst_RecTypeID: int
    rst_RequirementType: str
    rty_ID: int
    rty_Name: str
    rty_OrderInGroup: int
    rty_Description: Optional[str] = None
    rty_TitleMask: Optional[str] = None
    rty_CanonicalTitleMask: Optional[str] = None
    rty_Plural: Optional[str] = None
    rty_Status: str
    rty_OriginatingDBID: int
    rty_NameInOriginatingDB: Optional[str] = None
    rty_IDInOriginatingDB: Optional[int] = None
    rty_NonOwnerVisibility: str
    rty_ShowInLists: bool
    rty_RecTypeGroupID: int
    rty_RecTypeModelIDs: Optional[List[int]] = None
    rty_FlagAsFieldset: Optional[bool] = None
    rty_ReferenceURL: Optional[str] = None
    rty_AlternativeRecEditor: Optional[str] = None
    rty_Type: str
    rty_ShowURLOnEditForm: bool
    rty_ShowDescriptionOnEditForm: bool
    rty_Modified: datetime
    rty_LocallyModified: bool

    @computed_field
    @property
    def fieldname(self) -> str:
        s = self.dty_Name
        # Remove parentheses
        s = re.sub(r"\(.+\)", "", s)
        # Remove non-letters
        s = re.sub(r"\W", "_", s)
        # Remove backslashes
        s = re.sub(r"/", "_", s)
        # Remove spaces
        s = re.sub(r"\s", "_", s)
        # Remove double underscores
        s = re.sub(r"_+", "_", s)
        # Trim underscores
        s = s.strip("_")
        s = s.lower() + f" {self.dty_ID}"
        if self.dty_Type == "resource":
            s += " H-ID"
        return s
