from datetime import datetime
from typing import Optional

from pydantic_xml import BaseXmlModel, element


class RTG(BaseXmlModel, tag="rtg", search_mode="unordered"):
    """Dataclass to model one of the database's Record Type Groups. A Record Type \
        Group categorizes the record types in the database.

    When possible, the attribute descriptions are taken from Heurist's source code.

    Attributes:
        rtg_ID (int): __Description__.
        rtg_Name (str): __Description__.
        rtg_Domain (str): __Description__.
        rtg_Description (Optional[str]): __Description__.
        rtg_Modified (datetime): __Description__.
    """

    rtg_ID: int = element()
    rtg_Name: str = element()
    rtg_Domain: str = element()
    rtg_Description: Optional[str] = element(default=None)
    rtg_Modified: datetime = element()
