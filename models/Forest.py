import xml.etree.ElementTree as ET
from pytmx import TiledObject

class Forest:
    """
    Forests by default start with a 0.1 Bonus value. (SatIncrease) 
    Each year, it increases by 0.03 . Once the Forest is Mature (10 Years) , Maintenance fees can be taken
    """
    price = 500
    
    def __init__(self,x,y,creationTime,mapInstance):
        self.x = x 
        self.y = y
        self.price = Forest.price
        self.creationTime = creationTime
        objType = type(self).__name__
        placeholder = mapInstance.getStaticObjectByType(objType)
        width = mapInstance.getTileWidth()
        height = mapInstance.getTileHeight()
        id = mapInstance.getNextObjId()
        xml = ET.fromstring(f' \
            <object id="{id}" name="{placeholder.name}" type="{placeholder.type}" gid="{0}" x="{self.x*width}" y="{self.y*height}" width="{placeholder.width}" height="{placeholder.height}"> \
                <properties> \
                    <property name="Year" type="int" value="1"/> \
                    <property name="Placeholder" value="dynamic"/> \
                    <property name="CreationDate" value="{self.creationTime}"/> \
                    <property name="Price" value="{self.price}"/> \
                    <property name="Satisfaction" type="float" value="0.1"/> \
                    <property name="Mature" type="bool" value="False"/> \
                    <property name="MaintenanceFee" type="int" value="500"/> \
                    <property name="Radius" type="int" value="3"/> \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.returnMap(),xml)
        obj.gid=placeholder.gid
        self.instance = obj