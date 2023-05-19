import xml.etree.ElementTree as ET
from pytmx import TiledObject

class Road:
    
    price = 75
    
    def __init__(self,x,y,creation_time,mapInstance):
        self.x = x 
        self.y = y
        self.creation_time = creation_time
        self.price = Road.price
        self.instance = self.create_road_obj(mapInstance)
        self.instance.properties['MaintenanceFee'] = 400
        
    def create_road_obj(self,mapInstance) -> TiledObject:
        """Creates a road object, requires the map to be passed"""
        road_type = type(self).__name__
        placeholder = mapInstance.get_static_object_by_type(road_type)
        width = mapInstance.get_tile_width()
        height = mapInstance.get_tile_height()
        id = mapInstance.get_next_obj_id()
        xml = ET.fromstring(f' \
            <object id="{id}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{self.x*width}" y="{self.y*height}" width="{placeholder.width}" height="{placeholder.height}"> \
                <properties> \
                    <property name="Placeholder" value="dynamic"/> \
                    <property name="CreationDate" value="{self.creation_time}"/> \
                    <property name="Price" value="{self.price}"/> \
                    <property name="MaintenanceFee" type="int" value="{int(self.price/4)}"/> \
                    <property name="Citizens" value=""/>  \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.return_map(),xml)
        obj.gid = placeholder.gid
        obj.properties['Citizens'] = []
        return obj