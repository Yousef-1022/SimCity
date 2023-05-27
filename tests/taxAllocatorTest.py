import os
import unittest
from unittest.mock import MagicMock, patch
from models.TaxAllocator import TaskAllocator

os.environ["SDL_VIDEODRIVER"] = "dummy"

class TaxAllocatorTestCase(unittest.TestCase):
    def setUp(self):
        self.task_allocator = TaskAllocator()

    def test_get_input_text(self):
        # Set the input text to a specific value
        self.task_allocator.input_text = "Test input"

        # Call the get_input_text() method and assert the returned value
        self.assertEqual(self.task_allocator.get_input_text(), "Test input")


if __name__ == "__main__":
    unittest.main()
