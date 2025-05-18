from heurist.models.structural.trm import TRM
from pydantic_xml import BaseXmlModel, element


class Terms(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Terms.

    Attributes:
        trm (list): list of instantiated dataclasses that model all of the database's
            Terms.

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
        >>> first_detail_type = hml.Terms.trm[0]
        >>> first_detail_type.trm_ID
        12
    """

    trm: list[TRM] = element()
