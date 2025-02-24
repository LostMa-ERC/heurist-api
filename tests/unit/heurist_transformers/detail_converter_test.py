import unittest
from datetime import datetime

from heurist.converters.detail_converter import RecordDetailConverter

URI = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg"


class TestFile(unittest.TestCase):
    def setUp(self):
        from heurist.mock_data.file.single import DETAIL

        self.detail = DETAIL

    def test(self):
        expected = URI
        actual = RecordDetailConverter.file(self.detail)
        self.assertEqual(expected, actual)


class TestEnum(unittest.TestCase):
    def setUp(self):
        from heurist.mock_data.enum.single import DETAIL

        self.detail = DETAIL

    def test(self):
        expected = "dum (Middle Dutch)"
        actual = RecordDetailConverter.enum(self.detail)
        self.assertEqual(expected, actual)


class TestGeo(unittest.TestCase):
    def setUp(self):
        from heurist.mock_data.geo.single import DETAIL_POINT, DETAIL_POLYGON

        self.point_detail = DETAIL_POINT
        self.polygon_detail = DETAIL_POLYGON

    def test_point(self):
        expected = "POINT(2.19726563 48.57478991)"
        actual = RecordDetailConverter.geo(self.point_detail)
        self.assertEqual(expected, actual)

    def test_polygon(self):
        startswith = "POLYGON((-2.82548747 55.12653961,-2.82912354 55.12473717,\
            -2.83104469 55.12336704,"
        expected = startswith[:20]
        actual = RecordDetailConverter.geo(self.polygon_detail)[:20]
        self.assertEqual(expected, actual)


class TestDate(unittest.TestCase):
    def setUp(self):
        from heurist.mock_data.date.fuzzy.single import DETAIL as DETAIL_FUZZY
        from heurist.mock_data.date.simple.single import DETAIL as DETAIL_SIMPLE

        self.fuzzy_date_detail = DETAIL_FUZZY
        self.simple_date_detail = DETAIL_SIMPLE

    def test_simple_date(self):
        expected = [datetime(2024, 3, 19, 0, 0), None]
        actual = RecordDetailConverter.date(self.simple_date_detail)
        self.assertListEqual(expected, actual)

    def test_fuzzy_date(self):
        expected = [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31, 0, 0)]
        actual = RecordDetailConverter.date(self.fuzzy_date_detail)
        self.assertListEqual(expected, actual)


class TestResource(unittest.TestCase):
    def setUp(self):
        from heurist.mock_data.resource.single import DETAIL

        self.detail = DETAIL

    def test(self):
        expected = 36
        actual = RecordDetailConverter.resource(self.detail)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
