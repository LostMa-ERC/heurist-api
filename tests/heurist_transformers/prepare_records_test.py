import unittest

import _details
import _flat_kwarg
import _metadata
from src.heurist_transformers.prepare_records import RecordFlattener
from src.heurist_transformers.dynamic_record_type_modeler import DynamicRecordTypeModel


class TestResource(unittest.TestCase):
    def setUp(self):
        self.model = DynamicRecordTypeModel(
            rty_ID=103,
            rty_Name="Story",
            detail_metadata=_metadata.SINGULAR_RESOURCE,
        ).model
        self.flattener = RecordFlattener(self.model)

    def test_single_resource(self):
        actual = self.flattener(record_details=_details.ONE_RESOURCE)
        expected = _flat_kwarg.ONE_RESOURCE
        self.assertDictEqual(actual, expected)


class TestRepeatedValue(unittest.TestCase):
    def setUp(self):
        self.model = DynamicRecordTypeModel(
            rty_ID=103,
            rty_Name="Story",
            detail_metadata=_metadata.REPEATED_RESOURCES,
        ).model
        self.flattener = RecordFlattener(self.model)

    def test_repeated_resource(self):
        actual = self.flattener(record_details=_details.TWO_RESOURCES)
        expected = _flat_kwarg.TWO_RESOURCES
        self.assertDictEqual(actual, expected)


class TestTemporal(unittest.TestCase):
    def setUp(self):
        self.model = DynamicRecordTypeModel(
            rty_ID=103,
            rty_Name="Story",
            detail_metadata=_metadata.SINGULAR_TEMPORAL,
        ).model
        self.flattener = RecordFlattener(self.model)

    def test_single_temporal(self):
        actual = self.flattener(record_details=_details.ONE_TEMPORAL)
        expected = _flat_kwarg.ONE_TEMPORAL
        self.assertDictEqual(actual, expected)


class TestRepeatedTemporal(unittest.TestCase):
    def setUp(self):
        self.model = DynamicRecordTypeModel(
            rty_ID="103", rty_Name="Story", detail_metadata=_metadata.REPEATED_TEMPORAL
        ).model
        self.flattener = RecordFlattener(self.model)

    def test_repeated_temporal(self):
        actual = self.flattener(record_details=_details.TWO_TEMPORAL)
        expected = _flat_kwarg.TWO_TEMPORAL
        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
