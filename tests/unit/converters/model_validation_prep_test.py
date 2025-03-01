import unittest

import heurist.mock_data.enum.repeated
import heurist.mock_data.enum.single
import heurist.mock_data.freetext.single
import heurist.mock_data.date.compound.single
from heurist.converters.model_validation_prep import ModelValidationPrep
from heurist.converters.dynamic_record_type_modeler import (
    DynamicRecordTypeModel,
)


DETAIL_METADATA = [
    heurist.mock_data.enum.repeated.METADATA,
    heurist.mock_data.freetext.single.METADATA,
    heurist.mock_data.date.compound.single.METADATA,
]

ENUM_DTY_ID = heurist.mock_data.enum.repeated.DETAIL[0]["dty_ID"]
FREETEXT_DTY_ID = heurist.mock_data.freetext.single.DETAIL["dty_ID"]
DATE_DTY_ID = heurist.mock_data.date.compound.single.DETAIL["dty_ID"]

DETAILS = (
    heurist.mock_data.enum.repeated.DETAIL
    + [heurist.mock_data.freetext.single.DETAIL]
    + [heurist.mock_data.date.compound.single.DETAIL]
)


class RecordModelerTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rec_ID = 1
        self.rec_RecTypeID = 103
        self.record = {
            "rec_ID": self.rec_ID,
            "rec_RecTypeID": self.rec_RecTypeID,
            "rec_Name": "Story",
            "details": DETAILS,
        }
        self.pydantic_model = DynamicRecordTypeModel(
            rty_ID=self.record["rec_RecTypeID"],
            rty_Name=self.record["rec_Name"],
            detail_metadata=DETAIL_METADATA,
        )
        self.modeler = ModelValidationPrep(
            pydantic_model=self.pydantic_model,
        )

    def test_is_plural(self):
        actual = self.modeler.is_plural(dty_id=ENUM_DTY_ID)
        self.assertTrue(actual)

        actual = self.modeler.is_plural(dty_id=FREETEXT_DTY_ID)
        self.assertFalse(actual)

        actual = self.modeler.is_plural(dty_id=DATE_DTY_ID)
        self.assertFalse(actual)

    def test_aggregate_details(self):
        # The value of every key must be a list
        expected = {
            ENUM_DTY_ID: heurist.mock_data.enum.repeated.DETAIL,
            FREETEXT_DTY_ID: [heurist.mock_data.freetext.single.DETAIL],
            DATE_DTY_ID: [heurist.mock_data.date.compound.single.DETAIL],
        }
        actual = self.modeler.aggregate_details(DETAILS)
        self.assertDictEqual(expected, actual)

    def test_covert_generic_detail(self):
        actual = self.modeler.convert_generic_to_pydantic_kwarg(
            dty_id=FREETEXT_DTY_ID,
            details=[heurist.mock_data.freetext.single.DETAIL],
        )
        expected = heurist.mock_data.freetext.single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)

    def test_convert_enum_detail(self):
        actual = self.modeler.convert_enum_to_pydantic_kwarg(
            dty_id=ENUM_DTY_ID,
            details=heurist.mock_data.enum.repeated.DETAIL,
        )
        expected = heurist.mock_data.enum.repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)

    def test_convert_date_detail(self):
        actual = self.modeler.convert_date_to_pydantic_kwarg(
            dty_id=DATE_DTY_ID,
            details=[heurist.mock_data.date.compound.single.DETAIL],
        )
        expected = heurist.mock_data.date.compound.single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)

    def test_flatten_record_details(self):
        actual = self.modeler(record=self.record)
        frontmatter = {"rec_ID": self.rec_ID, "rec_RecTypeID": self.rec_RecTypeID}
        expected = (
            frontmatter
            | heurist.mock_data.enum.repeated.PYDANTIC_KEY_VALUE
            | heurist.mock_data.freetext.single.PYDANTIC_KEY_VALUE
            | heurist.mock_data.date.compound.single.PYDANTIC_KEY_VALUE
        )
        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
