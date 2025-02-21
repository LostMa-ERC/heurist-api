import unittest

import heurist.examples.enum.repeated
import heurist.examples.enum.single
import heurist.examples.freetext.single
import heurist.examples.date.fuzzy.single
from heurist.src.heurist_transformers.record_modeler import RecordModeler
from heurist.src.heurist_transformers.dynamic_record_type_modeler import (
    DynamicRecordTypeModel,
)


DETAIL_METADATA = [
    heurist.examples.enum.repeated.METADATA,
    heurist.examples.freetext.single.METADATA,
    heurist.examples.date.fuzzy.single.METADATA,
]

ENUM_DTY_ID = heurist.examples.enum.repeated.DETAIL[0]["dty_ID"]
FREETEXT_DTY_ID = heurist.examples.freetext.single.DETAIL["dty_ID"]
DATE_DTY_ID = heurist.examples.date.fuzzy.single.DETAIL["dty_ID"]

DETAILS = (
    heurist.examples.enum.repeated.DETAIL
    + [heurist.examples.freetext.single.DETAIL]
    + [heurist.examples.date.fuzzy.single.DETAIL]
)


class RecordModelerTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rec_ID = 1
        self.rec_RecTypeID = 103
        record = {
            "rec_ID": self.rec_ID,
            "rec_RecTypeID": self.rec_RecTypeID,
            "rec_Name": "Story",
            "details": DETAILS,
        }
        self.pydantic_model = DynamicRecordTypeModel(
            rty_ID=record["rec_RecTypeID"],
            rty_Name=record["rec_Name"],
            detail_metadata=DETAIL_METADATA,
        )
        self.modeler = RecordModeler(
            pydantic_model=self.pydantic_model,
            record=record,
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
            ENUM_DTY_ID: heurist.examples.enum.repeated.DETAIL,
            FREETEXT_DTY_ID: [heurist.examples.freetext.single.DETAIL],
            DATE_DTY_ID: [heurist.examples.date.fuzzy.single.DETAIL],
        }
        actual = self.modeler.aggregate_details(DETAILS)
        self.assertDictEqual(expected, actual)

    def test_covert_generic_detail(self):
        actual = self.modeler.convert_generic_to_pydantic_kwarg(
            dty_id=FREETEXT_DTY_ID,
            details=[heurist.examples.freetext.single.DETAIL],
        )
        expected = heurist.examples.freetext.single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)

    def test_convert_enum_detail(self):
        actual = self.modeler.convert_enum_to_pydantic_kwarg(
            dty_id=ENUM_DTY_ID,
            details=heurist.examples.enum.repeated.DETAIL,
        )
        expected = heurist.examples.enum.repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)

    def test_convert_date_detail(self):
        actual = self.modeler.convert_date_to_pydantic_kwarg(
            dty_id=DATE_DTY_ID,
            details=[heurist.examples.date.fuzzy.single.DETAIL],
        )
        expected = heurist.examples.date.fuzzy.single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)

    def test_flatten_record_details(self):
        actual = self.modeler.flatten_record_details()
        frontmatter = {"rec_ID": self.rec_ID, "rec_RecTypeID": self.rec_RecTypeID}
        expected = (
            frontmatter
            | heurist.examples.enum.repeated.PYDANTIC_KEY_VALUE
            | heurist.examples.freetext.single.PYDANTIC_KEY_VALUE
            | heurist.examples.date.fuzzy.single.PYDANTIC_KEY_VALUE
        )
        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
