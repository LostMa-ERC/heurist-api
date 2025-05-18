from heurist.models.structural.rst import RST
from pydantic_xml import BaseXmlModel, element


class RecStructure(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Record Structures.

    Attributes:
        rst (list): list of instantiated dataclasses that model all of the database's
            Record Structures.

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
        >>> first_record_structure = hml.RecStructure.rst[0]
        >>> first_record_structure.rst_ID
        1
    """

    rst: list[RST] = element()
