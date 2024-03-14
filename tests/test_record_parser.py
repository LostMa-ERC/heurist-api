from heurist_api.parsers.record import RecordParser
from heurist_api.parsers.db_structure import Table
import unittest
from pathlib import Path
import yaml

TEST_CONFIG = Path(__file__).parent.joinpath("config.yaml")


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        with open(TEST_CONFIG) as f:
            config = yaml.safe_load(f)
            self.cookie = config["cookie"]
            self.db = config["db"]
        self.output = Path(__file__).parent.joinpath("export")
        self.output.mkdir()

    def test_outfile_name(self):
        table = Table(name="test", record_id=200)
        export_xml = Path(__file__).parent.joinpath("mock.html")
        parser = RecordParser(record_xml=export_xml, table=table, output=self.output)
        self.assertEqual(parser.outfile.name, "test_RecID-200.csv")

    def tearDown(self) -> None:
        for file in self.output.iterdir():
            file.unlink()
        self.output.rmdir()


if __name__ == "__main__":
    unittest.main()
