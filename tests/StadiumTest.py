import os
import unittest
import xml.etree.ElementTree as ET
import pygame
from models.Map import Map
from models.Stadium import Stadium
from pytmx import TiledObject

os.environ["SDL_VIDEODRIVER"] = "dummy"

class StadiumTest(unittest.TestCase):
    def setUp(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Create a mock map instance for testing
        self.map_instance = Map(SCREEN, 10, 10)

    def test_stadium_initialization(self):
        x = 2
        y = 3
        creation_time = "2023-05-20"
        stadium = Stadium(x, y, creation_time, self.map_instance)

        # Check if attributes are set correctly
        self.assertEqual(stadium.x, x)
        self.assertEqual(stadium.y, y)
        self.assertEqual(stadium.price, Stadium.price)
        self.assertEqual(stadium.creationTime, creation_time)

        # Check if the TiledObject instance is created properly
        self.assertIsInstance(stadium.instance, TiledObject)

    def test_stadium_properties(self):
        x = 2
        y = 3
        creation_time = "2023-05-20"
        stadium = Stadium(x, y, creation_time, self.map_instance)

        # Check instance properties
        self.assertEqual(stadium.instance.properties['Level'], 1)
        self.assertEqual(stadium.instance.properties['Placeholder'], 'dynamic')
        self.assertEqual(stadium.instance.properties['Citizens'], [])
        self.assertEqual(stadium.instance.properties['CreationDate'], '2023-05-20')
        self.assertEqual(stadium.instance.properties['Price'], '600')
        self.assertEqual(stadium.instance.properties['Revenue'], 0)
        self.assertEqual(stadium.instance.properties['MaintenanceFee'], 300)
        self.assertEqual(stadium.instance.properties['Radius'], 6)
        self.assertEqual(stadium.instance.properties['Satisfaction'], 0.20)

if __name__ == "__main__":
    unittest.main()
