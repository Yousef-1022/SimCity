import xml.etree.ElementTree as ET
from pytmx import TiledObject

class PoliceDepartment:
    """
    PoliceDepartment has 4 tiles radius of satisfaction increase
    It can increase the satisfaction of Citizens in nearby RZones by 10%
    """

    def __init__(self,x,y,creationTime,mapInstance):
        self.x = x 
        self.y = y
        self.price = 500
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
                    <property name="Citizens" value=""/>  \
                    <property name="CreationDate" value="{self.creationTime}"/> \
                    <property name="Price" value="{self.price}"/> \
                    <property name="Revenue" type="int" value="0"/> \
                    <property name="MaintenanceFee" type="int" value="{int(self.price/2)}"/> \
                    <property name="Radius" type="int" value="4"/> \
                    <property name="Satisfaction" type="float" value="0.15"/> \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.returnMap(),xml)
        obj.gid=placeholder.gid
        obj.properties['Citizens'] = []
        self.instance = obj