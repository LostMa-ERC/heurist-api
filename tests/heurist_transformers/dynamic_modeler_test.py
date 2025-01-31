import unittest

from pydantic.fields import FieldInfo
from pydantic import create_model

from src.heurist_transformers.dynamic_pydantic_data_field import DynamicDataFieldBuilder

FREETEXT_FIELD = {
    "dty_ID": 1244,
    "rst_DisplayName": "preferred_name",
    "dty_Type": "freetext",
    "rst_MaxValues": 1,
}

ENUM_FIELD = {
    "dty_ID": 1090,
    "rst_DisplayName": "language",
    "dty_Type": "enum",
    "rst_MaxValues": 1,
}

RESOURCE_FIELD = {
    "dty_ID": 1097,
    "rst_DisplayName": "is_expression_of",
    "dty_Type": "resource",
    "rst_MaxValues": 0,
}

DATE_FIELD = {
    "dty_ID": 1285,
    "rst_DisplayName": "date_of_creation",
    "dty_Type": "date",
    "rst_MaxValues": 1,
}

REPEATED_DATE_FIELD = {
    "dty_ID": 1285,
    "rst_DisplayName": "date_of_creation",
    "dty_Type": "date",
    "rst_MaxValues": 0,
}


def get_field_info_from_dict(d: dict) -> FieldInfo:
    return tuple(d.values())[0][1]


class TestResource(unittest.TestCase):
    def setUp(self):
        builder = DynamicDataFieldBuilder(**RESOURCE_FIELD)
        self.field = builder.simple_field()
        self.field_info = get_field_info_from_dict(self.field)

    def test_serialization_alias(self):
        """Test that a record pointer's serlialization alias has H-ID at the end."""
        actual = self.field_info.serialization_alias
        expected = "is_expression_of H-ID"
        self.assertEqual(actual, expected)

    def test_array_validation(self):
        """Test that a field that should be repeatable correctly validates an array."""
        multiple_pointers = ["1", "2", "3"]
        data = {"DTY1097": multiple_pointers}

        model = create_model("TestTable", **self.field)
        actual = model.model_validate(data).model_dump(by_alias=True)
        expected = {"is_expression_of H-ID": multiple_pointers}
        self.assertEqual(actual, expected)


class TestEnum(unittest.TestCase):
    def setUp(self):
        builder = DynamicDataFieldBuilder(**ENUM_FIELD)
        self.field = builder.term_id()
        self.field_info = get_field_info_from_dict(self.field)

    def test_serialization_alias(self):
        actual = self.field_info.serialization_alias
        expected = "language_COLUMN TRM-ID"
        self.assertEqual(actual, expected)

    def test_validation_alias(self):
        actual = self.field_info.validation_alias
        expected = "DTY1090_TRM"
        self.assertEqual(actual, expected)


class TestDate(unittest.TestCase):
    def setUp(self):
        builder = DynamicDataFieldBuilder(**DATE_FIELD)
        self.field = builder.temporal_object()
        self.field_info = get_field_info_from_dict(self.field)

    def test_serialization_alias(self):
        actual = self.field_info.serialization_alias
        expected = "date_of_creation_TEMPORAL"
        self.assertEqual(actual, expected)

    def test_validation_alias(self):
        actual = self.field_info.validation_alias
        expected = "DTY1285_TEMPORAL"
        self.assertEqual(actual, expected)

    def test_validation(self):
        model = create_model("TestTable", **self.field)
        data = {"DTY1285_TEMPORAL": {"estMinDate": 1400, "estMaxDate": 1430.1231}}
        actual = model.model_validate(data).model_dump(by_alias=True)
        expected = {
            "date_of_creation_TEMPORAL": {"estMinDate": 1400, "estMaxDate": 1430.1231}
        }
        self.assertEqual(actual, expected)


class TestRepeatedDate(unittest.TestCase):
    def setUp(self):
        builder = DynamicDataFieldBuilder(**REPEATED_DATE_FIELD)
        self.field = builder.temporal_object()
        self.field_info = get_field_info_from_dict(self.field)

    def test_validation_of_repeated_value(self):
        model = create_model("TestTable", **self.field)
        data = {
            "DTY1285_TEMPORAL": [
                {"estMinDate": 1400, "estMaxDate": 1430.1231},
                {"estMinDate": 1440, "estMaxDate": 1450.1231},
            ]
        }
        actual = model.model_validate(data).model_dump(by_alias=True)
        expected = {
            "date_of_creation_TEMPORAL": [
                {"estMinDate": 1400, "estMaxDate": 1430.1231},
                {"estMinDate": 1440, "estMaxDate": 1450.1231},
            ]
        }
        self.assertEqual(actual, expected)


class TestReservedColumn(unittest.TestCase):
    def setUp(self):
        builder = DynamicDataFieldBuilder(**ENUM_FIELD)
        self.field = builder.simple_field()
        self.field_info = get_field_info_from_dict(self.field)

    def test_reserved_column_name(self):
        actual = self.field_info.serialization_alias
        expected = "language_COLUMN"
        self.assertEqual(actual, expected)


class TestFreetext(unittest.TestCase):
    def setUp(self):
        builder = DynamicDataFieldBuilder(**FREETEXT_FIELD)
        self.field = builder.simple_field()
        self.field_info = get_field_info_from_dict(self.field)

    def test_description(self):
        actual = self.field_info.description
        expected = 1244
        self.assertEqual(actual, expected)

    def test_serialization_alias(self):
        actual = self.field_info.serialization_alias
        expected = "preferred_name"
        self.assertEqual(actual, expected)

    def test_validation_alias(self):
        actual = self.field_info.validation_alias
        expected = "DTY1244"
        self.assertEqual(actual, expected)

    def test_validation(self):
        model = create_model("TestTable", **self.field)
        data = {"DTY1244": "Name"}
        actual = model.model_validate(data).model_dump(by_alias=True)
        expected = {"preferred_name": "Name"}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
