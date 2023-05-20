import unittest
import datetime
import pygame
from models.Timer import Timer

class TimerTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.timer = Timer(30, 2)  # Create a Timer object

    def test_get_current_time(self):
        current_time = self.timer.get_current_time()
        self.assertIsInstance(current_time, datetime.datetime, "Returned value is not a datetime object")

    def test_get_current_date_str(self):
        current_date_str = self.timer.get_current_date_str()
        self.assertRegex(current_date_str, r"\d{4}-\d{2}-\d{2}", "Returned value does not have the correct format")

    def test_update_time(self):
        paused = False
        initial_time = self.timer.get_current_time()
        self.timer.update_time(paused)
        new_time = self.timer.get_current_time()
        self.assertGreater(new_time, initial_time, "Current time was not updated correctly")

    def test_subtract_with_time_str(self):
        date_str = "2022-05-01"
        diff_in_days = self.timer.subtract_with_time_str(date_str)
        expected_diff = (datetime.datetime.now() - datetime.datetime.strptime(date_str, "%Y-%m-%d")).days
        self.assertEqual(diff_in_days, expected_diff, "Difference in days was not calculated correctly")

    def test_get_timer_from_str(self):
        str_date = "2022-05-01"
        timer_date = self.timer.get_timer_from_str(str_date)
        expected_date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
        self.assertEqual(timer_date, expected_date, "Returned value is not the expected datetime object")

if __name__ == '__main__':
    unittest.main()
