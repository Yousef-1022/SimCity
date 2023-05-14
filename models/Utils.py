import os
from pytmx import TiledObject
from models.Timer import Timer
from models.BuildingAdder import form_tiled_obj
import math


def get_files_from_dir (dir_path) -> list:
    """Returns all the files as a list from the given path"""
    return os.listdir(dir_path)

def get_icon_and_type (file , dir_attachment=None) -> tuple:
    """Returns a (FileLocation , ClassName) tuple"""
    parts = file.split("_")
    type = os.path.splitext(parts[1])[0]
    if (dir_attachment):
        return(dir_attachment+file,type)
    return (file,type)

def get_icon_loc_by_name (name,tuple_list) -> list:
    """Returns a list consisting of (FileLocation , ClassName) tuples"""
    return ([t[0] for t in tuple_list if name in t[0]])[0]

def add_citizen (tiledObj:TiledObject,citizen):
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
    
def remove_citizen_from_zone (tiledObj:TiledObject,citizen):
    """Removes a citizen from the tiledObj"""
    try:
        tiledObj.properties['Citizens'].remove(citizen)
    except Exception as e:
        print(f"Fatal failure removing citizen {citizen} from {tiledObj}. Error: {e}")

def has_year_passed_from_creation(obj:TiledObject,givenDate:Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a year has passed or not """
    x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
    return x != 0 and x % 365 == 0
    
def has_quarter_passed_from_creation(obj:TiledObject,givenDate:Timer) -> bool:
    """Checks if a quarter (90 days) passed since creation"""
    if obj:
        x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
        return x != 0 and x % 90 == 0
    return False

def simulate_building_addition(obj:TiledObject,map):
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
        building = form_tiled_obj(obj,map)
        objLayer = obj.parent.get_layer_by_name("ObjectsTop")
        objLayer.append(building)
            
    
def get_linked_ids_for_obj(obj:TiledObject) -> list:
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
    if image_type == "ResidentialZone" or image_type == "IndustrialZone" or "ServiceZone" == image_type:
        return 128
    elif image_type == "PoliceDepartment" or image_type == "Forest":
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

def distance_between_two(obj1:TiledObject,obj2:TiledObject):
    """
    Returns the minimal distance between the two tiled objects
    
    Checks the cirumference of both, and calculates the distance of the closest two points
    """
    
    c1=get_circumference(obj1)
    c2=get_circumference(obj2)
    min = 69420
    for p1 in c1:
        for p2 in c2:
            d = calc_d(p1,p2)
            if (d <= min):
                min = d
    return min

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
    zone.properties['Level'] += 1
    zone.properties['Capacity'] *= 1.5
    zone.properties['MaintenanceFee'] *= 0.25
    lst = get_linked_ids_for_obj(zone)
    obj_layer = mapInstance.returnMap().get_layer_by_name("ObjectsTop")
    for obj in lst:
        obj_layer.remove(obj)
    building = form_tiled_obj(zone,mapInstance)
    obj_layer.append(building)
            