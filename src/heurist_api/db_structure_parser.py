import duckdb
import polars as pl
from pathlib import Path
from lxml import etree
from pydantic import BaseModel

from heurist_api.schemas import (
    RecordType,
    RecordStructure,
    DetailType,
    RecordField,
    RecordBaseModel,
)
from heurist_api.constants import (
    JOIN_RECORD_STRUCTURES_AND_DETAIL_TYPES,
    JOIN_RECORD_TYPE_WITH_STRUCTURE,
)


class DBStructureParser:
    def __init__(self, xml: bytes, sql_connection: str | Path | None = "") -> None:
        """Initially parse the XML export that describes the database structure.

        Examples:
            >>> xml = b'<xml></xml>'
            >>> parser = DBStructureParser(xml=xml)
            >>> type(parser.root)
            <class 'lxml.etree._Element'>

        Args:
            xml (bytes): XML byte string exported from the Heurist API.
            sql_connection (str | Path | None, optional): If saving the parsed structure in a persistent database, the path to the database. Defaults to "", which creates an in-memory database connection.

        Raises:
            TypeError: If the xml variable is not a byte string, raise an error.
        """

        # If the databse is a persistent connection, cast the path as a string
        if isinstance(sql_connection, Path):
            sql_connection = str(sql_connection)

        # Connect to the duckdb database
        self.conn = duckdb.connect(sql_connection)

        # If the XML is not a byte string, raise an error
        if not isinstance(xml, bytes):
            raise TypeError()

        # Declare an XML parser for lxml
        parser = etree.XMLParser(ns_clean=True)

        # Parse the XML from the byte string
        self.root = etree.fromstring(xml, parser)

    @property
    def record_types(self) -> list:
        """Parse and validate Record Types in the database structure.

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>>
            >>> # Test the property
            >>> record_types = parser.record_types
            >>> len(record_types)
            1

        Returns:
            list: Array of validated Record Type data models.
        """
        f = []
        records = self.root.find("RecTypes")
        for record_type in records.xpath("./rty"):
            rty_dict = {r.tag: r.text for r in record_type}
            f.append(RecordType(**rty_dict))
        return f

    @property
    def record_structures(self) -> list:
        """Parse and validate Record Structure details in the database structure.

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>>
            >>> # Test the property
            >>> record_structures = parser.record_structures
            >>> len(record_structures)
            3

        Returns:
            list: Array of validated Record Structure data models.
        """
        f = []
        records = self.root.find("RecStructure")
        for record_structure in records.xpath("./rst"):
            rst_dict = {r.tag: r.text for r in record_structure}
            f.append(RecordStructure(**rst_dict))
        return f

    @property
    def detail_types(self) -> list:
        """Parse and validate Detail Types in the database structure.

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>>
            >>> # Test the property
            >>> detail_types = parser.detail_types
            >>> len(detail_types)
            3

        Returns:
            list: Array of validated Detail Type data models.
        """
        f = []
        details = self.root.find("DetailTypes")
        for detail in details.xpath("./dty"):
            dty_dict = {d.tag: d.text for d in detail}
            f.append(DetailType(**dty_dict))
        return f

    def create_tables_for_structural_properties(self) -> None:
        """Parse each of the class's properties as data models,
        convert the model into a pyarrow data frame, and create
        a DuckDB table from the data frame.

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>>
            >>> # Test the method
            >>> parser.create_tables_for_structural_properties()
        """
        structural_properties = ["detail_types", "record_structures", "record_types"]
        for class_property in structural_properties:
            df = pl.DataFrame(getattr(self, class_property))
            self.conn.sql(f"DROP TABLE IF EXISTS {class_property}")
            self.conn.sql(f"CREATE TABLE {class_property} AS FROM df")

    def join_detail_types_and_record_structures(self) -> None:
        """Join the structure's 3 relevant tables into one new table.

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>> parser.create_tables_for_structural_properties()
            >>>
            >>> # Test the method
            >>> parser.join_detail_types_and_record_structures()
        """
        self.conn.sql("DROP TABLE IF EXISTS joined_str")
        sql = "CREATE TABLE joined_str AS " + JOIN_RECORD_STRUCTURES_AND_DETAIL_TYPES
        self.conn.sql(sql)

    def parse_record_field_params(self, record_type: int) -> list[RecordField]:
        """_summary_

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>>
            >>> # Test the method
            >>> fields = parser.parse_record_field_params(record_type=102)
            >>> len(fields)
            1

        Args:
            record_type (int): Integer identifier of the Heurist record type.

        Returns:
            List[RecordField]: An array of composed data models of the record's field.
        """

        self.create_tables_for_structural_properties()
        self.join_detail_types_and_record_structures()
        sql = JOIN_RECORD_TYPE_WITH_STRUCTURE.format("joined_str", record_type)
        rel = self.conn.sql(sql)
        dicts = [dict(zip(rel.columns, r)) for r in rel.fetchall()]
        return [RecordField(**d) for d in dicts]

    def create_record_model(self, record_type: int) -> BaseModel:
        """_summary_

        Examples:
            >>> from heurist_api.constants import EXAMPLE_XML
            >>>
            >>>
            >>> # Set up the parser
            >>> parser = DBStructureParser(xml=EXAMPLE_XML)
            >>>
            >>> # Test the method
            >>> Model = parser.create_record_model(record_type=102)
            >>> model = Model(**{"rec_ID":1, "rec_RecTypeID":102, "details": []})
            >>> model.model_dump()
            {'H-ID': 1, 'type_id': 102, 'name_or_title 1': None}

        Args:
            record_type (int): Integer identifier of the Heurist record type.

        Returns:
            BaseModel: An uninstantiated data model dynamically composed for the record type.
        """

        fields = self.parse_record_field_params(record_type)
        model_name = f"RecType_{record_type}"
        return RecordBaseModel.from_payload(model_name=model_name, fields=fields)
