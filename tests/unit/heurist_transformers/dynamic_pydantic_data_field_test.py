import unittest

from pydantic.fields import FieldInfo

from src.heurist_transformers.dynamic_pydantic_data_field import DynamicDataFieldBuilder


def get_field_info_from_dict(d: dict) -> FieldInfo:
    return tuple(d.values())[0][1]


class Resource(unittest.TestCase):
    def setUp(self):
        from examples.resource.single import METADATA

        builder = DynamicDataFieldBuilder(**METADATA)
        self.field = builder.simple_field()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_alias(self):
        from examples.resource.single import PYDANTIC_KEY_VALUE

        actual = self.field_info.validation_alias
        expected = list(PYDANTIC_KEY_VALUE.keys())[0]
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        from examples.resource.single import ALIAS_KEY_VALUE

        actual = self.field_info.serialization_alias
        expected = list(ALIAS_KEY_VALUE.keys())[0]
        self.assertEqual(actual, expected)


class Enum(unittest.TestCase):
    def setUp(self):
        from examples.enum.single import METADATA

        builder = DynamicDataFieldBuilder(**METADATA)
        self.field = builder.term_id()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_alias(self):
        from examples.enum.single import PYDANTIC_KEY_VALUE

        actual = self.field_info.validation_alias
        expected = list(PYDANTIC_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        from examples.enum.single import ALIAS_KEY_VALUE

        actual = self.field_info.serialization_alias
        expected = list(ALIAS_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)


class FuzzyDate(unittest.TestCase):
    def setUp(self):
        from examples.date.simple.single import METADATA

        builder = DynamicDataFieldBuilder(**METADATA)
        self.field = builder.temporal_object()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_alias(self):
        from examples.date.simple.single import PYDANTIC_KEY_VALUE

        actual = self.field_info.validation_alias
        expected = list(PYDANTIC_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        from examples.date.simple.single import ALIAS_KEY_VALUE

        actual = self.field_info.serialization_alias
        expected = list(ALIAS_KEY_VALUE.keys())[1]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
