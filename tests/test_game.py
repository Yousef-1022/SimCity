import os
import pygame
import unittest
from models.Utils import *
from models.Map import Map
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.zones.ResidentialZone import ResidentialZone

# Set the display driver to dummy
os.environ["SDL_VIDEODRIVER"] = "dummy"

class TestGame(unittest.TestCase):

    def test_getFilesFromDir(self):
        """Returns all the files as a list from the given path"""
        all_files = [
            'icon1_bulldozer.png', 
            'icon2_road.png', 
            'icon3_PoliceDepartment.png', 
            'icon4_Stadium.png', 
            'icon5_ResidentialZone.png', 
            'icon6_IndustrialZone.png', 
            'icon7_ServiceZone.png', 
            'icon8_Forest.png', 
            'icon9_Disaster.png'
        ]
        filepath = "./Map/Assets/Builder_assets/"
        
        assert len(all_files) == len(get_files_from_dir(filepath))

    def test_get_icons_and_types(self):
        all_icons_and_types = [
            ('./Map/Assets/Builder_assets/icon1_bulldozer.png', 'bulldozer'), 
            ('./Map/Assets/Builder_assets/icon2_road.png', 'road'), 
            ('./Map/Assets/Builder_assets/icon3_PoliceDepartment.png', 'PoliceDepartment'), 
            ('./Map/Assets/Builder_assets/icon4_Stadium.png', 'Stadium'), 
            ('./Map/Assets/Builder_assets/icon5_ResidentialZone.png', 'ResidentialZone'), 
            ('./Map/Assets/Builder_assets/icon6_IndustrialZone.png', 'IndustrialZone'), 
            ('./Map/Assets/Builder_assets/icon7_ServiceZone.png', 'ServiceZone'), 
            ('./Map/Assets/Builder_assets/icon8_Forest.png', 'Forest'), 
            ('./Map/Assets/Builder_assets/icon9_Disaster.png', 'Disaster')
        ]

        icons_dir = "./Map/Assets/Builder_assets/"
        icons = [get_icon_and_type(f, icons_dir) for f in get_files_from_dir(icons_dir)]
        assert len(all_icons_and_types) == len(icons)

    def test_get_icon_loc_by_name(self):
        icons_dir = "./Map/Assets/Builder_assets/"
        icons = [get_icon_and_type(f, icons_dir) for f in get_files_from_dir(icons_dir)]

        cursorImg = pygame.image.load(get_icon_loc_by_name("bulldozer", icons))
        cursorImgRect = cursorImg.get_rect()
        my_cursor = "<rect(0, 0, 70, 70)>"
        assert my_cursor == str(cursorImgRect)

    def test_has_year_passed_from_creation(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        description_panel = DescriptionPanel(0, 0, SCREEN.get_width(), 32)
        builder_panel = BuilderPanel(0, 32, 96, SCREEN.get_height() - 32)
        map = Map(SCREEN, builder_panel.getWidth(), description_panel.getHeight())
        game_speed = 1
        timer = Timer(game_speed, 700)
        timer.update_time(False)
        timer.tick(60)
        x, y = 1, 1
        TiledObj = (ResidentialZone(x, y, timer.get_current_date_str(), map)).instance
        # TiledObj.properties['CreationDate'] = "2022-05-02"
        print(TiledObj.properties['CreationDate'], timer.get_current_date_str(), "BIGG")
        print("SDfsdf")
        assert False == has_year_passed_from_creation(TiledObj, timer)

if __name__ == '__main__':
    unittest.main()

