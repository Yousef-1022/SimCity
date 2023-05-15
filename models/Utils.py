import os
import random
from pytmx import TiledObject
from models.Timer import Timer
from models.BuildingAdder import form_tiled_obj
from models.Citizen import *
from models.Disaster import Disaster
import math

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


def remove_citizen_from_zone(tiledObj: TiledObject, citizen:Citizen) -> bool:
    """
    Removes a citizen from the tiledObj
    
    Returns:
    boolean value indicating the success of removing the given citizen
    """
    try:
        tiledObj.properties['Citizens'].remove(citizen)
        return True
    except Exception as e:
        #print(f"Fatal failure removing citizen {citizen} with data {citizen.__dict__} from {tiledObj}. Error: {e}")
        return False


def has_year_passed_from_creation(obj: TiledObject, givenDate: Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a year has passed or not """
    if obj:
        x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
        return x != 0 and x % 365 == 0
    return False

def has_month_passed_from_creation(obj: TiledObject, givenDate: Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a month has passed or not """
    if obj:
        x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
        return x != 0 and x % 30 == 0
    return False


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
        if obj.properties['Level'] == 1:
            ppl = len(obj.properties['Citizens'])
            quarter = obj.properties['Capacity'] // 4
            if ((ppl % quarter == 1) and length < 4):
                create = True
        else:
            create = False
    if (create):
        building = form_tiled_obj(obj,map)
        objLayer = obj.parent.get_layer_by_name("ObjectsTop")
        objLayer.append(building)
        obj.properties['Buildings'].append(building.__dict__)


def get_linked_ids_for_obj(obj: TiledObject) -> list:
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
        if o.type != 'Disaster':
            if o.properties['linked_id'] == obj.id:
                res.append(o)
    return res


def get_image_size(image_type):
    if image_type == "ResidentialZone" or image_type == "IndustrialZone" or "ServiceZone" == image_type:
        return 128
    elif image_type == "PoliceDepartment" or image_type == "Forest" or image_type == "Disaster":
        return 96      
    elif image_type == "Stadium":
        return 160 
    else:
        return 32

def calc_d (p1,p2) -> int:
    """
    Helper to calculate the distance between the two given points
    """
    horizontal_distance=abs(p1[0]-p2[0])
    vertical_distance=abs(p1[1]-p2[1])
    distance = (horizontal_distance + vertical_distance)
    return distance - 1 
    #distance = math.sqrt((horizontal_distance)**2 + (vertical_distance)**2)
    #return math.floor(distance)
    
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

def get_points_looking_at_each_other(Frst:TiledObject,RZone:TiledObject) -> list:
    """
    Usage: Forest
    Returns a list of points that represent the possible view between the Forest and RZone
    
    This can serve as two walls of coordinates
    
    Each point represents coordinates of the Tile
    
    Returns: a List of sorted tuples, half represents an object wall and the other half represents an object wall
    """
    
    c1=get_circumference(Frst)
    c2=get_circumference(RZone)
    res=[]
    min = 69420
    for p1 in c1:
        for p2 in c2:
            d = calc_d(p1,p2)
            if (d < min):
                min = d
                res.clear()
                res.append(p1)
                res.append(p2)
            elif(d == min):
                res.append(p1)
                res.append(p2)
    ans = sorted(res, key=lambda p: (p[0], p[1]))        
    return ans
    
def get_path_between_points(p1,p2) -> list:
    """
    Based on the two points, returns a list of points showing the path it takes to reach
    Doesn't include the two points themselves
    """
    if p1[0] < p2[0]:
        h = [(float(x),float(p1[1])) for x in range(int(p1[0])+1, int(p2[0])+1)]
        v = []
        if p1[1] < p2[1]:
            v = [(float(max(p1[0],p2[0])),float(y)) for y in range(int(p1[1])+1, int(p2[1]))]
        elif p1[1] == p2[1]:
            h = h[:-1]
        else:   
            v = [(float(max(p1[0],p2[0])),float(y)) for y in range(int(p2[1])+1, int(p1[1]))]
        return h+v
    else:
        h = [(float(x),float(p2[1])) for x in range(int(p2[0])+1, int(p1[0])+1)]
        v = []
        if p1[1] < p2[1]:
            v = [(float(max(p1[0],p2[0])),float(y)) for y in range(int(p1[1])+1, int(p2[1]))]
        elif p1[1] == p2[1]:
            h = h[:-1]
        else:
            v = [(float(max(p1[0],p2[0])),float(y)) for y in range(int(p2[1])+1, int(p1[1]))]
        return h+v

def is_satisfaction_zone(SZone:TiledObject):
    """
    Check if the given tiledobject is a satisfaction increaser
    """
    if (SZone.type == 'Stadium' or SZone.type == 'PoliceDepartment' or SZone.type == 'Forest'):
        return True
    return False
    
def get_zone_satisfaction(zone:TiledObject):
    """
    Returns the amount of satisfaction of the zone
    """
    sat = 0.0
    for c in zone.properties['Citizens']:
        sat += c.satisfaction
    return sat/float(len(zone.properties['Citizens']))

def tile_in_which_zone(coords,Zones) -> TiledObject:
    for zone in Zones:
        if coords in get_area(zone):
            return zone
    return None

def upgrade_zone(zone:TiledObject,mapInstance):
    """
    Upgrades the clicked Zone (RZone/CZone/IZone)
    """
    #def get_obj_by_id(id):
    #    for obj in mapInstance.returnMap().get_layer_by_name("ObjectsTop"):
    #        if obj.id == id:
    #            return obj
    #    return None

    zone.properties['Level'] += 1
    zone.properties['Capacity'] = math.ceil(zone.properties['Capacity'] * 1.5)
    zone.properties['MaintenanceFee'] *= 0.25
    lst = get_linked_ids_for_obj(zone)
    #to_delete = [i.id for i in lst]
    obj_layer = mapInstance.returnMap().get_layer_by_name("ObjectsTop")
    for obj in lst:
        obj_layer.remove(obj)
    #for i in to_delete:
    #    o = get_obj_by_id(i)
    #    if (o):
    #        del(o)
    zone.properties['Buildings'] = []
    building = form_tiled_obj(zone,mapInstance)
    obj_layer.append(building)
    zone.properties['Buildings'].append(building.__dict__)
            

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
            #print(f"Visiting road ({road.x}, {road.y})")
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

def handle_citizen_addition_satisfaction(c:Citizen,map):
    """
    After assigning a citizen to an RZone, checks nearby SatisfactionIncreasers and adds accordingly
    """
    for SZone in map.get_satisfaction_increasers():
        if (distance_between_two(c.home,SZone) <= SZone.properties['Radius']):
            if (SZone.type == "Forest"):
                if(is_there_a_blocker_between(c.home,SZone,map.get_all_objects())):
                    continue
                else:
                    tmp = c.satisfaction + (SZone.properties['Satisfaction']*c.satisfaction) 
                    if tmp <= 100:
                        c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
            else:
                tmp = c.satisfaction + (SZone.properties['Satisfaction']*c.satisfaction) 
                if tmp <= 100:
                    c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)

def add_citizens_to_game(map):
    distance_threshold = 5  # Minimum distance between residential and working zones
    possible_citizens = 5 # Max possible amount of citizens to arrive during the time period
    part2 = 0.0
    part3 = 0.0
    total_satisfaction = get_current_satisfaction()
    total_citizens = get_total_citizens()
    if total_citizens == 0:   
        average_satisfaction = 0
    else:
        average_satisfaction = total_satisfaction / total_citizens
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
            success_in_assign = assign_to_residential_zone(c,zone, map)
            if (success_in_assign):
                handle_citizen_addition_satisfaction(c,map)

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
    available_work_places = [obj for obj in get_connected_by_road_objects(zone, map) if len(obj.properties['Citizens']) < obj.properties['Capacity']]
    #print(available_work_places)
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
    #print("needed_citizens_for_I_zones", needed_citizens_for_I_zones )
    #print("needed_citizens_for_S_zones", needed_citizens_for_S_zones )
    if needed_citizens_for_I_zones  > needed_citizens_for_S_zones:
        assign_citizen_to_random_zone(citizen,I_zones, map)
        #print("adding citizen to I")
    else:
        assign_citizen_to_random_zone(citizen,S_zones, map)
        #print("adding citizen to S")

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

def assign_to_residential_zone(citizen, RZone,mapInstance) -> bool:
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
        return True
    else:
        if(citizen.work):
            citizen.work.remove_citizen(citizen)
        del Citizen.citizens[citizen.id]
        return False
        
def assign_to_work_zone(citizen,WorkZone,mapInstance) -> bool:
    """Assigns the citizen to either a ServiceZone or IndustrialZone, returns a bool value if a failure assigning work happens"""
    if (add_citizen(WorkZone,citizen)):
        citizen.work = WorkZone
        simulate_building_addition(WorkZone,mapInstance)
        return True
    else:
        #print("Can't assign citizen cuz W_zone is full", WorkZone.properties['Capacity'])
        return False

def delete_citizen(c:Citizen) -> bool:
    """
    Deletes the citizen and all data associated with it
    
    Returns:
    boolean value indicating that the citizen was deleted successfully.
    """
    c.home = None
    c.work = None
    try:
        del Citizen.citizens[c.id]
        return True
    except Exception as e:
        #print(f"Fatal failure deleting citizen {c} with data: {c.__dict__}. Error: {e}")
        return False
        
def handle_disaster_logic(map,givenDate:Timer):
    disasters = map.get_all_disasters()
    for disaster in disasters:
        if (has_month_passed_from_creation(disaster,givenDate)):
            for obj in disaster.properties['linked_objs']:
                lnked = [b for b in map.get_buildings() if b.type != 'Disaster' and b.properties['linked_id'] == obj.id]
                
                if (obj.type == 'ResidentialZone'):
                    rmf = []
                    for c in obj.properties['Citizens']:
                        rmf.append(c.id)
                        if (c.work):
                            remove_citizen_from_zone(obj,c.work)
                    for i in rmf:
                        c = get_citizen_by_id(i)
                        delete_citizen(c)
                    obj.properties['Citizens'] = []
                    for b in lnked:
                        map.remove_disaster_or_building(b)
                    map.reclassify_zone(obj)
                    
                elif (obj.type == 'IndustrialZone' or obj.type == 'ServiceZone'):
                    for c in obj.properties['Citizens']:
                        remove_citizen_from_zone(obj,c)
                        c.work = None
                    obj.properties['Citizens'] = []
                    for b in lnked:
                        map.remove_disaster_or_building(b)
                    map.reclassify_zone(obj)
                    
                elif (obj.type == 'PoliceDepartment' or obj.type == 'Stadium' or obj.type == 'Forest'):
                    map.reclassify_zone(obj)
            map.remove_disaster_or_building(disaster)

def handle_satisfaction_zone_removal(SZone:TiledObject,RZones):
    """
    After the player deletes a Stadium or PoliceDepartment , it checks nearby Citizens and decreases satisfaction
    
    (Reclassify Forest because of Disaster uses this function)
    """
    for RZone in RZones:
        if (distance_between_two(RZone,SZone) <= SZone.properties['Radius']):
            for c in RZone.properties['Citizens']:
                tmp = c.satisfaction + (SZone.properties['Satisfaction']*c.satisfaction) 
                if tmp >= 0:
                    c.satisfaction -= (SZone.properties['Satisfaction']*c.satisfaction)
                    
def handle_disaster_random_logic(mapInstance,givenDate,randomizer:bool):
    """
    Creates a random Disaster on the map on a yearly basis given that forests exist
    
    Args:
    mapInstance: the Map itself
    givenDate: the current time the disaster would be called
    randomizer: boolean value given by has_random_years_passed_from_start used in forest yearly pass checking
    """
    if randomizer:
        zones = [o for o in mapInstance.get_all_objects() if o.type != "Road"]
        if (len(zones) != 0):
            disasters = mapInstance.get_all_disasters()
            to_destroy = random.choice(zones)
            for d in disasters:
                if to_destroy in d.properties['linked_objs']:
                    return
            disaster_make = Disaster(to_destroy.x//32,to_destroy.y//32,givenDate,mapInstance)
            obj = disaster_make.instance
            obj.properties['linked_objs'] = [to_destroy]
            mapInstance.add_disaster_to_map(obj)
                    
def has_random_years_passed_from_start(gameStart, givenDate: Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a year has passed or not """
    years_passed = givenDate.subtract_with_time_str(gameStart) // 365
    random_array = [random.randint(years_passed+1, years_passed+99) for _ in range(99)]
    random_array.append(years_passed)
    choice = random.choice(random_array)
    if choice - years_passed == 0:
        return True
    else:
        return False