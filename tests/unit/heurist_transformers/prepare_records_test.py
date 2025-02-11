import unittest

from src.heurist_transformers.prepare_records import RecordFlattener
from src.heurist_transformers.dynamic_record_type_modeler import DynamicRecordTypeModel
from src import TABLES_LOG, DATABASE_LOG


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
    from examples.resource.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        from examples.resource import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedResource(BaseCase):
    from examples.resource.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        from examples.resource import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class SingularFuzzyDate(BaseCase):
    from examples.date.fuzzy.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        from examples.date.fuzzy import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedFuzzyDate(BaseCase):
    from examples.date.fuzzy.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        from examples.date.fuzzy import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class SingularSimpleDate(BaseCase):
    from examples.date.simple.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        from examples.date.simple import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedSimpleDate(BaseCase):
    from examples.date.simple.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test(self):
        from examples.date.simple import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class SingularEnum(BaseCase):
    from examples.enum.single import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test_value(self):
        from examples.enum import single

        actual = self.flattener(record_details=[single.DETAIL])
        expected = single.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


class RepeatedEnum(BaseCase):
    from examples.enum.repeated import METADATA

    def setUp(self, metadata=METADATA):
        return super().setUp(metadata)

    def test_value(self):
        from examples.enum import repeated

        actual = self.flattener(record_details=repeated.DETAIL)
        expected = repeated.PYDANTIC_KEY_VALUE
        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
