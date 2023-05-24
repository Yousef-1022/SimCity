import xml.etree.ElementTree as ET
from pytmx import TiledObject

class Disaster:
    """
    A disaster which can occur randomly or by the player request
    
    linked_objs are the objects which contain the affected zones
    """
    price = 0
    
    def __init__(self,x,y,creationTime,mapInstance):
        self.x = x 
        self.y = y
        self.creationTime = creationTime
        placeholder = mapInstance.getStaticObjectByType("Disaster")
        width = mapInstance.getTileWidth()
        height = mapInstance.getTileHeight()
        xml = ET.fromstring(f' \
        <object id="{-1}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{self.x*width}" y="{self.y*height}" width="{placeholder.width}" height="{placeholder.height}"> \
            <properties> \
                <property name="CreationDate" value="{self.creationTime}"/> \
                <property name="Placeholder" value="dynamic"/> \
                <property name="linked_objs" value=""/> \
            </properties> \
        </object>')
        obj = TiledObject(mapInstance.returnMap(),xml)
        obj.properties['linked_objs'] = []
        obj.gid=placeholder.gid
        self.instance = obj