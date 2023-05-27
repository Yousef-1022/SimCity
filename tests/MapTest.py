import os
import unittest
import pygame
from pytmx.util_pygame import load_pygame
from models.Map import Map
import unittest.mock
from models.Player import Player
from models.Road import Road
from models.Stadium import Stadium
from models.Tile import Tile


os.environ["SDL_VIDEODRIVER"] = "dummy"

class MapTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.map = Map(self.screen, 200, 100)

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.map._Map__screen, self.screen)
        self.assertEqual(self.map._Map__panel_width, 200)
        self.assertEqual(self.map._Map__panel_height, 100)
        self.assertEqual(self.map._Map__scroll_x, 0)
        self.assertEqual(self.map._Map__scroll_y, 0)
        self.assertEqual(self.map._Map__objcount, 0)



    def test_handle_scroll(self):
        # Set up initial scroll values and map dimensions
        self.map._Map__scroll_x = 0
        self.map._Map__scroll_y = 0
        self.map._Map__map.width = 5
        self.map._Map__map.height = 5
        self.map._Map__map.tilewidth = 32
        self.map._Map__map.tileheight = 32

        # Set up event key mock values
        event_left = pygame.K_LEFT
        event_right = pygame.K_RIGHT
        event_up = pygame.K_UP
        event_down = pygame.K_DOWN

        # Mock the pygame module and test different key presses
        with unittest.mock.patch('pygame.K_LEFT', event_left), \
             unittest.mock.patch('pygame.K_RIGHT', event_right), \
             unittest.mock.patch('pygame.K_UP', event_up), \
             unittest.mock.patch('pygame.K_DOWN', event_down):

            # Test left arrow key
            self.map.handle_scroll(pygame.K_LEFT)
            self.assertEqual(self.map._Map__scroll_x - 32, -32)

            # Test right arrow key
            self.map.handle_scroll(pygame.K_RIGHT)
            self.assertEqual(self.map._Map__scroll_x, 0)

            # Test up arrow key
            self.map.handle_scroll(pygame.K_UP)
            self.assertEqual(self.map._Map__scroll_y - 32, -32)

            # Test down arrow key
            self.map.handle_scroll(pygame.K_DOWN)
            self.assertEqual(self.map._Map__scroll_y, 0)

            # Test unknown key (should not change scroll values)
            self.map.handle_scroll(pygame.K_SPACE)
            self.assertEqual(self.map._Map__scroll_x, 0)
            self.assertEqual(self.map._Map__scroll_y, 0)


    def test_add_object_can_be_added(self):
        # Set up initial conditions
        self.map._Map__objcount = 0
        self.map._Map__map.nextobjectid = 1
        obj_layer_mock = unittest.mock.Mock()
        self.map._Map__map.get_layer_by_name = unittest.mock.Mock(return_value=obj_layer_mock)
        obj = Road(33,33, "2023-05-20" , self.map)
        player = Player("Abood", 10000)
        obj.properties = {'Price': '100'}
        obj.type =  'Road'

        # Mock collide_with_objects and collide_with_water to return False
        with unittest.mock.patch.object(self.map, 'collide_with_objects', return_value=False), \
             unittest.mock.patch.object(self.map, 'collide_with_water', return_value=False):

            # Call add_object method
            result = self.map.add_object(obj, player)

            # Verify that the object is added to the objLayer
            obj_layer_mock.append.assert_called_once_with(obj)

            # Verify that the player's money is updated
            self.assertEqual(player.money,  9900)

            # Verify that the objcount and nextobjectid are incremented
            self.assertEqual(self.map._Map__objcount, 1)
            self.assertEqual(self.map._Map__map.nextobjectid, 2)

            # Verify that the returned object is the same as the input object
            self.assertIs(result, obj)
