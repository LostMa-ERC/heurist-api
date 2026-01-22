import duckdb
import polars as pl
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from heurist.models.structural.hml_structure import HMLStructure
from heurist.sql import RECORD_TYPE_SCHEMA
from pydantic_xml import BaseXmlModel


class HeuristDatabase:
    """Base class for loading the original Heurist database structure."""

    BASE_TABLES = [
        ("rtg", "RecTypeGroups"),
        ("rst", "RecStructure"),
        ("rty", "RecTypes"),
        ("dty", "DetailTypes"),
        ("trm", "Terms"),
    ]

    def __init__(
        self,
        hml_xml: bytes,
        conn: DuckDBPyConnection | None = None,
        db: str = ":memory:",
    ) -> None:
        """
        Create a DuckDB database connection and populate the DuckDB database with the
        5 base tables that comprise the Heurist database structure.

        Args:
            hml_xml (bytes): Heurist database structure exported in XML format.
            conn (DuckDBPyConnection | None, optional): A DuckDB database connection. \
                Defaults to None.
            db (str, optional): Path to the DuckDB database. Defaults to ":memory:".
        """

        hml_xml = self.trim_xml_bytes(xml=hml_xml)
        if not conn:
            conn = duckdb.connect(db)
        self.conn = conn
        # Load the Heurist database structure XML into a nested Pydantic data model
        self.hml = HMLStructure.from_xml(hml_xml)

        # Create generic tables
        for t in self.BASE_TABLES:
            name = t[0]
            pydantic_model = getattr(getattr(self.hml, t[1]), t[0])
            self.create(name, pydantic_model)

    @classmethod
    def trim_xml_bytes(cls, xml: bytes) -> bytes:
        """
        Remove any extra whitespace from a potentially malformatted XML.

        Args:
            xml (bytes): Heurist database structure exported XML format.

        Returns:
            bytes: Validated Heurist database structure in XML format.
        """

        return xml.decode("utf-8").strip().encode("utf-8")

    def delete_existing_table(self, table_name: str) -> None:
        """
        If the table already exists in the DuckDB database, drop it.

        Args:
            table_name (str): Name of the table to potentially drop.
        """

        if self.conn.sql(
            f"""
SELECT *
FROM duckdb_tables()
WHERE table_name like '{table_name}'
"""
        ):
            self.conn.sql("DROP TABLE {}".format(table_name))

    def create(self, name: str, model: BaseXmlModel) -> None:
        """Create an empty table in the DuckDB database connection
        based on a Pydantic model.

        Examples:
            >>> # Set up the database class and parse a table model.
            >>> from mock_data import DB_STRUCTURE_XML
            >>> db = HeuristDatabase(hml_xml=DB_STRUCTURE_XML)
            >>> model = db.hml.RecTypeGroups.rtg
            >>>
            >>> # Create a table for the Record Type Group (rtg) table model.
            >>> db.create(name="rtg", model=model)
            >>> shape = db.conn.table("rtg").fetchall()
            >>> # The Record Type Group (rtg) table should have 11 columns.
            >>> len(shape)
            11

        Args:
            model (BaseXmlModel): A Pydantic XML model.
        """

        self.delete_existing_table(name)

        # Convert the model to a dataframe and register it for duckdb
        df = pl.DataFrame(model)
        assert df.shape[0] > 1

        # Create table from model dataframe
        sql = "CREATE TABLE {} AS FROM df".format(name)
        self.conn.sql(sql)

    def describe_record_schema(self, rty_ID: int) -> DuckDBPyRelation:
        """Join the tables 'dty' (detail), 'rst' (record structure), 'rty' (record type)
        to get all the relevant information for a specific record type, plus add the
        label and description of the section / separator associated with each detail
        (if any).

        Args:
            rty_ID (int): ID of the targeted record type.

        Returns:
            DuckDBPyRelation: A DuckDB Python relation that can be queried or converted.
        """

        return self.conn.from_query(query=RECORD_TYPE_SCHEMA, params=[rty_ID])
