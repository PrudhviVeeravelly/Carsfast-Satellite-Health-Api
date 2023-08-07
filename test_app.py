import unittest
from unittest.mock import patch, MagicMock
from app import check_health

class TestSatelliteHealth(unittest.TestCase):

    def setUp(self):
        # Set up a default value for the global variable last_warning_time
        self.last_warning_time = None

    # Test when the average altitude is less than 160 and no previous warning
    def test_health_below_160_no_warning(self):
        prev_1min_data = [{'altitude': '159.0'}, {'altitude': '158.0'}, {'altitude': '157.0'}]
        result = check_health(prev_1min_data)
        self.assertEqual(result, "WARNING: RAPID ORBITAL DECAY IMMINENT")

    # Test when the average altitude is less than 160 and previous warning less than 60 seconds ago
    def test_health_below_160_warning_recent(self):
        prev_1min_data = [{'altitude': '159.0'}, {'altitude': '158.0'}, {'altitude': '157.0'}]
        self.last_warning_time = 1000
        with patch('app.time') as mock_time:
            mock_time.time.return_value = 1029  # 29 seconds later
            result = check_health(prev_1min_data)
            self.assertEqual(result, "Altitude is A-OK")

    # Test when the average altitude is 160 or above and a previous warning was issued
    def test_health_above_160_with_warning(self):
        prev_1min_data = [{'altitude': '161s.0'}, {'altitude': '162.0'}, {'altitude': '163.0'}]
        self.last_warning_time = 1000
        with patch('app.time') as mock_time:
            mock_time.time.return_value = 1061  # 61 seconds later
            result = check_health(prev_1min_data)
            self.assertEqual(result, "Sustained Low Earth Orbit Resumed")

    # Test when the average altitude is 160 or above and no previous warning
    def test_health_above_160_no_warning(self):
        prev_1min_data = [{'altitude': '161.0'}, {'altitude': '162.0'}, {'altitude': '163.0'}]
        result = check_health(prev_1min_data)
        self.assertEqual(result, "Altitude is A-OK")

if __name__ == '__main__':
    unittest.main()