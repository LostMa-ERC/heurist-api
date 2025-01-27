from pydantic_xml import BaseXmlModel, element

from src.data_models.rtg import RTG


class RecTypeGroups(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Record Type Groups.

    Attributes:
        rtg (list): list of instantiated dataclasses that model all of the database's Record Type Groups.

    Examples:
        >>> from examples import DB_STRUCTURE_XML
        >>> from src.data_models import HMLStructure
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
