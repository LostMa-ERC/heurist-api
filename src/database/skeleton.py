import duckdb
import polars as pl
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from pydantic_xml import BaseXmlModel

from src.data_models.hml_structure import HMLStructure
from src.heurist_transformers.detail_modeler import RecordTypeModeler
from src.sql_models.select_record_structure import QUERY


class DatabaseSkeleton:
    """Base class for the ingesting and parsing a Heurist schema."""

    def __init__(
        self,
        hml_xml: bytes,
        conn: DuckDBPyConnection | None = None,
        db: str = ":memory:",
        save_structure: bool = False,
    ) -> None:
        hml_xml = self.trim_xml_bytes(xml=hml_xml)
        if not conn:
            conn = duckdb.connect(db)
        self.conn = conn
        self.hml = HMLStructure.from_xml(hml_xml)
        self.save_structure = save_structure

        # Create generic tables
        basics = [
            ("rtg", "RecTypeGroups"),
            ("rst", "RecStructure"),
            ("rty", "RecTypes"),
            ("dty", "DetailTypes"),
            ("trm", "Terms"),
        ]
        for b in basics:
            name = b[0]
            model = getattr(getattr(self.hml, b[1]), b[0])
            self.create(name, model)

    @classmethod
    def trim_xml_bytes(cls, xml: bytes) -> bytes:
        return xml.decode("utf-8").strip().encode("utf-8")

    def delete_existing_table(self, table_name: str) -> None:
        if self.conn.sql(
            f"""
SELECT *
FROM duckdb_tables()
WHERE table_name like '{table_name}'
"""
        ):
            print(f"Deleting existing table {table_name}")
            self.conn.sql("DROP TABLE {}".format(table_name))

    def create(self, name: str, model: BaseXmlModel) -> None:
        """Create an empty table in the DuckDB database connection
        based on a Pydantic model.

        Examples:
            >>> from examples import DB_STRUCTURE_XML
            >>>
            >>>
            >>> db = DatabaseSkeleton(hml_xml=DB_STRUCTURE_XML)
            >>> target = db.hml.RecTypeGroups.rtg
            >>> db.create("rtg", target)
            Deleting existing table rtg
            >>> shape = db.conn.table("rtg").fetchall()
            >>> len(shape)
            11

        Args:
            model (BaseXmlModel): _description_
        """
        self.delete_existing_table(name)
        df = pl.DataFrame(model)
        if self.save_structure:
            sql = "CREATE TABLE {} AS FROM df".format(name)
        else:
            sql = "CREATE TEMPORARY TABLE {} AS FROM df".format(name)
        self.conn.sql(sql)

    @classmethod
    def select_record_types(cls, record_type_groups: list[str]) -> str:
        condition = "WHERE rtg.rtg_Name like '{}'".format(record_type_groups[0])
        if len(record_type_groups) > 1:
            for rtg in record_type_groups[1:]:
                condition += " OR rtg.rtg_Name like '{}'".format(rtg)
        return """
SELECT
    rty.rty_ID,
    rty.rty_Name
FROM rty
INNER JOIN rtg ON rty.rty_RecTypeGroupID = rtg.rtg_ID
{}
""".format(
            condition
        )

    def yield_record_details(self, record_type_groups: list[str]):
        # Prepare a statement to select the record types in the target group(s)
        stmt = self.select_record_types(record_type_groups)

        # Select the targeted records' details (data fields)
        for rty_ID, rty_Name in self.conn.sql(stmt).fetchall():
            sql = """
SELECT
    dty_ID,
    rst_DisplayName,
    dty_Type
FROM rst
INNER JOIN rty ON rst.rst_RecTypeID = rty.rty_ID
INNER JOIN dty ON rst.rst_DetailTypeID = dty.dty_ID
WHERE rty.rty_ID = {}
AND dty.dty_Type NOT LIKE 'separator'
AND dty.dty_Type NOT LIKE 'relmarker'
ORDER BY rst.rst_DisplayOrder
""".format(
                rty_ID
            )
            rel = self.conn.sql(sql)

            # Model the targeted records in a Pydantic model
            yield RecordTypeModeler(
                rty_ID=rty_ID, rty_Name=rty_Name, detail_dicts=rel.pl().to_dicts()
            )

    def describe_record_fields(self, rty_ID: int) -> DuckDBPyRelation:
        """Join the tables 'dty' (detail), 'rst' (record structure), 'rty' (record type)
        to get all the relevant information for a specific record type, plus add the label
        and description of the section / separator associated with each detail (if any).

        Args:
            rty_ID (int): ID of the targeted record type.

        Returns:
            DuckDBPyRelation: A DuckDB Python relation that can be queried or converted.
        """
        return self.conn.from_query(query=QUERY, params=[rty_ID])
