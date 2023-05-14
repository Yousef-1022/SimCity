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
from models.Forest import Forest
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

def is_there_a_blocker_between(Frst:TiledObject,RZone:TiledObject,lst):
    """
    Get the points which represent the view of the RZone and the Forest,
    Checks if there is a blocker between the Forest and the RZone
    
    Args:
    Frst: Forest TiledObject
    RZone: ResidentialZone TiledObject
    lst: list consisting of all dynamic objects
    """
    wall = get_points_looking_at_each_other(Frst,RZone)
    mid = len(wall) // 2
    l1 = wall[:mid]
    l2 = wall[mid:]
    res = [get_path_between_points(p1,p2) for p1, p2 in zip(l1, l2)]
    flattened_res = [item for sublist in res for item in sublist]
    for obj in lst:
        if ((obj != Frst or obj != RZone) and obj.type != 'Road'):
            s1 = set(get_area(obj))
            s2 = set(flattened_res)
            if s1.intersection(s2):
                return True
    return False

def handle_citizen_addition_satisfaction(c:Citizen):
    """
    After assigning a citizen to an RZone, checks nearby SatisfactionIncreasers and adds accordingly
    """
    for SZone in map.get_satisfaction_increasers():
        if (distance_between_two(c.home,SZone) <= SZone.properties['Radius']):
            if (SZone.type == "Forest"):
                if(is_there_a_blocker_between(c.home,SZone,map.get_all_objects())):
                    continue
                else:
                    c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
            else:
                c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)

        
def handle_satisfaction_zone_addition(SZone:TiledObject):
    """
    After the player creates a Stadium, PoliceDepartment, or Forest, it checks nearby Citizens and adds satisfaction
    """
    for RZone in map.get_residential_zones():
        if (distance_between_two(RZone,SZone) <= SZone.properties['Radius']):
            if (SZone.type == "Forest"):
                if(is_there_a_blocker_between(RZone,SZone,map.get_all_objects())):
                    continue
                else:
                    for c in RZone.properties['Citizens']:
                        c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
            else:
                for c in RZone.properties['Citizens']:
                    c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
            
def handle_satisfaction_zone_removal(SZone:TiledObject):
    """
    After the player deletes a Stadium or PoliceDepartment, it checks nearby Citizens and decreases satisfaction
    """
    for RZone in map.get_residential_zones():
        if (distance_between_two(RZone,SZone) <= SZone.properties['Radius'] and SZone.type != "Forest"):
            for c in RZone.properties['Citizens']:
                c.satisfaction -= (SZone.properties['Satisfaction']*c.satisfaction)

def handle_prompt(clckd_crds,clckd_zn,upgrd,rclssfy):
    """
    Handles prompt when viewing the information of the Zone
    """
    if clckd_crds:
        if (clckd_zn):
            # Handle already clicked Zone
            if(clckd_zn.properties['Level'] <= 3):
                btn = map.draw_prompt(clckd_crds,clckd_zn)
                if (len(clckd_zn.properties['Citizens']) == 0):
                    upgrd = None
                    rclssfy = btn
                else:
                    upgrd = btn
                    rclssfy = None
            else:
                upgrd = rclssfy = None
        else:
            # Reterive the Zone if not clicked in the first place
            zones = map.get_residential_zones() + map.get_work_zones()
            clckd_zn = tile_in_which_zone(map.getClickedTile(clckd_crds),zones)
            if (clckd_zn):
                if(clckd_zn.properties['Level'] <= 3):
                    btn = map.draw_prompt(clckd_crds,clckd_zn)
                    if (len(clckd_zn.properties['Citizens']) == 0):
                        upgrd = None
                        rclssfy = btn
                    else:
                        upgrd = btn
                        rclssfy = None
                else:
                    upgrd = rclssfy = None
    return clckd_crds, clckd_zn, upgrd, rclssfy
    

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
    
    clicked_cords = None
    clicked_zone = None
    upgrade = None
    reclassify = None

    
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
            RZones = map.get_residential_zones()
            if(len(RZones) > 0):
                RZone = random.choice(RZones)
                for c in initial_citizens:
                    c.assign_to_residential_zone(RZone,map)
                    handle_citizen_addition_satisfaction(c)
                    initial_citizens.remove(c)
            
        if(timer.get_current_time().month != month):
            RZones = map.get_residential_zones()
            if len(RZones) > 0:
                s = Citizen.get_current_satisfaction()
                curr_per = s*100/Citizen.get_max_possible_satisfaction()
                # Amount of citizens possible to be added depends on current overall satisfaction
                if (curr_per >= 25):
                    n = int(curr_per / 100 * 10)
                    for _ in range (n):
                        RZone = random.choice(RZones)
                        if RZone.properties['Capacity'] != len(RZone.properties['Citizens']):
                            c = Citizen()
                            c.assign_to_residential_zone(RZone,map)
                else:
                    # Random amount of sad citizens leave
                    lst = Citizen.get_sad_citizens(20)
                    if len(lst) > 0:
                        to_remove = random.randint(0, len(lst) - 1)
                        for i in range(to_remove):
                            lst[i].delete_citizen()
            month = timer.get_current_time().month
        
        
        # Zones and (Buildings,Roads,Forest) Expense Logic 
        if(timer.get_current_time().day != day):
            for obj in map.get_all_objects():
                did_a_quarter_pass = has_quarter_passed_from_creation(obj,timer)
                did_a_year_pass = has_year_passed_from_creation(obj,timer)
                
                # Handle ServiceBuildings,Roads Expense
                if obj.type == "Road" or obj.type == "PoliceDepartment" or obj.type == "Stadium":
                    if(did_a_year_pass):
                        player.money -= obj.properties['MaintenanceFee']
                        
                # Handle Forest Expense and Grow
                elif obj.type == "Forest":
                    if(did_a_year_pass):
                        if obj.properties['Mature']:
                            player.money -= obj.properties['MaintenanceFee']
                        else:
                            obj.properties['Year'] += 1
                            obj.properties['Satisfaction'] += 0.03
                            # Handle tree update
                            if obj.properties['Year'] == 10:
                                obj.properties['Mature'] = True
                # Handle Zones Expense
                else:
                    # Deduct MaintenanceFees for any Zone from Player
                    if(did_a_quarter_pass):
                        player.money -= obj.properties['MaintenanceFee']
                    # IncreaseRevenue of each WorkZone per day
                    total_citizens = len(obj.properties['Citizens'])
                    if(obj.type != "ResidentialZone" and total_citizens != 0):
                        obj.properties['Revenue'] += (MONEY_PER_DAY * total_citizens)
                    # Get revenue (TAX) from WorkZone to Player
                    elif(obj.type != "ResidentialZone" and did_a_year_pass):
                        revenue = obj.properties['Revenue'] * TAX_VARIABLE
                        player.money += revenue
                        obj.properties['Revenue'] = 0
            day = timer.get_current_time().day
            
            
        for event in pygame.event.get(): # mouse button click, keyboard, or the x button.
            
            mouse_pos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[2]:
                normal_cursor = True
                clicked_zone = upgrade = reclassify = None
                clicked_cords = mouse_pos
                
            if pygame.mouse.get_pressed()[0]:
                if reclassify:
                    if reclassify.collidepoint(mouse_pos):
                        map.reclassify_zone(clicked_zone)
                        player.money += (float(clicked_zone.properties["Price"])*0.5)
                        clicked_cords = clicked_zone = upgrade = reclassify = None
                if upgrade:
                    if upgrade.collidepoint(mouse_pos):
                        upgrade_zone(clicked_zone,map)
                        player.money -= ((float(clicked_zone.properties["Price"])*0.5) * (clicked_zone.properties["Level"]+0.25))
                clicked_cords = clicked_zone = upgrade = reclassify = None

            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:    # Cursor handling
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

                            map.addObject(obj.instance,player)
                            # Satisfaction handling for: Forest, Stadium, and PoliceDepartment
                            if(is_satisfaction_zone(obj.instance)):
                                x = map.get_all_objects()
                                handle_satisfaction_zone_addition(obj.instance)
                            class_tobuild = -1
                        else:
                            map.remove_obj(x,y,"Road")
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
                clicked_cords = clicked_zone = upgrade = reclassify = None
                map.handleScroll(event.key)
        
        if not normal_cursor:
            clicked_cords = clicked_zone = upgrade = reclassify = None
            SCREEN.blit(cursorImg, cursorImgRect)
        
        clicked_cords,clicked_zone,upgrade,reclassify = handle_prompt(clicked_cords,clicked_zone,upgrade,reclassify)
                
        # Limit the frame rate to 60 FPS
        timer.update_time(paused)
        timer.tick(60)
        pygame.display.update()
        SCREEN.fill((0, 0, 0))
