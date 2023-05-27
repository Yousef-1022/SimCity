from models.zones.Zone import Zone
from models.Utils import remove_citizen_from_zone


class IndustrialZone(Zone):
    """
    A class representing an industrial zone in a city simulation game.
    It inherits from the Zone class.
    
    Attributes:
        price (int): The price of creating an industrial zone.
        instance (ZoneInstance): The instance of the industrial zone in the game world.
    """

    price = 300

    def __init__(self, x, y, creationTime, mapInstance):
        """
        Initializes an IndustrialZone object.
        
        Args:
            x (int): The x-coordinate of the industrial zone's position.
            y (int): The y-coordinate of the industrial zone's position.
            creationTime (datetime): The creation time of the industrial zone.
            mapInstance (MapInstance): The instance of the game map.
        """
        super().__init__(x, y, creationTime)
        self.price = IndustrialZone.price
        self.instance = super().create_zone_obj(mapInstance)
        self.instance.properties['MaintenanceFee'] = 500
        self.instance.properties['Capacity'] = 10
