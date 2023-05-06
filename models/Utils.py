import os
from pytmx import TiledObject
from models.Timer import Timer
from models.BuildingAdder import form_tiled_obj


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
    if x != 0 and x % 365 == 0:
        return True
    return False
    
def has_quarter_passed_from_creation(obj:TiledObject,givenDate:Timer) -> bool:
    """Checks if a quarter (90 days) passed since creation"""
    x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
    if x != 0 and x % 90 == 0:
        return True
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
        objLayer = map.returnMap().get_layer_by_name("ObjectsTop")
        objLayer.append(building)
            
    
def get_linked_ids_for_obj(obj:TiledObject) -> list[int]:
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
