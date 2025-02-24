import unittest

from heurist.src.heurist_transformers.prepare_records import RecordFlattener
from heurist.src.heurist_transformers.dynamic_record_type_modeler import (
    DynamicRecordTypeModel,
)
from heurist import TABLES_LOG, DATABASE_LOG


class BaseCase(unittest.TestCase):
    def setUp(self, metadata: dict):
        model = DynamicRecordTypeModel(
            rty_ID=101,
            rty_Name="Test",
            detail_metadata=[metadata],
        ).model
        self.flattener = RecordFlattener(model)

    def tearDown(self):
        TABLES_LOG.unlink(missing_ok=True)
        DATABASE_LOG.unlink(missing_ok=True)


class SingularResource(BaseCase):
    fromheurist.mock_data.resource.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        fromheurist.mock_data.resource import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedResource(BaseCase):
    fromheurist.mock_data.resource.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        fromheurist.mock_data.resource import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class SingularFuzzyDate(BaseCase):
    fromheurist.mock_data.date.fuzzy.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        fromheurist.mock_data.date.fuzzy import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedFuzzyDate(BaseCase):
    fromheurist.mock_data.date.fuzzy.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        fromheurist.mock_data.date.fuzzy import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class SingularSimpleDate(BaseCase):
    fromheurist.mock_data.date.simple.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        fromheurist.mock_data.date.simple import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedSimpleDate(BaseCase):
    fromheurist.mock_data.date.simple.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        fromheurist.mock_data.date.simple import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class SingularEnum(BaseCase):
    fromheurist.mock_data.enum.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test_value(self):
        fromheurist.mock_data.enum import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedEnum(BaseCase):
    fromheurist.mock_data.enum.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test_value(self):
        fromheurist.mock_data.enum import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
