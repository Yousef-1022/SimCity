import pygame , sys
from models.Map import Map
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.Panels.PricePanel import PricePanel
from models.zones.ResidentialZone import ResidentialZone
from models.zones.IndustrialZone import IndustrialZone
from models.zones.ServiceZone import ServiceZone
from models.PoliceDepartment import PoliceDepartment
from models.Stadium import Stadium
from models.Player import Player
from models.Timer import Timer
from models.Utils import *
from models.Road import Road
from models.GridSystem import GridSystem
from models.Citizen import Citizen
import random

pygame.init()

# Game static variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCROLL_SPEED = 5
MONEY_PER_DAY = 20
TAX_VARIABLE = 0.05

# Map & Panels
description_panel = DescriptionPanel(0,0, SCREEN.get_width(), 32)
builder_panel = BuilderPanel(0,32,96,SCREEN.get_height() - 32)
price_panel = PricePanel(96, SCREEN.get_height() - 32, SCREEN.get_width() - 96, 32)
icons_dir = "./Map/Assets/Builder_assets/"
icons = [get_icon_and_type(f,icons_dir) for f in get_files_from_dir(icons_dir)]
map = Map(SCREEN, builder_panel.getWidth(), description_panel.getHeight())
class_tobuild = ""

# Game simulation variables
player = Player("HUMAN", 100000)
game_speed  = 1
timer = Timer(game_speed, 200)
paused  = False

# Initialize grid system.
Grid = GridSystem(map)

def run():
    normal_cursor = True
    cursorImg = pygame.image.load(get_icon_loc_by_name("bulldozer",icons))
    cursorImgRect = cursorImg.get_rect()
    day = timer.get_current_time().day
    month = timer.get_current_time().month
    initial_citizens = []
    for i in range (1,11):
        c = Citizen()
        initial_citizens.append(c)
    
    while True:
        cursorImgRect.center = pygame.mouse.get_pos()
        map.display()

        description_panel.display(SCREEN,24,(10,10),(128,128,128),f"Funds: {player.money}$ , more industrial zones needed",(255,255,255))
        description_panel.displayTime(SCREEN,f"Time: {timer.get_current_date_str()}",(500,10))
        price_panel.display(SCREEN,24,(96, SCREEN.get_height() - 20),(128,128,128),"$100 Road",(255,255,255))
        builder_panel.display(SCREEN,0,(0,0),(90,90,90),"",(0,0,0))
        builder_panel.display_assets(SCREEN,icons)
        
    
        # Citizen adding Logic
        if (len(initial_citizens) != 0): # Initial edge case
            if len (map.get_residential_zones()) != 0:
                first_R_Zone = map.get_residential_zones()[0]
                for c in initial_citizens:
                    assign_to_residential_zone(c,first_R_Zone,map)
                    initial_citizens.remove(c)

        if(timer.get_current_time().month != month):   
            add_citizens_to_game(map)
            for zone in map.get_residential_zones():
                assign_zone_citizens_to_work(zone, map)
            month = timer.get_current_time().month
        
        # Zones and (Buildings,Roads) Expense Logic 
        if(timer.get_current_time().day != day):
            for obj in map.get_all_objects():
                # Handle Buildings,Roads
                if obj.type == "Road" or obj.type == "PoliceDepartment" or obj.type == "Stadium":
                    if(has_year_passed_from_creation(obj,timer)):
                        player.money -= obj.properties['MaintenanceFee'] 
                else:
                    # Deduct MaintenanceFees for any Zone from Player
                    if(has_quarter_passed_from_creation(obj,timer)):
                        player.money -= obj.properties['MaintenanceFee']
                    # IncreaseRevenue of each WorkZone per day
                    total_citizens = len(obj.properties['Citizens'])
                    if(obj.type != "ResidentialZone" and total_citizens != 0):
                        obj.properties['Revenue'] += (MONEY_PER_DAY * total_citizens)
                    # Get revenue (TAX) from WorkZone to Player
                    elif(obj.type != "ResidentialZone" and has_year_passed_from_creation(obj,timer)):
                        revenue = obj.properties['Revenue'] * TAX_VARIABLE
                        player.money += revenue
                        obj.properties['Revenue'] = 0
            day = timer.get_current_time().day
            
            
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
                            if class_tobuild == "Road":
                                obj = class_obj(x,y,timer.get_current_date_str(),map)    # Change
                            else:
                                obj = class_obj(x - 1,y - 1,timer.get_current_date_str(),map)    # Change

                            obj = map.addObject(obj.instance,player)
                            class_tobuild = -1
                        else:
                            map.remove_road(x,y,"Road", map)
                            #print(f"Can't build class: {class_tobuild} because it doesn't exist")
                        normal_cursor = True
                if selected_icon != None:
                    # Handle cursor at selection
                    cursorImgRect = cursorImg.get_rect()
                    image_size = get_image_size(icons[selected_icon][1])
                    cursorImg = pygame.transform.scale(pygame.image.load(icons[selected_icon][0]), (image_size,image_size))
                    cursorImgRect.center = pygame.mouse.get_pos()
                    normal_cursor = False
                    class_tobuild = icons[selected_icon][1]
            elif event.type == pygame.KEYDOWN:  # Scroll handling
                map.handleScroll(event.key)
        
        if not normal_cursor:
            SCREEN.blit(cursorImg, cursorImgRect)
        # Limit the frame rate to 60 FPS
        timer.update_time(paused)
        timer.tick(60)
        pygame.display.update()
        SCREEN.fill((0, 0, 0))
