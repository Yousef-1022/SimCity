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
            # if(len(RZones) > 0):
            # RZone = random.choice(RZones)
            if len (map.get_residential_zones()) != 0:
                first_R_Zone = map.get_residential_zones()[0]
                for c in initial_citizens:
                    c.assign_to_residential_zone(first_R_Zone,map)
                    initial_citizens.remove(c)
        if(timer.get_current_time().month != month):   
            add_citizens_to_game()
            for zone in map.get_residential_zones():
                assign_zone_citizens_to_work(zone)
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
                map.handleScroll(event.key)
        
        if not normal_cursor:
            SCREEN.blit(cursorImg, cursorImgRect)
        # Limit the frame rate to 60 FPS
        timer.update_time(paused)
        timer.tick(60)
        pygame.display.update()
        SCREEN.fill((0, 0, 0))

def add_citizens_to_game():
    distance_threshold = 5  # Minimum distance between residential and working zones
    possible_citizens = 5 # Max possible amount of citizens to arrive during the time period
    part2 = 0.0
    part3 = 0.0
    total_satisfaction = Citizen.get_current_satisfaction()
    average_satisfaction = total_satisfaction / Citizen.get_total_citizens() 
    zones_with_arrival_chances = [] 
    for zone in map.get_residential_zones():
        if len(zone.properties['Citizens']) < zone.properties['Capacity']:
            # part1
            arrival_chance = average_satisfaction
            
            # Iterate over the available work zones with free spaces within the given radius
            nearby_workzones = []
            for w_zone in map.get_work_zones():
                if len(w_zone.properties['Citizens']) < w_zone.properties['Capacity']:
                    distance = distance_between_two(zone, w_zone)
                    if(distance < distance_threshold):
                        nearby_workzones.append(w_zone)

            # part2
            available_cap = sum([(wz.properties['Capacity'] - len(wz.properties['Citizens'])) for wz in nearby_workzones])
            if available_cap >= possible_citizens:
                variety = len(nearby_workzones)
                if (variety >= possible_citizens):
                    part2 = 100.0
                else:
                    decrease = (possible_citizens - variety) * 2.0 # 3%
                    part2 = 100.0 - decrease
            else:
                part2 = available_cap * 10.0
            # part3
            nearby_industrial = industrial_buildings_nearby(zone)
            probs = [(abs(p - distance_threshold+1))*10.0 for p in nearby_industrial]
            part3 = sum(probs) / len(nearby_industrial) if  len(nearby_industrial) != 0 else 100

            # result
            res = (arrival_chance+part2+part3)/3.0
            zones_with_arrival_chances.append((zone, res))
    for zone , arrival_chance in zones_with_arrival_chances:
        n = int ((arrival_chance * possible_citizens) // 100)
        for _ in range(n):
            c = Citizen()
            c.assign_to_residential_zone(zone, map)


def industrial_buildings_nearby(zone):
    distance_threshold = 5  # Minimum distance between residential and industrial zones
    industrial_buildings_nearby = []
    I_zones = map.get_insustrial_zones()
    distance = 0
    for I_zone in I_zones:
        distance  = distance_between_two(zone, I_zone)
        if distance < distance_threshold:
            industrial_buildings_nearby.append(distance)
    return industrial_buildings_nearby

def get_area(obj:TiledObject):
    """
    Returns a list of (x,y) coordinates that reprsenet the object's area
    
    Each point represents coordinates of a Tile
    """
    res = []
    tilex = obj.x // obj.parent.tilewidth
    tiley = obj.y // obj.parent.tileheight
    rows = int(obj.width // obj.parent.tilewidth)
    cols = int(obj.height // obj.parent.tileheight)
    for i in range(rows):
        for j in range (cols):
            res.append((tilex+i,tiley+j))
    return res

def get_circumference(obj:TiledObject):
    """
    Returns a list of (x,y) coordinates the represent the object's circumference
    Each point represents coordinates of a Tile
    """
    tilex = obj.x // obj.parent.tilewidth
    tiley = obj.y // obj.parent.tileheight
    rows = int(obj.width // obj.parent.tilewidth)
    cols = int(obj.height // obj.parent.tileheight)
    res = []
    for i in range(rows):
        res.append((tilex+i,tiley))
        res.append((tilex+i,tiley+cols-1))

    for j in range(cols):
        res.append((tilex,tiley+j))
        res.append((tilex+rows-1,tiley+j))
    return list(set(res))

def get_outer_circumference(obj:TiledObject):
    tilex = (obj.x // 32) 
    tiley = (obj.y // 32) 
    res = []
    for i in range(0,4):
        res.append((tilex + i ,tiley - 1))
        res.append((tilex + i ,tiley + 4))

    for i in range(0,4):
        res.append((tilex - 1 ,tiley  + i))
        res.append((tilex + 4 ,tiley  + i))

    return list(set(res))

def distance_between_two(obj1:TiledObject,obj2:TiledObject):
    """
    Returns the minimal distance between the two tiled objects
    
    Checks the cirumference of both, and calculates the distance of the closest two points
    """
    
    c1 = get_circumference(obj1)
    c2 = get_circumference(obj2)
    c1_xs = [p[0] for p in c1]
    c1_ys = [p[1] for p in c1]
    
    c2_xs = [p[0] for p in c2]
    c2_ys = [p[1] for p in c2]

    in_c1_xs = False
    in_c1_ys = False
    for p in c1_xs:
        if  p in c2_xs:
            in_c1_xs = True
            break
    for p in c1_ys:
        if  p in c2_ys:
            in_c1_ys = True
            break

    l=[]
    min = 69420

    for p1 in c1:
        for p2 in c2:
            d = calc_d(p1,p2)
            if (d <= min):
                min = d
                l.clear()
                l.append(p1)
                l.append(p2)
    if(not in_c1_xs and not in_c1_ys):
        return (calc_d(l[0], l[1]) // 2) + 1 
    return min


def calc_d (p1,p2) -> int:
    """
    Helper to calculate the distance between the two given points
    """
    horizontal_distance=abs(p1[0]-p2[0])
    vertical_distance=abs(p1[1]-p2[1])
    distance = (horizontal_distance + vertical_distance)
    return distance - 1

def get_connected_by_road_objects(zone):
    roads = map.get_roads() 
    c = get_outer_circumference(zone) 
    roads_connected_to_zone = [] 
    for tup in c: # get all sorounding roads to the zone
        for road in roads:
            if int(tup[0]) == int (road.x // 32) and  int(tup[1]) == int (road.y // 32) :
                roads_connected_to_zone.append(road)
    print("roads_connected_to_zone" , len (roads_connected_to_zone))
    connected_roads = [] 
    for road in roads_connected_to_zone:
         connected_roads.extend(get_all_connected_roads(road, roads))
    # print(get_neighboring_objects(connected_roads))
    return get_neighboring_objects(connected_roads)

def get_neighboring_objects(roads):
    neighboring_objects = []
    for road in roads:
        object = get_neighboring_object(road)
        if object:
            neighboring_objects.append(object) 
    return neighboring_objects


def  get_neighboring_object(road):
    x = int (road.x // 32) 
    y = int (road.y // 32) 
    objects = map.get_all_objects()
    for object in objects:
        if object.type == "IndustrialZone" or object.type == "ServiceZone":
            c =  get_outer_circumference(object)
            for tup in c:
                if int(tup[0]) == x and  int(tup[1]) == y:
                    return object
    return None

def assign_zone_citizens_to_work(zone):
    available_work_places = [w_zone for w_zone in get_connected_by_road_objects(zone) if len(w_zone.properties['Citizens']) < w_zone.properties['Capacity']]
    for citizen in zone.properties['Citizens']:
        if citizen.work == None:
            assign_to_work_zones(citizen, available_work_places)

def assign_to_work_zones(citizen, available_work_places):
    I_zones = [zone for zone in available_work_places if zone.type == "IndustrialZone"] 
    S_zones = [zone for zone in available_work_places if zone.type == "ServiceZone"] 
    total_capacity_of_I_zones , total_number_of_citizens_in_I_zones = get_capacity_and_citizens_of_zones(I_zones)
    total_capacity_of_S_zones , total_number_of_citizens_in_S_zones = get_capacity_and_citizens_of_zones(S_zones)

    if total_capacity_of_I_zones == 0 and  total_capacity_of_S_zones == 0:
        return 
    
    needed_citizens_for_I_zones = total_capacity_of_I_zones - total_number_of_citizens_in_I_zones
    needed_citizens_for_S_zones = total_capacity_of_S_zones - total_number_of_citizens_in_S_zones
    print("needed_citizens_for_I_zones", needed_citizens_for_I_zones )
    print("needed_citizens_for_S_zones", needed_citizens_for_S_zones )
    if needed_citizens_for_I_zones  > needed_citizens_for_S_zones:
        assign_citizen_to_random_zone(citizen,I_zones)
        print("adding citizen to I")
    else:
        assign_citizen_to_random_zone(citizen,S_zones)
        print("adding citizen to S")

def get_num_of_unemployed_in_zone(zone):
    cnt = 0 
    for citizen in zone.properties['Citizens']:
        if citizen.work != None:
            cnt += 1
    return cnt

def get_capacity_and_citizens_of_zones(zones):
    total_capacity = 0
    total_number_of_citizens = 0
    for zone in zones:
        total_capacity += zone.properties['Capacity']
        total_number_of_citizens += len(zone.properties['Citizens'])
    return total_capacity, total_number_of_citizens

def assign_citizen_to_random_zone(c, zones):
    if zones:
        random_zone = random.choice(zones)
        Citizen.assign_to_work_zone(c, random_zone, map)
