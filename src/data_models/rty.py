from datetime import datetime
from typing import Literal, Optional

from pydantic_xml import BaseXmlModel, element


class RTY(BaseXmlModel, tag="rty", search_mode="unordered"):
    """Dataclass to model one of the database's Record Types. A Record Type is the \
        schema for an entity in the database.

    When possible, the attribute descriptions are taken from Heurist's source code.

    Attributes:
        rty_ID (int): Record type code, widely used to reference record types, primary \
            key
        rty_Name (str): The name which is used to describe this record (object) type
        rty_OrderInGroup (int): Ordering within record type display groups for pulldowns
        rty_Description (str): Description of this record type
        rty_TitleMask (str): Mask to build a composite title by combining field values
        rty_CanonicalTitleMask (str): Version of the mask converted to detail codes \
            for processing
        rty_Plural (Optional[str]): Plural form of the record type name, manually \
            entered
        rty_Status (Literal["reserved", "approved", "pending", "open"]): Reserved \
            Heurist codes, approved/pending by ''Board'', and user additions
        rty_OriginatingDBID (Optional[int]): Database where this record type \
            originated, 0 = locally
        rty_NameInOriginatingDB: (Optional[str]) Name used in database where this \
            record type originated
        rty_IDInOriginatingDB (Optional[int]): ID in database where this record type \
            originated
        rty_NonOwnerVisibility (Literal["hidden", "viewable", "public", "pending"]): \
            Allows blanket restriction of visibility of a particular record type
        rty_ShowInLists (bool): Flags if record type is to be shown in end-user \
            interface, 1=yes
        rty_RecTypeGroupID (int): Record type group to which this record type belongs
        rty_RecTypeModelIDs (str): The model group(s) to which this rectype belongs, \
            comma sep. list
        rty_FlagAsFieldset (bool): 0 = full record type, 1 = Fieldset = set of fields \
            to include in other rectypes
        rty_ReferenceURL (Optional[str]): A semantic reference URI for, or a URL \
            describing, the record type
        rty_AlternativeRecEditor (Optional[str]): Name or URL of alternative record \
            editor function to be used for this rectype
        rty_Type (Literal["normal", "relationship", "dummy"]): Use to flag special \
            record types to trigger special functions
        rty_ShowURLOnEditForm (bool): Determines whether special URL field is shown at \
            the top of the edit form
        rty_ShowDescriptionOnEditForm (bool): Determines whether the record type \
            description field is shown at the top of the edit form
        rty_Modified (datetime): Date of last modification of this record, used to get \
            last updated date for table
        rty_LocallyModified (bool): Flags a definition element which has been modified \
            relative to the original source
    """

    rty_ID: int = element()
    rty_Name: str = element()
    rty_OrderInGroup: int = element()
    rty_Description: str = element()
    rty_TitleMask: str = element()
    rty_CanonicalTitleMask: Optional[str] = element(default=None)
    rty_Plural: Optional[str] = element(default=None)
    rty_Status: Literal["reserved", "approved", "pending", "open"] = element()
    rty_OriginatingDBID: Optional[int] = element(default=None)
    rty_NameInOriginatingDB: Optional[str] = element(default=None)
    rty_IDInOriginatingDB: Optional[int] = element(default=None)
    rty_NonOwnerVisibility: Literal["hidden", "viewable", "public", "pending"] = (
        element()
    )
    rty_ShowInLists: bool = element()
    rty_RecTypeGroupID: int = element()
    rty_RecTypeModelIDs: str = element(default=None)
    rty_FlagAsFieldset: bool = element(default=None)
    rty_ReferenceURL: Optional[str] = element(default=None)
    rty_AlternativeRecEditor: Optional[str] = element(default=None)
    rty_Type: Literal["normal", "relationship", "dummy"] = element()
    rty_ShowURLOnEditForm: bool = element()
    rty_ShowDescriptionOnEditForm: bool = element()
    rty_Modified: datetime = element()
    rty_LocallyModified: bool = element()
