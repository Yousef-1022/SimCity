import pygame , sys
from models.Map import Map
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.Panels.PricePanel import PricePanel
from models.Zones.ResidentialZone import ResidentialZone
from models.Zones.IndustrialZone import IndustrialZone
from models.Zones.ServiceZone import ServiceZone
from models.PoliceDepartment import PoliceDepartment
from models.Stadium import Stadium
from models.Utils import getIconAndType , getFilesFromDir , getIconLocByName

pygame.init()

# Game static variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCROLL_SPEED = 5

# Map & Panels
description_panel = DescriptionPanel(0,0, SCREEN.get_width(), 32)
builder_panel = BuilderPanel(0,32,96,SCREEN.get_height() - 32)
price_panel = PricePanel(96, SCREEN.get_height() - 32, SCREEN.get_width() - 96, 32)
icons_dir = "./Map/Assets/Builder_assets/"
icons = [getIconAndType(f,icons_dir) for f in getFilesFromDir(icons_dir)]
map = Map(SCREEN, builder_panel.getWidth(), description_panel.getHeight())
class_tobuild = ""

def run():
    
    normal_cursor = True
    cursorImg = pygame.image.load(getIconLocByName("bulldozer",icons))
    cursorImgRect = cursorImg.get_rect()
    
    while True:
        
        cursorImgRect.center = pygame.mouse.get_pos()
        map.display()
        description_panel.display(SCREEN,24,(10,10),(128,128,128),"Funds: 2000 , more industrial zones needed",(255,255,255))
        price_panel.display(SCREEN,24,(96, SCREEN.get_height() - 20),(128,128,128),"$100 Road",(255,255,255))
        builder_panel.display(SCREEN,0,(0,0),(90,90,90),"",(0,0,0))
        builder_panel.display_assets(SCREEN,icons)
        
        for event in pygame.event.get(): # mouse button click, keyboard, or the x button.
            if pygame.mouse.get_pressed()[2]:
                normal_cursor = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:    # Cursor handling
                mouse_pos = pygame.mouse.get_pos()
                selected_icon = builder_panel.get_selected_icon_index(mouse_pos) 
                if (not normal_cursor):
                    x,y = map.getClickedTile(mouse_pos)
                    if  x == -1 or y == -1:
                        normal_cursor= True 
                    else:
                        # Handle object creation
                        class_obj = globals().get(class_tobuild)
                        obj = ""
                        if class_obj is not None:
                            obj = class_obj(x-1,y-1,map)    # Change
                            map.addObject(obj.instance)
                            class_tobuild = -1
                        else:
                            print(f"Can't build class: {class_tobuild} because it doesn't exist")
                        normal_cursor = True
                if selected_icon != None:
                    # Handle cursor at selection
                    cursorImgRect = cursorImg.get_rect()
                    cursorImg = pygame.transform.scale(pygame.image.load(icons[selected_icon][0]), (128,128))
                    cursorImgRect.center = mouse_pos
                    normal_cursor = False
                    class_tobuild = icons[selected_icon][1]
            elif event.type == pygame.KEYDOWN:  # Scroll handling
                map.handleScroll(event.key)
                
        if not normal_cursor:
            SCREEN.blit(cursorImg, cursorImgRect)
            
        pygame.display.update()
        SCREEN.fill((0, 0, 0))