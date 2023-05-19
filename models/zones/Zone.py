import xml.etree.ElementTree as ET
from pytmx import TiledObject

class Zone:
    def __init__(self,x,y,creationTime):
        self.x = x 
        self.y = y
        self.creationTime = creationTime
        self.price = 0
        
    def create_zone_obj(self,mapInstance) -> TiledObject:
        """Creates a zone object, requires the map to be passed"""
        zoneType = type(self).__name__
        placeholder = mapInstance.get_static_object_by_type(zoneType)
        width = mapInstance.get_tile_width()
        height = mapInstance.get_tile_height()
        id = mapInstance.get_next_obj_id()
        xml = ET.fromstring(f' \
            <object id="{id}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{self.x*width}" y="{self.y*height}" width="{placeholder.width}" height="{placeholder.height}"> \
                <properties> \
                    <property name="Level" type="int" value="1"/> \
                    <property name="Placeholder" value="dynamic"/> \
                    <property name="Citizens" value=""/>  \
                    <property name="Buildings" value=""/>  \
                    <property name="Capacity" type="int" value="0"/>  \
                    <property name="CreationDate" value="{self.creationTime}"/> \
                    <property name="Price" value="{self.price}"/> \
                    <property name="Revenue" type="int" value="0"/> \
                    <property name="MaintenanceFee" type="int" value="0"/> \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.return_map(),xml)
        obj.gid = placeholder.gid
        obj.properties['Citizens'] = []
        obj.properties['Buildings'] = []
        return obj