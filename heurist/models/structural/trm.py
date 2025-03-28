from datetime import datetime
from typing import Literal, Optional

from pydantic_xml import BaseXmlModel, element


class TRM(BaseXmlModel, tag="trm", search_mode="unordered"):
    """Dataclass to model one of the database's vocabulary terms.

    When possible, the attribute descriptions are taken from Heurist's source code.
    """

    trm_ID: int = element()
    trm_Label: str = element()
    trm_InverseTermId: Optional[int] = element(default=None)
    trm_Description: Optional[str] = element(default=None)
    trm_Status: Literal["open", "approved", "reserved"] = element()
    trm_OriginatingDBID: int = element()
    trm_NameInOriginatingDB: Optional[str] = element(default=None)
    trm_IDInOriginatingDB: Optional[int] = element(default=None)
    trm_AddedByImport: bool = element()
    trm_IsLocalExtension: bool = element()
    trm_Domain: Literal["relation", "enum"] = element()
    trm_OntID: int = element()
    trm_ChildCount: int = element()
    trm_ParentTermID: Optional[int] = element(default=None)
    trm_Depth: int = element()
    trm_Modified: datetime = element()
    trm_LocallyModified: bool = element()
    trm_Code: Optional[str] = element(default=None)
    trm_SemanticReferenceURL: Optional[str] = element(default=None)
    trm_IllustrationURL: Optional[str] = element(default=None)
    trm_VocabularyGroupID: Optional[int] = element(default=None)
    trm_OrderInBranch: Optional[int] = element(default=None)
