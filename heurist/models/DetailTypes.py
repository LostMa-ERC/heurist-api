from pydantic_xml import BaseXmlModel, element

from heurist.models.dty import DTY


class DetailTypes(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Detail Types.

    Attributes:
        dty (list): list of instantiated dataclasses that model all of the database's Detail Types.

    Examples:
        >>> from examples import DB_STRUCTURE_XML
        >>> from heurist.models import HMLStructure
        >>>
        >>>
        >>> # Parse structure
        >>> xml = DB_STRUCTURE_XML
        >>> hml = HMLStructure.from_xml(xml)
        >>>
        >>> # Test class
        >>> first_detail_type = hml.DetailTypes.dty[0]
        >>> first_detail_type.dty_ID
        1
    """

    dty: list[DTY] = element()
