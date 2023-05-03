import xml.etree.ElementTree as ET
from pytmx import TiledObject

class PoliceDepartment:

    def __init__(self,x,y,creationTime,mapInstance):
        self.x = x 
        self.y = y
        self.creationTime = creationTime
        objType = type(self).__name__
        placeholder = mapInstance.getStaticObjectByType(objType)
        width = mapInstance.getTileWidth()
        height = mapInstance.getTileHeight()
        id = mapInstance.getNextObjId()+mapInstance.getObjCount()
        xml = ET.fromstring(f' \
            <object id="{id}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{self.x*width}" y="{self.y*height}" width="{placeholder.width}" height="{placeholder.height}"> \
                <properties> \
                    <property name="Level" type="int" value="1"/> \
                    <property name="Placeholder" value="dynamic"/> \
                    <property name="CreationDate" value="{self.creationTime}"/> \
                    <property name="MaintenanceFee" type="int" value="0"/> \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.returnMap(),xml)
        obj.gid=placeholder.gid
        self.instance = obj