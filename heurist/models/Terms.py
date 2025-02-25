from pydantic_xml import BaseXmlModel, element

from heurist.models.trm import TRM


class Terms(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Terms.

    Attributes:
        trm (list): list of instantiated dataclasses that model all of the database's
            Terms.

    Examples:
        >>> from heurist.mock_data import DB_STRUCTURE_XML
        >>> from heurist.models import HMLStructure
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

    Args:
        BaseXmlModel (_type_): _description_
    """

    trm: list[TRM] = element()
