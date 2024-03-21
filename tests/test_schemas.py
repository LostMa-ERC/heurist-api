import unittest
from lxml import etree


from heurist_api.client import make_client
from heurist_api.schemas import RecordType, RecordStructure, DetailType


class SchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = make_client()
        xml = self.client.get_structure()

        # Parse the structure
        parser = etree.XMLParser(ns_clean=True)
        self.root = etree.fromstring(xml, parser)

    def test_schemas(self):
        records = self.root.find("RecStructure")
        for record_structure in records.xpath("./rst"):
            rst_dict = {r.tag: r.text for r in record_structure}
            RecordStructure(**rst_dict)

        records = self.root.find("RecTypes")
        for record_type in records.xpath("./rty"):
            rty_dict = {r.tag: r.text for r in record_type}
            RecordType(**rty_dict)

        details = self.root.find("DetailTypes")
        for detail in details.xpath("./dty"):
            dty_dict = {d.tag: d.text for d in detail}
            DetailType(**dty_dict)


if __name__ == "__main__":
    unittest.main()
