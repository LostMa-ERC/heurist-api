from heurist.models.structural.dty import DTY
from pydantic_xml import BaseXmlModel, element


class DetailTypes(BaseXmlModel):
    """Dataclass for modeling all of the database structure's Detail Types.

    Attributes:
        dty (list): list of instantiated dataclasses that model all of the database's
            Detail Types.

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
        >>> first_detail_type = hml.DetailTypes.dty[0]
        >>> first_detail_type.dty_ID
        1
        >>> singular_pointer = [d for d in hml.DetailTypes.dty if d.dty_ID == 1295][0]
        >>> singular_pointer.dty_PtrTargetRectypeIDs
        [101]
        >>> plural_pointer = [d for d in hml.DetailTypes.dty if d.dty_ID == 1256][0]
        >>> plural_pointer.dty_PtrTargetRectypeIDs
        [101, 105, 106]

    """

    dty: list[DTY] = element()
