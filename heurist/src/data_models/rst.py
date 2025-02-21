from datetime import datetime
from typing import Literal, Optional

from pydantic_xml import BaseXmlModel, element


class RST(BaseXmlModel, tag="rst", search_mode="unordered"):
    """Dataclass to model one of the database's Record Structures. Record Structures
        are the fields of a Record Type.

    When possible, the attribute descriptions are taken from Heurist's source code.

    Attributes:
        rst_ID (int): Primary key for the record structures table
        rst_RecTypeID (int): The record type to which this detail is allocated, \
            0 = all rectypes
        rst_DetailTypeID (int): Detail type for this field or, if MSB set, \
            FieldSet code + 32767
        rst_DisplayName (str): Display name for this dtl type in this rectype, \
            autofill with dty_Name
        rst_DisplayHelpText (Optional[str]): The user help text to be displayed for \
            this detail type for this record type
        rst_DisplayExtendedDescription (Optional[str]): The rollover text to be \
            displayed for this detail type for this record type
        rst_DisplayOrder (int): A sort order for display of this detail type in the \
            record edit form
        rst_DisplayWidth (int): The field width displayed for this detail type in \
            this record type
        rst_DisplayHeight (int): The field height for this detail type in this record \
            type, only relevant for memo fields
        rst_DefaultValue (Optional[str]): The default value for this detail type for \
            this record type
        rst_RecordMatchOrder (int): Indicates order of significance in detecting \
            duplicate records, 1 = highest
        rst_CalcFunctionID (Optional[int]): FK to table of function specifications for \
            calculating string values
        rst_CalcFieldMask (Optional[str]): A mask string along the lines of the title \
            mask allowing a composite field to be generated from other fields in the \
            record
        rst_RequirementType (Literal["required", "recommended", "optional", \
            "forbidden"]):
        rst_NonOwnerVisibility (Literal["hidden", "viewable", "public", "pending"]): \
            Allows restriction of visibility of a particular field in a specified \
            record type
        rst_Status (Literal["reserved", "approved", "pending", "open"]): Reserved \
            Heurist codes, approved/pending by ''Board'', and user additions
        rst_MayModify (Literal["locked", "discouraged", "open"]): Extent to which \
            detail may be modified within this record structure
        rst_OriginatingDBID (int): Database where this record structure element \
            originated, 0 = locally
        rst_IDInOriginatingDB (Optional[int]): ID used in database where this record \
            structure element originated
        rst_MaxValues (int): Maximum number of values per record for this detail, 1 - \
            single, >1 limited, NULL or 0 = no limit
        rst_MinValues (int): If required, minimum number of values per record for this \
            detail
        rst_InitialRepeats (int): Number of repeat values to be displayed for this \
            field when a new record is first displayed
        rst_DisplayDetailTypeGroupID (Optional[int]): If set, places detail in \
            specified group instead of according to dty_DetailTypeGroup
        rst_FilteredJsonTermIDTree (Optional[str]): JSON encoded tree of allowed \
            terms, subset of those defined in defDetailType. This field is no \
            longer used
        rst_PtrFilteredIDs (Optional[str]): Allowed Rectypes (CSV) within list defined \
            by defDetailType (for pointer details) This field is no longer used
        rst_CreateChildIfRecPtr (bool): For pointer fields, flags that new records \
            created from this field should be marked as children of the creating record
        rst_PointerMode (Literal["dropdown_add", "dropdown", "addorbrowse", "addonly", \
            "browseonly"]): When adding record pointer values, default or null = show \
            both add and browse, otherwise only allow add or only allow \
            browse-for-existing
        rst_PointerBrowseFilter (Optional[str]): When adding record pointer values, \
            defines a Heurist filter to restrict the list of target records browsed
        rst_OrderForThumbnailGeneration (Optional[str]): Priority order of fields to \
            use in generating thumbnail, null = do not use
        rst_TermIDTreeNonSelectableIDs (Optional[str]): Term IDs to use as \
            non-selectable headers for this field
        rst_ShowDetailCertainty (bool): When editing the field, allow editng of the \
            dtl_Certainty value (off by default)
        rst_ShowDetailAnnotation (bool): When editing the field, allow editng of the \
            dtl_Annotation value (off by default)
        rst_NumericLargestValueUsed (Optional[int]): For numeric fields, Null = \
            no auto increment, 0 or more indicates largest value used so far. \
            Set to 0 to switch on incrementing
        rst_EntryMask (Optional[str]): Data entry mask, use to control decimals on \
            numeric values, content of text fields etc. for this record type - future \
            implementation Aug 2017
        rst_Modified (datetime): Date of last modification of this record, used to get \
            last updated date for table
        rst_LocallyModified (int): Flags a definition element which has been modified \
            relative to the original source
        rst_SemanticReferenceURL (Optional[str]): The URI to a semantic definition or \
            web page describing this field used within this record type
        rst_TermsAsButtons (bool): If 1, term list fields are represented as buttons \
            (if single value) or checkboxes (if repeat values)
    """

    rst_ID: int = element()
    rst_RecTypeID: int = element()
    rst_DetailTypeID: int = element()
    rst_DisplayName: str = element()
    rst_DisplayHelpText: Optional[str] = element(default=None)
    rst_DisplayExtendedDescription: Optional[str] = element(default=None)
    rst_DisplayOrder: int = element()
    rst_DisplayWidth: int = element()
    rst_DisplayHeight: int = element()
    rst_DefaultValue: Optional[str] = element(default=None)
    rst_RecordMatchOrder: int = element()
    rst_CalcFunctionID: Optional[int] = element(default=None)
    rst_CalcFieldMask: Optional[str] = element(default=None)
    rst_RequirementType: Literal["required", "recommended", "optional", "forbidden"] = (
        element()
    )
    rst_NonOwnerVisibility: Literal["hidden", "viewable", "public", "pending"] = (
        element()
    )
    rst_Status: Literal["reserved", "approved", "pending", "open"] = element()
    rst_MayModify: Literal["locked", "discouraged", "open"] = element()
    rst_OriginatingDBID: int = element()
    rst_IDInOriginatingDB: Optional[int] = element(default=None)
    rst_MaxValues: int = element()
    rst_MinValues: int = element()
    rst_InitialRepeats: int = element()
    rst_DisplayDetailTypeGroupID: Optional[int] = element(default=None)
    rst_FilteredJsonTermIDTree: Optional[str] = element(default=None)
    rst_PtrFilteredIDs: Optional[str] = element(default=None)
    rst_CreateChildIfRecPtr: bool = element()
    rst_PointerMode: Literal[
        "dropdown_add", "dropdown", "addorbrowse", "addonly", "browseonly"
    ] = element()
    rst_PointerBrowseFilter: Optional[str] = element(default=None)
    rst_OrderForThumbnailGeneration: Optional[str] = element(default=None)
    rst_TermIDTreeNonSelectableIDs: Optional[str] = element(default=None)
    rst_ShowDetailCertainty: bool = element()
    rst_ShowDetailAnnotation: bool = element()
    rst_NumericLargestValueUsed: Optional[int] = element(default=None)
    rst_EntryMask: Optional[str] = element(default=None)
    rst_Modified: datetime = element()
    rst_LocallyModified: int = element()
    rst_SemanticReferenceURL: Optional[str] = element(default=None)
    rst_TermsAsButtons: bool = element()
