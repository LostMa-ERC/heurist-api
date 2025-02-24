import unittest

from pydantic.fields import FieldInfo

from heurist.src.heurist_transformers.dynamic_pydantic_data_field import (
    DynamicDataFieldBuilder,
)
from heurist import TABLES_LOG, DATABASE_LOG


def get_field_info_from_dict(d: dict) -> FieldInfo:
    return tuple(d.values())[0][1]


class BaseCase(unittest.TestCase):
    def tearDown(self):
        TABLES_LOG.unlink(missing_ok=True)
        DATABASE_LOG.unlink(missing_ok=True)
        return super().tearDown()


class Resource(BaseCase):
    def setUp(self):
        fromheurist.mock_data.resource.single import METADATA

        builder = DynamicDataFieldBuilder(**METADATA)
        self.field = builder.simple_field()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_alias(self):
        fromheurist.mock_data.resource.single import PYDANTIC_KEY_VALUE

        actual = self.field_info.validation_alias
        expected = list(PYDANTIC_KEY_VALUE.keys())[0]
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        fromheurist.mock_data.resource.single import ALIAS_KEY_VALUE

        actual = self.field_info.serialization_alias
        expected = list(ALIAS_KEY_VALUE.keys())[0]
        self.assertEqual(actual, expected)


class Enum(BaseCase):
    def setUp(self):
        fromheurist.mock_data.enum.single import METADATA

        builder = DynamicDataFieldBuilder(**METADATA)
        self.field = builder.term_id()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_alias(self):
        fromheurist.mock_data.enum.single import PYDANTIC_KEY_VALUE

        actual = self.field_info.validation_alias
        expected = list(PYDANTIC_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        fromheurist.mock_data.enum.single import ALIAS_KEY_VALUE

        actual = self.field_info.serialization_alias
        expected = list(ALIAS_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)


class FuzzyDate(BaseCase):
    def setUp(self):
        fromheurist.mock_data.date.simple.single import METADATA

        builder = DynamicDataFieldBuilder(**METADATA)
        self.field = builder.temporal_object()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_alias(self):
        fromheurist.mock_data.date.simple.single import PYDANTIC_KEY_VALUE

        actual = self.field_info.validation_alias
        expected = list(PYDANTIC_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        fromheurist.mock_data.date.simple.single import ALIAS_KEY_VALUE

        actual = self.field_info.serialization_alias
        expected = list(ALIAS_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
