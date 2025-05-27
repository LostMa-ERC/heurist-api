import unittest
from pathlib import Path

from heurist.log import yield_log_blocks, LogDetail


LOG_FILE = Path(__file__).parent.joinpath("mock_log.txt")

LINES = [
    "2025-05-26 18:50 - WARNING - ",
    "	[rec_Type 104]",
    "	[rec_ID 834]",
    "	The detail 'note' is limited to a maximum of 1 values.",
    "	Count of values = 3.",
    "2025-05-26 18:50 - WARNING - ",
    "	[rec_Type 104]",
    "	[rec_ID 834]",
    "	The detail 'contam' is limited to a maximum of 1 values.",
    "	Count of values = 2.",
]


class TestLog(unittest.TestCase):
    def assess_log_block(self, log: LogDetail):
        self.assertEqual(log.level, "WARNING")
        self.assertIsNotNone(log.rule)
        self.assertIsNotNone(log.problem)
        self.assertGreater(log.recID, 100)
        self.assertGreater(log.recType, 99)

    def test_parsed_lines(self):
        for log in yield_log_blocks(LINES):
            self.assess_log_block(log)

    def test_log_file(self):
        print(LOG_FILE)
        with open(LOG_FILE) as f:
            lines = f.readlines()
            for log in yield_log_blocks(lines):
                self.assess_log_block(log)


if __name__ == "__main__":
    unittest.main()
