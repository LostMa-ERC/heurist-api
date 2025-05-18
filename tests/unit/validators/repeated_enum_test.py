import unittest

from heurist.models.dynamic import HeuristRecord
from heurist.validators.record_validator import VALIDATION_LOG, RecordValidator

# Result of joining the database schema tables for a detail that takes only 1 value.
LIMITED_METADATA = [
    {
        "dty_ID": 1090,
        "rst_DisplayName": "language",
        "dty_Type": "enum",
        "rst_MaxValues": 1,
    }
]


# Result of joining the database schema tables for a detail that takes => 0 values.
REPEATED_METADATA = [
    {
        "dty_ID": 1090,
        "rst_DisplayName": "language",
        "dty_Type": "enum",
        "rst_MaxValues": 0,
    }
]

# Result of a record's JSON export
RECORDS = [
    {
        "rec_ID": 1001,
        "rec_RecTypeID": 100,
        "details": [
            # Repeated enum detail
            {
                "dty_ID": 1090,
                "value": "9728",
                "termLabel": "dum (Middle Dutch)",
                "termCode": "dum",
                "fieldName": "language",
                "fieldType": "enum",
                "conceptID": "",
            },
            {
                "dty_ID": 1090,
                "value": "9470",
                "termLabel": "fro (Old French)",
                "termCode": "fro",
                "fieldName": "language",
                "fieldType": "enum",
                "conceptID": "",
            },
        ],
    }
]


class ValidRepeatedDetailTest(unittest.TestCase):
    def test(self):
        hr = HeuristRecord(
            rty_ID=100, rty_Name="Example", detail_metadata=REPEATED_METADATA
        )
        validator = RecordValidator(
            rty_ID=100, pydantic_model=hr.model, records=RECORDS
        )
        # Assert that this process does NOT raise a warning that is logged to stdout.
        with self.assertNoLogs():
            for model in validator:
                break

        actual_record_type = model.type
        expected_record_type = 100
        self.assertEqual(actual_record_type, expected_record_type)

        expected_foreign_keys = [9728, 9470]
        actual_foreign_keys = model.DTY1090_TRM
        self.assertListEqual(expected_foreign_keys, actual_foreign_keys)

    def tearDown(self):
        if VALIDATION_LOG.is_file():
            VALIDATION_LOG.unlink()
        return super().tearDown()


class InvalidRepeatedDetaiTest(unittest.TestCase):
    def test(self):
        """Run the validation process on records that should log an error."""
        hr = HeuristRecord(
            rty_ID=100, rty_Name="Example", detail_metadata=LIMITED_METADATA
        )
        validator = RecordValidator(
            rty_ID=100, pydantic_model=hr.model, records=RECORDS
        )
        # Assert that this validation raises a warning that is logged to stdout.
        with self.assertLogs():
            for model in validator:
                actual_foreign_key = model.DTY1090_TRM
                self.assertIsNone(actual_foreign_key)

    def tearDown(self):
        if VALIDATION_LOG.is_file():
            VALIDATION_LOG.unlink()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
