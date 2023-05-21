import os
import unittest
import xml.etree.ElementTree as ET
import pygame
from pytmx import TiledObject
from unittest.mock import MagicMock
from models.Map import Map
from models.Road import Road

os.environ["SDL_VIDEODRIVER"] = "dummy"

class RoadTest(unittest.TestCase):
    def setUp(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Create a mock map instance for testing
        self.map_instance = Map(SCREEN, 10, 10)

    def test_road_initialization(self):
        x = 5
        y = 10
        creation_time = "2023-05-20"
        road = Road(x, y, creation_time, self.map_instance)

        # Assert the attributes are set correctly
        self.assertEqual(road.x, x)
        self.assertEqual(road.y, y)
        self.assertEqual(road.creation_time, creation_time)
        self.assertEqual(road.price, Road.price)

        # Assert the instance property is set correctly
        self.assertIsInstance(road.instance, TiledObject)
        self.assertEqual(
            road.instance.gid, self.map_instance.get_static_object_by_type('Road').gid)
        self.assertEqual(
            road.instance.properties['MaintenanceFee'], int(Road.price / 4))

    def test_create_road_obj(self):
        x = 5
        y = 10
        creation_time = "2023-05-20"
        road = Road(x, y, creation_time, self.map_instance)

        # Call the create_road_obj function
        road_obj = road.create_road_obj(self.map_instance)

        # Assert the returned object is of type TiledObject
        self.assertIsInstance(road_obj, TiledObject)

        # Assert the object properties are set correctly
        self.assertEqual(
            road_obj.gid, self.map_instance.get_static_object_by_type('Road').gid)
        self.assertEqual(
            road_obj.properties['MaintenanceFee'], int(Road.price / 4))

        # check object properties
        self.assertEqual(road.instance.properties['Placeholder'], 'dynamic')
        self.assertEqual(
            road.instance.properties['CreationDate'], '2023-05-20')
        self.assertEqual(road.instance.properties['Price'], '75')
        self.assertEqual(road.instance.properties['MaintenanceFee'], 18)


if __name__ == '__main__':
    unittest.main()
