import duckdb
import polars as pl
from duckdb import DuckDBPyConnection
from pydantic_xml import BaseXmlModel

from heurist.components.sql_models.record_details import RecordTypeModeler
from heurist.models.hml_structure import HMLStructure


class DuckBase:
    def __init__(
        self,
        hml_xml: bytes,
        conn: DuckDBPyConnection | None = None,
        db: str = ":memory:",
        save_structure: bool = False,
    ) -> None:
        hml_xml = self.trim_xml_byes(xml=hml_xml)
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
        ]
        for b in basics:
            name = b[0]
            model = getattr(getattr(self.hml, b[1]), b[0])
            self.create(name, model)

    @classmethod
    def trim_xml_byes(cls, xml: bytes) -> bytes:
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
            >>> db = DuckBase(hml_xml=DB_STRUCTURE_XML)
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
    dty_Name,
    dty_Type
FROM rty
INNER JOIN rst ON rst.rst_RecTypeID = rty.rty_ID
INNER JOIN dty ON dty.dty_ID = rst.rst_DetailTypeID
WHERE rty.rty_ID = {}
AND dty.dty_Type NOT LIKE 'separator'
AND dty.dty_Type NOT LIKE 'relmarker'
""".format(
                rty_ID
            )
            rel = self.conn.sql(sql)

            # Model the targeted records in a Pydantic model
            yield RecordTypeModeler(
                rty_ID=rty_ID, rty_Name=rty_Name, detail_dicts=rel.pl().to_dicts()
            )
