import os
import unittest
import xml.etree.ElementTree as ET
import pygame
from pytmx import TiledObject
from models.Map import Map
from models.PoliceDepartment import PoliceDepartment

os.environ["SDL_VIDEODRIVER"] = "dummy"

class PoliceDepartmentTest(unittest.TestCase):
    def setUp(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Create a mock map instance for testing
        self.map_instance = Map(SCREEN,10,10)

    def test_police_department_initialization(self):
        x = 2
        y = 3
        creation_time = "2023-05-20"
        police_dept = PoliceDepartment(x, y, creation_time, self.map_instance)

        # Check if attributes are set correctly
        self.assertEqual(police_dept.x, x)
        self.assertEqual(police_dept.y, y)
        self.assertEqual(police_dept.price, PoliceDepartment.price)
        self.assertEqual(police_dept.creationTime, creation_time)

        # Check if the TiledObject instance is created properly
        self.assertIsInstance(police_dept.instance, TiledObject)
        

    def test_police_department_properties(self):
        x = 2
        y = 3
        creation_time = "2023-05-20"
        police_dept = PoliceDepartment(x, y, creation_time, self.map_instance)

        # Check if instance properties
        self.assertEqual(police_dept.instance.properties['Level'], 1)
        self.assertEqual(police_dept.instance.properties['Placeholder'], 'dynamic')
        self.assertEqual(police_dept.instance.properties['Citizens'], [])
        self.assertEqual(police_dept.instance.properties['CreationDate'], '2023-05-20')
        self.assertEqual(police_dept.instance.properties['Price'], '500')
        self.assertEqual(police_dept.instance.properties['Revenue'], 0)
        self.assertEqual(police_dept.instance.properties['MaintenanceFee'], 250)
        self.assertEqual(police_dept.instance.properties['Radius'], 4)
        self.assertEqual(police_dept.instance.properties['Satisfaction'], 0.15)
  

if __name__ == "__main__":
    unittest.main()
