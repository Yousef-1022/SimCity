import unittest
import pygame
from models.Utils import *

class TestAssets(unittest.TestCase):

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
        
        self.assertEqual(len(all_files), len(get_files_from_dir(filepath)))

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
        self.assertEqual(len(all_icons_and_types), len(icons))

    def test_get_icon_loc_by_name(self):
        icons_dir = "./Map/Assets/Builder_assets/"
        icons = [get_icon_and_type(f, icons_dir) for f in get_files_from_dir(icons_dir)]

        cursorImg = pygame.image.load(get_icon_loc_by_name("bulldozer", icons))
        cursorImgRect = cursorImg.get_rect()
        my_cursor = "<rect(0, 0, 70, 70)>"
        self.assertEqual(str(cursorImgRect), my_cursor)

if __name__ == '__main__':
    unittest.main()
