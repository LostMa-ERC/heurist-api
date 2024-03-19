from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Field(BaseModel):

    dty_ID: int
    dty_Name: str
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
