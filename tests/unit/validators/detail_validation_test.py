import unittest
from datetime import datetime

from heurist.validators.detail_validator import DetailValidator

URI = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg"


DATE_DEFAULT = {
    "comment": None,
    "value": None,
    "start": {
        "earliest": None,
        "latest": None,
        "estProfile": None,
        "estDetermination": None,
    },
    "end": {
        "earliest": None,
        "latest": None,
        "estProfile": None,
        "estDetermination": None,
    },
    "estDetermination": None,
    "estProfile": None,
    "timestamp": {"in": None, "type": None, "circa": False},
    "estMinDate": None,
    "estMaxDate": None,
}


class TestFile(unittest.TestCase):
    def setUp(self):
        from mock_data.file.single import DETAIL

        self.detail = DETAIL

    def test(self):
        expected = URI
        actual = DetailValidator.validate_file(self.detail)
        self.assertEqual(expected, actual)


class TestEnum(unittest.TestCase):
    def setUp(self):
        from mock_data.enum.single import DETAIL

        self.detail = DETAIL

    def test(self):
        expected = "dum (Middle Dutch)"
        actual = DetailValidator.validate_enum(self.detail)
        self.assertEqual(expected, actual)


class TestGeo(unittest.TestCase):
    def setUp(self):
        from mock_data.geo.single import DETAIL_POINT, DETAIL_POLYGON

        self.point_detail = DETAIL_POINT
        self.polygon_detail = DETAIL_POLYGON

    def test_point(self):
        expected = "POINT(2.19726563 48.57478991)"
        actual = DetailValidator.validate_geo(self.point_detail)
        self.assertEqual(expected, actual)

    def test_polygon(self):
        startswith = "POLYGON((-2.82548747 55.12653961,-2.82912354 55.12473717,\
            -2.83104469 55.12336704,"
        expected = startswith[:20]
        actual = DetailValidator.validate_geo(self.polygon_detail)[:20]
        self.assertEqual(expected, actual)


class TestDate(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.expected_result = DATE_DEFAULT.copy()
        return super().setUp()

    def test_simple_date(self):
        detail = {
            "dty_ID": 1000,
            "value": "2024-03-19",
        }
        self.expected_result.update(
            {
                "value": datetime(2024, 3, 19, 0, 0),
            }
        )
        actual_result = DetailValidator.validate_date(detail)
        self.assertDictEqual(actual_result, self.expected_result)

    def test_fuzzy_date(self):
        detail = {
            "value": {
                "start": {
                    "earliest": "1180",
                    "latest": "1231",
                    "profile": "1",
                },
                "end": {
                    "latest": "1250",
                    "earliest": "1246",
                    "profile": "3",
                },
                "determination": "2",
                "estMinDate": 1180,
                "estMaxDate": 1250.1231,
            },
        }
        self.expected_result.update(
            {
                "start": {
                    "earliest": datetime(1180, 1, 1, 0, 0),
                    "latest": datetime(1231, 1, 1, 0, 0),
                    "estProfile": "central",
                    "estDetermination": None,  # Don't forget to keep this null
                },
                "end": {
                    "earliest": datetime(1246, 1, 1, 0, 0),
                    "latest": datetime(1250, 1, 1, 0, 0),
                    "estProfile": "slowFinish",
                    "estDetermination": None,  # Don't forget to keep this null
                },
                "estDetermination": "conjecture",
                "estMinDate": datetime(1180, 1, 1, 0, 0),
                "estMaxDate": datetime(1250, 12, 31, 0, 0),
            }
        )
        actual_result = DetailValidator.validate_date(detail)
        self.assertDictEqual(actual_result, self.expected_result)


class TestResource(unittest.TestCase):
    def setUp(self):
        from mock_data.resource.single import DETAIL

        self.detail = DETAIL

    def test(self):
        expected = 36
        actual = DetailValidator.validate_resource(self.detail)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
