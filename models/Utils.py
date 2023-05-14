import os
from pytmx import TiledObject
from models.Timer import Timer
from models.BuildingAdder import form_tiled_obj


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

