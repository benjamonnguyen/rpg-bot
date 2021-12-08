import unittest
import logging

from src.utils import app_logger


class MyTestCase(unittest.TestCase):
    logging.basicConfig()
    app_logger.setLevel(logging.DEBUG)

    def test_interval_settings_value_error(self):
        from src.models.IntervalSettings import IntervalSettings
        self.assertRaises(ValueError, IntervalSettings, 181, None, None, None)
        self.assertRaises(ValueError, IntervalSettings, -1, None, None, None)
        self.assertIsNotNone(IntervalSettings(180, None, None, None))
        self.assertRaises(ValueError, IntervalSettings, 150, None, 181, None)
        self.assertRaises(ValueError, IntervalSettings, None, -1, None, 150)


if __name__ == '__main__':
    unittest.main()
