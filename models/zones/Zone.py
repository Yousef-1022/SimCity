import xml.etree.ElementTree as ET
from pytmx import TiledObject


class Zone:
    """
    A base class representing a zone in a city simulation game.
    
    Attributes:
        x (int): The x-coordinate of the zone's position.
        y (int): The y-coordinate of the zone's position.
        creationTime (datetime): The creation time of the zone.
        price (int): The price of the zone.
    """

    def __init__(self, x, y, creationTime):
        """
        Initializes a Zone object.
        
        Args:
            x (int): The x-coordinate of the zone's position.
            y (int): The y-coordinate of the zone's position.
            creationTime (datetime): The creation time of the zone.
        """
        self.x = x
        self.y = y
        self.creationTime = creationTime
        self.price = 0

    def create_zone_obj(self, mapInstance) -> TiledObject:
        """
        Creates a zone object based on the mapInstance.
        
        Args:
            mapInstance (MapInstance): The instance of the game map.
        
        Returns:
            TiledObject: The created zone object.
        """
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
        obj = TiledObject(mapInstance.return_map(), xml)
        obj.gid = placeholder.gid
        obj.properties['Citizens'] = []
        obj.properties['Buildings'] = []
        return obj
