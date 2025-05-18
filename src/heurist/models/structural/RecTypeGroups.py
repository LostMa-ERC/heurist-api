from heurist.models.structural.rtg import RTG
from pydantic_xml import BaseXmlModel, element


class RecTypeGroups(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Record Type Groups.

    Attributes:
        rtg (list): list of instantiated dataclasses that model all of the database's
            Record Type Groups.

    Examples:
        >>> from mock_data import DB_STRUCTURE_XML
        >>> from heurist.models.structural import HMLStructure
        >>>
        >>>
        >>> # Parse structure
        >>> xml = DB_STRUCTURE_XML
        >>> hml = HMLStructure.from_xml(xml)
        >>>
        >>> # Test class
        >>> first_record_type = hml.RecTypeGroups.rtg[0]
        >>> first_record_type.rtg_ID
        4
    """

    rtg: list[RTG] = element()
