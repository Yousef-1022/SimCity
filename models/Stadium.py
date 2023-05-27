import xml.etree.ElementTree as ET
from pytmx import TiledObject


class Stadium:
    """
    Stadium has 6 tiles radius of satisfaction increase
    It can  increase the satisfaction of Citizens in nearby RZones by 15%
    """
    price = 600

    def __init__(self, x, y, creationTime, mapInstance):
        self.x = x
        self.y = y
        self.price = Stadium.price
        self.creationTime = creationTime
        objType = type(self).__name__
        placeholder = mapInstance.get_static_object_by_type(objType)
        width = mapInstance.get_tile_width()
        height = mapInstance.get_tile_height()
        id = mapInstance.get_next_obj_id()
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
                    <property name="Radius" type="int" value="6"/> \
                    <property name="Satisfaction" type="float" value="0.20"/> \
                </properties> \
            </object>')
        obj = TiledObject(mapInstance.return_map(), xml)
        obj.gid = placeholder.gid
        obj.properties['Citizens'] = []
        self.instance = obj
