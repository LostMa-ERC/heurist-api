from datetime import datetime
from typing import List, Literal, Optional

from heurist.models.structural.utils import split_ids
from pydantic import field_validator
from pydantic_xml import BaseXmlModel, element


class DTY(BaseXmlModel, tag="dty", search_mode="unordered"):
    """Dataclass to model one of the database's Detail Types. A Detail Type is the
        generic schema that defines the type of data one of a record's field.

    When possible, the attribute descriptions are taken from Heurist's source code.

    Attributes:
        dty_ID (int): Code for the detail type (field) - may vary between Heurist DBs.
        dty_Name (str): The canonical (standard) name of the detail type, used as \
            default in edit form.
        dty_Documentation (Optional[str]): Documentation of the detail type, what it \
            means, how defined.
        dty_Type (Literal['freetext','blocktext','integer','date','year','relmarker',\
            'boolean','enum','relationtype','resource','float','file','geo','separator',\
            'calculated','fieldsetmarker','urlinclude']): The value-type of this \
            detail type, what sort of data is stored.
        dty_HelpText (Optional[str]):The default help text displayed to the user under \
            the field.
        dty_ExtendedDescription (Optional[str]): Extended text describing this detail \
            type, for display in rollover.
        dty_EntryMask (Optional[str]): Data entry mask, use to control decimals on \
            numeric values, content of text fields etc.
        dty_Status (Literal["reserved","approved","pending","open"]): 'Reserved' for \
            the system, cannot be changed; 'Approved' for community standards; \
            'Pending' for work in progress; 'Open' for freely modifiable/personal \
            record types.
        dty_OriginatingDBID (int): Database where this detail type originated, 0 = \
            locally.
        dty_NameInOriginatingDB (Optional[str]): Name used in database where this \
            detail type originated.
        dty_IDInOriginatingDB (int): ID used in database where this detail type \
            originated.
        dty_DetailTypeGroupID (int): The general role of this detail allowing \
            differentiated lists of detail types.
        dty_OrderInGroup (int): The display order of DetailType within group, \
            alphabetic if equal values.
        dty_JsonTermIDTree (Optional[str]): Tree of Term IDs to show for this field \
            (display-only header terms set in HeaderTermIDs).
        dty_TermIDTreeNonSelectableIDs (List[Optional[int]]): Term IDs to use as \
            non-selectable headers for this field.
        dty_PtrTargetRectypeIDs (List[Optional[int]]): CSVlist of target Rectype IDs, \
            null = any.
        dty_FieldSetRectypeID (Optional[int]): For a FieldSetMarker, the record type \
            to be inserted as a fieldset.
        dty_ShowInLists (bool): Show this field type in pulldown lists etc. (always \
            visible in field management screen).
        dty_NonOwnerVisibility (Literal["hidden","viewable","public"]): Hidden = \
            visible only to owners, Viewable = any logged in user, Public = visible \
                to non-logged in viewers.
        dty_Modified (datetime): Date of last modification of this record, used to get \
            last updated date for table.
        dty_LocallyModified (bool): Flags a definition element which has been modified \
            relative to the original source.
        dty_SemanticReferenceURL (Optional[str]): URI to a full description or \
            ontological reference definition of the base field (optional).
    """

    dty_ID: int = element()
    dty_Name: str = element()
    dty_Documentation: Optional[str] = element(default=None)
    dty_Type: Literal[
        "freetext",
        "blocktext",
        "integer",
        "date",
        "year",
        "relmarker",
        "boolean",
        "enum",
        "relationtype",
        "resource",
        "float",
        "file",
        "geo",
        "separator",
        "calculated",
        "fieldsetmarker",
        "urlinclude",
    ] = element()
    dty_HelpText: Optional[str] = element(default=None)
    dty_ExtendedDescription: Optional[str] = element(default=None)
    dty_EntryMask: Optional[str] = element(default=None)
    dty_Status: Literal["reserved", "approved", "pending", "open"] = element()
    dty_OriginatingDBID: int = element()
    dty_NameInOriginatingDB: Optional[str] = element(default=None)
    dty_IDInOriginatingDB: int = element()
    dty_DetailTypeGroupID: int = element()
    dty_OrderInGroup: int = element()
    dty_JsonTermIDTree: Optional[str] = element(default=None)
    dty_TermIDTreeNonSelectableIDs: List[Optional[int]] = element(default=[])
    dty_PtrTargetRectypeIDs: List[Optional[int]] = element(default=[])
    dty_FieldSetRectypeID: Optional[int] = element(default=None)
    dty_ShowInLists: bool = element()
    dty_NonOwnerVisibility: Literal["hidden", "viewable", "public"] = element()
    dty_Modified: datetime = element()
    dty_LocallyModified: bool = element()
    dty_SemanticReferenceURL: Optional[str] = element(default=None)

    @field_validator("dty_TermIDTreeNonSelectableIDs", mode="before")
    @classmethod
    def validate_selectable_ids(cls, input_value: str | None) -> list:
        if input_value:
            return split_ids(input=input_value)
        else:
            return []

    @field_validator("dty_PtrTargetRectypeIDs", mode="before")
    @classmethod
    def validate_rectype_ids(cls, input_value: str | None) -> list:
        if input_value:
            return split_ids(input=input_value)
        else:
            return []
