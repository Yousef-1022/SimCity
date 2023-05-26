import os
import sys
import random
import math
import pygame
import pickle
from pytmx import TiledObject
from models.Forest import Forest
from models.TaxAllocator import TaskAllocator
from models.Timer import Timer
from models.BuildingAdder import form_tiled_obj
from models.Citizen import *
from models.Disaster import Disaster

"""
Getters
"""


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


def get_image_size(image_type: str) -> int:
    """
    Returns the size of an image based on the given image type.

    Args:
        image_type (str): The type of the image.

    Returns:
        int: The size of the image.

    Raises:
        None.

    Examples:
        >>> get_image_size("ResidentialZone")
        128
        >>> get_image_size("PoliceDepartment")
        96
        >>> get_image_size("Stadium")
        160
        >>> get_image_size("UnknownType")
        32
    """
    if image_type == "ResidentialZone" or image_type == "IndustrialZone" or image_type == "ServiceZone":
        return 128
    elif image_type == "PoliceDepartment" or image_type == "Forest" or image_type == "Disaster":
        return 96
    elif image_type == "Stadium":
        return 160
    else:
        return 32


def get_area(obj: TiledObject):
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
        for j in range(cols):
            res.append((tilex+i, tiley+j))
    return res


def get_circumference(obj: TiledObject):
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
        res.append((tilex+i, tiley))
        res.append((tilex+i, tiley+cols-1))
    for j in range(cols):
        res.append((tilex, tiley+j))
        res.append((tilex+rows-1, tiley+j))

    return list(set(res))


def get_points_looking_at_each_other(Frst: TiledObject, RZone: TiledObject) -> list:
    """
    Usage: Forest
    Returns a list of points that represent the possible view between the Forest and RZone

    This can serve as two walls of coordinates

    Each point represents coordinates of the Tile

    Returns: a List of sorted tuples, half represents an object wall and the other half represents an object wall
    """

    c1 = get_circumference(Frst)
    c2 = get_circumference(RZone)
    res = []
    min = 69420
    for p1 in c1:
        for p2 in c2:
            d = calc_d(p1, p2)
            if (d < min):
                min = d
                res.clear()
                res.append(p1)
                res.append(p2)
            elif (d == min):
                res.append(p1)
                res.append(p2)
    ans = sorted(res, key=lambda p: (p[0], p[1]))
    return ans


def get_path_between_points(p1, p2) -> list:
    """
    Based on the two points, returns a list of points showing the path it takes to reach
    Doesn't include the two points themselves
    """
    if p1[0] < p2[0]:
        h = [(float(x), float(p1[1]))
             for x in range(int(p1[0])+1, int(p2[0])+1)]
        v = []
        if p1[1] < p2[1]:
            v = [(float(max(p1[0], p2[0])), float(y))
                 for y in range(int(p1[1])+1, int(p2[1]))]
        elif p1[1] == p2[1]:
            h = h[:-1]
        else:
            v = [(float(max(p1[0], p2[0])), float(y))
                 for y in range(int(p2[1])+1, int(p1[1]))]
        return h+v
    else:
        h = [(float(x), float(p2[1]))
             for x in range(int(p2[0])+1, int(p1[0])+1)]
        v = []
        if p1[1] < p2[1]:
            v = [(float(max(p1[0], p2[0])), float(y))
                 for y in range(int(p1[1])+1, int(p2[1]))]
        elif p1[1] == p2[1]:
            h = h[:-1]
        else:
            v = [(float(max(p1[0], p2[0])), float(y))
                 for y in range(int(p2[1])+1, int(p1[1]))]
        return h+v


def get_zone_satisfaction(zone: TiledObject) -> float:
    """
    Returns the average satisfaction of the citizens in the given zone.

    Args:
        zone (TiledObject): The zone object containing the citizens.

    Returns:
        float: The average satisfaction of the citizens.

    Raises:
        None.

    Examples:
        >>> zone_obj = create_zone_obj(...)
        >>> get_zone_satisfaction(zone_obj)
        75.0
    """
    sat = 0.0
    for c in zone.properties['Citizens']:
        sat += c.satisfaction
    return sat / float(len(zone.properties['Citizens']))


def get_all_connected_roads(road, road_list):
    """
    Returns a set of all roads connected to the given road using depth-first search (DFS).

    Args:
        road: The starting road.
        road_list: The list of all roads.

    Returns:
        set: A set of all connected roads.

    Raises:
        None.

    Examples:
        >>> roads = [road1, road2, road3, road4]
        >>> get_all_connected_roads(road1, roads)
        {road1, road2, road3}
    """
    visited = set()
    dfs(road, visited, road_list)
    return visited


def get_connected_roads(current_road, road_list, dimension_tuple=None):
    """
    Returns a list of all roads connected to the given current road.

    Args:
        current_road: The current road coordinates as a tuple (x, y).
        road_list: The list of all roads.
        dimension_tuple: Tuple consisting of tilewidth and tileheight

    Returns:
        list: A list of all connected roads.

    Raises:
        None.

    Examples:
        >>> roads = [road1, road2, road3, road4]
        >>> current_road = (32, 64)
        >>> get_connected_roads(current_road, roads)
        [road1, road2, road3]
    """
    tilewidth , tileheight = 32 , 32
    if dimension_tuple:
        tilewidth = dimension_tuple[0]
        tileheight = dimension_tuple[1]
        
    connected_roads = []
    x = int(current_road[0] // tilewidth) - 1
    y = int(current_road[1] // tileheight)
    road = get_connected_road_tiles(x, y, 'L', road_list)
    while (road != None):
        x = x - 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'L', road_list)
    x = int(current_road[0] // tilewidth) + 1
    y = int(current_road[1] // tileheight)
    road = get_connected_road_tiles(x, y, 'R', road_list)
    while (road != None):
        x = x + 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'R', road_list)
    x = int(current_road[0] // tilewidth)
    y = int(current_road[1] // tileheight) - 1
    road = get_connected_road_tiles(x, y, 'U', road_list)
    while (road != None):
        y = y - 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'U', road_list)
    x = int(current_road[0] // tilewidth)
    y = int(current_road[1] // tileheight) + 1
    road = get_connected_road_tiles(x, y, 'D', road_list)
    while (road != None):
        y = y + 1
        connected_roads.append(road)
        road = get_connected_road_tiles(x, y, 'D', road_list)
    return connected_roads


def get_connected_road_tiles(x, y, direction, roads):
    """
    Returns the connected road tile based on the given coordinates and direction.

    Args:
        x (int): The x-coordinate of the current tile.
        y (int): The y-coordinate of the current tile.
        direction (str): The direction to search for the connected road ('U', 'D', 'L', 'R').
        roads (list): The list of all roads.

    Returns:
        road: The connected road tile, or None if no road is found.

    Raises:
        None.

    Examples:
        >>> roads = [road1, road2, road3, road4]
        >>> get_connected_road_tiles(2, 3, 'U', roads)
        road2
    """
    obj_coord_x = x
    obj_coord_y = y
    for road in roads:
        if direction == 'U':
            if int(road.x // (road.parent.tilewidth)) == x and int(road.y // (road.parent.tileheight)) == obj_coord_y:
                return road
        elif direction == 'D':
            if int(road.x // (road.parent.tilewidth)) == x and int(road.y // (road.parent.tileheight)) == obj_coord_y:
                return road
        elif direction == 'L':
            if int(road.x // (road.parent.tilewidth)) == obj_coord_x and int(road.y // (road.parent.tileheight)) == y:
                return road
        elif direction == 'R':
            if int(road.x // (road.parent.tilewidth)) == obj_coord_x and int(road.y // (road.parent.tileheight)) == y:
                return road
    return None


def get_outer_circumference(obj: TiledObject):
    """
    Returns the outer circumference tiles surrounding the given object.

    Args:
        obj (TiledObject): The object for which to calculate the outer circumference.

    Returns:
        list: A list of (x, y) coordinates representing the outer circumference tiles.

    Raises:
        None.

    Examples:
        >>> tiled_obj = TiledObject(...)
        >>> get_outer_circumference(tiled_obj)
        [(x1, y1), (x2, y2), ...]
    """
    tilex = (obj.x // (obj.parent.tilewidth))
    tiley = (obj.y // (obj.parent.tileheight))
    res = []
    for i in range(0, 4):
        res.append((tilex + i, tiley - 1))
        res.append((tilex + i, tiley + 4))

    for i in range(0, 4):
        res.append((tilex - 1, tiley + i))
        res.append((tilex + 4, tiley + i))
    return list(set(res))


def get_connected_by_road_objects(zone, map):
    """
    Returns the objects connected to the given zone through roads.

    Args:
        zone: The zone object for which to find connected objects.
        map: The map object containing the roads and other objects.

    Returns:
        list: A list of objects connected to the zone through roads.

    Raises:
        None.

    Examples:
        >>> zone_obj = Zone(...)
        >>> map_obj = Map(...)
        >>> get_connected_by_road_objects(zone_obj, map_obj)
        [obj1, obj2, ...]
    """
    roads = map.get_roads()
    c = get_outer_circumference(zone)
    roads_connected_to_zone = []
    for tup in c:  # get all surrounding roads to the zone
        for road in roads:
            if int(tup[0]) == int(road.x // ((map.get_tile_width()))) and int(tup[1]) == int(road.y // ((map.get_tile_height()))):
                roads_connected_to_zone.append(road)
    connected_roads = []
    for road in roads_connected_to_zone:
        connected_roads.extend(get_all_connected_roads(road, roads))
    return get_neighboring_objects(connected_roads, map)


def get_neighboring_objects(roads, map):
    """
    Returns a list of neighboring objects connected to the given roads.

    Args:
        roads (list): A list of road objects.
        map: The map object containing the objects.

    Returns:
        list: A list of neighboring objects connected to the roads.

    Raises:
        None.

    Examples:
        >>> road_objs = [road1, road2, ...]
        >>> map_obj = Map(...)
        >>> get_neighboring_objects(road_objs, map_obj)
        [obj1, obj2, ...]
    """
    neighboring_objects = []
    for road in roads:
        obj = get_neighboring_object(road, map)
        if obj:
            neighboring_objects.append(obj)
    return neighboring_objects


def get_all_neighboring_objects(roads, map):
    """
    Returns a list of all neighboring objects connected to the given roads.

    Args:
        roads (list): A list of road objects.
        map: The map object containing the objects.

    Returns:
        list: A list of all neighboring objects connected to the roads.

    Raises:
        None.

    Examples:
        >>> road_objs = [road1, road2, ...]
        >>> map_obj = Map(...)
        >>> get_all_neighboring_objects(road_objs, map_obj)
        [obj1, obj2, ...]
    """
    neighboring_objects = []
    for road in roads:
        object = get_all_neighboring_object(road, map)
        if object:
            neighboring_objects.append(object)
    return neighboring_objects


def get_neighboring_object(road, map):
    """
    Returns the neighboring object connected to the given road.

    Args:
        road: The road object.
        map: The map object containing the objects.

    Returns:
        object: The neighboring object connected to the road, or None if no object is found.

    Raises:
        None.

    Examples:
        >>> road_obj = road1
        >>> map_obj = Map(...)
        >>> get_neighboring_object(road_obj, map_obj)
        obj1
    """
    x = int(road.x // (map.get_tile_width()))
    y = int(road.y // (map.get_tile_height()))
    objects = map.get_all_objects()
    for obj in objects:
        if obj.type == "IndustrialZone" or obj.type == "ServiceZone":
            c = get_outer_circumference(obj)
            for tup in c:
                if int(tup[0]) == x and int(tup[1]) == y:
                    return obj
    return None


def get_all_neighboring_object(road, map):
    """
    Returns all neighboring objects connected to the given road.

    Args:
        road: The road object.
        map: The map object containing the objects.

    Returns:
        List: A list of neighboring objects connected to the road, or an empty list if no objects are found.

    Raises:
        None.

    Examples:
        >>> road_obj = road1
        >>> map_obj = Map(...)
        >>> get_all_neighboring_object(road_obj, map_obj)
        [obj1, obj2, obj3]
    """
    x = int(road.x // (map.get_tile_width()))
    y = int(road.y // (map.get_tile_height()))
    objects = map.get_all_objects()
    for object in objects:
        c = get_outer_circumference(object)
        for tup in c:
            if int(tup[0]) == x and int(tup[1]) == y:
                return object
    return None


def get_num_of_unemployed_in_zone(zone):
    """
    Returns the number of unemployed citizens in the given zone.

    Args:
        zone: The zone object.

    Returns:
        int: The number of unemployed citizens in the zone.

    Raises:
        None.

    Examples:
        >>> zone_obj = zone1
        >>> get_num_of_unemployed_in_zone(zone_obj)
        5
    """
    cnt = 0
    for citizen in zone.properties['Citizens']:
        if citizen.work is None:
            cnt += 1
    return cnt


def get_capacity_and_citizens_of_zones(zones):
    """
    Calculates the total capacity and total number of citizens in a list of zones.

    Args:
        zones (list): A list of zone objects.

    Returns:
        tuple: A tuple containing the total capacity and total number of citizens.
            The first element is the total capacity (int) of all zones.
            The second element is the total number of citizens (int) in all zones.

    Raises:
        None.

    Examples:
        >>> zone_list = [zone1, zone2, zone3]
        >>> get_capacity_and_citizens_of_zones(zone_list)
        (300, 150)
    """
    total_capacity = 0
    total_number_of_citizens = 0
    for zone in zones:
        total_capacity += zone.properties['Capacity']
        total_number_of_citizens += len(zone.properties['Citizens'])
    return total_capacity, total_number_of_citizens


def get_citizen_by_id(id: int):
    """Returns a Citizen object using the id"""
    return Citizen.citizens.get(id)


def get_current_satisfaction() -> int:
    """Returns current overall satisfaction for all citizens"""
    return sum(citizen.satisfaction for citizen in Citizen.citizens.values())


def get_max_possible_satisfaction() -> int:
    """Returns the max satisfaction possible for all created citizens"""
    return len(Citizen.citizens) * 100


def get_total_citizens() -> int:
    """Returns the total number of citizens"""
    return len(Citizen.citizens)


"""
Adders , Assigners, and Deleters
"""


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


def add_citizens_to_game(map):
    """
    Adds citizens to the game based on various factors.

    Args:
        map (Map): The game map.

    Returns:
        None

    Raises:
        None

    Examples:
        map = Map()
        add_citizens_to_game(map)
    """

    distance_threshold = 5  # Minimum distance between residential and working zones
    possible_citizens = 5  # Max possible amount of citizens to arrive during the time period
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
                    if (distance < distance_threshold):
                        nearby_workzones.append(w_zone)

            # part2
            available_cap = sum(
                [(wz.properties['Capacity'] - len(wz.properties['Citizens'])) for wz in nearby_workzones])
            if available_cap >= possible_citizens:
                variety = len(nearby_workzones)
                if (variety >= possible_citizens):
                    part2 = 100.0
                else:
                    decrease = (possible_citizens - variety) * 2.0  # 3%
                    part2 = 100.0 - decrease
            else:
                part2 = available_cap * 10.0
            # part3
            nearby_industrial = industrial_buildings_nearby(zone, map)
            probs = [(abs(p - distance_threshold+1)) *
                     10.0 for p in nearby_industrial]
            part3 = sum(
                probs) / len(nearby_industrial) if len(nearby_industrial) != 0 else 100

            # result
            res = (arrival_chance+part2+part3)/3.0
            zones_with_arrival_chances.append((zone, res))
    for zone, arrival_chance in zones_with_arrival_chances:
        n = int((arrival_chance * possible_citizens) // 100)
        for _ in range(n):
            c = Citizen()
            success_in_assign = assign_to_residential_zone(c, zone, map)
            if (success_in_assign):
                handle_citizen_addition_satisfaction(c, map)


def assign_zone_citizens_to_work(zone, map):
    """
    Assigns citizens of a zone to work zones based on the available work places.

    Args:
        zone (TiledObject): The zone whose citizens need to be assigned to work zones.
        map (Map): The map containing the zone and work places.

    Returns:
        None

    Raises:
        None

    Examples:
        zone = ResidentialZone()
        map = Map()
        assign_zone_citizens_to_work(zone, map)
    """
    available_work_places = [obj for obj in get_connected_by_road_objects(
        zone, map) if len(obj.properties['Citizens']) < obj.properties['Capacity']]
    for citizen in zone.properties['Citizens']:
        if citizen.work == None:
            assign_to_work_zones(citizen, available_work_places, map)


def assign_to_work_zones(citizen, available_work_places, map):
    """
    Assigns a citizen to a work zone based on the available work places.

    Args:
        citizen (Citizen): The citizen to be assigned to a work zone.
        available_work_places (list): A list of available work places (zones) to choose from.
        map (Map): The map containing the work places (zones).

    Returns:
        None

    Raises:
        None

    Examples:
        citizen = Citizen()
        available_work_places = [zone1, zone2, zone3]
        map = Map()
        assign_to_work_zones(citizen, available_work_places, map)
    """
    I_zones = [
        zone for zone in available_work_places if zone.type == "IndustrialZone"]
    S_zones = [
        zone for zone in available_work_places if zone.type == "ServiceZone"]
    total_capacity_of_I_zones, total_number_of_citizens_in_I_zones = get_capacity_and_citizens_of_zones(
        I_zones)
    total_capacity_of_S_zones, total_number_of_citizens_in_S_zones = get_capacity_and_citizens_of_zones(
        S_zones)

    if total_capacity_of_I_zones == 0 and total_capacity_of_S_zones == 0:
        return

    needed_citizens_for_I_zones = total_capacity_of_I_zones - \
        total_number_of_citizens_in_I_zones
    needed_citizens_for_S_zones = total_capacity_of_S_zones - \
        total_number_of_citizens_in_S_zones
    if needed_citizens_for_I_zones > needed_citizens_for_S_zones:
        assign_citizen_to_random_zone(citizen, I_zones, map)
    else:
        assign_citizen_to_random_zone(citizen, S_zones, map)


def assign_citizen_to_random_zone(c, zones, map):
    """
    Assigns a citizen to a randomly selected zone from the given list of zones.

    Args:
        c (Citizen): The citizen to be assigned to a zone.
        zones (list): A list of zones to choose from.
        map (Map): The map containing the zones.

    Returns:
        None

    Raises:
        None

    Examples:
        c = Citizen()
        zones = [zone1, zone2, zone3]
        map = Map()
        assign_citizen_to_random_zone(c, zones, map)
    """
    if zones:
        random_zone = random.choice(zones)
        assign_to_work_zone(c, random_zone, map)


def assign_to_residential_zone(citizen, RZone, mapInstance) -> bool:
    """
    Gives the citizen a home, deletes the Citizen if there's a failure assigning a home.
    mapInstance is required to be passed in order to simulate the addition of the buildings on top of the Zone

    Args:
        RZone: ResidentialZone
        mapInstance : Map object

    Returns:
        Nothing 
    """
    if (add_citizen(RZone, citizen)):
        citizen.home = RZone
        simulate_building_addition(RZone, mapInstance)
        return True
    else:
        if (citizen.work):
            citizen.work.remove_citizen(citizen)
        del Citizen.citizens[citizen.id]
        return False


def assign_to_work_zone(citizen, WorkZone, mapInstance) -> bool:
    """Assigns the citizen to either a ServiceZone or IndustrialZone, returns a bool value if a failure assigning work happens"""
    if (add_citizen(WorkZone, citizen)):
        citizen.work = WorkZone
        simulate_building_addition(WorkZone, mapInstance)
        return True
    else:
        return False


def delete_citizen(c: Citizen) -> bool:
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
        print(
            f"Fatal failure deleting citizen {c} with data: {c.__dict__}. Error: {e}")
        return False


def remove_citizen_from_zone(tiledObj: TiledObject, citizen: Citizen) -> bool:
    """
    Removes a citizen from the tiledObj

    Returns:
    boolean value indicating the success of removing the given citizen
    """
    try:
        tiledObj.properties['Citizens'].remove(citizen)
        return True
    except Exception as e:
        print(
            f"Fatal failure removing citizen {citizen} with data {citizen.__dict__} from {tiledObj}. Error: {e}")
        return False


"""
Checkers
"""


def is_satisfaction_zone(SZone: TiledObject):
    """
    Check if the given tiledobject is a satisfaction increaser
    """
    if (SZone.type == 'Stadium' or SZone.type == 'PoliceDepartment' or SZone.type == 'Forest'):
        return True
    return False


def is_in_visited(road_tuple, visited):
    """
    Checks if a road with the given coordinates is in the visited set.

    Args:
        road_tuple (tuple): A tuple containing the x and y coordinates of the road.
        visited (set): A set of visited roads.

    Returns:
        bool: True if the road is in the visited set, False otherwise.

    Raises:
        None

    Examples:
        road_tuple = (2, 3)
        visited = {(1, 2), (3, 4), (2, 3)}
        is_in_visited(road_tuple, visited)
    """
    for road in visited:
        if road_tuple[0] == road.x and road_tuple[1] == road.y:
            return True
    return False


def is_there_a_blocker_between(Frst: TiledObject, RZone: TiledObject, lst):
    """
    Get the points which represent the view of the RZone and the Forest,
    Checks if there is a blocker between the Forest and the RZone

    Args:
    Frst: Forest TiledObject
    RZone: ResidentialZone TiledObject
    lst: list consisting of all dynamic objects
    """
    wall = get_points_looking_at_each_other(Frst, RZone)
    mid = len(wall) // 2
    l1 = wall[:mid]
    l2 = wall[mid:]
    res = [get_path_between_points(p1, p2) for p1, p2 in zip(l1, l2)]
    flattened_res = [item for sublist in res for item in sublist]
    for obj in lst:
        if ((obj != Frst or obj != RZone) and obj.type != 'Road'):
            s1 = set(get_area(obj))
            s2 = set(flattened_res)
            if s1.intersection(s2):
                return True
    return False


def can_move_into(zone: TiledObject) -> bool:
    """
    Checks if a Citizen can move into the Zone
    """
    if len(zone.properties['Citizens']) < zone.properties['Capacity']:
        return True
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


def has_random_years_passed_from_start(gameStart, givenDate: Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a year has passed or not """
    years_passed = givenDate.subtract_with_time_str(gameStart) // 365
    random_array = [random.randint(
        years_passed+1, years_passed+99) for _ in range(99)]
    random_array.append(years_passed)
    choice = random.choice(random_array)
    if choice - years_passed == 0:
        return True
    else:
        return False


def industrial_buildings_nearby(zone, map):
    """
    Finds industrial buildings near the given zone within a certain distance threshold.

    Args:
        zone (TiledObject): The zone object to check for nearby industrial buildings.
        map (Map): The map object containing all the zones.

    Returns:
        list: A list of distances between the given zone and nearby industrial buildings.

    Raises:
        None

    Examples:
        zone = residential_zone
        map = game_map
        industrial_buildings_nearby(zone, map)
    """
    distance_threshold = 5  # Minimum distance between residential and industrial zones
    industrial_buildings_nearby = []
    I_zones = map.get_industrial_zones()
    for I_zone in I_zones:
        distance = distance_between_two(zone, I_zone)
        if distance < distance_threshold:
            industrial_buildings_nearby.append(distance)
    return industrial_buildings_nearby


def distance_between_two(obj1: TiledObject, obj2: TiledObject):
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
        if p in c2_xs:
            in_c1_xs = True
            break
    for p in c1_ys:
        if p in c2_ys:
            in_c1_ys = True
            break

    l = []
    min = 69420

    for p1 in c1:
        for p2 in c2:
            d = calc_d(p1, p2)
            if (d <= min):
                min = d
                l.clear()
                l.append(p1)
                l.append(p2)
    if (not in_c1_xs and not in_c1_ys):
        return (calc_d(l[0], l[1]) // 2) + 1
    return min


def calc_d(p1, p2) -> int:
    """
    Helper to calculate the distance between the two given points
    """
    horizontal_distance = abs(p1[0]-p2[0])
    vertical_distance = abs(p1[1]-p2[1])
    distance = (horizontal_distance + vertical_distance)
    return distance - 1
    # distance = math.sqrt((horizontal_distance)**2 + (vertical_distance)**2)
    # return math.floor(distance)


def tile_in_which_zone(coords, zones):
    """
    Finds the zone object that contains the given coordinates.

    Args:
        coords (tuple): The coordinates (x, y) of the tile to check.
        zones (list): A list of zone objects to search.

    Returns:
        TiledObject: The zone object that contains the given coordinates,
            or None if no zone contains the coordinates.

    Raises:
        None

    Examples:
        coords = (4, 5)
        zones = [zone1, zone2, zone3]
        tile_in_which_zone(coords, zones)
    """
    for zone in zones:
        if coords in get_area(zone):
            return zone
    return None


"""
PathFinding , Handlers, Simulators
"""


def dfs(current_road, visited, road_list):
    """
    Performs a Depth-First Search (DFS) traversal on a road network.

    Args:
        current_road (Road): The current road to start the DFS traversal from.
        visited (set): A set to store visited roads.
        road_list (list): A list of all roads in the road network.

    Returns:
        None

    Raises:
        None

    Examples:
        visited = set()
        road_list = [road1, road2, road3]
        dfs(road1, visited, road_list)
    """
    # Extract relevant attributes into a tuple
    road_tuple = (current_road.x, current_road.y)
    dimension_tuple = (current_road.parent.tilewidth,current_road.parent.tileheight)
    visited.add(current_road)

    # Explore adjacent roads (branches)
    connected_roads = get_connected_roads(road_tuple, road_list,dimension_tuple)

    for road in connected_roads:
        # Extract relevant attributes into a tuple
        road_tuple = (road.x, road.y)
        if not is_in_visited(road_tuple, visited):
            dfs(road, visited, road_list)


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
        building = form_tiled_obj(obj, map)
        objLayer = obj.parent.get_layer_by_name("ObjectsTop")
        objLayer.append(building)
        obj.properties['Buildings'].append(building.__dict__)


def upgrade_zone(zone: TiledObject, mapInstance):
    """
    Upgrades the clicked Zone (RZone/CZone/IZone)
    """
    zone.properties['Level'] += 1
    zone.properties['Capacity'] = math.ceil(zone.properties['Capacity'] * 1.5)
    zone.properties['MaintenanceFee'] *= 0.25
    lst = get_linked_ids_for_obj(zone)
    obj_layer = mapInstance.return_map().get_layer_by_name("ObjectsTop")
    for obj in lst:
        obj_layer.remove(obj)
        del (obj)
    zone.properties['Buildings'] = []
    building = form_tiled_obj(zone, mapInstance)
    obj_layer.append(building)
    zone.properties['Buildings'].append(building.__dict__)


def delete_zone_data(zone: TiledObject, mapInstance) -> list:
    """
    Function to destory the data of the Zone and the Zone itself

    Modifies Citizens data accordingly

    Args:
    zone: Zone to destory
    mapInstance: Map class

    Returns:
    list of Citizens who were removed from the Zone
    """
    if zone.type[-4:] != 'Zone':
        return []
    citizens = []
    for c in zone.properties['Citizens']:
        citizens.append(c)
    for c in citizens:
        remove_citizen_from_zone(zone, c)
        if (zone.type == 'ResidentialZone'):
            c.home = None
        elif (zone.type == 'IndustrialZone' or zone.type == 'ServiceZone'):
            c.work = None
    buildings = get_linked_ids_for_obj(zone)
    for b in buildings:
        mapInstance.remove_disaster_or_building(b)
    mapInstance.reclassify_zone(zone)
    return citizens


def demolish_zone(zone: TiledObject, mapInstance, player):
    """
    Demolishes the clicked Zone (RZone/CZone/IZone)
    """
    if (zone.type == 'ResidentialZone'):
        citizens = delete_zone_data(zone, mapInstance)
        homeless = len(citizens)
        for c in citizens:
            if (c.work):
                remove_citizen_from_zone(c.work, c)
                c.work = None
        # Give home
        for c in citizens:
            RZones = mapInstance.get_yet_to_occupy_homes()
            if (len(RZones) == 0):
                break
            random.shuffle(RZones)
            for RZone in RZones:
                if can_move_into(RZone):
                    if (assign_to_residential_zone(c, RZone, mapInstance)):
                        player.money -= 100
                        homeless -= 1
                    break
        if (homeless != 0):
            to_leave = citizens[-homeless:]
            for c in to_leave:
                player.money -= 150
                delete_citizen(c)
    elif (zone.type == 'IndustrialZone' or zone.type == 'ServiceZone'):
        citizens = delete_zone_data(zone, mapInstance)
        for c in citizens:
            player.money -= 100


def handle_citizen_addition_satisfaction(c: Citizen, map):
    """
    After assigning a citizen to an RZone, checks nearby SatisfactionIncreasers and adds accordingly
    """
    for SZone in map.get_satisfaction_increasers():
        if (distance_between_two(c.home, SZone) <= SZone.properties['Radius']):
            if (SZone.type == "Forest"):
                if (is_there_a_blocker_between(c.home, SZone, map.get_all_objects())):
                    continue
                else:
                    tmp = c.satisfaction + \
                        (SZone.properties['Satisfaction']*c.satisfaction)
                    if tmp <= 100:
                        c.satisfaction += (
                            SZone.properties['Satisfaction']*c.satisfaction)
            else:
                tmp = c.satisfaction + \
                    (SZone.properties['Satisfaction']*c.satisfaction)
                if tmp <= 100:
                    c.satisfaction += (
                        SZone.properties['Satisfaction']*c.satisfaction)


def handle_disaster_logic(map, givenDate: Timer):
    """
    Internal logic handling for disaster object
    """
    disasters = map.get_all_disasters()
    for disaster in disasters:
        if (has_month_passed_from_creation(disaster, givenDate)):
            for obj in disaster.properties['linked_objs']:
                lnked = [b for b in map.get_buildings() if b.type !=
                         'Disaster' and b.properties['linked_id'] == obj.id]

                if (obj.type == 'ResidentialZone'):
                    rmf = []
                    for c in obj.properties['Citizens']:
                        rmf.append(c)
                        if (c.work):
                            remove_citizen_from_zone(c.work, c)
                            c.work = None
                    for c in rmf:
                        remove_citizen_from_zone(obj, c)
                        c.home = None
                        delete_citizen(c)
                    obj.properties['Citizens'] = []
                    for b in lnked:
                        map.remove_disaster_or_building(b)
                    map.reclassify_zone(obj)

                elif (obj.type == 'IndustrialZone' or obj.type == 'ServiceZone'):
                    rmf = []
                    for c in obj.properties['Citizens']:
                        rmf.append(c)
                        c.work = None
                    for c in rmf:
                        remove_citizen_from_zone(obj, c)
                    obj.properties['Citizens'] = []
                    for b in lnked:
                        map.remove_disaster_or_building(b)
                    map.reclassify_zone(obj)

                elif (obj.type == 'PoliceDepartment' or obj.type == 'Stadium' or obj.type == 'Forest'):
                    map.reclassify_zone(obj)
            map.remove_disaster_or_building(disaster)


def handle_satisfaction_zone_removal(SZone: TiledObject, RZones):
    """
    After the player deletes a Stadium or PoliceDepartment , it checks nearby Citizens and decreases satisfaction

    (Reclassify Forest because of Disaster uses this function)
    """
    for RZone in RZones:
        if (distance_between_two(RZone, SZone) <= SZone.properties['Radius']):
            for c in RZone.properties['Citizens']:
                tmp = c.satisfaction + \
                    (SZone.properties['Satisfaction']*c.satisfaction)
                if tmp >= 0:
                    c.satisfaction -= (
                        SZone.properties['Satisfaction']*c.satisfaction)


def handle_disaster_random_logic(mapInstance, givenDate, randomizer: bool):
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
            disaster_make = Disaster(
                to_destroy.x//(mapInstance.get_tile_width()), to_destroy.y//(mapInstance.get_tile_height()), givenDate, mapInstance)
            obj = disaster_make.instance
            obj.properties['linked_objs'] = [to_destroy]
            mapInstance.add_disaster_to_map(obj)


def handle_prompt_logic(map, clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh):
    """
    Prompt handling internal logic

    Changes upgrd,rclssfy parameters accordingly

    Args:
    map: Map class
    clckd_crds: mouse pos
    clcked_zn: Clicked TiledObject
    upgrd: pygame rect
    rclssfy: pygame rect, used to reclassify a Zone, also to delete PoliceDepartment,Stadium
    dmlsh: pygame rect

    Returns:
    All given parameters except for map as a tuple
    """
    # Handle deletion of PoliceDepartment or Stadium
    if (clckd_zn.type == "PoliceDepartment" or clckd_zn.type == "Stadium"):
        upgrd = dmlsh = None
        rclssfy = map.draw_prompt(clckd_crds, clckd_zn)[0]
    else:
        # Handle already clicked Zone (RZone,CZone,IZone)
        upgrd = rclssfy = dmlsh = None
        if (clckd_zn.properties['Level'] < 3 and clckd_zn.type[-4:] == 'Zone'):
            amount_citizens = len(clckd_zn.properties['Citizens'])
            amount_buildings = len(clckd_zn.properties['Buildings'])
            if (amount_citizens == 0):
                # Reclassify
                btns = map.draw_prompt(clckd_crds, clckd_zn)
                if amount_buildings == 0:
                    rclssfy = btns[0]
                    upgrd = dmlsh = None
                # Destroy
                elif amount_buildings <= 4 and amount_buildings > 0:
                    dmlsh = btns[0]
                    upgrd = rclssfy = None
            elif (amount_citizens >= 1):
                # Upgrade and Demolish
                btns = map.draw_prompt(clckd_crds, clckd_zn)
                upgrd = btns[0]
                dmlsh = btns[1]
                rclssfy = None
            else:
                upgrd = rclssfy = dmlsh = None
        elif (clckd_zn.properties['Level'] == 3 and clckd_zn.type[-4:] == 'Zone'):
            upgrd = rclssfy = None
            dmlsh = map.draw_prompt(clckd_crds, clckd_zn)[0]
        else:
            upgrd = rclssfy = dmlsh = None
    return clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh


def handle_prompt(map, clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh, dmlsh_cnfrm):
    """
    Handles prompt when viewing the information of the Zone

    Args:
    map: Map class
    clckd_crds: mouse pos
    clcked_zn: Clicked TiledObject
    upgrd: pygame rect
    rclssfy: pygame rect
    dmlsh: pygame rect
    dmlsh_cnfrm: pygame rect

    Returns:
    All given parameters except for map as a tuple
    """
    if clckd_crds:
        if (clckd_zn):
            if (not map.does_obj_exist(clckd_zn)):
                clckd_crds = clckd_zn = upgrd = rclssfy = dmlsh = dmlsh_cnfrm = None
                return clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh, dmlsh_cnfrm

            if (dmlsh_cnfrm):
                dmlsh_cnfrm = map.draw_confirm_prompt_to_demolish(
                    clckd_crds, clckd_zn)
            else:
                clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh = handle_prompt_logic(
                    map, clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh)
        else:
            # Reterive the Zone if not clicked in the first place
            zones = [obj for obj in map.get_all_objects() if (
                obj.type != "Forest" and obj.type != "Road")]
            clckd_zn = tile_in_which_zone(
                map.get_clicked_tile(clckd_crds), zones)
            if (clckd_zn):
                if (not map.does_obj_exist(clckd_zn)):
                    clckd_crds = clckd_zn = upgrd = rclssfy = dmlsh = dmlsh_cnfrm = None
                    return clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh, dmlsh_cnfrm

                if (dmlsh_cnfrm):
                    dmlsh_cnfrm = map.draw_confirm_prompt_to_demolish(
                        clckd_crds, clckd_zn)
                else:
                    clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh = handle_prompt_logic(
                        map, clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh)
            else:
                clckd_crds = clckd_zn = upgrd = rclssfy = dmlsh = dmlsh_cnfrm = None
    return clckd_crds, clckd_zn, upgrd, rclssfy, dmlsh, dmlsh_cnfrm


def handle_tree_growth(map, SZone: TiledObject):
    """
    After the tree grows, it must affect the nearby citizens
    """
    for RZone in map.get_residential_zones():
        if (distance_between_two(RZone, SZone) <= SZone.properties['Radius']):
            if (is_there_a_blocker_between(SZone, RZone, map.get_all_objects())):
                continue
            else:
                for c in RZone.properties['Citizens']:
                    tmp = c.satisfaction + \
                        (SZone.properties['Satisfaction']*c.satisfaction)
                    if tmp <= 100:
                        c.satisfaction += (
                            SZone.properties['Satisfaction']*c.satisfaction)


def handle_satisfaction_zone_addition(map, SZone: TiledObject):
    """
    After the player creates a Stadium, PoliceDepartment, or Forest, it checks nearby Citizens and adds satisfaction
    """
    for RZone in map.get_residential_zones():
        if (distance_between_two(RZone, SZone) <= SZone.properties['Radius']):
            if (SZone.type == "Forest"):
                if (is_there_a_blocker_between(SZone, RZone, map.get_all_objects())):
                    continue
                else:
                    for c in RZone.properties['Citizens']:
                        tmp = c.satisfaction + \
                            (SZone.properties['Satisfaction']*c.satisfaction)
                        if tmp <= 100:
                            c.satisfaction += (
                                SZone.properties['Satisfaction']*c.satisfaction)
            else:
                for c in RZone.properties['Citizens']:
                    tmp = c.satisfaction + \
                        (SZone.properties['Satisfaction']*c.satisfaction)
                    if tmp <= 100:
                        c.satisfaction += (
                            SZone.properties['Satisfaction']*c.satisfaction)


def randomize_initial_forests(map, player, timer):
    """
    Creates random forests at the start of the game
    """
    coords = [(11, 5), (28, 33), (6, 16), (32, 23)]
    num_choices = random.randint(1, len(coords))
    to_insert = random.sample(coords, num_choices)
    for p in to_insert:
        frst = Forest(p[0], p[1], timer.get_current_date_str(), map)
        map.add_object(frst.instance, player, True)


"""
Menu functions
"""


def resume_game(running, game_loop, run_call_back, allocated_tax):
    """
    Resumes a game.

    This function is used to resume a game. It sets the `game_loop` variable to True
    to indicate that the game loop should continue running. It then calls the
    `run_call_back` function, passing the `running`, `False`, `False`, and
    `allocated_tax` values to indicate that the game should be resumed with the
    specified parameters.

    Args:
        running (bool): The running flag indicating whether the game loop should continue.
        game_loop (bool): The game loop flag indicating whether the game loop is active.
        run_call_back (function): The callback function to start the game.
        allocated_tax (float): The allocated tax value for the game.

    Returns:
        None
    """
    print("========================== resume ==================================")
    game_loop = True
    run_call_back(running, False, False, allocated_tax)


def save_game(running, map, game_loop, run_call_back, allocated_tax, list_of_tiled_objs, saved_game_speed, saved_speed_multiplier, saved_current_time_str):
    """
    Saves the game state.

    This function is used to save the current game state. It collects relevant information
    about the game, such as the state of citizens, tiled objects, timers, and object counts.
    It then saves this information to a file using the pickle module.

    Args:
        running (bool): The running flag indicating whether the game loop should continue.
        map: The map object representing the game map.
        game_loop (bool): The game loop flag indicating whether the game loop is active.
        run_call_back (function): The callback function to start the game.
        allocated_tax (float): The allocated tax value for the game.
        list_of_tiled_objs (list): A list of tiled objects in the game.
        saved_game_speed (int): The saved game speed.
        saved_speed_multiplier (int): The saved speed multiplier.
        saved_current_time_str (str): The saved current time as a string.

    Returns:
        None
    """
    print("========================== save ==================================")
    citizens = []
    citizens_objs = Citizen.get_all_citizens()
    for citizen_id, citizen in citizens_objs.items():
        citizen_list = []
        citizen_list.append(citizen_id)
        if citizen.home:
            citizen_list.append(citizen.home.id)
        else:
            citizen_list.append(-1)
        if citizen.work:
            citizen_list.append(citizen.work.id)
        else:
            citizen_list.append(-1)
        citizen_list.append(citizen.satisfaction)
        citizens.append(citizen_list)

    saved_citizens = []
    # update tiled_object list
    for obj in list_of_tiled_objs:
        if obj['type'][-4:] == 'Zone':
            saved_citizens.append(obj['properties']['Citizens'])
            for building in obj['properties']['Buildings']:
                building['parent'] = ""
        obj['properties']['Citizens'] = []
        obj['parent'] = ""

    my_timer = []
    my_timer.append(saved_game_speed)
    my_timer.append(saved_speed_multiplier)
    my_timer.append(saved_current_time_str)
    obj_count = map.get_object_count()
    next_obj_count = map.get_next_obj_id()

    # load the parent back (since parent object is not serilizable and therfore cannot be pickled)
    with open('game_state.pickle', 'wb') as f:
        pickle.dump(citizens, f)
        pickle.dump(list_of_tiled_objs, f)
        pickle.dump(my_timer, f)
        pickle.dump(obj_count, f)
        pickle.dump(next_obj_count, f)
        pickle.dump(allocated_tax,f)

    tmp_counter = 0
    for obj in list_of_tiled_objs:
        obj['parent'] = map.return_map()
        if obj['type'][-4:] == 'Zone':
            obj['properties']['Citizens'] = saved_citizens[tmp_counter]
            tmp_counter += 1
            for building in obj['properties']['Buildings']:
                building['parent'] = map.return_map()

    game_loop = True
    run_call_back(running, False, False, allocated_tax)


def main_menu(running, game_loop, run_call_back, allocated_tax):
    """
    Displays the main menu.
    """
    print("========================== Main menu ==================================")
    game_loop = False


def allocate_tax(running, game_loop, run_call_back, allocated_tax):
    """
    Handles the tax allocation process in the game.

    This function is used to handle the tax allocation process in the game.
    It takes the running flag, game loop flag, callback function, and current tax allocation as parameters.

    Args:
        running (bool): The running flag indicating whether the game loop should continue.
        game_loop (bool): The game loop flag indicating whether the game loop is active.
        run_call_back (function): The callback function to start the game.
        allocated_tax (float): The current allocated tax value for the game.

    Returns:
        None
    """
    print("========================== Tax allocation is running ==================================")
    taskAllactor = TaskAllocator()
    taskAllactor.run()
    allocated_tax = float(taskAllactor.get_input_text())
    run_call_back(running, False, False, allocated_tax)


def show_menu(screen, map, running, game_loop, run_call_back, allocated_tax, list_of_tiled_objs, saved_game_speed, saved_speed_multiplier, saved_current_time_str):
    """
    Displays the ingame menu screen to the player.

    This function is used to display a menu screen to the player with various options.
    It takes several parameters including the screen surface, game map, running flag, game loop flag,
    callback function, current tax allocation, list of tiled objects, saved game speed, saved speed multiplier,
    and saved current time.

    Args:
        screen (pygame.Surface): The screen surface to display the menu on.
        map: The game map object.
        running (bool): The running flag indicating whether the game loop should continue.
        game_loop (bool): The game loop flag indicating whether the game loop is active.
        run_call_back (function): The callback function to start or resume the game.
        allocated_tax (float): The current allocated tax value for the game.
        list_of_tiled_objs (list): The list of tiled objects in the game.
        saved_game_speed (int): The saved game speed value.
        saved_speed_multiplier (int): The saved speed multiplier value.
        saved_current_time_str (str): The saved current time in string format.

    Returns:
        None
    """
    menu_height = 400
    menu_width = 400
    screen_width = 1024
    screen_height = 768
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2

    menu_surface = pygame.Surface((menu_width, menu_height))
    menu_surface.fill((200, 200, 200))
    # Create the menu options
    menu_options = [
        ("Resume Game", resume_game),
        ("Save Game", save_game),
        ("Main menu", main_menu),
        ("Allocate Tax", allocate_tax)
    ]

    # Add the menu options to the menu surface
    font = pygame.font.SysFont("Calibri", 48, bold=True)
    selected_option = 0
    menu_loop = True
    while menu_loop:
        for i, (text, action) in enumerate(menu_options):
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(menu_width / 2, 75 + i * 75))
            if i == selected_option:
                pygame.draw.rect(menu_surface, (220, 220, 220), text_rect, 2)
            else:
                pygame.draw.rect(menu_surface, (180, 180, 180), text_rect, 2)
            menu_surface.blit(text_surface, text_rect)

        # Show the menu surface on the main surface
        screen.blit(menu_surface, (menu_x, menu_y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    selected_option = max(0, selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    selected_option = min(
                        len(menu_options) - 1, selected_option + 1)
                elif event.key == pygame.K_RETURN:
                    selected = menu_options[selected_option][0]
                    action = menu_options[selected_option][1]
                    if (selected == "Save Game"):
                        game_loop = action(running, map, game_loop, run_call_back, allocated_tax, list_of_tiled_objs,
                                           saved_game_speed, saved_speed_multiplier, saved_current_time_str)
                    else:
                        game_loop = action(running, game_loop,
                                           run_call_back, allocated_tax)
                    menu_loop = False
