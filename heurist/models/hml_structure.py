from pydantic_xml import BaseXmlModel, element

from heurist.models.DetailTypes import DetailTypes as DetailTypesModel
from heurist.models.RecStructure import RecStructure as RecStructureModel
from heurist.models.RecTypeGroups import RecTypeGroups as RecTypeGroupsModel
from heurist.models.RecTypes import RecTypes as RecTypesModel
from heurist.models.Terms import Terms as TermsModel


class HMLStructure(BaseXmlModel, tag="hml_structure", search_mode="unordered"):
    """Parent dataclass forr modeling the entire Heurist database structure.

    Attributes:
        detail_types (DetailTypes): model for data nested in the DetailTypes tag.
        record_structures (RecStructure): model for data nested in the RecStructure tag.
        record_types (RecTypes): model for data nested in the RecTypes tag.

    Examples:
        >>> fromheurist.mock_data import DB_STRUCTURE_XML
        >>>
        >>>
        >>> # Parse structure
        >>> xml = DB_STRUCTURE_XML
        >>> hml = HMLStructure.from_xml(xml)
    """

    DetailTypes: DetailTypesModel = element(tag="DetailTypes")
    RecStructure: RecStructureModel = element(tag="RecStructure")
    RecTypes: RecTypesModel = element(tag="RecTypes")
    RecTypeGroups: RecTypeGroupsModel = element(tag="RecTypeGroups")
    Terms: TermsModel = element(tag="Terms")
