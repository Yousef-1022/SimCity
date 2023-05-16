import xml.etree.ElementTree as ET
from pytmx import TiledObject
import random

def get_possible_coords(TiledObj:TiledObject) -> list:
    """
    Returns a list of possible coordinates which building can be added to
    Used only by residential zone
    """
    lst = []
    x1,y1 = (TiledObj.x)//32 , (TiledObj.y)//32
    lst.append((x1,y1))
    x2,y2 = (x1 + 2) , y1
    lst.append((x2,y2))
    x3,y3 = x1 , (y1+2)
    lst.append((x3,y3))
    x4,y4 = (x1 + 2) , (y1 + 2)
    lst.append((x4,y4))
    return lst

def get_occupied_tiles(TiledObj:TiledObject) -> list:
    """
    Returns a list of already occupied coordinates (built buildings on the Zone)
    """
    lst = []
    Objects = TiledObj.parent.get_layer_by_name("ObjectsTop")
    for o in Objects:
        if o.properties['linked_id'] == TiledObj.id:
            lst.append((o.x//32,o.y//32))
    return lst

def form_tiled_obj (TiledObj:TiledObject,mapInstance) -> TiledObject:
    """
    Creates an object that can be put on top of the Zone for the visual effect
    
    UseCase: Zones only
    
    Args:
    tiledObj: TiledObject (the required zone)
    mapInstance: Map object (required)
    
    Returns:
    Newly formed TiledObject
    """
    the_name = ""
    xtile = TiledObj.x
    ytile = TiledObj.y
    if (TiledObj.name == "RZone"):
        the_name = f'RZoneHouse{random.randint(1,4)}'
        occupied = get_occupied_tiles(TiledObj)
        possible = get_possible_coords(TiledObj)
        take = [xy for xy in possible if xy not in occupied]
        xy = random.choice(take)
        xtile=xy[0]*32
        ytile=xy[1]*32
    else:
        the_name = f'{TiledObj.name}LVL{TiledObj.properties["Level"]}'
    placeholder = mapInstance.getStaticObjectByName(the_name)        
    xml = ET.fromstring(f' \
        <object id="{-1}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{xtile}" y="{ytile}" width="{placeholder.width}" height="{placeholder.height}"> \
            <properties> \
                <property name="linked_id" type="int" value="{TiledObj.id}"/> \
                <property name="Placeholder" value="static"/> \
            </properties> \
        </object>')
    
    obj = TiledObject(mapInstance.returnMap(),xml)
    obj.gid = placeholder.gid
    return obj