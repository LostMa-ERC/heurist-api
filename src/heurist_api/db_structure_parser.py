import duckdb
import polars as pl
from lxml import etree
from pydantic import BaseModel

from heurist_api.sql_functions import SQLSafeFunction, ConvertReqFunction
from heurist_api.schemas import (
    RecordType,
    RecordStructure,
    DetailType,
    RecordField,
    RecordBaseModel,
)


class DBStructureParser:
    def __init__(self, xml: bytes, sql_connection: str | None = "") -> None:
        if not isinstance(xml, bytes):
            raise TypeError()
        parser = etree.XMLParser(ns_clean=True)
        self.root = etree.fromstring(xml, parser)
        self.conn = duckdb.connect(sql_connection)
        # self.build_sql_functions()
        self.join_detail_types_and_record_structures()

    def build_sql_functions(self):
        SQLSafeFunction.create(self.conn)
        ConvertReqFunction.create(self.conn)

    @property
    def record_types(self) -> list:
        f = []
        records = self.root.find("RecTypes")
        for record_type in records.xpath("./rty"):
            rty_dict = {r.tag: r.text for r in record_type}
            f.append(RecordType(**rty_dict))
        return f

    @property
    def record_structures(self) -> list:
        f = []
        records = self.root.find("RecStructure")
        for record_structure in records.xpath("./rst"):
            rst_dict = {r.tag: r.text for r in record_structure}
            f.append(RecordStructure(**rst_dict))
        return f

    @property
    def detail_types(self) -> list:
        f = []
        details = self.root.find("DetailTypes")
        for detail in details.xpath("./dty"):
            dty_dict = {d.tag: d.text for d in detail}
            f.append(DetailType(**dty_dict))
        return f

    def ingest_dataframe(self, name: str):
        df = pl.DataFrame(getattr(self, name))
        self.conn.sql(f"DROP TABLE IF EXISTS {name}")
        self.conn.sql(f"CREATE TABLE {name} AS FROM df")

    def join_detail_types_and_record_structures(self) -> None:
        props = ["detail_types", "record_structures", "record_types"]
        for prop in props:
            self.ingest_dataframe(prop)
        self.conn.sql("DROP TABLE IF EXISTS joined_str")
        self.conn.sql(
            f"""
CREATE TABLE joined_str
AS SELECT
    rst.rst_RecTypeID,
    dty.dty_ID,
    dty.dty_Name,
    rst.rst_RequirementType,
	dty.dty_Type
FROM main.record_structures rst
JOIN main.detail_types dty
	ON dty.dty_ID = rst.rst_DetailTypeID
WHERE dty.dty_Type NOT LIKE 'separator'
ORDER BY rst.rst_DisplayOrder
"""
        )

    def parse_record_field_params(self, record_type: int) -> list[RecordField]:
        """_summary_

        Args:
            record_type (int): _description_

        Returns:
            List[RecordField]: _description_
        """

        sql = f"""
SELECT
    rty.rty_Name,
    *
FROM joined_str
JOIN main.record_types AS rty
    ON rst_RecTypeID = rty.rty_ID
WHERE rty.rty_ID = '{record_type}'
        """
        rel = self.conn.sql(sql)
        dicts = [dict(zip(rel.columns, r)) for r in rel.fetchall()]
        return [RecordField(**d) for d in dicts]

    def create_record_model(self, record_type: int) -> BaseModel:
        """_summary_

        Args:
            record_type (int): _description_

        Returns:
            BaseModel: _description_
        """

        fields = self.parse_record_field_params(record_type)
        model_name = f"RecType_{record_type}"
        return RecordBaseModel.from_payload(model_name=model_name, fields=fields)
