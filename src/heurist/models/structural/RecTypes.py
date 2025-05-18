from heurist.models.structural.rty import RTY
from pydantic_xml import BaseXmlModel, element


class RecTypes(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Record Types.

    Attributes:
        rty (list): list of instantiated dataclasses that model all of the database's
            Record Types.

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
        >>> first_record_type = hml.RecTypes.rty[0]
        >>> first_record_type.rty_ID
        1
    """

    rty: list[RTY] = element()
