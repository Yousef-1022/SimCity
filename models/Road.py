import xml.etree.ElementTree as ET
from pytmx import TiledObject


class Road:
    """
    A class representing a road in a city simulation game.

    Attributes:
        price (int): The price of the road.
        x (int): The x-coordinate of the road's position.
        y (int): The y-coordinate of the road's position.
        creation_time (str): The creation time of the road.
        instance (TiledObject): The TiledObject representing the road.
    """

    price = 75

    def __init__(self, x, y, creation_time, mapInstance):
        """
        Initializes a Road object.

        Args:
            x (int): The x-coordinate of the road's position.
            y (int): The y-coordinate of the road's position.
            creation_time (str): The creation time of the road.
            mapInstance: The map instance object.

        """
        self.x = x
        self.y = y
        self.creation_time = creation_time
        self.price = Road.price
        self.instance = self.create_road_obj(mapInstance)
        self.instance.properties['MaintenanceFee'] = int(self.price / 4)

    def create_road_obj(self, mapInstance) -> TiledObject:
        """
        Creates a road object based on the map.

        Args:
            mapInstance: The map instance object.

        Returns:
            TiledObject: The created road object.
        """
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
        obj = TiledObject(mapInstance.return_map(), xml)
        obj.gid = placeholder.gid
        obj.properties['Citizens'] = []
        return obj
