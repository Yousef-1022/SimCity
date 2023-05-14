import os
import random
from pytmx import TiledObject
from models.Timer import Timer
from models.BuildingAdder import form_tiled_obj
from models.Citizen import *

def get_files_from_dir(dir_path) -> list:
    """Returns all the files as a list from the given path"""
    return os.listdir(dir_path)


def get_icon_and_type(file, dir_attachment=None) -> tuple:
    """Returns a (FileLocation , ClassName) tuple"""
    parts = file.split("_")
    type = os.path.splitext(parts[1])[0]
    if (dir_attachment):
        return (dir_attachment+file, type)
    return (file, type)


def get_icon_loc_by_name(name, tuple_list) -> list:
    """Returns a list consisting of (FileLocation , ClassName) tuples"""
    return ([t[0] for t in tuple_list if name in t[0]])[0]


def add_citizen(tiledObj: TiledObject, citizen):
    """
    Adds a citizen into the tiledObj, modifies the tiledObj to link accordingly with ObjectsTop layer
    in order to display the capacity of citizens on the Zone
    
    Args:
        tiledObj: tiledObj representing a Zone
        citizen: Citizen object
    Returns:
        a boolean value if its citizen insertion is successful.
    """
    if tiledObj.properties['Capacity'] != len(tiledObj.properties['Citizens']):
        tiledObj.properties['Citizens'].append(citizen)
        return True
    return False


def remove_citizen_from_zone(tiledObj: TiledObject, citizen):
    """Removes a citizen from the tiledObj"""
    try:
        tiledObj.properties['Citizens'].remove(citizen)
    except Exception as e:
        print(
            f"Fatal failure removing citizen {citizen} from {tiledObj}. Error: {e}")


def has_year_passed_from_creation(obj: TiledObject, givenDate: Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a year has passed or not """
    x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
    return x != 0 and x % 365 == 0


def has_quarter_passed_from_creation(obj: TiledObject, givenDate: Timer) -> bool:
    """Checks if a quarter (90 days) passed since creation"""
    if obj:
        x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
        return x != 0 and x % 90 == 0
    return False


def simulate_building_addition(obj: TiledObject, map):
    """
    Added the building (Second object layer) ontop of the current object (Zone)
    
    Args:
    obj: TiledObject you would like to add a building on top
    map: mapInstance
    
    Info:
    Has a checker for the RZone to only allow 4 buildings
    Has a checker for the CZone,IZone to only allow 1 building
    """
    built = get_linked_ids_for_obj(obj)
    length = len(built)
    create = False
    if (obj.name == 'IZone' or obj.name == 'CZone'):
        if (length == 0):
            create = True
    elif (obj.name == 'RZone'):
        ppl = len(obj.properties['Citizens'])
        quarter = obj.properties['Capacity'] // 4
        if ((ppl % quarter == 1) and length < 4):
            create = True
    if (create):
        building = form_tiled_obj(obj, map)
        objLayer = map.returnMap().get_layer_by_name("ObjectsTop")
        objLayer.append(building)


def get_linked_ids_for_obj(obj: TiledObject) -> list[int]:
    """
    Gets all the linked objects (Second object layer) representing the buildings
    on top of the current object
    
    Args:
    obj: TiledObject representing a Zone
    
    Returns:
    a List of linked ids to the Zone
    """
    Objects = obj.parent.get_layer_by_name("ObjectsTop")
    res = []
    for o in Objects:
        if o.properties['linked_id'] == obj.id:
            res.append(o)
    return res


def get_image_size(image_type):
    if image_type == "ResidentialZone" or image_type == "IndustrialZone" or image_type == "IndustrialZone" or "ServiceZone" == image_type:
        return 128
    elif image_type == "PoliceDepartment":
        return 96
    elif image_type == "Stadium":
        return 160
    else:
        return 32


def get_all_connected_roads(road, road_list):
    visited = set()
    # Perform DFS traversal starting from the first road
    dfs(road, visited, road_list)
    # print(visited)
    return visited


def dfs(current_road, visited, road_list):
    # Extract relevant attributes into a tuple
    road_tuple = (current_road.x, current_road.y)
    visited.add(current_road)

    # Explore adjacent roads (branches)
    connected_roads = get_connected_roads(road_tuple, road_list)

    for road in connected_roads:
        # Extract relevant attributes into a tuple
        road_tuple = (road.x, road.y)
        if not is_in_visited(road_tuple, visited):
            print(f"Visiting road ({road.x}, {road.y})")
            dfs(road, visited, road_list)


def get_connected_roads(current_road, road_list):
    connected_roads = []
    x = int(current_road[0] // 32) - 1
    y = int(current_road[1] // 32)
    road = get_connected_road_tiles(x, y, 'L', road_list)
    while (road != None):
        x = x - 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'L', road_list)
    x = int(current_road[0] // 32) + 1
    y = int(current_road[1] // 32)
    road = get_connected_road_tiles(x, y, 'R', road_list)
    while (road != None):
        x = x + 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'R', road_list)
    x = int(current_road[0] // 32)
    y = int(current_road[1] // 32) - 1
    road = get_connected_road_tiles(x, y, 'U', road_list)
    while (road != None):
        y = y - 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'U', road_list)
    x = int(current_road[0] // 32)
    y = int(current_road[1] // 32) + 1
    road = get_connected_road_tiles(x, y, 'D', road_list)
    while (road != None):
        y = y + 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'D', road_list)
    return connected_roads


def get_connected_road_tiles(x, y, direction, roads):
    obj_coord_x = x
    obj_coord_y = y
    for road in roads:
        if (direction == 'U'):
            if int(road.x // 32) == x and int(road.y // 32) == obj_coord_y:
                return road
        elif (direction == 'D'):
            if int(road.x // 32) == x and int(road.y // 32) == obj_coord_y:
                return road
        elif (direction == 'L'):
            if int(road.x // 32) == obj_coord_x and int(road.y // 32) == y:
                return road
        elif (direction == 'R'):
            if int(road.x // 32) == obj_coord_x and int(road.y // 32) == y:
                return road
    return None

def is_in_visited(road_tuple, visited):
    for road in visited:
        if road_tuple[0] == road.x and road_tuple[1] == road.y:
            return True
    return False

def add_citizens_to_game(map):
    distance_threshold = 5  # Minimum distance between residential and working zones
    possible_citizens = 5 # Max possible amount of citizens to arrive during the time period
    part2 = 0.0
    part3 = 0.0
    total_satisfaction = get_current_satisfaction()
    average_satisfaction = total_satisfaction / get_total_citizens() 
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
            nearby_industrial = industrial_buildings_nearby(zone, map)
            probs = [(abs(p - distance_threshold+1))*10.0 for p in nearby_industrial]
            part3 = sum(probs) / len(nearby_industrial) if  len(nearby_industrial) != 0 else 100

            # result
            res = (arrival_chance+part2+part3)/3.0
            zones_with_arrival_chances.append((zone, res))
    for zone , arrival_chance in zones_with_arrival_chances:
        n = int ((arrival_chance * possible_citizens) // 100)
        for _ in range(n):
            c = Citizen()
            assign_to_residential_zone(c,zone, map)


def industrial_buildings_nearby(zone, map):
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

def get_connected_by_road_objects(zone, map):
    roads = map.get_roads() 
    c = get_outer_circumference(zone) 
    roads_connected_to_zone = [] 
    for tup in c: # get all sorounding roads to the zone
        for road in roads:
            if int(tup[0]) == int (road.x // 32) and  int(tup[1]) == int (road.y // 32) :
                roads_connected_to_zone.append(road)
    connected_roads = [] 
    for road in roads_connected_to_zone:
         connected_roads.extend(get_all_connected_roads(road, roads))
    return get_neighboring_objects(connected_roads, map)

def get_neighboring_objects(roads, map):
    neighboring_objects = []
    for road in roads:
        object = get_neighboring_object(road,map)
        if object:
            neighboring_objects.append(object) 
    return neighboring_objects


def  get_neighboring_object(road, map):
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

def assign_zone_citizens_to_work(zone, map):
    available_work_places = [obj for obj in get_connected_by_road_objects(zone, map) if  len(obj.properties['Citizens']) < obj.properties['Capacity']]
    print(available_work_places)
    for citizen in zone.properties['Citizens']:
        if citizen.work == None:
            assign_to_work_zones(citizen, available_work_places, map)

def assign_to_work_zones(citizen, available_work_places, map):
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
        assign_citizen_to_random_zone(citizen,I_zones, map)
        print("adding citizen to I")
    else:
        assign_citizen_to_random_zone(citizen,S_zones, map)
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

def assign_citizen_to_random_zone(c, zones, map):
    if zones:
        random_zone = random.choice(zones)
        assign_to_work_zone(c, random_zone, map)

def get_citizen_by_id(id:int):
    """Returns a Citizen object using the id"""
    return Citizen.citizens.get(id)

def get_current_satisfaction() -> int:
    """Returns current overall satisfaction for all citizens"""
    return sum (citizen.satisfaction for citizen in Citizen.citizens.values())

def get_max_possible_satisfaction() -> int:
    """Returns the max satisfaction possible for all created citizens"""
    return len(Citizen.citizens) * 100

def get_total_citizens() -> int:
    """Returns the total number of citizens"""
    return len(Citizen.citizens)

def get_sad_citizens(s_lvl:int) -> list['Citizen']:
    """
    Gets a list of citizens who have a satisfaction level
    less or equal to the given lvl

    Args:
        s_lvl: The satisfaction level the citizens should be less or equal to
        
    Returns:
        List of sad citizens  
    """
    return (c for c in Citizen.citizens.values() if c.satisfaction <= s_lvl)

def assign_to_residential_zone(citizen, RZone,mapInstance):
    """
    Gives the citizen a home, deletes the Citizen if there's a failure assigning a home.
    mapInstance is required to be passed in order to simulate the addition of the buildings on top of the Zone
    
    Args:
        RZone: ResidentialZone
        mapInstance : Map object
    
    Returns:
        Nothing 
    """
    if (add_citizen(RZone,citizen)):
        citizen.home = RZone
        simulate_building_addition(RZone,mapInstance)
    else:
        if(citizen.work):
            citizen.work.remove_citizen(citizen)
        del Citizen.citizens[citizen.id]
        
def assign_to_work_zone(citizen,WorkZone,mapInstance):
    """Assigns the citizen to either a ServiceZone or IndustrialZone, deletes the Citizen if there's a failure assigning work"""
    if (add_citizen(WorkZone,citizen)):
        citizen.work = WorkZone
        simulate_building_addition(WorkZone,mapInstance)
    else:
        print("Can't assign citizen cuz W_zone is full", WorkZone.properties['Capacity'])


