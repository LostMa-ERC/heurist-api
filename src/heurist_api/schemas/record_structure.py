from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RecordStructure(BaseModel):
    rst_CalcFieldMask: Optional[str] = None
    rst_CalcFunctionID: Optional[int] = None
    rst_CreateChildIfRecPtr: bool
    rst_DefaultValue: Optional[str] = None
    rst_DetailTypeID: int
    rst_DisplayDetailTypeGroupID: Optional[int] = None
    rst_DisplayExtendedDescription: Optional[str] = None
    rst_DisplayHeight: Optional[int] = None
    rst_DisplayHelpText: Optional[str] = None
    rst_DisplayName: str
    rst_DisplayOrder: int
    rst_DisplayWidth: int
    rst_EntryMask: Optional[str] = None
    rst_FilteredJsonTermIDTree: Optional[str] = None
    rst_ID: int
    rst_IDInOriginatingDB: Optional[int] = None
    rst_InitialRepeats: int
    rst_LocallyModified: int
    rst_MaxValues: int
    rst_MayModify: str
    rst_MinValues: int
    rst_Modified: datetime
    rst_NonOwnerVisibility: str
    rst_NumericLargestValueUsed: Optional[int] = None
    rst_OrderForThumbnailGeneration: Optional[int] = None
    rst_OriginatingDBID: int
    rst_PointerBrowseFilter: Optional[str] = None
    rst_PointerMode: str
    rst_PtrFilteredIDs: Optional[List[int]] = None
    rst_RecTypeID: int
    rst_RecordMatchOrder: int
    rst_RequirementType: str
    rst_SemanticReferenceURL: Optional[str] = None
    rst_ShowDetailAnnotation: bool
    rst_ShowDetailCertainty: bool
    rst_Status: str
    rst_TermIDTreeNonSelectableIDs: Optional[List[str]] = None
    rst_TermsAsButtons: bool
