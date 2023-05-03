import xml.etree.ElementTree as ET
from pytmx import TiledObject

class Zone:
    def __init__(self,x,y):
        self.x = x 
        self.y = y
        
        
    def createZoneObj(self,mapInstance,currentTime) -> TiledObject:
        """Creates a zone object, requires the map to be passed and the currentTime object"""
        zoneType = type(self).__name__
        placeholder = mapInstance.getStaticObjectByType(zoneType)
        width = mapInstance.getTileWidth()
        height = mapInstance.getTileHeight()
        id = mapInstance.getNextObjId()+mapInstance.getObjCount()
        xml = ET.fromstring(f' \
            <object id="{id}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{self.x*width}" y="{self.y*height}" width="{placeholder.width}" height="{placeholder.height}"> \
                <properties> \
                    <property name="Level" type="int" value="1"/> \
                    <property name="Placeholder" value="dynamic"/> \
                    <property name="Citizens" value=""/>  \
                    <property name="CreationDate" value="{currentTime}"/> \
                    <property name="RevenueGenerate" type="int" value="0"/> \
                    <property name="MaintenanceFee" type="int" value="0"/> \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.returnMap(),xml)
        obj.gid=placeholder.gid
        obj.properties['Citizens'] = []       
        
        return obj