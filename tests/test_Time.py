import os
import pygame
import unittest
from models.Utils import *
from models.Map import Map
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.zones.ResidentialZone import ResidentialZone

os.environ["SDL_VIDEODRIVER"] = "dummy"

class TestTime(unittest.TestCase):

    @unittest.skipIf(pygame.get_init() is None, "Skipping test due to non-graphical environment")
    def test_has_year_passed_from_creation(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        description_panel = DescriptionPanel(0, 0, SCREEN.get_width(), 32)
        builder_panel = BuilderPanel(0, 32, 96, SCREEN.get_height() - 32)
        map = Map(SCREEN, builder_panel.get_width(), description_panel.get_height())
        game_speed = 1
        timer = Timer(game_speed, 700)
        timer.update_time(False)
        timer.tick(60)
        x, y = 1, 1
        TiledObj = (ResidentialZone(x, y, timer.get_current_date_str(), map)).instance
        self.assertFalse(has_year_passed_from_creation(TiledObj, timer))

    @unittest.skipIf(pygame.get_init() is None, "Skipping test due to non-graphical environment")
    def test_has_month_passed_from_creation(self):
        game_speed = 1
        timer = Timer(game_speed, 700)
        timer.update_time(False)
        timer.tick(60)
        x, y = 1, 1

        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        description_panel = DescriptionPanel(0, 0, SCREEN.get_width(), 32)
        builder_panel = BuilderPanel(0, 32, 96, SCREEN.get_height() - 32)
        map = Map(SCREEN, builder_panel.get_width(), description_panel.get_height())
        TiledObj = (ResidentialZone(x, y, timer.get_current_date_str(), map)).instance

        self.assertFalse(has_month_passed_from_creation(TiledObj, timer))

    @unittest.skipIf(pygame.get_init() is None, "Skipping test due to non-graphical environment")
    def test_has_quarter_passed_from_creation(self):
        game_speed = 1
        timer = Timer(game_speed, 700)
        timer.update_time(False)
        timer.tick(60)
        x, y = 1, 1

        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        description_panel = DescriptionPanel(0, 0, SCREEN.get_width(), 32)
        builder_panel = BuilderPanel(0, 32, 96, SCREEN.get_height() - 32)
        map = Map(SCREEN, builder_panel.get_width(), description_panel.get_height())
        TiledObj = (ResidentialZone(x, y, timer.get_current_date_str(), map)).instance

        self.assertFalse(has_quarter_passed_from_creation(TiledObj, timer))

    def test_has_random_years_passed_from_start(self):
        game_speed = 1
        timer = Timer(game_speed, 700)
        timer.update_time(False)
        timer.tick(60)
        game_start_time = timer.get_current_date_str()

        self.assertFalse(has_random_years_passed_from_start(game_start_time, timer))

if __name__ == '__main__':
    unittest.main()
