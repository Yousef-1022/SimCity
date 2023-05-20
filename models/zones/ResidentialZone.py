from models.zones.Zone import Zone
from models.Utils import remove_citizen_from_zone


class ResidentialZone(Zone):
    """
    A class representing a residential zone in a city simulation game.
    It inherits from the Zone class.
    
    Attributes:
        price (int): The price of creating a residential zone.
        instance (ZoneInstance): The instance of the residential zone in the game world.
    """

    price = 200

    def __init__(self, x, y, creationTime, mapInstance):
        """
        Initializes a ResidentialZone object.
        
        Args:
            x (int): The x-coordinate of the residential zone's position.
            y (int): The y-coordinate of the residential zone's position.
            creationTime (datetime): The creation time of the residential zone.
            mapInstance (MapInstance): The instance of the game map.
        """
        super().__init__(x, y, creationTime)
        self.price = ResidentialZone.price
        self.instance = super().create_zone_obj(mapInstance)
        self.instance.properties['MaintenanceFee'] = 200
        self.instance.properties['Capacity'] = 20
