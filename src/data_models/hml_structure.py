from pydantic_xml import BaseXmlModel, element

from src.data_models.DetailTypes import DetailTypes as DetailTypesModel
from src.data_models.RecStructure import RecStructure as RecStructureModel
from src.data_models.RecTypeGroups import RecTypeGroups as RecTypeGroupsModel
from src.data_models.RecTypes import RecTypes as RecTypesModel
from src.data_models.Terms import Terms as TermsModel


class HMLStructure(BaseXmlModel, tag="hml_structure", search_mode="unordered"):
    """Parent dataclass forr modeling the entire Heurist database structure.

    Attributes:
        detail_types (DetailTypes): model for data nested in the DetailTypes tag.
        record_structures (RecStructure): model for data nested in the RecStructure tag.
        record_types (RecTypes): model for data nested in the RecTypes tag.

    Examples:
        >>> from examples import DB_STRUCTURE_XML
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
