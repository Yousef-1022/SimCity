from models.zones.Zone import Zone
from models.Utils import remove_citizen_from_zone


class ServiceZone(Zone):
    """
    A class representing a service zone in a city simulation game.
    It inherits from the Zone class.
    
    Attributes:
        price (int): The price of creating a service zone.
        instance (ZoneInstance): The instance of the service zone in the game world.
    """

    price = 700

    def __init__(self, x, y, creationTime, mapInstance):
        """
        Initializes a ServiceZone object.
        
        Args:
            x (int): The x-coordinate of the service zone's position.
            y (int): The y-coordinate of the service zone's position.
            creationTime (datetime): The creation time of the service zone.
            mapInstance (MapInstance): The instance of the game map.
        """
        super().__init__(x, y, creationTime)
        self.price = ServiceZone.price
        self.instance = super().create_zone_obj(mapInstance)
        self.instance.properties['MaintenanceFee'] = 400
        self.instance.properties['Capacity'] = 5
